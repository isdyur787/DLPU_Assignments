#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LL(1)语法分析器启动程序
By Group2 邵昱铭 王宝飞 孙智博 肖宇航
"""

import sys
import os

def main():
    """主函数"""
    print("=" * 60)
    print("LL(1)语法分析器")
    print("编译原理小组作业2")
    print("By DLPU Computer Science（ISEC）231")
    print("邵昱铭 王宝飞 孙智博 肖宇航")
    print("=" * 60)
    print()
    
    try:
        print("启动图形界面...")
        import tkinter as tk
        from gui import LL1ParserGUI
        root = tk.Tk()
        app = LL1ParserGUI(root)
        print("GUI界面启动成功！")
        print("\n使用说明：")
        print("1. 点击'加载示例文法'加载默认文法")
        print("2. 点击'计算分析表'计算First/Follow集合和预测分析表")
        print("3. 输入测试字符串如'id + id * id'")
        print("4. 点击'分析'按钮查看分析结果")
        print("5. 切换标签页查看详细信息")
        print("=" * 60)
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装tkinter库")
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()