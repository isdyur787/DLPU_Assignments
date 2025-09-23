#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 词法分析器 - 编译原理小组任务 1
#By 邵昱铭 孙智博 王宝飞 肖宇航

"""
简单测试版本
"""

from lexical_analyzer import LexicalAnalyzer

def simple_test():
    """简单测试"""
    print("开始简单测试...")
    
    analyzer = LexicalAnalyzer()
    
    # 最简单的测试代码
    test_code = "int a = 10;"
    
    print(f"测试代码: {test_code}")
    
    try:
        analyzer.set_source(test_code)
        tokens = analyzer.analyze()
        
        print("分析成功!")
        print(f"识别到 {len(tokens)} 个单词:")
        
        for i, (token_type, token_value) in enumerate(tokens[:5]):  # 只显示前5个
            print(f"  {i+1}. ({token_type}, {token_value})")
        
        if len(tokens) > 5:
            print(f"  ... 还有 {len(tokens)-5} 个单词")
            
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_test()
