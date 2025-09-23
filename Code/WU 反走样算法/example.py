#!/usr/bin/env python3
"""
Wu反走样算法使用示例
展示如何使用Wu反走样算法绘制各种图形
"""

from wu_antialiasing import WuAntialiasing, draw_circle_points, draw_star
import math


def example_basic_usage():
    """基本使用示例"""
    print("基本使用示例...")
    
    # 创建画布
    wu = WuAntialiasing(400, 400)
    
    # 绘制简单直线
    wu.draw_line(50, 50, 350, 350)
    wu.draw_line(50, 350, 350, 50)
    
    # 保存图像
    wu.save_image("example_basic.png")
    print("基本示例完成，结果保存为 example_basic.png")


def example_different_angles():
    """不同角度直线示例"""
    print("不同角度直线示例...")
    
    wu = WuAntialiasing(400, 400)
    center_x, center_y = 200, 200
    
    # 绘制不同角度的直线
    angles = [0, 30, 45, 60, 90, 120, 135, 150, 180]
    colors = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.8]
    
    for angle, color in zip(angles, colors):
        rad = math.radians(angle)
        x = center_x + 150 * math.cos(rad)
        y = center_y + 150 * math.sin(rad)
        wu.draw_line(center_x, center_y, x, y, color)
    
    wu.save_image("example_angles.png")
    print("角度示例完成，结果保存为 example_angles.png")


def example_complex_shapes():
    """复杂图形示例"""
    print("复杂图形示例...")
    
    wu = WuAntialiasing(500, 500)
    
    # 绘制多个星形
    stars_config = [
        (125, 125, 60, 30, 5),   # 五角星
        (375, 125, 50, 25, 6),   # 六角星
        (125, 375, 55, 27, 8),   # 八角星
        (375, 375, 45, 22, 7),   # 七角星
    ]
    
    for center_x, center_y, outer_r, inner_r, points in stars_config:
        draw_star(wu, center_x, center_y, outer_r, inner_r, points)
    
    # 绘制中心圆形
    draw_circle_points(wu, 250, 250, 80, 60)
    
    wu.save_image("example_complex.png")
    print("复杂图形示例完成，结果保存为 example_complex.png")


def example_gradient_effect():
    """渐变效果示例"""
    print("渐变效果示例...")
    
    wu = WuAntialiasing(400, 400)
    
    # 创建渐变效果
    for i in range(20):
        y = 50 + i * 15
        intensity = 0.1 + 0.9 * (i / 19)  # 从0.1到1.0的渐变
        wu.draw_line(50, y, 350, y + 10, intensity)
    
    # 添加中心装饰
    draw_circle_points(wu, 200, 200, 50, 30)
    
    wu.save_image("example_gradient.png")
    print("渐变效果示例完成，结果保存为 example_gradient.png")


def example_artistic_pattern():
    """艺术图案示例"""
    print("艺术图案示例...")
    
    wu = WuAntialiasing(600, 600)
    
    # 创建花瓣效果
    center_x, center_y = 300, 300
    
    for petal in range(12):
        angle_offset = math.radians(petal * 30)
        
        for i in range(80):
            t = i / 80
            angle = angle_offset + t * math.pi / 3
            radius = 200 * t * (1 - t) * 6  # 花瓣形状
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            if i > 0:
                prev_angle = angle_offset + (i-1) / 80 * math.pi / 3
                prev_radius = 200 * (i-1) / 80 * (1 - (i-1) / 80) * 6
                prev_x = center_x + prev_radius * math.cos(prev_angle)
                prev_y = center_y + prev_radius * math.sin(prev_angle)
                
                intensity = 0.2 + 0.8 * (1 - t)
                wu.draw_line(prev_x, prev_y, x, y, intensity)
    
    # 添加中心装饰
    draw_circle_points(wu, center_x, center_y, 40, 25)
    
    wu.save_image("example_artistic.png")
    print("艺术图案示例完成，结果保存为 example_artistic.png")


def main():
    """主函数"""
    print("Wu反走样算法使用示例")
    print("=" * 40)
    
    try:
        example_basic_usage()
        example_different_angles()
        example_complex_shapes()
        example_gradient_effect()
        example_artistic_pattern()
        
        print("\n🎉 所有示例完成！")
        print("\n生成的示例图像:")
        print("- example_basic.png: 基本使用示例")
        print("- example_angles.png: 不同角度直线示例")
        print("- example_complex.png: 复杂图形示例")
        print("- example_gradient.png: 渐变效果示例")
        print("- example_artistic.png: 艺术图案示例")
        
    except Exception as e:
        print(f"❌ 运行示例时出错: {e}")
        print("请确保已安装所需依赖: pip install -r requirements.txt")


if __name__ == "__main__":
    main()
