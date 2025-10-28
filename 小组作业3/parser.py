"""
递归下降语法分析器
文法定义：
    Program -> Statement END
    Statement -> ID ASSIGN Expr | Expr
    Expr -> Term Expr'
    Expr' -> PLUS Term Expr' | MINUS Term Expr' | ε
    Term -> Factor Term'
    Term' -> MULT Factor Term' | DIV Factor Term' | ε
    Factor -> LPAREN Expr RPAREN | ID | NUM
"""

from lexer import Token, TokenType, Lexer


class ParseError(Exception):
    """语法分析错误异常"""
    pass


class Parser:
    """递归下降语法分析器"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
        self.parse_steps = []  # 记录分析过程
        self.error_messages = []  # 错误信息
        
    def error(self, expected=""):
        """语法错误处理"""
        msg = f"语法错误 at position {self.current_token.position}:\n"
        msg += f"  期望: {expected}\n"
        msg += f"  实际: {self.current_token}\n"
        msg += f"  已分析的步骤数: {len(self.parse_steps)}"
        self.error_messages.append(msg)
        raise ParseError(msg)
    
    def advance(self):
        """移动到下一个Token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TokenType.EOF, '', -1)
    
    def match(self, token_type):
        """匹配当前Token类型"""
        if self.current_token.type == token_type:
            matched_token = self.current_token
            self.log_step(f"匹配 {token_type.name}: '{matched_token.value}'")
            self.advance()
            return matched_token
        else:
            self.error(f"{token_type.name}")
            return None
    
    def log_step(self, step):
        """记录分析步骤"""
        self.parse_steps.append(step)
    
    def get_parse_tree(self):
        """获取分析过程"""
        return "\n".join(self.parse_steps)
    
    # ==================== 文法产生式对应的递归函数 ====================
    # 王宝飞
    
    def parse(self):
        """入口函数：Program -> Statement END"""
        self.log_step("开始语法分析")
        self.log_step("应用产生式: Program -> Statement END")
        
        try:
            self.statement()
            
            # 检查是否以 # 结束
            if self.current_token.type == TokenType.END:
                self.match(TokenType.END)
                self.log_step("✓ 语法分析成功！")
                return True, self.get_parse_tree()
            else:
                self.error("输入串应以 '#' 结束")
                return False, self.get_parse_tree()
        
        except ParseError as e:
            self.log_step(f"✗ 语法分析失败")
            return False, self.get_parse_tree()
    
    def statement(self):
        """Statement -> ID ASSIGN Expr | Expr"""
        self.log_step("进入 Statement")
        
        # 预测：如果是 ID ASSIGN，则是赋值语句
        if self.current_token.type == TokenType.ID:
            # 需要向前看一个token判断是否是赋值语句
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == TokenType.ASSIGN:
                self.log_step("应用产生式: Statement -> ID ASSIGN Expr")
                self.match(TokenType.ID)
                self.match(TokenType.ASSIGN)
                self.expr()
            else:
                # 只是表达式
                self.log_step("应用产生式: Statement -> Expr")
                self.expr()
        else:
            # 表达式
            self.log_step("应用产生式: Statement -> Expr")
            self.expr()
        
        self.log_step("退出 Statement")
    
    def expr(self):
        """Expr -> Term Expr'"""
        self.log_step("进入 Expr")
        self.log_step("应用产生式: Expr -> Term Expr'")
        
        self.term()
        self.expr_prime()
        
        self.log_step("退出 Expr")
    
    def expr_prime(self):
        """Expr' -> PLUS Term Expr' | MINUS Term Expr' | ε"""
        self.log_step("进入 Expr'")
        
        if self.current_token.type == TokenType.PLUS:
            self.log_step("应用产生式: Expr' -> PLUS Term Expr'")
            self.match(TokenType.PLUS)
            self.term()
            self.expr_prime()
        elif self.current_token.type == TokenType.MINUS:
            self.log_step("应用产生式: Expr' -> MINUS Term Expr'")
            self.match(TokenType.MINUS)
            self.term()
            self.expr_prime()
        else:
            # ε产生式
            self.log_step("应用产生式: Expr' -> ε")
        
        self.log_step("退出 Expr'")
    
    def term(self):
        """Term -> Factor Term'"""
        self.log_step("进入 Term")
        self.log_step("应用产生式: Term -> Factor Term'")
        
        self.factor()
        self.term_prime()
        
        self.log_step("退出 Term")
    
    def term_prime(self):
        """Term' -> MULT Factor Term' | DIV Factor Term' | ε"""
        self.log_step("进入 Term'")
        
        if self.current_token.type == TokenType.MULT:
            self.log_step("应用产生式: Term' -> MULT Factor Term'")
            self.match(TokenType.MULT)
            self.factor()
            self.term_prime()
        elif self.current_token.type == TokenType.DIV:
            self.log_step("应用产生式: Term' -> DIV Factor Term'")
            self.match(TokenType.DIV)
            self.factor()
            self.term_prime()
        else:
            # ε产生式
            self.log_step("应用产生式: Term' -> ε")
        
        self.log_step("退出 Term'")
    
    def factor(self):
        """Factor -> LPAREN Expr RPAREN | ID | NUM"""
        self.log_step("进入 Factor")
        
        if self.current_token.type == TokenType.LPAREN:
            self.log_step("应用产生式: Factor -> LPAREN Expr RPAREN")
            self.match(TokenType.LPAREN)
            self.expr()
            self.match(TokenType.RPAREN)
        
        elif self.current_token.type == TokenType.ID:
            self.log_step("应用产生式: Factor -> ID")
            self.match(TokenType.ID)
        
        elif self.current_token.type == TokenType.NUM:
            self.log_step("应用产生式: Factor -> NUM")
            self.match(TokenType.NUM)
        
        else:
            self.error("ID, NUM 或 '('")
        
        self.log_step("退出 Factor")


