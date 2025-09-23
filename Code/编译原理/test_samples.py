#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 词法分析器 - 编译原理小组任务 1
#By 邵昱铭 孙智博 王宝飞 肖宇航
"""
测试用例
包含各种测试样本代码
"""

# 测试用例1: 简单C程序
test_case_1 = """
int main() {
    int a = 10;
    printf("Hello World");
    return 0;
}
"""

# 测试用例2: 包含各种运算符和界符
test_case_2 = """
int x = 5;
float y = 3.14;
char c = 'A';
string name = "John";

if (x > 0 && y < 10.0) {
    x = x + y;
    y = y * 2.0;
}
"""

# 测试用例3: 循环和条件语句
test_case_3 = """
for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) {
        printf("Even: %d", i);
    } else {
        continue;
    }
}
"""

# 测试用例4: 复杂表达式
test_case_4 = """
int a = 10, b = 20;
float result = (a + b) * 3.14 / 2.0;
string message = "Result is: " + result;
"""

# 测试用例5: 错误字符测试
test_case_5 = """
int valid_var = 100;
int @invalid = 200;  // 错误字符
float num = 3.14;
"""

def get_test_cases():
    """获取所有测试用例"""
    return {
        "简单C程序": test_case_1,
        "运算符和界符": test_case_2,
        "循环和条件": test_case_3,
        "复杂表达式": test_case_4,
        "错误字符测试": test_case_5
    }

if __name__ == "__main__":
    cases = get_test_cases()
    for name, code in cases.items():
        print(f"=== {name} ===")
        print(code)
        print("-" * 50)
