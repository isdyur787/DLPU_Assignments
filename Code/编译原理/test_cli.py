#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 词法分析器 - 编译原理小组任务 1
#By 邵昱铭 孙智博 王宝飞 肖宇航

"""
命令行测试版本
"""

from lexical_analyzer import LexicalAnalyzer, TokenType

def test_analyzer():
    """测试词法分析器"""
    analyzer = LexicalAnalyzer()
    
    # 测试代码
    test_code = """
int main() {
    int a = 10;
    printf("Hello World");
    return 0;
}
"""
    
    print("测试代码:")
    print(test_code)
    print("=" * 50)
    
    # 设置源代码并分析
    analyzer.set_source(test_code)
    tokens = analyzer.analyze()
    
    print("分析结果:")
    print("二元组 (单词种别码, 单词属性值):")
    print("=" * 50)
    
    token_count = 0
    for token_type, token_value in tokens:
        if token_type == TokenType.ERROR:
            print(f"错误: 无法识别的字符 '{token_value}'")
        else:
            token_name = analyzer.get_token_name(token_type)
            if isinstance(token_value, (int, float)):
                print(f"({token_type:3d}, {token_value:10}) - {token_name}")
            else:
                print(f"({token_type:3d}, '{token_value:10}') - {token_name}")
            token_count += 1
    
    print("=" * 50)
    print(f"总共识别出 {token_count} 个单词符号")

if __name__ == "__main__":
    test_analyzer()
