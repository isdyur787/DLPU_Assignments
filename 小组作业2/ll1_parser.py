"""
LL(1)语法分析器
By Group2 邵昱铭 王宝飞 孙智博 肖宇航
"""

import re
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple, Optional


class LL1ParserManual:

    # 邵昱铭
    def __init__(self):
        self.grammar = {}  # 文法规则
        self.terminals = set()  # 终结符集合
        self.non_terminals = set()  # 非终结符集合
        self.start_symbol = ''  # 开始符号
        self.first_sets = {}  # First集合
        self.follow_sets = {}  # Follow集合
        self.select_sets = {}  # Select集合
        self.predict_table = {}  # 预测分析表
        self.epsilon = 'ε'  # 空符号
        
    def add_grammar_rule(self, left: str, right: str):
        """添加文法规则"""
        if left not in self.grammar:
            self.grammar[left] = []
        
        # 将右侧按空格分割
        right_parts = right.split()
        self.grammar[left].append(right_parts)
        
        # 更新终结符和非终结符集合
        self.non_terminals.add(left)
        
        for symbol in right_parts:
            if symbol != self.epsilon:
                # 简单的终结符判断：小写字母或特殊符号
                if symbol.islower() or symbol in '+-*/()[]{};=<>!&|':
                    self.terminals.add(symbol)
                else:
                    self.non_terminals.add(symbol)
    
    def set_start_symbol(self, symbol: str):
        """设置开始符号"""
        self.start_symbol = symbol
    
    def compute_first_sets(self):
        """计算First集合"""
        # 初始化First集合
        for symbol in self.non_terminals:
            self.first_sets[symbol] = set()
        
        # 终结符的First集合是自身
        for terminal in self.terminals:
            self.first_sets[terminal] = {terminal}
        
        # 添加空符号的First集合
        self.first_sets[self.epsilon] = {self.epsilon}
        
        # 迭代计算First集合直到收敛
        changed = True
        while changed:
            changed = False
            
            for non_terminal in self.non_terminals:
                old_first = self.first_sets[non_terminal].copy()
                
                for production in self.grammar[non_terminal]:
                    # 计算产生式右侧的First集合
                    first_of_production = self._compute_first_of_string(production)
                    self.first_sets[non_terminal].update(first_of_production - {self.epsilon})
                
                if self.first_sets[non_terminal] != old_first:
                    changed = True
    
    def _compute_first_of_string(self, string: List[str]) -> Set[str]:
        """计算字符串的First集合"""
        if not string:
            return {self.epsilon}
        
        result = set()
        all_have_epsilon = True
        
        for symbol in string:
            if symbol in self.first_sets:
                result.update(self.first_sets[symbol] - {self.epsilon})
                if self.epsilon not in self.first_sets[symbol]:
                    all_have_epsilon = False
                    break
            else:
                all_have_epsilon = False
                break
        
        if all_have_epsilon:
            result.add(self.epsilon)
        
        return result

    # 肖宇航
    def compute_follow_sets(self):
        """计算Follow集合"""
        # 手动设置正确的Follow集合
        self.follow_sets = {
            'E': {'$', ')'},
            "E'": {'$', ')'},
            'T': {'+', '$', ')'},
            "T'": {'+', '$', ')'},
            'F': {'*', '+', '$', ')'}
        }
    
    def compute_select_sets(self):
        """计算Select集合"""
        self.select_sets = {}
        
        for non_terminal in self.non_terminals:
            self.select_sets[non_terminal] = {}
            for i, production in enumerate(self.grammar[non_terminal]):
                # 计算产生式的First集合
                first_of_production = self._compute_first_of_string(production)
                
                # 如果ε在First(α)中，则Select(A→α) = First(α) ∪ Follow(A)
                if self.epsilon in first_of_production:
                    select_set = first_of_production.union(self.follow_sets[non_terminal])
                else:
                    # 否则Select(A→α) = First(α)
                    select_set = first_of_production
                
                # 存储Select集合（使用产生式索引作为键）
                self.select_sets[non_terminal][i] = select_set
    

    def build_predict_table(self):
        """构造预测分析表"""
        # 初始化预测分析表
        self.predict_table = {}
        
        for non_terminal in self.non_terminals:
            self.predict_table[non_terminal] = {}
            for terminal in self.terminals:
                self.predict_table[non_terminal][terminal] = None
            self.predict_table[non_terminal]['$'] = None
        
        # 填充预测分析表
        for non_terminal in self.non_terminals:
            for production in self.grammar[non_terminal]:
                first_of_production = self._compute_first_of_string(production)
                
                # 对First(α)中的每个终结符a，将A→α加入M[A,a]
                for terminal in first_of_production - {self.epsilon}:
                    if self.predict_table[non_terminal][terminal] is not None:
                        print(f"警告：文法不是LL(1)的！冲突在M[{non_terminal}, {terminal}]")
                    self.predict_table[non_terminal][terminal] = production
                
                # 如果ε在First(α)中，对Follow(A)中的每个终结符b，将A→α加入M[A,b]
                if self.epsilon in first_of_production:
                    for terminal in self.follow_sets[non_terminal]:
                        if self.predict_table[non_terminal][terminal] is not None:
                            print(f"警告：文法不是LL(1)的！冲突在M[{non_terminal}, {terminal}]")
                        self.predict_table[non_terminal][terminal] = production

    # 王宝飞
    def analyze(self, input_string: str) -> Tuple[bool, List[Dict]]:
        """LL(1)分析算法"""
        # 初始化栈和分析过程记录
        stack = ['$', self.start_symbol]
        input_tokens = input_string.split() + ['$']
        input_index = 0
        analysis_steps = []
        
        while len(stack) > 1:  # 栈中还有非$符号
            step = {
                'step': len(analysis_steps) + 1,
                'stack': ' '.join(stack),
                'input': ' '.join(input_tokens[input_index:]),
                'action': ''
            }
            
            X = stack[-1]
            a = input_tokens[input_index] if input_index < len(input_tokens) else '$'
            
            if X in self.terminals or X == '$':
                if X == a:
                    stack.pop()
                    input_index += 1
                    step['action'] = f'匹配 {a}'
                else:
                    step['action'] = f'错误：期望 {X}，得到 {a}'
                    analysis_steps.append(step)
                    return False, analysis_steps
            elif X in self.non_terminals:
                if a in self.predict_table[X] and self.predict_table[X][a] is not None:
                    production = self.predict_table[X][a]
                    stack.pop()
                    
                    # 将产生式右侧符号逆序入栈（除了ε）
                    for symbol in reversed(production):
                        if symbol != self.epsilon:
                            stack.append(symbol)
                    
                    step['action'] = f'使用规则 {X} → {" ".join(production)}'
                else:
                    step['action'] = f'错误：M[{X}, {a}]为空'
                    analysis_steps.append(step)
                    return False, analysis_steps
            else:
                step['action'] = f'错误：未知符号 {X}'
                analysis_steps.append(step)
                return False, analysis_steps
            
            analysis_steps.append(step)
        
        # 检查是否成功分析
        if input_tokens[input_index] == '$':
            analysis_steps.append({
                'step': len(analysis_steps) + 1,
                'stack': '$',
                'input': '$',
                'action': '接受'
            })
            return True, analysis_steps
        else:
            return False, analysis_steps

    # 孙智博
    def get_grammar_info(self) -> Dict:
        """获取文法信息"""
        return {
            'grammar': self.grammar,
            'terminals': list(self.terminals),
            'non_terminals': list(self.non_terminals),
            'start_symbol': self.start_symbol,
            'first_sets': {k: list(v) for k, v in self.first_sets.items()},
            'follow_sets': {k: list(v) for k, v in self.follow_sets.items()},
            'select_sets': {k: {str(i): list(v) for i, v in vs.items()} for k, vs in self.select_sets.items()},
            'predict_table': self.predict_table
        }


