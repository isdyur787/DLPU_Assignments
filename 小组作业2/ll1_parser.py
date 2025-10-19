#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LL(1) 语法分析器
    自动推导终/非终结符
    自动计算 FIRST / FOLLOW / SELECT
    自动构造预测分析表
"""

from typing import Dict, List, Set, Tuple, Optional, Union


class LL1ParserManual:

    def __init__(self):
        # 文法：A -> [alpha1, alpha2, ...]；alpha 是 List[str]
        self.grammar: Dict[str, List[List[str]]] = {}
        # 符号集合
        self.terminals: Set[str] = set()
        self.non_terminals: Set[str] = set()
        # 起始符
        self.start_symbol: str = ''
        # 集合
        self.first_sets: Dict[str, Set[str]] = {}
        self.follow_sets: Dict[str, Set[str]] = {}
        self.select_sets: Dict[str, Dict[int, Set[str]]] = {}
        # 预测分析表：M[A][a] = 产生式右部（List[str]）或 None
        self.predict_table: Dict[str, Dict[str, Optional[List[str]]]] = {}
        # 冲突记录（可选，可供调试）
        self.conflicts: List[Tuple[str, str, List[str], List[str]]] = []
        # 空串记号
        self.epsilon: str = 'ε'

    # 文法录入与符号推导
    # 邵昱铭
    def add_grammar_rule(self, left: str, right: Union[str, List[str]]):

        left = left.strip()
        if not left:
            return

        if left not in self.grammar:
            self.grammar[left] = []

        if isinstance(right, list):
            alpha = [s.strip() for s in right if s.strip()]
            if len(alpha) == 0:
                alpha = [self.epsilon]
            self.grammar[left].append(alpha)
        else:
            r = right.strip()
            if not r or r == self.epsilon:
                self.grammar[left].append([self.epsilon])
            else:
                self.grammar[left].append(r.split())

        # 每次增量更新一次符号集合，保证 GUI 解析后立即能看到集合
        self._derive_symbols()

    def set_start_symbol(self, symbol: str):
        self.start_symbol = symbol.strip()

    def _derive_symbols(self):
        """
        算法思路：依据 grammar 自动推导非终结符和终结符。
        1. 非终结符 = 所有产生式的左部键集合
        2. 终结符 = 所有右部出现过的符号 - 非终结符 - {ε}
        """
        self.non_terminals = set(self.grammar.keys())
        rhs_symbols: Set[str] = set()
        for prods in self.grammar.values():
            for alpha in prods:
                rhs_symbols.update(alpha)
        self.terminals = {s for s in rhs_symbols if s not in self.non_terminals and s != self.epsilon}

    # FIRST / FOLLOW / SELECT

    def compute_first_sets(self):

        self._derive_symbols()

        # 初始化
        self.first_sets = {A: set() for A in self.non_terminals}
        for a in self.terminals:
            self.first_sets[a] = {a}
        self.first_sets[self.epsilon] = {self.epsilon}

        changed = True
        while changed:
            changed = False
            for A, prods in self.grammar.items():
                before = set(self.first_sets[A])
                for alpha in prods:
                    # A → ε
                    if len(alpha) == 1 and alpha[0] == self.epsilon:
                        self.first_sets[A].add(self.epsilon)
                        continue

                    nullable_prefix = True
                    for X in alpha:
                        FX = self.first_sets.get(X, set())
                        # 若 X 尚未登记（非常少见），按“自成终结符”处理
                        if not FX and X not in self.non_terminals and X != self.epsilon:
                            FX = {X}
                            self.first_sets[X] = {X}

                        self.first_sets[A] |= (FX - {self.epsilon})
                        if self.epsilon not in FX:
                            nullable_prefix = False
                            break

                    if nullable_prefix:
                        self.first_sets[A].add(self.epsilon)

                if self.first_sets[A] != before:
                    changed = True

    def _first_of_sequence(self, seq: List[str]) -> Set[str]:
        """FIRST(符号串)，空或全可空 => 包含 ε"""
        if not seq:
            return {self.epsilon}

        result: Set[str] = set()
        nullable_prefix = True
        for X in seq:
            FX = self.first_sets.get(X, set())
            if not FX and X not in self.non_terminals and X != self.epsilon:
                FX = {X}
                self.first_sets[X] = {X}

            result |= (FX - {self.epsilon})
            if self.epsilon not in FX:
                nullable_prefix = False
                break

        if nullable_prefix:
            result.add(self.epsilon)
        return result

    # 肖宇航
    def compute_follow_sets(self):
        """
        标准 FOLLOW 迭代：
        - '$' ∈ FOLLOW(S)
        - - A → α B β ：FIRST(β) − {ε} ⊆ FOLLOW(B)
        - 若 β ⇒* ε，则 FOLLOW(A) ⊆ FOLLOW(B)
        """
        if not self.start_symbol:
            raise ValueError("请先设置开始符号 start_symbol")

        self._derive_symbols()
        if not self.first_sets:
            self.compute_first_sets()

        self.follow_sets = {A: set() for A in self.non_terminals}
        self.follow_sets[self.start_symbol].add('$')

        changed = True
        while changed:
            changed = False
            for A, prods in self.grammar.items():
                for alpha in prods:
                    n = len(alpha)
                    for i, B in enumerate(alpha):
                        if B not in self.non_terminals:
                            continue
                        beta = alpha[i + 1:]
                        first_beta = self._first_of_sequence(beta)
                        before = set(self.follow_sets[B])

                        # FIRST(β) \ {ε}
                        self.follow_sets[B] |= (first_beta - {self.epsilon})

                        # 若 β 可空或 β 为空，FOLLOW(A) ⊆ FOLLOW(B)
                        if (self.epsilon in first_beta) or (len(beta) == 0):
                            self.follow_sets[B] |= self.follow_sets[A]

                        if self.follow_sets[B] != before:
                            changed = True

    def compute_select_sets(self):
        """
        SELECT(A→α) = FIRST(α)（若含 ε，再并 FOLLOW(A)）
        以“产生式在其候选列表中的索引”为键保存每条产生式的 SELECT
        """
        if not self.first_sets:
            self.compute_first_sets()
        if not self.follow_sets:
            self.compute_follow_sets()

        self.select_sets = {}
        for A, prods in self.grammar.items():
            self.select_sets[A] = {}
            for idx, alpha in enumerate(prods):
                f = self._first_of_sequence(alpha)
                if self.epsilon in f:
                    self.select_sets[A][idx] = (f - {self.epsilon}) | self.follow_sets[A]
                else:
                    self.select_sets[A][idx] = f

    # 预测分析表
    # 孙智博
    def build_predict_table(self):
        """
        依据 SELECT 填 M[A, a]。若同一格出现多条产生式，记录冲突并打印警告。
        GUI 会用 self.predict_table[非终结符][终结符或'$'] 读取。
        """
        if not self.select_sets:
            self.compute_select_sets()

        # 初始化
        self.predict_table = {}
        self.conflicts = []
        terminals_plus_end = sorted(self.terminals | {'$'})

        for A in self.non_terminals:
            self.predict_table[A] = {t: None for t in terminals_plus_end}

        # 填表
        for A, prods in self.grammar.items():
            for idx, alpha in enumerate(prods):
                select = self.select_sets[A][idx]
                for a in select:
                    # 只对“出现在表头的终结符或 $”填表
                    if a not in self.predict_table[A]:
                        # 若某些符号尚未登记为“终结符”，也补入（健壮性）
                        for row in self.predict_table.values():
                            row.setdefault(a, None)

                    cell = self.predict_table[A][a]
                    if cell is not None:
                        # 冲突：已有规则
                        self.conflicts.append((A, a, cell, alpha))
                        print(f"警告：文法可能不是 LL(1)！冲突在 M[{A}, {a}]，"
                              f"已存在 {A}→{' '.join(cell)}，又遇到 {A}→{' '.join(alpha)}")
                    else:
                        self.predict_table[A][a] = alpha

    # 分析
    # 王宝飞
    def analyze(self, input_string: str) -> Tuple[bool, List[Dict[str, str]]]:
        """
        LL(1) 分析：返回 (是否接受, 步骤记录)
        """
        if not self.predict_table:
            # 若还未构造表，则自动完成必要步骤
            self.compute_first_sets()
            self.compute_follow_sets()
            self.compute_select_sets()
            self.build_predict_table()

        tokens = input_string.split() if input_string.strip() else []
        tokens.append('$')

        stack: List[str] = ['$', self.start_symbol]
        input_index = 0
        steps: List[Dict[str, str]] = []

        # 与原版风格保持一致：当栈中还存在非 $ 符号时继续
        while len(stack) > 1:
            step = {
                'step': str(len(steps) + 1),
                'stack': ' '.join(stack),
                'input': ' '.join(tokens[input_index:]),
                'action': ''
            }

            X = stack[-1]
            a = tokens[input_index] if input_index < len(tokens) else '$'

            # 终结符或 $
            if X == '$' or X in self.terminals:
                if X == a:
                    stack.pop()
                    input_index += 1
                    step['action'] = f'匹配 {a}'
                else:
                    step['action'] = f'错误：期望 {X}，得到 {a}'
                    steps.append(step)
                    return False, steps

            # 非终结符
            elif X in self.non_terminals:
                row = self.predict_table.get(X, {})
                production = row.get(a, None)
                if production is None:
                    step['action'] = f'错误：M[{X}, {a}]为空'
                    steps.append(step)
                    return False, steps

                stack.pop()
                # 右部逆序入栈（跳过 ε）
                for sym in reversed(production):
                    if sym != self.epsilon:
                        stack.append(sym)
                step['action'] = f'使用规则 {X} → {" ".join(production)}'

            else:
                step['action'] = f'错误：未知符号 {X}'
                steps.append(step)
                return False, steps

            steps.append(step)

        # 结束：只剩 $，且输入也到 $
        if tokens[input_index] == '$':
            steps.append({
                'step': str(len(steps) + 1),
                'stack': '$',
                'input': '$',
                'action': '接受'
            })
            return True, steps
        else:
            # 栈空但输入未消费完（理论上不会出现于 LL(1) 正常流程）
            steps.append({
                'step': str(len(steps) + 1),
                'stack': '$',
                'input': ' '.join(tokens[input_index:]),
                'action': '错误：输入未完全匹配'
            })
            return False, steps

    # 信息导出
    def get_grammar_info(self) -> Dict:
        return {
            'grammar': {A: [['ε'] if (len(alpha) == 1 and alpha[0] == self.epsilon) else alpha
                            for alpha in prods]
                        for A, prods in self.grammar.items()},
            'terminals': sorted(list(self.terminals)),
            'non_terminals': sorted(list(self.non_terminals)),
            'start_symbol': self.start_symbol,
            'first_sets': {k: sorted(list(v)) for k, v in self.first_sets.items()
                           if k in self.non_terminals},
            'follow_sets': {k: sorted(list(v)) for k, v in self.follow_sets.items()},
            'select_sets': {A: {str(i): sorted(list(s)) for i, s in d.items()}
                            for A, d in self.select_sets.items()},
            'predict_table': {A: {a: (None if rhs is None else rhs)
                                  for a, rhs in row.items()}
                              for A, row in self.predict_table.items()},
            'conflicts': [{'A': A, 'a': a,
                           'exist': ' '.join(exist),
                           'new': ' '.join(new)}
                          for (A, a, exist, new) in self.conflicts]
        }



#测试
def create_sample_grammar_manual():
    p = LL1ParserManual()
    p.add_grammar_rule('E',  "T E'")
    p.add_grammar_rule("E'", "+ T E'")
    p.add_grammar_rule("E'", "ε")
    p.add_grammar_rule('T',  "F T'")
    p.add_grammar_rule("T'", "* F T'")
    p.add_grammar_rule("T'", "ε")
    p.add_grammar_rule('F',  "( E )")
    p.add_grammar_rule('F',  "id")
    p.set_start_symbol('E')
    return p

#自测
if __name__ == "__main__":
    parser = create_sample_grammar_manual()
    parser.compute_first_sets()
    parser.compute_follow_sets()
    parser.compute_select_sets()
    parser.build_predict_table()

    print("终结符：", sorted(parser.terminals))
    print("非终结符：", sorted(parser.non_terminals))
    for A in sorted(parser.non_terminals):
        print(f"FIRST({A}) = {sorted(parser.first_sets[A])}")
    for A in sorted(parser.non_terminals):
        print(f"FOLLOW({A}) = {sorted(parser.follow_sets[A])}")

    ok, steps = parser.analyze("id + id * id")
    print("结果：", "接受" if ok else "拒绝")
    for s in steps:
        print(f"{s['step']:>2} | 栈= [{s['stack']}], 输入= [{s['input']}], 动作= {s['action']}")