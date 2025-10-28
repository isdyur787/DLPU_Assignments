#!/bin/bash

# 递归下降语法分析器 - 启动脚本

echo "=================================="
echo "  递归下降语法分析器"
echo "  编译原理小组作业3"
echo "=================================="
echo ""

# 检查Python版本
if command -v python3 &> /dev/null; then
    echo "使用 python3 启动图形界面..."
    python3 gui.py
elif command -v python &> /dev/null; then
    echo "使用 python 启动图形界面..."
    python gui.py
else
    echo "错误：未找到 Python！请先安装 Python 3.6 或更高版本。"
    exit 1
fi

