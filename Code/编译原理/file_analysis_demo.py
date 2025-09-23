#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 词法分析器 - 编译原理小组任务 1
#By 邵昱铭 孙智博 王宝飞 肖宇航

"""
初始版本1:
文件分析演示程序 源代码写死 无交互功能
演示如何分析文件并保存结果
"""

from lexical_analyzer import LexicalAnalyzer, TokenType
import os

def analyze_file_and_save(input_file_path, output_file_path=None):
    """分析文件并保存结果"""
    analyzer = LexicalAnalyzer()
    
    # 读取源文件
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            source_code = file.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        return False
    
    print(f"正在分析文件: {input_file_path}")
    print("源代码内容:")
    print("-" * 50)
    print(source_code)
    print("-" * 50)
    
    # 执行词法分析
    analyzer.set_source(source_code)
    tokens = analyzer.analyze()
    
    # 生成输出内容
    output_content = []
    output_content.append("词法分析结果")
    output_content.append("=" * 50)
    output_content.append(f"源文件: {input_file_path}")
    output_content.append("分析时间: " + get_current_time())
    output_content.append("=" * 50)
    output_content.append("")
    output_content.append("二元组 (单词种别码, 单词属性值):")
    output_content.append("=" * 50)
    
    token_count = 0
    for token_type, token_value in tokens:
        if token_type == TokenType.ERROR:
            output_content.append(f"错误: 无法识别的字符 '{token_value}'")
        else:
            token_name = analyzer.get_token_name(token_type)
            if isinstance(token_value, (int, float)):
                output_content.append(f"({token_type:3d}, {token_value:10}) - {token_name}")
            else:
                output_content.append(f"({token_type:3d}, '{token_value:10}') - {token_name}")
            token_count += 1
    
    output_content.append("=" * 50)
    output_content.append(f"总共识别出 {token_count} 个单词符号")
    output_content.append("=" * 50)
    output_content.append("分析完成")
    
    # 如果没有指定输出文件路径，自动生成
    if not output_file_path:
        file_dir = os.path.dirname(input_file_path)
        file_name = os.path.basename(input_file_path)
        file_name_without_ext = os.path.splitext(file_name)[0]
        file_ext = os.path.splitext(file_name)[1]
        output_file_path = os.path.join(file_dir, f"{file_name_without_ext}_lexical_analysis{file_ext}")
    
    # 保存结果
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(output_content))
        
        print(f"分析完成！识别出 {token_count} 个单词符号")
        print(f"结果已保存到: {output_file_path}")
        
        # 显示前几个分析结果
        print("\n前10个分析结果:")
        for i, line in enumerate(output_content[6:16]):  # 跳过头部信息
            if line.startswith('('):
                print(f"  {line}")
        
        return True
        
    except Exception as e:
        print(f"保存文件失败: {e}")
        return False

def get_current_time():
    """获取当前时间字符串"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    """主函数"""
    print("文件分析演示程序")
    print("=" * 50)
    
    # 分析测试文件
    input_file = "test_program.c"
    if os.path.exists(input_file):
        analyze_file_and_save(input_file)
    else:
        print(f"测试文件 {input_file} 不存在")

if __name__ == "__main__":
    main()
