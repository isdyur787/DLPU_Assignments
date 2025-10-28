"""
递归下降语法分析器 - 图形用户界面
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from parser import analyze
from grammar_analyzer import LeftRecursionAnalyzer, GrammarParser
from config import (
    GUI_CONFIG, EXAMPLE_INPUTS, GRAMMAR_EXAMPLES, 
    GRAMMAR_DEFINITION, ERROR_MESSAGES, SUCCESS_MESSAGES,
    FILE_TYPES, WINDOW_CONFIGS
)


class ParserGUI:
    """语法分析器图形界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(GUI_CONFIG["window_title"])
        self.root.geometry(GUI_CONFIG["window_size"])
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面组件
        self.create_widgets()
        
        # 显示文法说明
        self.show_grammar()
    
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置颜色
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Success.TLabel', foreground='green', font=('Arial', 12, 'bold'))
        style.configure('Error.TLabel', foreground='red', font=('Arial', 12, 'bold'))
    
    def create_widgets(self):
        """创建界面组件"""
        
        # ==================== 标题栏 ====================
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            title_frame,
            text="递归下降语法分析器",
            style='Title.TLabel'
        )
        title_label.pack()
        
        # ==================== 文法说明区 ====================
        grammar_frame = ttk.LabelFrame(self.root, text="文法定义", padding="10")
        grammar_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.grammar_text = tk.Text(
            grammar_frame,
            height=8,
            width=80,
            font=GUI_CONFIG["grammar_font"],
            bg=GUI_CONFIG["grammar_bg_color"],
            fg=GUI_CONFIG["grammar_fg_color"],
            relief=tk.FLAT,
            insertbackground='white'
        )
        self.grammar_text.pack(fill=tk.BOTH, expand=True)
        self.grammar_text.config(state=tk.DISABLED)
        
        # ==================== 输入区 ====================
        input_frame = ttk.LabelFrame(self.root, text="输入区（以 # 结束）", padding="10")
        input_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        # 输入框
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=6,
            font=GUI_CONFIG["input_font"],
            wrap=tk.WORD
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # 按钮区
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.analyze_btn = ttk.Button(
            button_frame,
            text="开始分析",
            command=self.analyze_input
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        self.load_btn = ttk.Button(
            button_frame,
            text="从文件加载",
            command=self.load_from_file
        )
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            button_frame,
            text="清空",
            command=self.clear_input
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.example_btn = ttk.Button(
            button_frame,
            text="加载示例",
            command=self.load_example
        )
        self.example_btn.pack(side=tk.LEFT, padx=5)
        
        # ==================== 结果区 ====================
        result_frame = ttk.LabelFrame(self.root, text="分析结果", padding="10")
        result_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        # 状态标签
        self.status_label = ttk.Label(
            result_frame,
            text="等待输入...",
            font=('Arial', 12)
        )
        self.status_label.pack(pady=5)
        
        # 创建Notebook（标签页）
        self.notebook = ttk.Notebook(result_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Token序列标签页
        token_frame = ttk.Frame(self.notebook)
        self.notebook.add(token_frame, text="Token序列")
        
        self.token_text = scrolledtext.ScrolledText(
            token_frame,
            font=('Courier', 10),
            wrap=tk.WORD
        )
        self.token_text.pack(fill=tk.BOTH, expand=True)
        
        # 分析过程标签页
        process_frame = ttk.Frame(self.notebook)
        self.notebook.add(process_frame, text="分析过程")
        
        self.process_text = scrolledtext.ScrolledText(
            process_frame,
            font=('Courier', 10),
            wrap=tk.WORD
        )
        self.process_text.pack(fill=tk.BOTH, expand=True)
        
        # 错误信息标签页
        error_frame = ttk.Frame(self.notebook)
        self.notebook.add(error_frame, text="错误信息")
        
        self.error_text = scrolledtext.ScrolledText(
            error_frame,
            font=('Courier', 10),
            wrap=tk.WORD,
            fg='red'
        )
        self.error_text.pack(fill=tk.BOTH, expand=True)
        
        # 文法分析标签页
        grammar_analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(grammar_analysis_frame, text="文法分析")
        
        # 文法分析输入区
        grammar_input_frame = ttk.LabelFrame(grammar_analysis_frame, text="文法输入", padding="5")
        grammar_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.grammar_input_text = scrolledtext.ScrolledText(
            grammar_input_frame,
            height=8,
            font=('Courier', 10),
            wrap=tk.WORD
        )
        self.grammar_input_text.pack(fill=tk.BOTH, expand=True)
        
        # 文法分析按钮
        grammar_button_frame = ttk.Frame(grammar_input_frame)
        grammar_button_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.analyze_grammar_btn = ttk.Button(
            grammar_button_frame,
            text="分析文法",
            command=self.analyze_grammar
        )
        self.analyze_grammar_btn.pack(side=tk.LEFT, padx=5)
        
        self.load_grammar_btn = ttk.Button(
            grammar_button_frame,
            text="加载文法示例",
            command=self.load_grammar_example
        )
        self.load_grammar_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_grammar_btn = ttk.Button(
            grammar_button_frame,
            text="清空",
            command=self.clear_grammar_input
        )
        self.clear_grammar_btn.pack(side=tk.LEFT, padx=5)
        
        # 文法分析结果显示区
        grammar_result_frame = ttk.LabelFrame(grammar_analysis_frame, text="分析结果", padding="5")
        grammar_result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.grammar_result_text = scrolledtext.ScrolledText(
            grammar_result_frame,
            font=('Courier', 10),
            wrap=tk.WORD
        )
        self.grammar_result_text.pack(fill=tk.BOTH, expand=True)
        
        # ==================== 状态栏 ====================
        status_bar = ttk.Frame(self.root)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_bar_label = ttk.Label(
            status_bar,
            text="就绪",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar_label.pack(fill=tk.X, padx=5, pady=2)
    
    def show_grammar(self):
        """显示文法定义"""
        self.grammar_text.config(state=tk.NORMAL)
        self.grammar_text.delete(1.0, tk.END)
        self.grammar_text.insert(1.0, GRAMMAR_DEFINITION)
        self.grammar_text.config(state=tk.DISABLED)
    
    def analyze_input(self):
        """分析输入的字符串"""
        input_string = self.input_text.get(1.0, tk.END).strip()
        
        if not input_string:
            messagebox.showwarning("警告", ERROR_MESSAGES["empty_input"])
            return
        
        # 检查是否以#结束
        if not input_string.endswith('#'):
            messagebox.showwarning("警告", ERROR_MESSAGES["missing_end_symbol"])
            return
        
        # 执行分析
        self.status_bar_label.config(text="正在分析...")
        self.root.update()
        
        try:
            result = analyze(input_string)
            
            # 显示状态
            if result['success']:
                self.status_label.config(
                    text=f"✓ 分析成功：{result['message'].upper()}",
                    style='Success.TLabel'
                )
                self.status_bar_label.config(text="分析成功")
            else:
                self.status_label.config(
                    text=f"✗ 分析失败：{result['message'].upper()}",
                    style='Error.TLabel'
                )
                self.status_bar_label.config(text="分析失败")
            
            # 显示Token序列
            self.token_text.delete(1.0, tk.END)
            if result['tokens']:
                self.token_text.insert(1.0, "Token序列：\n\n")
                for i, token in enumerate(result['tokens'], 1):
                    self.token_text.insert(tk.END, f"{i:3d}. {token}\n")
            
            # 显示分析过程
            self.process_text.delete(1.0, tk.END)
            if result['parse_tree']:
                self.process_text.insert(1.0, result['parse_tree'])
            
            # 显示错误信息
            self.error_text.delete(1.0, tk.END)
            if result['error']:
                self.error_text.insert(1.0, result['error'])
            else:
                self.error_text.insert(1.0, "无错误")
            
            # 自动切换到相应标签页
            if result['success']:
                self.notebook.select(1)  # 切换到分析过程
            else:
                self.notebook.select(2)  # 切换到错误信息
        
        except Exception as e:
            messagebox.showerror("错误", f"分析过程出错：\n{str(e)}")
            self.status_bar_label.config(text="分析出错")
    
    def load_from_file(self):
        """从文件加载输入"""
        filename = filedialog.askopenfilename(
            title="选择输入文件",
            filetypes=FILE_TYPES
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, content)
                self.status_bar_label.config(text=f"已加载文件: {filename}")
            
            except Exception as e:
                messagebox.showerror("错误", f"无法读取文件：\n{str(e)}")
    
    def clear_input(self):
        """清空输入和输出"""
        self.input_text.delete(1.0, tk.END)
        self.token_text.delete(1.0, tk.END)
        self.process_text.delete(1.0, tk.END)
        self.error_text.delete(1.0, tk.END)
        self.status_label.config(text="等待输入...")
        self.status_bar_label.config(text="就绪")
    
    def load_example(self):
        """加载示例输入"""
        # 创建示例选择窗口
        example_window = tk.Toplevel(self.root)
        example_window.title(WINDOW_CONFIGS["example_window"]["title"])
        example_window.geometry(WINDOW_CONFIGS["example_window"]["size"])
        
        ttk.Label(
            example_window,
            text="请选择一个示例：",
            font=('Arial', 11, 'bold')
        ).pack(pady=10)
        
        listbox = tk.Listbox(
            example_window,
            font=('Courier', 10),
            height=10
        )
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for example in EXAMPLE_INPUTS:
            listbox.insert(tk.END, example)
        
        def select_example():
            selection = listbox.curselection()
            if selection:
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, EXAMPLE_INPUTS[selection[0]])
                example_window.destroy()
                self.status_bar_label.config(text="已加载示例")
        
        ttk.Button(
            example_window,
            text="确定",
            command=select_example
        ).pack(pady=10)
    
    def analyze_grammar(self):
        """分析文法中的左递归"""
        grammar_text = self.grammar_input_text.get(1.0, tk.END).strip()
        
        if not grammar_text:
            messagebox.showwarning("警告", ERROR_MESSAGES["empty_grammar"])
            return
        
        try:
            # 创建左递归分析器
            analyzer = LeftRecursionAnalyzer()
            result = analyzer.analyze_grammar(grammar_text)
            
            # 显示分析结果
            self.grammar_result_text.delete(1.0, tk.END)
            
            # 显示原始文法
            self.grammar_result_text.insert(tk.END, "原始文法：\n")
            self.grammar_result_text.insert(tk.END, "=" * 50 + "\n")
            self.grammar_result_text.insert(tk.END, GrammarParser.format_grammar(result['grammar']) + "\n\n")
            
            # 显示左递归检测结果
            self.grammar_result_text.insert(tk.END, "左递归检测结果：\n")
            self.grammar_result_text.insert(tk.END, "=" * 50 + "\n")
            
            if result['has_left_recursion']:
                self.grammar_result_text.insert(tk.END, "✓ 发现左递归！\n\n")
                
                if result['left_recursive_symbols']:
                    self.grammar_result_text.insert(tk.END, f"直接左递归符号: {', '.join(result['left_recursive_symbols'])}\n")
                
                if result['indirect_left_recursive_symbols']:
                    self.grammar_result_text.insert(tk.END, f"间接左递归符号: {', '.join(result['indirect_left_recursive_symbols'])}\n")
                
                # 显示消除左递归后的文法
                self.grammar_result_text.insert(tk.END, "\n消除左递归后的文法：\n")
                self.grammar_result_text.insert(tk.END, "=" * 50 + "\n")
                
                eliminated_grammar = analyzer.eliminate_left_recursion()
                self.grammar_result_text.insert(tk.END, GrammarParser.format_grammar(eliminated_grammar) + "\n")
                
            else:
                self.grammar_result_text.insert(tk.END, "✓ 文法无左递归\n")
            
            # 显示分析步骤
            if result['analysis_steps']:
                self.grammar_result_text.insert(tk.END, "\n分析步骤：\n")
                self.grammar_result_text.insert(tk.END, "=" * 50 + "\n")
                for step in result['analysis_steps']:
                    self.grammar_result_text.insert(tk.END, f"• {step}\n")
            
            # 切换到文法分析标签页
            # 动态查找文法分析标签页的索引
            grammar_tab_index = None
            for i in range(self.notebook.index("end")):
                if self.notebook.tab(i, "text") == "文法分析":
                    grammar_tab_index = i
                    break
            if grammar_tab_index is not None:
                self.notebook.select(grammar_tab_index)
            
        except Exception as e:
            messagebox.showerror("错误", f"文法分析出错：\n{str(e)}")
    
    def load_grammar_example(self):
        """加载文法示例"""
        # 创建示例选择窗口
        example_window = tk.Toplevel(self.root)
        example_window.title(WINDOW_CONFIGS["grammar_example_window"]["title"])
        example_window.geometry(WINDOW_CONFIGS["grammar_example_window"]["size"])
        
        ttk.Label(
            example_window,
            text="请选择一个文法示例：",
            font=('Arial', 11, 'bold')
        ).pack(pady=10)
        
        listbox = tk.Listbox(
            example_window,
            font=('Courier', 10),
            height=8
        )
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for i, example in enumerate(GRAMMAR_EXAMPLES):
            listbox.insert(tk.END, f"{i+1}. {example['name']}")
        
        def select_example():
            selection = listbox.curselection()
            if selection:
                selected_example = GRAMMAR_EXAMPLES[selection[0]]
                self.grammar_input_text.delete(1.0, tk.END)
                self.grammar_input_text.insert(1.0, selected_example['grammar'])
                example_window.destroy()
                self.status_bar_label.config(text=f"已加载示例: {selected_example['name']}")
        
        ttk.Button(
            example_window,
            text="确定",
            command=select_example
        ).pack(pady=10)
    
    def clear_grammar_input(self):
        """清空文法输入和结果"""
        self.grammar_input_text.delete(1.0, tk.END)
        self.grammar_result_text.delete(1.0, tk.END)


def main():
    """主函数"""
    root = tk.Tk()
    app = ParserGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