def analyze(input_string):
    # 对输入串进行完整的词法和语法分析
    # 王宝飞
    result = {
        'success': False,
        'message': '',
        'tokens': [],
        'parse_tree': '',
        'error': None
    }
    
    try:
        # 1. 词法分析
        lexer = Lexer(input_string)
        tokens = lexer.tokenize()
        result['tokens'] = tokens
        
        # 2. 语法分析
        parser = Parser(tokens)
        success, parse_tree = parser.parse()
        result['parse_tree'] = parse_tree
        result['success'] = success
        
        if success:
            result['message'] = "acc"
        else:
            result['message'] = "error"
            if parser.error_messages:
                result['error'] = parser.error_messages[0]
        
    except Exception as e:
        result['success'] = False
        result['message'] = "error"
        result['error'] = str(e)
    
    return result


def test_parser():
    """测试语法分析器"""
    test_cases = [
        ("a+b#", True),
        ("a+b*c#", True),
        ("(a+b)*c#", True),
        ("x=3+5*2#", True),
        ("(a+b)*(c-d)#", True),
        ("123+456#", True),
        ("a+b*#", False),  # 错误：缺少操作数
        ("a+b", False),    # 错误：缺少结束符
        ("(a+b#", False),  # 错误：括号不匹配
    ]
    
    print("=" * 80)
    print("递归下降语法分析器测试")
    print("=" * 80)
    
    for input_str, expected_success in test_cases:
        print(f"\n输入: {input_str}")
        print(f"预期结果: {'成功' if expected_success else '失败'}")
        print("-" * 80)
        
        result = analyze(input_str)
        
        print(f"分析结果: {result['message']}")
        
        if result['tokens']:
            print("\nToken序列:")
            for token in result['tokens']:
                print(f"  {token}")
        
        print("\n分析过程:")
        print(result['parse_tree'])
        
        if result['error']:
            print(f"\n错误信息:\n{result['error']}")
        
        print("=" * 80)


if __name__ == "__main__":
    test_parser()

