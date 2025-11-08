// 应用程序主逻辑

let parser = null;

// DOM元素
const grammarInput = document.getElementById("grammarInput");
const sentenceInput = document.getElementById("sentenceInput");
const loadGrammarBtn = document.getElementById("loadGrammarBtn");
const loadSentenceBtn = document.getElementById("loadSentenceBtn");
const grammarFileInput = document.getElementById("grammarFileInput");
const sentenceFileInput = document.getElementById("sentenceFileInput");
const clearGrammarBtn = document.getElementById("clearGrammarBtn");
const clearSentenceBtn = document.getElementById("clearSentenceBtn");
const analyzeBtn = document.getElementById("analyzeBtn");
const constructTableBtn = document.getElementById("constructTableBtn");
const itemSetsOutput = document.getElementById("itemSetsOutput");
const tableOutput = document.getElementById("tableOutput");
const processOutput = document.getElementById("processOutput");
const resultOutput = document.getElementById("resultOutput");

// 文件加载
loadGrammarBtn.addEventListener("click", () => {
  grammarFileInput.click();
});

grammarFileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      grammarInput.value = event.target.result;
    };
    reader.readAsText(file);
  }
});

loadSentenceBtn.addEventListener("click", () => {
  sentenceFileInput.click();
});

sentenceFileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      sentenceInput.value = event.target.result;
    };
    reader.readAsText(file);
  }
});

// 清空按钮
clearGrammarBtn.addEventListener("click", () => {
  grammarInput.value = "";
});

clearSentenceBtn.addEventListener("click", () => {
  sentenceInput.value = "";
});

// 构造分析表
constructTableBtn.addEventListener("click", () => {
  const grammarText = grammarInput.value.trim();

  if (!grammarText) {
    alert("请先输入文法！");
    return;
  }

  try {
    parser = new LR0Parser(grammarText);
    parser.constructItemSets();
    parser.constructTable();

    displayItemSets();
    displayTable();

    resultOutput.innerHTML =
      '<div class="result-success">分析表构造成功！</div>';
  } catch (error) {
    resultOutput.innerHTML = `<div class="result-error">错误：${error.message}</div>`;
    console.error(error);
  }
});

// 分析
analyzeBtn.addEventListener("click", () => {
  const grammarText = grammarInput.value.trim();
  const sentenceText = sentenceInput.value.trim();

  if (!grammarText) {
    alert("请先输入文法！");
    return;
  }

  if (!sentenceText) {
    alert("请先输入要分析的句子！");
    return;
  }

  try {
    // 如果还没有构造分析表，先构造
    if (!parser) {
      parser = new LR0Parser(grammarText);
      parser.constructItemSets();
      parser.constructTable();
      displayItemSets();
      displayTable();
    }

    const result = parser.analyze(sentenceText);
    displayProcess(result.steps);
    displayResult(result);
  } catch (error) {
    resultOutput.innerHTML = `<div class="result-error">错误：${error.message}</div>`;
    console.error(error);
  }
});

// 显示项目集
function displayItemSets() {
  if (!parser || !parser.itemSets) {
    itemSetsOutput.innerHTML = '<div class="empty-state">请先构造分析表</div>';
    return;
  }

  let html = "";
  for (let i = 0; i < parser.itemSets.length; i++) {
    html += `<div class="item-set">
            <div class="item-set-header">I${i}:</div>
            <div class="items">${parser
              .getItemSetString(parser.itemSets[i])
              .split("\n")
              .map((item) => `<div class="item">${item}</div>`)
              .join("")}</div>
        </div>`;
  }

  itemSetsOutput.innerHTML = html || '<div class="empty-state">无项目集</div>';
}

// 显示分析表
function displayTable() {
  if (!parser || !parser.actionTable || !parser.gotoTable) {
    tableOutput.innerHTML = '<div class="empty-state">请先构造分析表</div>';
    return;
  }

  const terminals = Array.from(parser.terminals)
    .filter((t) => t !== "$")
    .sort();
  terminals.push("$");
  // 排除增广文法的开始符号
  const nonTerminals = Array.from(parser.nonTerminals)
    .filter((nt) => nt !== "S'")
    .sort();

  let html = "<table><thead><tr><th>状态</th>";

  // ACTION表头
  for (const term of terminals) {
    html += `<th>ACTION(${term})</th>`;
  }

  // GOTO表头
  for (const nonTerm of nonTerminals) {
    html += `<th>GOTO(${nonTerm})</th>`;
  }

  html += "</tr></thead><tbody>";

  for (let i = 0; i < parser.itemSets.length; i++) {
    html += `<tr><td><strong>I${i}</strong></td>`;

    // ACTION表
    for (const term of terminals) {
      const action = parser.actionTable[i]?.[term] || "";
      html += `<td>${action || "&nbsp;"}</td>`;
    }

    // GOTO表
    for (const nonTerm of nonTerminals) {
      const goto = parser.gotoTable[i]?.[nonTerm] || "";
      html += `<td>${goto !== "" ? goto : "&nbsp;"}</td>`;
    }

    html += "</tr>";
  }

  html += "</tbody></table>";
  tableOutput.innerHTML = html;
}

// 显示分析过程
function displayProcess(steps) {
  if (!steps || steps.length === 0) {
    processOutput.innerHTML = '<div class="empty-state">无分析过程</div>';
    return;
  }

  let html = "";
  for (const step of steps) {
    // 将状态栈中的数字转换为 I0, I1, ... In 格式
    const stateStack = step.stack.map((s) => `I${s}`).join(" ");
    html += `<div class="process-step">
            <div class="process-step-header">步骤 ${step.step}</div>
            <div class="process-step-content">
                <div><strong>状态栈：</strong>${stateStack}</div>
                <div><strong>符号栈：</strong>${step.symbolStack.join(
                  " "
                )}</div>
                <div><strong>剩余输入：</strong>${step.input}</div>
            </div>
            <div style="margin-top: 8px; padding: 8px; background: #e9ecef; border-radius: 4px;">
                <strong>动作：</strong>${step.action || step.error || "无"}
            </div>
        </div>`;
  }

  processOutput.innerHTML = html;
}

// 显示结果
function displayResult(result) {
  if (result.success) {
    resultOutput.innerHTML = `<div class="result-success">${result.message}</div>`;
  } else {
    resultOutput.innerHTML = `<div class="result-error">${result.message}</div>`;
  }
}

// 页面加载时加载示例
window.addEventListener("load", () => {
  // 可以在这里加载默认示例
  console.log("LR(0) 语法分析器已加载");
});
