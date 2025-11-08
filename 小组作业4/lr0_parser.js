// LR(0) 语法分析器核心实现

class LR0Parser {
  // By 邵昱铭
  constructor(grammarText) {
    const rawGrammar = this.parseGrammar(grammarText);
    if (rawGrammar.length === 0) {
      throw new Error("文法不能为空");
    }

    // 创建增广文法：添加 S' -> S
    this.startSymbol = rawGrammar[0].left;
    this.grammar = [
      { left: "S'", right: [this.startSymbol] }, // 增广文法的开始产生式
      ...rawGrammar,
    ];

    this.terminals = new Set();
    this.nonTerminals = new Set();
    this.itemSets = [];
    this.actionTable = {};
    this.gotoTable = {};
    this.extractSymbols();
  }

  // 解析文法文本
  parseGrammar(grammarText) {
    const lines = grammarText
      .trim()
      .split("\n")
      .filter((line) => line.trim());
    const grammar = [];

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;

      // 支持 -> 或 ::= 作为箭头
      const arrowMatch = trimmed.match(/^(.*?)\s*(->|::=)\s*(.*)$/);
      if (!arrowMatch) continue;

      const left = arrowMatch[1].trim();
      const right = arrowMatch[3].trim();

      // 处理多个选择（用 | 分隔）
      const productions = right.split("|").map((p) => p.trim());

      for (const production of productions) {
        // 处理空产生式（ε 或 empty）
        const symbols =
          production === "ε" || production === "empty" || production === ""
            ? []
            : production.split(/\s+/).filter((s) => s);

        grammar.push({
          left: left,
          right: symbols,
        });
      }
    }

