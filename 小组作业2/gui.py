"""
LL(1)语法分析器图形化界面
提供用户友好的可视化界面，支持文法输入、分析表显示和分析过程可视化
By Group2 邵昱铭 王宝飞 孙智博 肖宇航
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import tkinter.font as tkFont
from ll1_parser import LL1ParserManual as LL1Parser, create_sample_grammar_manual as create_sample_grammar


class LL1ParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LL(1)语法分析器")
        self.root.geometry("1200x800")
        
        # 创建LL(1)分析器实例
        self.parser = LL1Parser()
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 加载示例文法
        self.load_sample_grammar()
    
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置字体
        self.default_font = tkFont.Font(family="Consolas", size=10)
        self.title_font = tkFont.Font(family="Microsoft YaHei", size=12, weight="bold")
        self.mono_font = tkFont.Font(family="Consolas", size=9)
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="LL(1)语法分析器", font=self.title_font)
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 文法输入区域
        self.create_grammar_input_area(main_frame)
        
        # 分析区域
        self.create_analysis_area(main_frame)
        
        # 结果显示区域
        self.create_result_area(main_frame)
    
    def create_grammar_input_area(self, parent):
        """创建文法输入区域"""
        # 文法输入框架
        grammar_frame = ttk.LabelFrame(parent, text="文法规则输入", padding="10")
        grammar_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        grammar_frame.columnconfigure(1, weight=1)
        
        # 文法输入文本区域
        ttk.Label(grammar_frame, text="文法规则:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.grammar_text = scrolledtext.ScrolledText(
            grammar_frame, height=8, font=self.mono_font,
            wrap=tk.WORD
        )
        self.grammar_text.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 按钮框架
        button_frame = ttk.Frame(grammar_frame)
        button_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="加载示例文法", 
                  command=self.load_sample_grammar).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="从文件加载", 
                  command=self.load_from_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="解析文法", 
                  command=self.parse_grammar).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="计算分析表", 
                  command=self.compute_analysis_table).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="清空", 
                  command=self.clear_grammar).pack(side=tk.LEFT)
    
    def create_analysis_area(self, parent):
        """创建分析区域"""
        # 分析框架
        analysis_frame = ttk.LabelFrame(parent, text="输入串分析", padding="10")
        analysis_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        analysis_frame.columnconfigure(0, weight=1)
        
        # 输入串输入
        ttk.Label(analysis_frame, text="输入串:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        input_frame = ttk.Frame(analysis_frame)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        self.input_string_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_string_var, font=self.mono_font)
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(input_frame, text="分析", 
                  command=self.analyze_input).grid(row=0, column=1)
        
        # 预设输入串
        ttk.Label(analysis_frame, text="预设输入串:").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        preset_frame = ttk.Frame(analysis_frame)
        preset_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.preset_inputs = [
            "id + id * id",
            "id * ( id + id )",
            "( id + id ) * id",
            "id + id + id",
            "id * id * id"
        ]
        
        for i, preset in enumerate(self.preset_inputs):
            btn = ttk.Button(preset_frame, text=preset, 
                           command=lambda p=preset: self.set_input_string(p))
            btn.grid(row=i//2, column=i%2, sticky=(tk.W, tk.E), padx=(0, 5), pady=2)
        
        # 分析过程显示
        ttk.Label(analysis_frame, text="分析过程:").grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
        
        # 创建Treeview显示分析过程
        columns = ('步骤', '栈', '输入', '动作')
        self.analysis_tree = ttk.Treeview(analysis_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.analysis_tree.heading(col, text=col)
            self.analysis_tree.column(col, width=150)
        
        # 添加滚动条
        analysis_scrollbar = ttk.Scrollbar(analysis_frame, orient=tk.VERTICAL, command=self.analysis_tree.yview)
        self.analysis_tree.configure(yscrollcommand=analysis_scrollbar.set)
        
        self.analysis_tree.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        analysis_scrollbar.grid(row=5, column=1, sticky=(tk.N, tk.S))
        
        analysis_frame.rowconfigure(5, weight=1)
    
    def create_result_area(self, parent):
        """创建结果显示区域"""
        # 结果显示框架
        result_frame = ttk.LabelFrame(parent, text="分析结果", padding="10")
        result_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(1, weight=1)
        
        # 创建Notebook用于显示不同类型的结果
        self.result_notebook = ttk.Notebook(result_frame)
        self.result_notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # First集合标签页
        self.first_frame = ttk.Frame(self.result_notebook)
        self.result_notebook.add(self.first_frame, text="First集合")
        
        self.first_text = scrolledtext.ScrolledText(
            self.first_frame, font=self.mono_font, wrap=tk.WORD
        )
        self.first_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Follow集合标签页
        self.follow_frame = ttk.Frame(self.result_notebook)
        self.result_notebook.add(self.follow_frame, text="Follow集合")
        
        self.follow_text = scrolledtext.ScrolledText(
            self.follow_frame, font=self.mono_font, wrap=tk.WORD
        )
        self.follow_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Select集合标签页
        self.select_frame = ttk.Frame(self.result_notebook)
        self.result_notebook.add(self.select_frame, text="Select集合")
        
        self.select_text = scrolledtext.ScrolledText(
            self.select_frame, font=self.mono_font, wrap=tk.WORD
        )
        self.select_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 预测分析表标签页
        self.table_frame = ttk.Frame(self.result_notebook)
        self.result_notebook.add(self.table_frame, text="预测分析表")
        
        self.table_text = scrolledtext.ScrolledText(
            self.table_frame, font=self.mono_font, wrap=tk.WORD
        )
        self.table_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 文法信息标签页
        self.grammar_info_frame = ttk.Frame(self.result_notebook)
        self.result_notebook.add(self.grammar_info_frame, text="文法信息")
        
        self.grammar_info_text = scrolledtext.ScrolledText(
            self.grammar_info_frame, font=self.mono_font, wrap=tk.WORD
        )
        self.grammar_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def load_sample_grammar(self):
        """加载示例文法"""
        sample_grammar = """E → T E'
