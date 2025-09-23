"""
Wu反走样算法演示程序
展示各种图形和反走样效果
"""

import numpy as np
import matplotlib.pyplot as plt
from wu_antialiasing import WuAntialiasing, draw_circle_points, draw_star
import math


def demo_basic_lines():
    """演示基本直线绘制"""
    print("演示基本直线绘制...")
    
    wu = WuAntialiasing(300, 300)
    
    # 绘制不同角度的直线
    center_x, center_y = 150, 150
    radius = 120
    
    # 绘制放射状直线
    for i in range(0, 360, 15):
        angle = math.radians(i)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        wu.draw_line(center_x, center_y, x, y, 0.8)
    
    wu.save_image("demo_basic_lines.png")
    print("基本直线演示完成，结果保存为 demo_basic_lines.png")


def demo_complex_shapes():
    """演示复杂图形"""
    print("演示复杂图形...")
    
    wu = WuAntialiasing(400, 400)
    
    # 绘制多个星形
    stars = [
        (100, 100, 50, 25, 5),   # 五角星
        (300, 100, 40, 20, 6),   # 六角星
        (100, 300, 45, 22, 8),   # 八角星
        (300, 300, 35, 17, 7),   # 七角星
    ]
    
    for center_x, center_y, outer_r, inner_r, points in stars:
        draw_star(wu, center_x, center_y, outer_r, inner_r, points)
    
    # 绘制圆形点集
    draw_circle_points(wu, 200, 200, 80, 100)
    
    wu.save_image("demo_complex_shapes.png")
    print("复杂图形演示完成，结果保存为 demo_complex_shapes.png")


def demo_antialiasing_comparison():
    """演示反走样效果对比"""
    print("演示反走样效果对比...")
    
    # 创建高分辨率画布用于放大显示
    wu = WuAntialiasing(600, 200)
    
    # 绘制细线以展示反走样效果
    for i in range(10):
        y = 20 + i * 16
        wu.draw_line(50, y, 550, y + 5, 0.9)
    
    wu.save_image("demo_antialiasing_comparison.png")
    print("反走样效果对比演示完成，结果保存为 demo_antialiasing_comparison.png")


def demo_gradient_lines():
    """演示渐变直线"""
    print("演示渐变直线...")
    
    wu = WuAntialiasing(400, 400)
    
    # 绘制从中心向外的渐变直线
    center_x, center_y = 200, 200
    
    for i in range(0, 360, 5):
        angle = math.radians(i)
        x = center_x + 150 * math.cos(angle)
        y = center_y + 150 * math.sin(angle)
        
        # 根据角度计算颜色强度
        intensity = 0.3 + 0.7 * abs(math.sin(angle * 3))
        wu.draw_line(center_x, center_y, x, y, intensity)
    
    wu.save_image("demo_gradient_lines.png")
    print("渐变直线演示完成，结果保存为 demo_gradient_lines.png")


def demo_spiral():
    """演示螺旋图形"""
    print("演示螺旋图形...")
    
    wu = WuAntialiasing(400, 400)
    
    center_x, center_y = 200, 200
    max_radius = 150
    num_turns = 3
    num_points = 1000
    
    prev_x, prev_y = center_x, center_y
    
    for i in range(1, num_points):
        t = i / num_points
        angle = 2 * math.pi * num_turns * t
        radius = max_radius * t
        
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        # 根据半径计算颜色强度
        intensity = 0.5 + 0.5 * (1 - t)
        wu.draw_line(prev_x, prev_y, x, y, intensity)
        
        prev_x, prev_y = x, y
    
    wu.save_image("demo_spiral.png")
    print("螺旋图形演示完成，结果保存为 demo_spiral.png")


def demo_geometric_patterns():
    """演示几何图案"""
    print("演示几何图案...")
    
    wu = WuAntialiasing(500, 500)
    
    # 绘制六边形
    center_x, center_y = 250, 250
    radius = 100
    
    hex_points = []
    for i in range(6):
        angle = math.radians(i * 60)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        hex_points.append((x, y))
    
    # 连接六边形顶点
    for i in range(6):
        x0, y0 = hex_points[i]
        x1, y1 = hex_points[(i + 1) % 6]
        wu.draw_line(x0, y0, x1, y1, 0.8)
    
    # 绘制内部连接线
    for i in range(6):
        x0, y0 = hex_points[i]
        x1, y1 = hex_points[(i + 2) % 6]
        wu.draw_line(x0, y0, x1, y1, 0.6)
    
    # 绘制同心圆
    for r in range(20, 100, 20):
        draw_circle_points(wu, center_x, center_y, r, 50)
    
    wu.save_image("demo_geometric_patterns.png")
    print("几何图案演示完成，结果保存为 demo_geometric_patterns.png")


