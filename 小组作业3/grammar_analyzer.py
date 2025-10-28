"""
文法分析器 - 左递归检测和消除模块
用于检测文法中的左递归并进行消除
"""

import re
from typing import List, Dict, Set, Tuple, Optional


class Production:
    """产生式类"""
    def __init__(self, left: str, right: List[str]):
        self.left = left  # 左部非终结符
        self.right = right  # 右部符号列表
    
    def __repr__(self):
        return f"{self.left} -> {' '.join(self.right)}"
    
    def __str__(self):
        return f"{self.left} -> {' '.join(self.right)}"


class Grammar:
    """文法类"""
    def __init__(self):
        self.productions: List[Production] = []
        self.nonterminals: Set[str] = set()
        self.terminals: Set[str] = set()
        self.start_symbol: Optional[str] = None
    
    def add_production(self, left: str, right: List[str]):
        """添加产生式"""
        production = Production(left, right)
        self.productions.append(production)
        self.nonterminals.add(left)
        
        # 识别终结符和非终结符
        for symbol in right:
            if symbol != 'ε' and not self._is_nonterminal(symbol):
                self.terminals.add(symbol)
    
    def _is_nonterminal(self, symbol: str) -> bool:
        """判断是否为非终结符（大写字母开头）"""
        if not symbol:
            return False
        # 更严格的判断：大写字母开头，且不是纯数字
        return symbol[0].isupper() and not symbol.isdigit()
    
    def get_productions_for(self, nonterminal: str) -> List[Production]:
        """获取指定非终结符的所有产生式"""
        return [p for p in self.productions if p.left == nonterminal]
    
    def has_left_recursion(self, nonterminal: str) -> bool:
        """检测指定非终结符是否有左递归"""
        productions = self.get_productions_for(nonterminal)
        for prod in productions:
            if prod.right and prod.right[0] == nonterminal:
                return True
        return False
    
    def has_indirect_left_recursion(self, nonterminal: str) -> bool:
        """检测间接左递归"""
        # 使用深度优先搜索检测间接左递归
        visited = set()
        return self._dfs_left_recursion(nonterminal, nonterminal, visited)
    
    def _dfs_left_recursion(self, start: str, current: str, visited: Set[str]) -> bool:
        """深度优先搜索检测间接左递归"""
        if current in visited:
            return False  # 避免循环
        
        visited.add(current)
        productions = self.get_productions_for(current)
        
        for prod in productions:
            if prod.right:  # 非空产生式
                first_symbol = prod.right[0]
                if first_symbol == start:
                    return True  # 找到间接左递归
                elif first_symbol in self.nonterminals:
                    if self._dfs_left_recursion(start, first_symbol, visited.copy()):
                        return True
        
        return False
    
    def eliminate_left_recursion(self, nonterminal: str) -> List[Production]:
        """消除指定非终结符的左递归"""
        productions = self.get_productions_for(nonterminal)
        
        # 分离左递归和非左递归产生式
        left_recursive = []
        non_left_recursive = []
        
        for prod in productions:
            if prod.right and prod.right[0] == nonterminal:
                left_recursive.append(prod)
            else:
                non_left_recursive.append(prod)
        
        if not left_recursive:
            return []  # 没有左递归，无需处理
        
        # 创建新的非终结符，避免命名冲突
        base_name = nonterminal.rstrip("'")
        counter = 1
        new_nonterminal = f"{base_name}'"
        while new_nonterminal in self.nonterminals:
            counter += 1
            new_nonterminal = f"{base_name}'{counter}"
        
        # 生成新的产生式
        new_productions = []
        
        # A -> Aα | Aβ | γ 转换为 A -> γA', A' -> αA' | βA' | ε
        for prod in non_left_recursive:
            if prod.right == ['ε']:
                # A -> ε 转换为 A -> A'
                new_productions.append(Production(nonterminal, [new_nonterminal]))
            else:
                # A -> γ 转换为 A -> γA'
                new_right = prod.right + [new_nonterminal]
                new_productions.append(Production(nonterminal, new_right))
        
        # 处理左递归产生式
        for prod in left_recursive:
            # A -> Aα 转换为 A' -> αA'
            if len(prod.right) > 1:
                alpha = prod.right[1:]  # α部分
                new_right = alpha + [new_nonterminal]
                new_productions.append(Production(new_nonterminal, new_right))
        
        # 添加 A' -> ε
        new_productions.append(Production(new_nonterminal, ['ε']))
        
        return new_productions
    
    def eliminate_all_left_recursion(self) -> 'Grammar':
        """消除所有左递归（使用标准算法）"""
        new_grammar = Grammar()
        new_grammar.start_symbol = self.start_symbol
        
        # 复制所有产生式
        for prod in self.productions:
            new_grammar.add_production(prod.left, prod.right)
        
        # 按顺序处理每个非终结符
        nonterminals = list(self.nonterminals)
        
        for i, A in enumerate(nonterminals):
            # 对于每个 A_i，处理所有 A_j (j < i) 的替换
            A_productions = new_grammar.get_productions_for(A)
            
            # 替换 A -> A_j γ 形式的产生式
            for j in range(i):
                A_j = nonterminals[j]
                A_j_productions = new_grammar.get_productions_for(A_j)
                
                # 找到所有 A -> A_j γ 形式的产生式
                to_replace = []
                to_keep = []
                
                for prod in A_productions:
                    if prod.right and prod.right[0] == A_j:
                        to_replace.append(prod)
                    else:
                        to_keep.append(prod)
                
                # 替换这些产生式
                if to_replace:
                    new_A_productions = []
                    
                    # 保留非 A_j 开头的产生式
                    for prod in to_keep:
                        new_A_productions.append(prod)
                    
                    # 替换 A -> A_j γ 为 A -> β γ (对所有 A_j -> β)
                    for replace_prod in to_replace:
                        gamma = replace_prod.right[1:]  # γ 部分
                        for A_j_prod in A_j_productions:
                            if A_j_prod.right == ['ε']:
                                # A_j -> ε，则 A -> γ
                                new_right = gamma if gamma else ['ε']
                            else:
                                # A_j -> β，则 A -> β γ
                                new_right = A_j_prod.right + gamma
                            
                            new_A_productions.append(Production(A, new_right))
                    
                    # 更新文法
                    new_grammar.productions = [p for p in new_grammar.productions if p.left != A]
                    for prod in new_A_productions:
                        new_grammar.add_production(prod.left, prod.right)
                    
                    # 重新获取 A 的产生式
                    A_productions = new_grammar.get_productions_for(A)
            
            # 消除 A 的直接左递归
            if new_grammar.has_left_recursion(A):
                new_productions = new_grammar.eliminate_left_recursion(A)
                
                # 删除原有的 A 产生式
                new_grammar.productions = [p for p in new_grammar.productions if p.left != A]
                
                # 添加新的产生式
                for prod in new_productions:
                    new_grammar.add_production(prod.left, prod.right)
        
        return new_grammar
    
    def __str__(self):
        """字符串表示"""
        result = []
        for prod in self.productions:
            result.append(str(prod))
        return '\n'.join(result)


