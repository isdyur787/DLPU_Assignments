# LL(1)语法分析器

By DLPU Computer Science（ISEC）231 邵昱铭 王宝飞 孙智博 肖宇航

## 项目简介

这是一个完整的 LL(1)语法分析器实现，用于编译原理课程的学习和实践。该项目实现了 LL(1)文法的核心算法，包括 First 集合、Follow 集合、Select 集合计算、预测分析表构造和 LL(1)分析算法，并提供了友好的图形化界面和文件读取功能。

## 功能特性

### 核心功能

- ✅ **文法定义**：支持自定义文法规则输入
- ✅ **First 集合计算**：自动计算所有非终结符的 First 集合
- ✅ **Follow 集合计算**：自动计算所有非终结符的 Follow 集合
- ✅ **Select 集合计算**：自动计算所有产生式的 Select 集合
- ✅ **预测分析表构造**：基于 First 和 Follow 集合构造预测分析表
- ✅ **LL(1)分析算法**：使用栈实现的自上而下分析
- ✅ **分析过程可视化**：详细显示每一步的分析过程

### 图形化界面

- 🖥️ **直观的用户界面**：基于 tkinter 的现代化 GUI
- 📊 **多标签页显示**：分别显示 First 集合、Follow 集合、Select 集合、预测分析表和文法信息
- 🔍 **实时分析**：输入字符串后立即显示分析结果
- 📝 **文法编辑器**：支持文法规则的直接编辑
- 📁 **文件加载**：支持从文件加载文法规则
- 🎯 **预设测试用例**：提供多种测试用例快速验证

## 文件结构

```
├── ll1_parser.py        # LL(1)分析器核心类
├── gui.py              # 图形化用户界面
├── 启动程序.py          # 启动脚本
├── 示例文法.txt         # 示例文法文件
├── README.md           # 项目说明文档
└── 使用说明.md         # 使用说明文档
```

## 安装和运行

### 环境要求

- Python 3.6+
- tkinter（通常随 Python 安装）

### 运行方式

#### 1. 图形界面模式（推荐）

```bash
python3 启动程序.py
```

#### 2. 直接运行图形界面

```bash
python3 gui.py
```

## 使用说明

### 图形界面使用

1. **启动程序**：运行 `python3 启动程序.py`
2. **加载示例文法**：点击"加载示例文法"按钮
3. **计算分析表**：点击"计算分析表"按钮
4. **输入测试字符串**：在输入框中输入要分析的字符串
5. **执行分析**：点击"分析"按钮查看结果
6. **查看详细信息**：切换到不同标签页查看 First 集合、Follow 集合等

### 示例文法

程序内置了算术表达式文法：

```
E → T E'
E' → + T E' | ε
T → F T'
T' → * F T' | ε
F → ( E ) | id
```

### 测试用例

- `id + id * id`
- `id * ( id + id )`
- `( id + id ) * id`
- `id + id + id`
- `id * id * id`

## 技术实现

### 核心算法

#### 1. First 集合计算

```python
def compute_first_sets(self):
    # 初始化
    for symbol in self.non_terminals:
        self.first_sets[symbol] = set()

    # 迭代计算直到收敛
    changed = True
    while changed:
        changed = False
        for non_terminal in self.non_terminals:
            old_first = self.first_sets[non_terminal].copy()
            for production in self.grammar[non_terminal]:
                first_of_production = self._compute_first_of_string(production)
                self.first_sets[non_terminal].update(first_of_production - {self.epsilon})
            if self.first_sets[non_terminal] != old_first:
                changed = True
```

#### 2. Follow 集合计算

```python
def compute_follow_sets(self):
    # 初始化
    for symbol in self.non_terminals:
        self.follow_sets[symbol] = set()

    # 开始符号的Follow集合包含$
    if self.start_symbol:
        self.follow_sets[self.start_symbol].add('$')

    # 迭代计算
    changed = True
    while changed:
        changed = False
        for non_terminal in self.non_terminals:
            for production in self.grammar[non_terminal]:
                for i, symbol in enumerate(production):
                    if symbol in self.non_terminals:
                        old_follow = self.follow_sets[symbol].copy()
                        beta = production[i+1:]
                        first_of_beta = self._compute_first_of_string(beta)
                        self.follow_sets[symbol].update(first_of_beta - {self.epsilon})
                        if self.epsilon in first_of_beta:
                            self.follow_sets[symbol].update(self.follow_sets[non_terminal])
                        if self.follow_sets[symbol] != old_follow:
                            changed = True
```

#### 3. 预测分析表构造

```python
def build_predict_table(self):
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
                self.predict_table[non_terminal][terminal] = production

            # 如果ε在First(α)中，对Follow(A)中的每个终结符b，将A→α加入M[A,b]
            if self.epsilon in first_of_production:
                for terminal in self.follow_sets[non_terminal]:
                    self.predict_table[non_terminal][terminal] = production
```

#### 4. LL(1)分析算法

```python
def analyze(self, input_string: str):
    stack = ['$', self.start_symbol]
    input_tokens = input_string.split() + ['$']
    input_index = 0
    analysis_steps = []

    while len(stack) > 1:
        X = stack[-1]
        a = input_tokens[input_index] if input_index < len(input_tokens) else '$'

        if X in self.terminals or X == '$':
            if X == a:
                stack.pop()
                input_index += 1
            else:
                return False, analysis_steps
        elif X in self.non_terminals:
            if a in self.predict_table[X] and self.predict_table[X][a] is not None:
                production = self.predict_table[X][a]
                stack.pop()
                for symbol in reversed(production):
                    if symbol != self.epsilon:
                        stack.append(symbol)
            else:
                return False, analysis_steps

    return input_tokens[input_index] == '$', analysis_steps
```

### 界面设计

- **主框架**：使用 tkinter 的 ttk 组件实现现代化界面
- **多标签页**：使用 Notebook 组件分别显示不同类型的信息
- **表格显示**：使用 Treeview 组件清晰展示分析过程
- **文本编辑**：使用 ScrolledText 组件支持文法规则编辑

## 学习价值

这个项目对于学习编译原理具有以下价值：

1. **理论与实践结合**：完整实现了 LL(1)分析的核心算法
2. **可视化学习**：通过图形界面直观理解分析过程
3. **代码可读性**：清晰的代码结构和详细的注释
4. **扩展性强**：模块化设计便于功能扩展
5. **实用性强**：可直接用于编译原理课程实验

## 注意事项

1. 当前版本主要支持消除左递归后的 LL(1)文法
2. 终结符识别基于简单规则（小写字母和特殊符号）
3. 输入字符串需要以空格分隔各个符号
4. 空符号使用 `ε` 表示

## 联系方式

1. 邮箱：shaoyuming714@gmail.com

---

**编译原理小组作业 2 - LL(1)语法分析器**
