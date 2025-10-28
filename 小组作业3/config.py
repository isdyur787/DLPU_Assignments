"""
配置文件 - 管理项目中的硬编码数据
"""

# GUI界面配置
GUI_CONFIG = {
    "window_title": "递归下降语法分析器 - 编译原理作业",
    "window_size": "1200x800",
    "grammar_font": ('Courier', 10),
    "grammar_bg_color": '#000000',
    "grammar_fg_color": '#00FF00',
    "input_font": ('Courier', 11),
    "result_font": ('Courier', 10),
    "error_color": 'red'
}

# 示例输入数据
EXAMPLE_INPUTS = [
    "a+b*c#",
    "(a+b)*c#",
    "x=3+5*2#",
    "(a+b)*(c-d)#",
    "result = (num1 + num2) * num3 / num4#"
]

# 文法分析示例数据
GRAMMAR_EXAMPLES = [
    {
        "name": "直接左递归文法",
        "description": "经典的算术表达式文法，包含直接左递归",
        "grammar": """E -> E + T | T
T -> T * F | F
F -> ( E ) | id"""
    },
    {
        "name": "间接左递归文法",
        "description": "包含间接左递归的文法",
        "grammar": """S -> A a | b
A -> S c | d"""
    },
    {
        "name": "无左递归文法",
        "description": "已经消除左递归的LL(1)文法",
        "grammar": """E -> T E'
E' -> + T E' | ε
T -> F T'
T' -> * F T' | ε
F -> ( E ) | id"""
    }
]

# 文法定义
GRAMMAR_DEFINITION = """文法定义（算术表达式文法，已消除左递归）：

    Program   -> Statement END
    Statement -> ID ASSIGN Expr | Expr
    Expr      -> Term Expr'
    Expr'     -> PLUS Term Expr' | MINUS Term Expr' | ε
    Term      -> Factor Term'
    Term'     -> MULT Factor Term' | DIV Factor Term' | ε
    Factor    -> LPAREN Expr RPAREN | ID | NUM

说明：
    - ID: 标识符（字母或下划线开头，后接字母、数字或下划线）
    - NUM: 数字（整数或小数）
    - ASSIGN: 赋值符号 =
    - END: 结束符 #
    - PLUS/MINUS/MULT/DIV: 运算符 + - * /
    - LPAREN/RPAREN: 括号 ( )"""

# 错误消息
ERROR_MESSAGES = {
    "empty_input": "请输入要分析的字符串！",
    "missing_end_symbol": "输入串必须以 '#' 结束！",
    "empty_grammar": "请输入要分析的文法！",
    "file_load_error": "无法读取文件：",
    "analysis_error": "分析过程出错：",
    "grammar_analysis_error": "文法分析出错："
}

# 成功消息
SUCCESS_MESSAGES = {
    "analysis_success": "✓ 分析成功：",
    "analysis_failed": "✗ 分析失败：",
    "left_recursion_found": "✓ 发现左递归！",
    "no_left_recursion": "✓ 文法无左递归"
}

# 文件类型配置
FILE_TYPES = [
    ("文本文件", "*.txt"),
    ("所有文件", "*.*")
]

# 窗口配置
WINDOW_CONFIGS = {
    "example_window": {
        "title": "选择示例",
        "size": "400x300"
    },
    "grammar_example_window": {
        "title": "选择文法示例",
        "size": "500x400"
    }
}