class GrammarParser:
    """文法解析器"""
    
    @staticmethod
    def parse_grammar(grammar_text: str) -> Grammar:
        """解析文法文本"""
        if not grammar_text or not grammar_text.strip():
            raise ValueError("文法文本不能为空")
        
        grammar = Grammar()
        lines = grammar_text.strip().split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # 解析产生式 A -> α | β | γ
            if '->' not in line:
                raise ValueError(f"第{line_num}行格式错误：缺少 '->' 符号")
            
            parts = line.split('->', 1)
            if len(parts) != 2:
                raise ValueError(f"第{line_num}行格式错误：'->' 符号使用不当")
            
            left, right_part = parts
            left = left.strip()
            
            if not left:
                raise ValueError(f"第{line_num}行格式错误：左部非终结符不能为空")
            
            # 设置开始符号
            if grammar.start_symbol is None:
                grammar.start_symbol = left
            
            # 解析右部
            if not right_part.strip():
                raise ValueError(f"第{line_num}行格式错误：右部不能为空")
            
            alternatives = [alt.strip() for alt in right_part.split('|')]
            
            for alt in alternatives:
                if not alt:
                    raise ValueError(f"第{line_num}行格式错误：产生式右部不能为空")
                
                if alt == 'ε':
                    symbols = ['ε']
                else:
                    symbols = alt.split()
                
                grammar.add_production(left, symbols)
        
        if not grammar.productions:
            raise ValueError("文法中没有有效的产生式")
        
        return grammar
    
    @staticmethod
    def format_grammar(grammar: Grammar) -> str:
        """格式化文法输出"""
        result = []
        
        # 按非终结符分组
        nonterminal_groups = {}
        for prod in grammar.productions:
            if prod.left not in nonterminal_groups:
                nonterminal_groups[prod.left] = []
            nonterminal_groups[prod.left].append(prod)
        
        for nonterminal in sorted(nonterminal_groups.keys()):
            productions = nonterminal_groups[nonterminal]
            right_parts = []
            
            for prod in productions:
                if prod.right == ['ε']:
                    right_parts.append('ε')
                else:
                    right_parts.append(' '.join(prod.right))
            
            result.append(f"{nonterminal} -> {' | '.join(right_parts)}")
        
        return '\n'.join(result)


