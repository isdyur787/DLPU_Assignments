"""
词法分析器
用于将输入的字符串分解成单词序列
"""

import re
from enum import Enum, auto

# 邵昱铭
class TokenType(Enum):
    """Token类型枚举"""
    ID = auto()          # 标识符
    NUM = auto()         # 数字
    PLUS = auto()        # +
    MINUS = auto()       # -
    MULT = auto()        # *
    DIV = auto()         # /
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    ASSIGN = auto()      # =
    SEMICOLON = auto()   # ;
    END = auto()         # #
    EOF = auto()         # 文件结束
    ERROR = auto()       # 错误


class Token:
    """Token类，表示一个单词"""
    def __init__(self, token_type, value, position):
        self.type = token_type
        self.value = value
        self.position = position  # 在输入串中的位置
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', pos={self.position})"
    
    def __str__(self):
        return f"<{self.type.name}, {self.value}>"


class Lexer:
    """词法分析器"""
    
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None
        self.tokens = []
        
    def error(self, msg=""):
        """词法错误"""
        raise Exception(f"词法分析错误 at position {self.pos}: {msg}")
    
    def advance(self):
        """向前移动指针"""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        """跳过空白字符"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        """跳过注释（支持//和/* */两种注释）"""
        if self.current_char == '/' and self.peek() == '/':
            # 单行注释
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
            self.advance()
        elif self.current_char == '/' and self.peek() == '*':
            # 多行注释
            self.advance()  # skip /
            self.advance()  # skip *
            while self.current_char is not None:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance()  # skip *
                    self.advance()  # skip /
                    break
                self.advance()
    
    def peek(self):
        """查看下一个字符但不移动指针"""
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def number(self):
        """识别数字"""
        # 肖宇航
        start_pos = self.pos
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        # 支持小数
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        
        return Token(TokenType.NUM, result, start_pos)
    
    def identifier(self):
        """识别标识符或关键字"""
        start_pos = self.pos
        result = ''
        
        # 标识符：字母或下划线开头，后接字母、数字或下划线
        while (self.current_char is not None and 
               (self.current_char.isalnum() or self.current_char == '_')):
            result += self.current_char
            self.advance()
        
        return Token(TokenType.ID, result, start_pos)
    
    def get_next_token(self):
        """获取下一个Token"""
        while self.current_char is not None:
            
            # 跳过空白字符
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # 跳过注释
            if self.current_char == '/' and (self.peek() == '/' or self.peek() == '*'):
                self.skip_comment()
                continue
            
            # 数字
            if self.current_char.isdigit():
                return self.number()
            
            # 标识符
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            
            # 运算符和分隔符
            start_pos = self.pos
            
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+', start_pos)
            
            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-', start_pos)
            
            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULT, '*', start_pos)
            
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIV, '/', start_pos)
            
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', start_pos)
            
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', start_pos)
            
            if self.current_char == '=':
                self.advance()
                return Token(TokenType.ASSIGN, '=', start_pos)
            
            if self.current_char == ';':
                self.advance()
                return Token(TokenType.SEMICOLON, ';', start_pos)
            
            if self.current_char == '#':
                self.advance()
                return Token(TokenType.END, '#', start_pos)
            
            # 未识别字符
            return Token(TokenType.ERROR, self.current_char, start_pos)
        
        # 文件结束
        return Token(TokenType.EOF, '', self.pos)
    
    def tokenize(self):
        """将整个输入串转换为Token列表"""
        self.tokens = []
        while True:
            token = self.get_next_token()
            self.tokens.append(token)
            
            if token.type == TokenType.ERROR:
                raise Exception(f"词法错误：未识别的字符 '{token.value}' at position {token.position}")
            
            if token.type in (TokenType.END, TokenType.EOF):
                break
        
        return self.tokens


def test_lexer():
    """测试词法分析器"""
    test_cases = [
        "a+b*c#",
        "x = 3 + 5 * 2#",
        "(a+b)*(c-d)#",
        "123 + 456#",
        "a1 + b2 * c3#",
    ]
    
    for test in test_cases:
        print(f"\n输入: {test}")
        lexer = Lexer(test)
        try:
            tokens = lexer.tokenize()
            print("Token序列:")
            for token in tokens:
                print(f"  {token}")
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    test_lexer()