def demo_artistic_design():
    """演示艺术设计"""
    print("演示艺术设计...")
    
    wu = WuAntialiasing(600, 600)
    
    # 创建花瓣效果
    center_x, center_y = 300, 300
    
    for petal in range(8):
        angle_offset = math.radians(petal * 45)
        
        for i in range(50):
            t = i / 50
            angle = angle_offset + t * math.pi / 2
            radius = 150 * t * (1 - t) * 4  # 花瓣形状
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            if i > 0:
                prev_angle = angle_offset + (i-1) / 50 * math.pi / 2
                prev_radius = 150 * (i-1) / 50 * (1 - (i-1) / 50) * 4
                prev_x = center_x + prev_radius * math.cos(prev_angle)
                prev_y = center_y + prev_radius * math.sin(prev_angle)
                
                intensity = 0.3 + 0.7 * (1 - t)
                wu.draw_line(prev_x, prev_y, x, y, intensity)
    
    # 添加中心装饰
    draw_circle_points(wu, center_x, center_y, 30, 20)
    
    wu.save_image("demo_artistic_design.png")
    print("艺术设计演示完成，结果保存为 demo_artistic_design.png")


def create_summary_image():
    """创建总结图像，展示所有效果"""
    print("创建总结图像...")
    
    # 创建一个大画布
    wu = WuAntialiasing(800, 600)
    
    # 绘制标题
    title_lines = [
        (100, 550, 700, 550),  # 上边框
        (100, 50, 700, 50),    # 下边框
        (100, 550, 100, 50),   # 左边框
        (700, 550, 700, 50),   # 右边框
    ]
    
    for x0, y0, x1, y1 in title_lines:
        wu.draw_line(x0, y0, x1, y1, 0.8)
    
    # 绘制各种示例
    # 1. 基本直线
    for i in range(5):
        y = 100 + i * 20
        wu.draw_line(150, y, 250, y + 10, 0.7)
    
    # 2. 星形
    draw_star(wu, 350, 150, 40, 20, 5)
    
    # 3. 圆形
    draw_circle_points(wu, 500, 150, 40, 30)
    
    # 4. 螺旋
    center_x, center_y = 200, 350
    prev_x, prev_y = center_x, center_y
    for i in range(1, 100):
        t = i / 100
        angle = 2 * math.pi * 2 * t
        radius = 60 * t
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        wu.draw_line(prev_x, prev_y, x, y, 0.6)
        prev_x, prev_y = x, y
    
    # 5. 几何图案
    hex_center_x, hex_center_y = 450, 350
    for i in range(6):
        angle = math.radians(i * 60)
        x = hex_center_x + 50 * math.cos(angle)
        y = hex_center_y + 50 * math.sin(angle)
        wu.draw_line(hex_center_x, hex_center_y, x, y, 0.8)
    
    # 6. 渐变效果
    for i in range(20):
        x = 600 + i * 5
        y = 350 + i * 2
        intensity = 0.2 + 0.8 * (i / 20)
        wu.draw_line(600, 350, x, y, intensity)
    
    wu.save_image("summary_demo.png")
    print("总结图像创建完成，结果保存为 summary_demo.png")


def main():
    """主函数"""
    print("Wu反走样算法演示程序")
    print("=" * 50)
    
    # 运行所有演示
    demo_basic_lines()
    demo_complex_shapes()
    demo_antialiasing_comparison()
    demo_gradient_lines()
    demo_spiral()
    demo_geometric_patterns()
    demo_artistic_design()
    create_summary_image()
    
    print("\n所有演示完成！")
    print("生成的图像文件:")
    print("- demo_basic_lines.png: 基本直线演示")
    print("- demo_complex_shapes.png: 复杂图形演示")
    print("- demo_antialiasing_comparison.png: 反走样效果对比")
    print("- demo_gradient_lines.png: 渐变直线演示")
    print("- demo_spiral.png: 螺旋图形演示")
    print("- demo_geometric_patterns.png: 几何图案演示")
    print("- demo_artistic_design.png: 艺术设计演示")
    print("- summary_demo.png: 总结图像")


if __name__ == "__main__":
    main()