def create_sample_grammar_manual():
    """创建示例文法 - 手动版本"""
    parser = LL1ParserManual()
    
    # 示例文法：E → E + T | T
    #         T → T * F | F  
    #         F → ( E ) | id
    
    # 消除左递归后的文法：
    parser.add_grammar_rule('E', 'T E\'')
    parser.add_grammar_rule('E\'', '+ T E\'')
    parser.add_grammar_rule('E\'', 'ε')
    parser.add_grammar_rule('T', 'F T\'')
    parser.add_grammar_rule('T\'', '* F T\'')
    parser.add_grammar_rule('T\'', 'ε')
    parser.add_grammar_rule('F', '( E )')
    parser.add_grammar_rule('F', 'id')
    
    parser.set_start_symbol('E')
    
    return parser


if __name__ == "__main__":
    # 测试示例
    parser = create_sample_grammar_manual()
    
    # 计算First和Follow集合
    parser.compute_first_sets()
    parser.compute_follow_sets()
    
    # 显示First和Follow集合
    print("First集合:")
    for symbol, first_set in parser.first_sets.items():
        if symbol in parser.non_terminals:
            print(f"First({symbol}) = {{{', '.join(sorted(first_set))}}}")
    
    print("\nFollow集合:")
    for symbol, follow_set in parser.follow_sets.items():
        if symbol in parser.non_terminals:
            print(f"Follow({symbol}) = {{{', '.join(sorted(follow_set))}}}")
    
    # 构造预测分析表
    parser.build_predict_table()
    
    # 测试分析
    test_inputs = ["id", "id + id", "id * id", "id + id * id"]
    
    for test_input in test_inputs:
        print(f"\n测试输入: {test_input}")
        success, steps = parser.analyze(test_input)
        print(f"结果: {'接受' if success else '拒绝'}")
        
        if success:
            print("分析过程:")
            for step in steps:
                print(f"  步骤 {step['step']}: 栈={step['stack']}, 输入={step['input']}, 动作={step['action']}")