    return grammar;
  }

  // 提取终结符和非终结符
  extractSymbols() {
    this.nonTerminals.clear();
    this.terminals.clear();

    // 添加所有非终结符
    for (const rule of this.grammar) {
      this.nonTerminals.add(rule.left);
    }

    // 添加终结符（在产生式右侧但不是非终结符的符号）
    for (const rule of this.grammar) {
      for (const symbol of rule.right) {
        if (!this.nonTerminals.has(symbol)) {
          this.terminals.add(symbol);
        }
      }
    }

    // 添加结束符 $
    this.terminals.add("$");
    // 确保增广文法的开始符号不在终结符集合中
    this.terminals.delete("S'");
  }

  // 计算项目集的闭包
  closure(items) {
    const closureSet = new Set();
    const queue = [...items];

    // 将初始项目添加到闭包
    for (const item of items) {
      closureSet.add(JSON.stringify(item));
    }

    while (queue.length > 0) {
      const item = queue.shift();
      const [ruleIndex, dotPos] = item;
      const rule = this.grammar[ruleIndex];

      // 如果点后面还有符号
      if (dotPos < rule.right.length) {
        const nextSymbol = rule.right[dotPos];

        // 如果下一个符号是非终结符，添加所有以该非终结符为左部的产生式的项目
        if (this.nonTerminals.has(nextSymbol)) {
          for (let i = 0; i < this.grammar.length; i++) {
            const rule2 = this.grammar[i];
            if (rule2.left === nextSymbol) {
              const newItem = [i, 0];
              const itemStr = JSON.stringify(newItem);

              if (!closureSet.has(itemStr)) {
                closureSet.add(itemStr);
                queue.push(newItem);
              }
            }
          }
        }
      }
    }

    return Array.from(closureSet).map((s) => JSON.parse(s));
  }

  // 计算项目集的转换函数
  // By 孙智博
  goto(items, symbol) {
    const gotoItems = [];

    for (const item of items) {
      const [ruleIndex, dotPos] = item;
      const rule = this.grammar[ruleIndex];

      // 如果点后面是给定符号
      if (dotPos < rule.right.length && rule.right[dotPos] === symbol) {
        gotoItems.push([ruleIndex, dotPos + 1]);
      }
    }

    return gotoItems.length > 0 ? this.closure(gotoItems) : [];
  }

  // 比较两个项目集是否相等
  itemSetsEqual(set1, set2) {
    if (set1.length !== set2.length) return false;
    const s1 = new Set(set1.map((i) => JSON.stringify(i)));
    const s2 = new Set(set2.map((i) => JSON.stringify(i)));
    if (s1.size !== s2.size) return false;
    for (const item of s1) {
      if (!s2.has(item)) return false;
    }
    return true;
  }

  // 查找项目集在列表中的索引
  findItemSetIndex(itemSet) {
    for (let i = 0; i < this.itemSets.length; i++) {
      if (this.itemSetsEqual(this.itemSets[i], itemSet)) {
        return i;
      }
    }
    return -1;
  }

  // 构造LR(0)项目集规范族
  constructItemSets() {
    this.itemSets = [];
    const itemSetMap = new Map();

    // 初始化：添加增广文法的初始项目 [0, 0] 表示第一个产生式（S' -> S）的项目
    const initialItems = this.closure([[0, 0]]);
    this.itemSets.push(initialItems);
    const initialKey = JSON.stringify(
      initialItems.map((i) => JSON.stringify(i)).sort()
    );
    itemSetMap.set(initialKey, 0);

    let setIndex = 0;

    while (setIndex < this.itemSets.length) {
      const currentSet = this.itemSets[setIndex];
      // 排除增广文法的开始符号
      const allSymbols = [...this.terminals, ...this.nonTerminals].filter(
        (s) => s !== "S'"
      );

      for (const symbol of allSymbols) {
        const gotoSet = this.goto(currentSet, symbol);

        if (gotoSet.length > 0) {
          const gotoSetKey = JSON.stringify(
            gotoSet.map((i) => JSON.stringify(i)).sort()
          );

          if (!itemSetMap.has(gotoSetKey)) {
            // 新项目集
            const newIndex = this.itemSets.length;
            this.itemSets.push(gotoSet);
            itemSetMap.set(gotoSetKey, newIndex);
          }
        }
      }

      setIndex++;
    }

    return this.itemSets;
  }

  // 构造LR(0)分析表
  // By 王宝飞
  constructTable() {
    this.actionTable = {};
    this.gotoTable = {};

    // 初始化表
    for (let i = 0; i < this.itemSets.length; i++) {
      this.actionTable[i] = {};
      this.gotoTable[i] = {};

      for (const term of this.terminals) {
        if (term !== "$") {
          this.actionTable[i][term] = "";
        }
      }
      this.actionTable[i]["$"] = "";

      for (const nonTerm of this.nonTerminals) {
        this.gotoTable[i][nonTerm] = "";
      }
    }

    // 填充表
    for (let i = 0; i < this.itemSets.length; i++) {
      const itemSet = this.itemSets[i];

      for (const item of itemSet) {
        const [ruleIndex, dotPos] = item;
        const rule = this.grammar[ruleIndex];

        if (dotPos < rule.right.length) {
          // 移进项目
          const nextSymbol = rule.right[dotPos];
          const gotoSet = this.goto(itemSet, nextSymbol);

          if (gotoSet.length > 0) {
            const j = this.findItemSetIndex(gotoSet);

            if (j !== -1) {
              if (this.terminals.has(nextSymbol)) {
                // 移进动作
                const currentAction = this.actionTable[i][nextSymbol];
                if (currentAction === "") {
                  this.actionTable[i][nextSymbol] = `s${j}`;
                } else if (currentAction === `s${j}`) {
                  // 已经设置过相同的移进动作，保持不变
                } else {
                  // 冲突：移进-归约冲突或移进-移进冲突
                  if (!currentAction.includes(`s${j}`)) {
                    this.actionTable[i][nextSymbol] = `${currentAction},s${j}`;
                  }
                }
              } else if (this.nonTerminals.has(nextSymbol)) {
                // GOTO表：如果已经有值且不同，表示冲突
                const currentGoto = this.gotoTable[i][nextSymbol];
                if (currentGoto === "" || currentGoto === j) {
                  this.gotoTable[i][nextSymbol] = j;
                } else {
                  // GOTO冲突（不应该在LR(0)中发生）
                  this.gotoTable[i][nextSymbol] = `${currentGoto},${j}`;
                }
              }
            }
          }
        } else {
          // 归约项目
          if (ruleIndex === 0 && rule.left === "S'") {
            // 接受项目（增广文法的第一个产生式）
            this.actionTable[i]["$"] = "acc";
          } else {
            // 归约项目：对所有终结符都添加归约动作
            // 注意：ruleIndex > 0，因为增广文法的产生式（ruleIndex=0）已经在上面处理
            for (const term of this.terminals) {
              if (term === "$" && ruleIndex === 0) continue; // 接受项目已处理
              const currentAction = this.actionTable[i][term];
              if (currentAction === "") {
                this.actionTable[i][term] = `r${ruleIndex}`;
              } else if (currentAction === `r${ruleIndex}`) {
                // 已经设置过相同的归约动作，保持不变
              } else {
                // 冲突：归约-归约冲突或移进-归约冲突
                if (!currentAction.includes(`r${ruleIndex}`)) {
                  this.actionTable[i][term] = `${currentAction},r${ruleIndex}`;
                }
              }
            }
          }
        }
      }
    }

    return {
      action: this.actionTable,
      goto: this.gotoTable,
    };
  }

  // 分析输入串
  // By 肖宇航
  analyze(input) {
    const tokens = input
      .trim()
      .split(/\s+/)
      .filter((t) => t);
    if (tokens.length === 0) {
      return {
        success: false,
        message: "输入串为空",
        steps: [],
      };
    }

    tokens.push("$"); // 添加结束符

    const stack = [0]; // 状态栈
    const symbolStack = ["$"]; // 符号栈
    const steps = [];
    let ip = 0; // 输入指针

    while (true) {
      const state = stack[stack.length - 1];
      const symbol = tokens[ip];

      const action = this.actionTable[state]?.[symbol] || "";

      const step = {
        step: steps.length + 1,
        stack: [...stack],
        symbolStack: [...symbolStack],
        input: tokens.slice(ip).join(" "),
        action: action,
      };

      if (!action) {
        step.error = `错误：在状态 I${state}，符号 ${symbol} 处没有可执行的动作`;
        steps.push(step);
        return {
          success: false,
          message: `语法错误：在状态 I${state}，遇到符号 ${symbol} 时没有可执行的动作`,
          steps: steps,
        };
      }

      if (action === "acc") {
        step.action = "接受";
        steps.push(step);
        return {
          success: true,
          message: "分析成功：输入串是语法上正确的句子",
          steps: steps,
        };
      }

      if (action.startsWith("s")) {
        // 移进
        const nextState = parseInt(action.substring(1));
        stack.push(nextState);
        symbolStack.push(symbol);
        ip++;
        step.action = `移进 ${symbol}，进入状态 I${nextState}`;
      } else if (action.startsWith("r")) {
        // 归约
        const ruleIndex = parseInt(action.substring(1));
        const rule = this.grammar[ruleIndex];
        const popCount = rule.right.length;

        // 对于空产生式，不需要弹出符号
        if (popCount > 0 && popCount > stack.length - 1) {
          step.error = `错误：无法归约，栈中元素不足`;
          steps.push(step);
          return {
            success: false,
            message: `语法错误：无法归约产生式 ${this.getProductionString(
              ruleIndex
            )}`,
            steps: steps,
          };
        }

        // 弹出栈（对于空产生式，popCount为0，不弹出）
        for (let i = 0; i < popCount; i++) {
          stack.pop();
          symbolStack.pop();
        }

        // 获取新的状态
        const newState = stack[stack.length - 1];
        const gotoState = this.gotoTable[newState]?.[rule.left];

        if (gotoState === "" || gotoState === undefined) {
          step.error = `错误：GOTO表中没有状态转移`;
          steps.push(step);
          return {
            success: false,
            message: `语法错误：无法从状态 I${newState} 转移到 ${rule.left}`,
            steps: steps,
          };
        }

        stack.push(gotoState);
        symbolStack.push(rule.left);
        step.action = `归约：${this.getProductionString(
          ruleIndex
        )}，进入状态 I${gotoState}`;
        step.gotoState = gotoState;
      } else {
        step.error = `未知动作：${action}`;
        steps.push(step);
        return {
          success: false,
          message: `未知动作：${action}`,
          steps: steps,
        };
      }

      steps.push(step);
    }
  }

  // 获取项目集的可读表示
  getItemSetString(itemSet) {
    return itemSet
      .map(([ruleIndex, dotPos]) => {
        const rule = this.grammar[ruleIndex];
        const right = [...rule.right];
        if (right.length === 0) {
          return `${rule.left} -> ·`;
        }
        right.splice(dotPos, 0, "·");
        return `${rule.left} -> ${right.join(" ")}`;
      })
      .join("\n");
  }

  // 获取产生式的字符串表示
  getProductionString(ruleIndex) {
    const rule = this.grammar[ruleIndex];
    if (rule.right.length === 0) {
      return `${rule.left} -> ε`;
    }
    return `${rule.left} -> ${rule.right.join(" ")}`;
  }
}
