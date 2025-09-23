#!/usr/bin/env python3
"""
Wu反走样算法简化测试（不依赖matplotlib）
"""

import numpy as np
import math
from wu_antialiasing import WuAntialiasing, draw_circle_points, draw_star


def test_basic_functionality():
    """测试基本功能"""
    print("测试基本功能...")
    
    # 创建画布
    wu = WuAntialiasing(200, 200)
    
    # 绘制测试直线
    wu.draw_line(10, 10, 190, 190)
    wu.draw_line(10, 190, 190, 10)
    
    # 检查是否有像素被绘制
    total_pixels = np.sum(wu.canvas > 0)
    max_brightness = np.max(wu.canvas)
    
    print(f"✅ 绘制的像素数量: {total_pixels}")
    print(f"✅ 最大亮度值: {max_brightness:.3f}")
    
    if total_pixels > 0 and max_brightness > 0:
        print("✅ 基本功能测试通过")
        return True
    else:
        print("❌ 基本功能测试失败")
        return False


def test_different_angles():
    """测试不同角度"""
    print("\n测试不同角度...")
    
    wu = WuAntialiasing(200, 200)
    center_x, center_y = 100, 100
    
    # 绘制不同角度的直线
    angles = [0, 45, 90, 135, 180, 225, 270, 315]
    for angle in angles:
        rad = math.radians(angle)
        x = center_x + 80 * math.cos(rad)
        y = center_y + 80 * math.sin(rad)
        wu.draw_line(center_x, center_y, x, y, 0.8)
    
    total_pixels = np.sum(wu.canvas > 0)
    print(f"✅ 多角度绘制像素数量: {total_pixels}")
    
    if total_pixels > 100:  # 应该有足够的像素
        print("✅ 多角度测试通过")
        return True
    else:
        print("❌ 多角度测试失败")
        return False


def test_complex_shapes():
    """测试复杂图形"""
    print("\n测试复杂图形...")
    
    wu = WuAntialiasing(200, 200)
    
    # 绘制星形
    draw_star(wu, 100, 100, 60, 30, 5)
    
    # 绘制圆形点集
    draw_circle_points(wu, 100, 100, 40, 20)
    
    total_pixels = np.sum(wu.canvas > 0)
    print(f"✅ 复杂图形像素数量: {total_pixels}")
    
    if total_pixels > 50:
        print("✅ 复杂图形测试通过")
        return True
    else:
        print("❌ 复杂图形测试失败")
        return False


def test_edge_cases():
    """测试边界情况"""
    print("\n测试边界情况...")
    
    wu = WuAntialiasing(100, 100)
    
    # 测试单点
    wu.draw_line(50, 50, 50, 50)
    single_point = wu.canvas[50, 50]
    
    # 测试边界
    wu.draw_line(0, 0, 99, 99)
    corner_pixels = wu.canvas[0, 0] + wu.canvas[99, 99]
    
    print(f"✅ 单点亮度: {single_point:.3f}")
    print(f"✅ 边界像素亮度: {corner_pixels:.3f}")
    
    if single_point > 0 and corner_pixels > 0:
        print("✅ 边界情况测试通过")
        return True
    else:
        print("❌ 边界情况测试失败")
        return False


def test_antialiasing_quality():
    """测试反走样质量"""
    print("\n测试反走样质量...")
    
    wu = WuAntialiasing(200, 200)
    
    # 绘制细线
    wu.draw_line(50, 100, 150, 110)
    
    # 检查是否有中间亮度值（反走样的特征）
    unique_values = len(np.unique(wu.canvas))
    max_brightness = np.max(wu.canvas)
    min_brightness = np.min(wu.canvas[wu.canvas > 0])
    
    print(f"✅ 唯一亮度值数量: {unique_values}")
    print(f"✅ 最大亮度: {max_brightness:.3f}")
    print(f"✅ 最小非零亮度: {min_brightness:.3f}")
    
    # 反走样应该有多个不同的亮度值
    if unique_values > 3 and min_brightness < max_brightness:
        print("✅ 反走样质量测试通过")
        return True
    else:
        print("❌ 反走样质量测试失败")
        return False


def save_simple_output():
    """保存简单的文本输出"""
    print("\n保存测试结果...")
    
    wu = WuAntialiasing(50, 50)
    wu.draw_line(10, 10, 40, 40)
    
    # 保存为简单的文本格式
    with open("test_output.txt", "w") as f:
        f.write("Wu反走样算法测试结果\n")
        f.write("=" * 30 + "\n")
        f.write("画布大小: 50x50\n")
        f.write("绘制直线: (10,10) -> (40,40)\n\n")
        
        f.write("画布数据 (0-1范围):\n")
        for y in range(50):
            line = ""
            for x in range(50):
                value = wu.canvas[y, x]
                if value > 0.5:
                    line += "█"
                elif value > 0.1:
                    line += "▓"
                elif value > 0:
                    line += "░"
                else:
                    line += " "
            f.write(line + "\n")
        
        f.write(f"\n统计信息:\n")
        f.write(f"总像素数: {np.sum(wu.canvas > 0)}\n")
        f.write(f"最大亮度: {np.max(wu.canvas):.3f}\n")
        f.write(f"平均亮度: {np.mean(wu.canvas[wu.canvas > 0]):.3f}\n")
    
    print("✅ 测试结果已保存为 test_output.txt")


def main():
    """主函数"""
    print("Wu反走样算法简化测试")
    print("=" * 40)
    
    tests = [
        test_basic_functionality,
        test_different_angles,
        test_complex_shapes,
        test_edge_cases,
        test_antialiasing_quality,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试出错: {e}")
    
    print(f"\n测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
        save_simple_output()
    else:
        print("⚠️  部分测试失败，请检查代码")


if __name__ == "__main__":
    main()
