#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
最终版本
词法分析器 - 编译原理小组任务 1 2025-9-20
By 邵昱铭 孙智博 王宝飞 肖宇航
"""

import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from typing import List, Tuple, Union, Optional


class TokenType:
    """单词种别码定义"""
    # 关键字 (1-20)
    IF = 1
    ELSE = 2
    WHILE = 3
    FOR = 4
    INT = 5
    FLOAT = 6
    CHAR = 7
    STRING = 8
    RETURN = 9
    VOID = 10
    MAIN = 11
    PRINTF = 12
    SCANF = 13
    BREAK = 14
    CONTINUE = 15
    
    # 运算符 (21-30)
    PLUS = 21      # +
    MINUS = 22     # -
    MULTIPLY = 23  # *
    DIVIDE = 24    # /
    ASSIGN = 25    # =
    EQUAL = 26     # ==
    NOT_EQUAL = 27 # !=
    LESS = 28      # <
    GREATER = 29   # >
    LESS_EQUAL = 30 # <=
    
    # 界符 (31-45)
    LEFT_BRACE = 31    # {
    RIGHT_BRACE = 32   # }
    LEFT_BRACKET = 33  # [
    RIGHT_BRACKET = 34 # ]
    SEMICOLON = 35     # ;
    COMMA = 36         # ,
    DOT = 37           # .
    LEFT_PAREN = 38    # (
    RIGHT_PAREN = 39   # )
    COLON = 40         # :
    
    # 标识符和常量 (46-50)
    IDENTIFIER = 46    # 标识符
    INTEGER = 47       # 整数常量
    FLOAT_CONST = 48   # 浮点数常量
    STRING_CONST = 49  # 字符串常量
    CHAR_CONST = 50    # 字符常量
    
    # 其他
    EOF = 99           # 文件结束
    ERROR = 100        # 错误


class LexicalAnalyzer:
    """词法分析器类"""
    
    def __init__(self):
        # 关键字表
        self.keywords = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'char': TokenType.CHAR,
            'string': TokenType.STRING,
            'return': TokenType.RETURN,
            'void': TokenType.VOID,
            'main': TokenType.MAIN,
            'printf': TokenType.PRINTF,
            'scanf': TokenType.SCANF,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE
        }
        
        # 运算符表
        self.operators = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '=': TokenType.ASSIGN,
            '==': TokenType.EQUAL,
            '!=': TokenType.NOT_EQUAL,
            '<': TokenType.LESS,
            '>': TokenType.GREATER,
            '<=': TokenType.LESS_EQUAL
        }
        
        # 界符表
        self.delimiters = {
            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_BRACE,
            '[': TokenType.LEFT_BRACKET,
            ']': TokenType.RIGHT_BRACKET,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            ':': TokenType.COLON
        }
        
        # 初始化分析器状态
        self.reset()
    
    def reset(self):
        """重置分析器状态"""
        self.source_code = ""
        self.position = 0
        self.line_number = 1
        self.column_number = 1
        self.tokens = []
    
    def set_source(self, source_code: str):
        """设置源代码"""
        self.reset()
        self.source_code = source_code
    
    def get_current_char(self) -> Optional[str]:
        """获取当前字符"""
        if self.position >= len(self.source_code):
            return None
        return self.source_code[self.position]
    
    def peek_next_char(self) -> Optional[str]:
        """预读下一个字符"""
        if self.position + 1 >= len(self.source_code):
            return None
        return self.source_code[self.position + 1]
    
    def advance(self):
        """前进一个字符"""
        if self.position < len(self.source_code):
            if self.source_code[self.position] == '\n':
                self.line_number += 1
                self.column_number = 1
            else:
                self.column_number += 1
            self.position += 1
        # 如果已经到达文件末尾，不再前进
    
    def skip_whitespace(self):
        """跳过空白字符和注释"""
        while self.get_current_char():
            # 跳过空白字符
            if self.get_current_char().isspace():
                self.advance()
            # 处理单行注释 //
            elif self.get_current_char() == '/' and self.peek_next_char() == '/':
                self.advance()  # 跳过第一个 /
                self.advance()  # 跳过第二个 /
                # 跳过直到行尾
                while self.get_current_char() and self.get_current_char() != '\n':
                    self.advance()
            # 处理多行注释 /* */
            elif self.get_current_char() == '/' and self.peek_next_char() == '*':
                self.advance()  # 跳过 /
                self.advance()  # 跳过 *
                # 跳过直到 */
                while self.get_current_char():
                    if self.get_current_char() == '*' and self.peek_next_char() == '/':
                        self.advance()  # 跳过 *
                        self.advance()  # 跳过 /
                        break
                    self.advance()
            else:
                break
    
    def is_identifier_start(self, char: str) -> bool:
        """判断是否为标识符起始字符"""
        return char.isalpha() or char == '_'
    
    def is_identifier_char(self, char: str) -> bool:
        """判断是否为标识符字符"""
        return char.isalnum() or char == '_'
    
    def read_identifier(self) -> str:
        """读取标识符"""
        start_pos = self.position
        while self.get_current_char() and self.is_identifier_char(self.get_current_char()):
            self.advance()
        return self.source_code[start_pos:self.position]
    
    def read_number(self) -> Tuple[str, int]:
        """读取数字（整数或浮点数）"""
        start_pos = self.position
        number_type = TokenType.INTEGER
        
        # 读取整数部分
        while self.get_current_char() and self.get_current_char().isdigit():
            self.advance()
        
        # 检查是否为浮点数
        if self.get_current_char() == '.' and self.peek_next_char() and self.peek_next_char().isdigit():
            self.advance()  # 跳过小数点
            number_type = TokenType.FLOAT_CONST
            while self.get_current_char() and self.get_current_char().isdigit():
                self.advance()
        
        number = self.source_code[start_pos:self.position]
        return number, number_type
    
    def read_string(self) -> str:
        """读取字符串常量"""
        start_pos = self.position
        quote_char = self.get_current_char()  # ' 或 "
        self.advance()  # 跳过开始引号
        
        while self.get_current_char() and self.get_current_char() != quote_char:
            if self.get_current_char() == '\\':  # 处理转义字符
                self.advance()
                if not self.get_current_char():  # 防止转义字符后没有字符
                    break
            self.advance()
        
        if self.get_current_char() == quote_char:
            self.advance()  # 跳过结束引号
        
        return self.source_code[start_pos:self.position]
    
    def get_next_token(self) -> Tuple[int, Union[str, int]]:
        """获取下一个单词符号"""
        # 跳过空白字符
        self.skip_whitespace()
        
        # 检查是否到达文件末尾
        if not self.get_current_char():
            return TokenType.EOF, ""
        
        current_char = self.get_current_char()
        
        # 处理标识符和关键字
        if self.is_identifier_start(current_char):
            identifier = self.read_identifier()
            if identifier in self.keywords:
                return self.keywords[identifier], identifier
            else:
                return TokenType.IDENTIFIER, identifier
        
        # 处理数字
        elif current_char.isdigit():
            number, number_type = self.read_number()
            if number_type == TokenType.INTEGER:
                return number_type, int(number)
            else:
                return number_type, float(number)
        
        # 处理字符串和字符常量
        elif current_char in ['"', "'"]:
            string_value = self.read_string()
            if current_char == '"':
                return TokenType.STRING_CONST, string_value
            else:
                return TokenType.CHAR_CONST, string_value
        
        # 处理双字符运算符
        elif current_char in ['=', '!', '<', '>']:
            two_char = current_char + (self.peek_next_char() or '')
            if two_char in self.operators:
                self.advance()
                self.advance()
                return self.operators[two_char], two_char
            # 如果不是双字符运算符，继续处理单字符运算符
        
        # 处理单字符运算符
        if current_char in self.operators:
            self.advance()
            return self.operators[current_char], current_char
        
        # 处理界符
        elif current_char in self.delimiters:
            self.advance()
            return self.delimiters[current_char], current_char
        
        # 处理未知字符
        else:
            self.advance()
            return TokenType.ERROR, current_char
        
        # 如果所有条件都不匹配，返回错误
        return TokenType.ERROR, current_char
    
    def analyze(self) -> List[Tuple[int, Union[str, int]]]:
        """分析整个源代码"""
        # 重置位置但不清空源代码
        self.position = 0
        self.line_number = 1
        self.column_number = 1
        tokens = []
        
        # 添加安全计数器防止无限循环
        max_tokens = len(self.source_code) * 2  # 最多处理字符数的2倍
        token_count = 0
        
        while token_count < max_tokens:
            old_position = self.position
            token_type, token_value = self.get_next_token()
            
            # 如果位置没有前进，说明出现了问题，退出循环
            if self.position == old_position and token_type != TokenType.EOF:
                tokens.append((TokenType.ERROR, f"位置未前进: {self.get_current_char()}"))
                self.advance()  # 强制前进一个字符
            
            if token_type == TokenType.EOF:
                break
            tokens.append((token_type, token_value))
            token_count += 1
        
        return tokens
    
    def get_token_name(self, token_type: int) -> str:
        """获取单词种别码对应的名称"""
        token_names = {
            TokenType.IF: "IF",
            TokenType.ELSE: "ELSE",
            TokenType.WHILE: "WHILE",
            TokenType.FOR: "FOR",
            TokenType.INT: "INT",
            TokenType.FLOAT: "FLOAT",
            TokenType.CHAR: "CHAR",
            TokenType.STRING: "STRING",
            TokenType.RETURN: "RETURN",
            TokenType.VOID: "VOID",
            TokenType.MAIN: "MAIN",
            TokenType.PRINTF: "PRINTF",
            TokenType.SCANF: "SCANF",
            TokenType.BREAK: "BREAK",
            TokenType.CONTINUE: "CONTINUE",
            TokenType.PLUS: "PLUS",
            TokenType.MINUS: "MINUS",
            TokenType.MULTIPLY: "MULTIPLY",
            TokenType.DIVIDE: "DIVIDE",
            TokenType.ASSIGN: "ASSIGN",
            TokenType.EQUAL: "EQUAL",
            TokenType.NOT_EQUAL: "NOT_EQUAL",
            TokenType.LESS: "LESS",
            TokenType.GREATER: "GREATER",
            TokenType.LESS_EQUAL: "LESS_EQUAL",
            TokenType.LEFT_BRACE: "LEFT_BRACE",
            TokenType.RIGHT_BRACE: "RIGHT_BRACE",
            TokenType.LEFT_BRACKET: "LEFT_BRACKET",
            TokenType.RIGHT_BRACKET: "RIGHT_BRACKET",
            TokenType.SEMICOLON: "SEMICOLON",
            TokenType.COMMA: "COMMA",
            TokenType.DOT: "DOT",
            TokenType.LEFT_PAREN: "LEFT_PAREN",
            TokenType.RIGHT_PAREN: "RIGHT_PAREN",
            TokenType.COLON: "COLON",
            TokenType.IDENTIFIER: "IDENTIFIER",
            TokenType.INTEGER: "INTEGER",
            TokenType.FLOAT_CONST: "FLOAT_CONST",
            TokenType.STRING_CONST: "STRING_CONST",
            TokenType.CHAR_CONST: "CHAR_CONST",
            TokenType.ERROR: "ERROR"
        }
        return token_names.get(token_type, f"UNKNOWN_{token_type}")


class LexicalAnalyzerGUI:
    """词法分析器图形界面"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("词法分析器 - 编译原理课程设计")
        self.root.geometry("1000x700")
        
        self.analyzer = LexicalAnalyzer()
        self.current_file_path = None  # 跟踪当前打开的文件路径
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # 输入区域
        ttk.Label(main_frame, text="源代码输入:", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=3, sticky=tk.E)
        
        ttk.Button(button_frame, text="打开文件", command=self.open_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="分析代码", command=self.analyze_code).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="保存结果", command=self.save_result).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="清空", command=self.clear_all).pack(side=tk.LEFT)
        
        # 源代码输入文本框
        self.input_text = scrolledtext.ScrolledText(main_frame, height=15, width=80, font=("Consolas", 10))
        self.input_text.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 输出区域
        ttk.Label(main_frame, text="词法分析结果:", font=("Arial", 12, "bold")).grid(row=2, column=0, columnspan=4, sticky=tk.W, pady=(10, 5))
        
        # 创建输出文本框和滚动条
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, width=80, font=("Consolas", 10))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 插入示例代码
        self.insert_sample_code()
    
    def insert_sample_code(self):
        """插入示例代码"""
        sample_code = """int main() {
    int a = 10;
    float b = 3.14;
    char c = 'A';
    string str = "Hello 编译原理，我们是二组";
    
    if (a > 5) {
        printf("a 大于 5");
        a = a + 1;
    } else {
        a = a - 1;
    }
    
    while (a < 20) {
        a = a * 2;
        if (a == 16) break;
    }
    
    return 0;
}"""
        self.input_text.insert(tk.END, sample_code)
    
    def open_file(self):
        """打开文件"""
        file_path = filedialog.askopenfilename(
            title="选择源代码文件",
            filetypes=[("C文件", "*.c"), ("C++文件", "*.cpp"), ("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, content)
                self.current_file_path = file_path  # 保存当前文件路径
                self.status_var.set(f"已加载文件: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"无法打开文件: {str(e)}")
                self.current_file_path = None
    
    def analyze_code(self):
        """分析代码"""
        source_code = self.input_text.get(1.0, tk.END).strip()
        
        if not source_code:
            messagebox.showwarning("警告", "请输入源代码！")
            return
        
        try:
            self.status_var.set("正在分析...")
            self.root.update()
            
            # 设置源代码到分析器
            self.analyzer.set_source(source_code)
            
            # 执行词法分析
            tokens = self.analyzer.analyze()
            
            # 清空输出区域
            self.output_text.delete(1.0, tk.END)
            
            # 显示结果
            self.output_text.insert(tk.END, "二元组 (单词种别码, 单词属性值):\n")
            self.output_text.insert(tk.END, "=" * 60 + "\n")
            
            token_count = 0
            for token_type, token_value in tokens:
                if token_type == TokenType.ERROR:
                    self.output_text.insert(tk.END, f"错误: 无法识别的字符 '{token_value}'\n")
                else:
                    token_name = self.analyzer.get_token_name(token_type)
                    if isinstance(token_value, (int, float)):
                        self.output_text.insert(tk.END, f"({token_type:3d}, {token_value:10}) - {token_name}\n")
                    else:
                        self.output_text.insert(tk.END, f"({token_type:3d}, '{token_value:10}') - {token_name}\n")
                    token_count += 1
            
            self.output_text.insert(tk.END, "=" * 60 + "\n")
            self.output_text.insert(tk.END, f"总共识别出 {token_count} 个单词符号\n")
            
            self.status_var.set(f"分析完成，识别出 {token_count} 个单词")
            
        except Exception as e:
            messagebox.showerror("错误", f"分析过程中出现错误: {str(e)}")
            self.status_var.set("分析失败")
    
    def save_result(self):
        """保存分析结果到文件"""
        if not self.current_file_path:
            messagebox.showwarning("警告", "请先打开一个文件！")
            return
        
        output_content = self.output_text.get(1.0, tk.END).strip()
        if not output_content:
            messagebox.showwarning("警告", "没有分析结果可保存！")
            return
        
        # 生成输出文件名（在原文件名基础上添加_lexical_analysis）
        import os
        file_dir = os.path.dirname(self.current_file_path)
        file_name = os.path.basename(self.current_file_path)
        file_name_without_ext = os.path.splitext(file_name)[0]
        file_ext = os.path.splitext(file_name)[1]
        
        output_file_path = os.path.join(file_dir, f"{file_name_without_ext}_lexical_analysis{file_ext}")
        
        try:
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write("词法分析结果\n")
                file.write("=" * 50 + "\n")
                file.write(f"源文件: {self.current_file_path}\n")
                file.write(f"分析时间: {self.get_current_time()}\n")
                file.write("=" * 50 + "\n\n")
                file.write(output_content)
                file.write("\n\n")
                file.write("=" * 50 + "\n")
                file.write("分析完成\n")
            
            self.status_var.set(f"分析结果已保存到: {output_file_path}")
            messagebox.showinfo("成功", f"分析结果已保存到:\n{output_file_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存文件失败: {str(e)}")
    
    def get_current_time(self):
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def clear_all(self):
        """清空所有内容"""
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.current_file_path = None  # 清空当前文件路径
        self.status_var.set("已清空")
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()


def main():
    """主函数"""
    print("词法分析器启动中...")
    print("支持的单词类型:")
    print("- 关键字: if, else, while, for, int, float, char, string, return, void, main, printf, scanf, break, continue")
    print("- 运算符: +, -, *, /, =, ==, !=, <, >, <=")
    print("- 界符: {, }, [, ], ;, ,, ., (, ), :")
    print("- 标识符: 字母或下划线开头，可包含字母、数字、下划线")
    print("- 常量: 整数、浮点数、字符串、字符")
    print()
    
    # 启动GUI
    app = LexicalAnalyzerGUI()
    app.run()


if __name__ == "__main__":
    main()