E' → + T E' | ε
T → F T'
T' → * F T' | ε
F → ( E ) | id"""
        
        self.grammar_text.delete(1.0, tk.END)
        self.grammar_text.insert(1.0, sample_grammar)
        
        # 解析文法
        self.parse_grammar()
    
    def load_from_file(self):
        """从文件加载文法"""
        try:
            # 打开文件选择对话框
            file_path = filedialog.askopenfilename(
                title="选择文法文件",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 将文件内容加载到文法文本区域
                self.grammar_text.delete(1.0, tk.END)
                self.grammar_text.insert(1.0, content)
                
                # 自动解析文法
                self.parse_grammar()
                messagebox.showinfo("成功", f"已从文件加载文法：{file_path}")
                
        except Exception as e:
            messagebox.showerror("错误", f"文件读取失败：{str(e)}")
    
    def parse_grammar(self):
        """解析文法规则"""
        try:
            # 清空当前文法
            self.parser = LL1Parser()
            
            grammar_text = self.grammar_text.get(1.0, tk.END).strip()
            lines = grammar_text.split('\n')
            
            start_symbol_set = False
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 解析文法规则
                if '→' in line or '->' in line:
                    # 替换箭头符号
                    line = line.replace('→', '->')
                    parts = line.split('->')
                    
                    if len(parts) != 2:
                        continue
                    
                    left = parts[0].strip()
                    right = parts[1].strip()
                    
                    # 设置开始符号（第一个非终结符）
                    if not start_symbol_set:
                        self.parser.set_start_symbol(left)
                        start_symbol_set = True
                    
                    # 处理多个产生式（用|分隔）
                    if '|' in right:
                        productions = right.split('|')
                        for production in productions:
                            production = production.strip()
                            self.parser.add_grammar_rule(left, production)
                    else:
                        self.parser.add_grammar_rule(left, right)
            
            if not start_symbol_set:
                raise ValueError("未找到有效的文法规则")
            
            messagebox.showinfo("成功", "文法解析成功！")
            
            # 显示文法信息
            self.display_grammar_info()
            
        except Exception as e:
            messagebox.showerror("错误", f"文法解析失败：{str(e)}")
    
    def compute_analysis_table(self):
        """计算分析表"""
        try:
            # 计算First和Follow集合
            self.parser.compute_first_sets()
            self.parser.compute_follow_sets()
            
            # 计算Select集合
            self.parser.compute_select_sets()
            
            # 构造预测分析表
            self.parser.build_predict_table()
            
            # 显示结果
            self.display_first_sets()
            self.display_follow_sets()
            self.display_select_sets()
            self.display_predict_table()
            
            messagebox.showinfo("成功", "分析表计算完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"分析表计算失败：{str(e)}")
    
    def analyze_input(self):
        """分析输入串"""
        input_string = self.input_string_var.get().strip()
        
        if not input_string:
            messagebox.showwarning("警告", "请输入要分析的字符串")
            return
        
        try:
            # 执行分析
            success, steps = self.parser.analyze(input_string)
            
            # 清空之前的分析过程
            for item in self.analysis_tree.get_children():
                self.analysis_tree.delete(item)
            
            # 显示分析过程
            for step in steps:
                self.analysis_tree.insert('', tk.END, values=(
                    step['step'],
                    step['stack'],
                    step['input'],
                    step['action']
                ))
            
            # 显示分析结果
            result = "接受" if success else "拒绝"
            messagebox.showinfo("分析结果", f"输入串 '{input_string}' 的分析结果：{result}")
            
        except Exception as e:
            messagebox.showerror("错误", f"分析失败：{str(e)}")
    
    def set_input_string(self, input_string):
        """设置输入串"""
        self.input_string_var.set(input_string)
    
    def clear_grammar(self):
        """清空文法"""
        self.grammar_text.delete(1.0, tk.END)
        self.parser = LL1Parser()
        self.clear_result_displays()
    
    def clear_result_displays(self):
        """清空结果显示"""
        self.first_text.delete(1.0, tk.END)
        self.follow_text.delete(1.0, tk.END)
        self.select_text.delete(1.0, tk.END)
        self.table_text.delete(1.0, tk.END)
        self.grammar_info_text.delete(1.0, tk.END)
        
        for item in self.analysis_tree.get_children():
            self.analysis_tree.delete(item)
    
    def display_first_sets(self):
        """显示First集合"""
        self.first_text.delete(1.0, tk.END)
        
        content = "First集合：\n\n"
        for symbol, first_set in self.parser.first_sets.items():
            if symbol in self.parser.non_terminals:
                content += f"First({symbol}) = {{{', '.join(sorted(first_set))}}}\n"
        
        self.first_text.insert(1.0, content)
    
    def display_follow_sets(self):
        """显示Follow集合"""
        self.follow_text.delete(1.0, tk.END)
        
        content = "Follow集合：\n\n"
        for symbol, follow_set in self.parser.follow_sets.items():
            if symbol in self.parser.non_terminals:
                content += f"Follow({symbol}) = {{{', '.join(sorted(follow_set))}}}\n"
        
        self.follow_text.insert(1.0, content)
    
    def display_select_sets(self):
        """显示Select集合"""
        self.select_text.delete(1.0, tk.END)
        
        content = "Select集合：\n\n"
        for non_terminal in sorted(self.parser.non_terminals):
            if non_terminal in self.parser.select_sets:
                content += f"{non_terminal}:\n"
                for i, select_set in self.parser.select_sets[non_terminal].items():
                    production = self.parser.grammar[non_terminal][i]
                    production_str = f"{non_terminal} → {' '.join(production)}"
                    content += f"  Select({production_str}) = {{{', '.join(sorted(select_set))}}}\n"
                content += "\n"
        
        self.select_text.insert(1.0, content)
    
    def display_predict_table(self):
        """显示预测分析表"""
        self.table_text.delete(1.0, tk.END)
        
        content = "预测分析表：\n\n"
        
        # 获取所有终结符（包括$）
        terminals = sorted(self.parser.terminals) + ['$']
        
        # 表头
        header = "非终结符".ljust(12)
        for terminal in terminals:
            header += terminal.ljust(15)
        content += header + "\n"
        content += "-" * len(header) + "\n"
        
        # 表格内容
        for non_terminal in sorted(self.parser.non_terminals):
            row = non_terminal.ljust(12)
            for terminal in terminals:
                production = self.parser.predict_table[non_terminal][terminal]
                if production is not None:
                    production_str = f"{non_terminal}→{' '.join(production)}"
                else:
                    production_str = ""
                row += production_str.ljust(15)
            content += row + "\n"
        
        self.table_text.insert(1.0, content)
    
    def display_grammar_info(self):
        """显示文法信息"""
        self.grammar_info_text.delete(1.0, tk.END)
        
        content = "文法信息：\n\n"
        content += f"开始符号：{self.parser.start_symbol}\n\n"
        
        content += "终结符集合：\n"
        content += f"{{{', '.join(sorted(self.parser.terminals))}}}\n\n"
        
        content += "非终结符集合：\n"
        content += f"{{{', '.join(sorted(self.parser.non_terminals))}}}\n\n"
        
        content += "文法规则：\n"
        for non_terminal in sorted(self.parser.grammar.keys()):
            for production in self.parser.grammar[non_terminal]:
                content += f"{non_terminal} → {' '.join(production)}\n"
        
        self.grammar_info_text.insert(1.0, content)


def main():
    """主函数"""
    root = tk.Tk()
    app = LL1ParserGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