class LeftRecursionAnalyzer:
    """左递归分析器"""
    
    def __init__(self):
        self.grammar = None
        self.left_recursive_symbols = set()
        self.indirect_left_recursive_symbols = set()
    
    def analyze_grammar(self, grammar_text: str) -> Dict:
        """分析文法的左递归情况"""
        self.grammar = GrammarParser.parse_grammar(grammar_text)
        
        result = {
            'grammar': self.grammar,
            'has_left_recursion': False,
            'left_recursive_symbols': [],
            'indirect_left_recursive_symbols': [],
            'analysis_steps': []
        }
        
        # 检测直接左递归
        for nonterminal in self.grammar.nonterminals:
            if self.grammar.has_left_recursion(nonterminal):
                self.left_recursive_symbols.add(nonterminal)
                result['left_recursive_symbols'].append(nonterminal)
                result['has_left_recursion'] = True
                result['analysis_steps'].append(f"发现直接左递归: {nonterminal}")
        
        # 检测间接左递归
        for nonterminal in self.grammar.nonterminals:
            if self.grammar.has_indirect_left_recursion(nonterminal):
                if nonterminal not in self.left_recursive_symbols:
                    self.indirect_left_recursive_symbols.add(nonterminal)
                    result['indirect_left_recursive_symbols'].append(nonterminal)
                    result['has_left_recursion'] = True
                    result['analysis_steps'].append(f"发现间接左递归: {nonterminal}")
        
        return result
    
    def eliminate_left_recursion(self) -> Grammar:
        """消除左递归"""
        if self.grammar is None:
            raise ValueError("请先分析文法")
        
        return self.grammar.eliminate_all_left_recursion()


def test_left_recursion_analyzer():
    """测试左递归分析器"""
    # 测试用例1：直接左递归
    grammar1 = """
    E -> E + T | T
    T -> T * F | F
    F -> ( E ) | id
    """
    
    # 测试用例2：间接左递归
    grammar2 = """
    S -> A a | b
    A -> S c | d
    """
    
    # 测试用例3：无左递归
    grammar3 = """
    E -> T E'
    E' -> + T E' | ε
    T -> F T'
    T' -> * F T' | ε
    F -> ( E ) | id
    """
    
    analyzer = LeftRecursionAnalyzer()
    
    test_cases = [
        ("直接左递归文法", grammar1),
        ("间接左递归文法", grammar2),
        ("无左递归文法", grammar3)
    ]
    
    print("=" * 80)
    print("左递归分析器测试")
    print("=" * 80)
    
    for name, grammar_text in test_cases:
        print(f"\n{name}:")
        print("-" * 40)
        
        try:
            result = analyzer.analyze_grammar(grammar_text)
            
            print("原始文法:")
            print(GrammarParser.format_grammar(result['grammar']))
            
            print(f"\n是否有左递归: {result['has_left_recursion']}")
            
            if result['left_recursive_symbols']:
                print(f"直接左递归符号: {result['left_recursive_symbols']}")
            
            if result['indirect_left_recursive_symbols']:
                print(f"间接左递归符号: {result['indirect_left_recursive_symbols']}")
            
            if result['has_left_recursion']:
                print("\n消除左递归后的文法:")
                eliminated_grammar = analyzer.eliminate_left_recursion()
                print(GrammarParser.format_grammar(eliminated_grammar))
            
            print("\n分析步骤:")
            for step in result['analysis_steps']:
                print(f"  - {step}")
                
        except Exception as e:
            print(f"分析错误: {e}")
        
        print("=" * 80)


if __name__ == "__main__":
    test_left_recursion_analyzer()
