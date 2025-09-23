# Wu反走样算法测试用例

import unittest
import numpy as np
import math
import matplotlib.pyplot as plt
import os
from wu_antialiasing import WuAntialiasing, draw_circle_points, draw_star


class TestWuAntialiasing(unittest.TestCase):
    """Wu反走样算法测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.width = 200
        self.height = 200
        self.wu = WuAntialiasing(self.width, self.height)
    
    def test_basic_line_horizontal(self):
        """测试水平直线"""
        self.wu.clear()
        self.wu.draw_line(10, 50, 190, 50)
        
        # 检查水平线上的像素
        line_pixels = self.wu.canvas[50, 10:191]
        self.assertGreater(np.sum(line_pixels), 0, "水平直线应该有像素被绘制")
        
        # 保存测试结果
        self.wu.save_image("test_horizontal_line.png")
        print("水平直线测试完成，结果保存为 test_horizontal_line.png")
    
    def test_basic_line_vertical(self):
        """测试垂直直线"""
        self.wu.clear()
        self.wu.draw_line(100, 10, 100, 190)
        
        # 检查垂直线上的像素
        line_pixels = self.wu.canvas[10:191, 100]
        self.assertGreater(np.sum(line_pixels), 0, "垂直直线应该有像素被绘制")
        
        # 保存测试结果
        self.wu.save_image("test_vertical_line.png")
        print("垂直直线测试完成，结果保存为 test_vertical_line.png")
    
    def test_diagonal_line(self):
        """测试对角线"""
        self.wu.clear()
        self.wu.draw_line(10, 10, 190, 190)
        
        # 检查对角线上的像素
        diagonal_sum = 0
        for i in range(10, 191):
            diagonal_sum += self.wu.canvas[i, i]
        
        self.assertGreater(diagonal_sum, 0, "对角线应该有像素被绘制")
        
        # 保存测试结果
        self.wu.save_image("test_diagonal_line.png")
        print("对角线测试完成，结果保存为 test_diagonal_line.png")
    
    def test_thin_line(self):
        """测试细线（小角度）"""
        self.wu.clear()
        self.wu.draw_line(10, 100, 190, 110)
        
        # 检查细线区域
        line_region = self.wu.canvas[95:115, 10:191]
        self.assertGreater(np.sum(line_region), 0, "细线应该有像素被绘制")
        
        # 保存测试结果
        self.wu.save_image("test_thin_line.png")
        print("细线测试完成，结果保存为 test_thin_line.png")
    
    def test_antialiasing_quality(self):
        """测试反走样质量"""
        self.wu.clear()
        # 绘制多条不同角度的直线
        angles = [0, 15, 30, 45, 60, 75, 90]
        center_x, center_y = 100, 100
        radius = 80
        
        for i, angle in enumerate(angles):
            rad = math.radians(angle)
            x = center_x + radius * math.cos(rad)
            y = center_y + radius * math.sin(rad)
            self.wu.draw_line(center_x, center_y, x, y, 0.8)
        
        # 保存测试结果
        self.wu.save_image("test_antialiasing_quality.png")
        print("反走样质量测试完成，结果保存为 test_antialiasing_quality.png")
    
    def test_circle_points(self):
        """测试圆形点集"""
        self.wu.clear()
        draw_circle_points(self.wu, 100, 100, 80, 50)
        
        # 检查圆形区域
        circle_region = self.wu.canvas[20:180, 20:180]
        self.assertGreater(np.sum(circle_region), 0, "圆形点集应该有像素被绘制")
        
        # 保存测试结果
        self.wu.save_image("test_circle_points.png")
        print("圆形点集测试完成，结果保存为 test_circle_points.png")
    
    def test_star_shape(self):
        """测试星形"""
        self.wu.clear()
        draw_star(self.wu, 100, 100, 80, 40, 5)
        
        # 检查星形区域
        star_region = self.wu.canvas[20:180, 20:180]
        self.assertGreater(np.sum(star_region), 0, "星形应该有像素被绘制")
        
        # 保存测试结果
        self.wu.save_image("test_star_shape.png")
        print("星形测试完成，结果保存为 test_star_shape.png")
    
    def test_edge_cases(self):
        """测试边界情况"""
        self.wu.clear()
        
        # 测试单点
        self.wu.draw_line(100, 100, 100, 100)
        self.assertGreater(self.wu.canvas[100, 100], 0, "单点应该被绘制")
        
        # 测试画布边界
        self.wu.draw_line(0, 0, self.width-1, self.height-1)
        self.assertGreater(self.wu.canvas[0, 0], 0, "边界点应该被绘制")
        
        # 保存测试结果
        self.wu.save_image("test_edge_cases.png")
        print("边界情况测试完成，结果保存为 test_edge_cases.png")
    
    def test_color_intensity(self):
        """测试颜色强度"""
        self.wu.clear()
        
        # 绘制不同强度的直线
        intensities = [0.2, 0.5, 0.8, 1.0]
        for i, intensity in enumerate(intensities):
            y = 50 + i * 30
            self.wu.draw_line(20, y, 180, y, intensity)
        
        # 保存测试结果
        self.wu.save_image("test_color_intensity.png")
        print("颜色强度测试完成，结果保存为 test_color_intensity.png")


def run_comparison_test():
    """运行对比测试，比较Wu算法和简单直线算法的效果"""
    import matplotlib.pyplot as plt
    
    # 创建两个画布进行对比
    wu_canvas = WuAntialiasing(200, 200)
    simple_canvas = np.zeros((200, 200), dtype=np.float32)
    
    # 绘制相同的直线
    x0, y0, x1, y1 = 10, 10, 190, 190
    
    # Wu反走样算法
    wu_canvas.draw_line(x0, y0, x1, y1)
    
    # 简单直线算法（Bresenham算法）
    def simple_line(x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        x, y = x0, y0
        while True:
            if 0 <= x < 200 and 0 <= y < 200:
                simple_canvas[y, x] = 1.0
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
    
    simple_line(int(x0), int(y0), int(x1), int(y1))
    
    # 创建对比图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    ax1.imshow(wu_canvas.get_canvas(), cmap='gray', origin='lower')
    ax1.set_title('Wu反走样算法')
    ax1.set_xlabel('X坐标')
    ax1.set_ylabel('Y坐标')
    
    ax2.imshow(simple_canvas, cmap='gray', origin='lower')
    ax2.set_title('简单直线算法')
    ax2.set_xlabel('X坐标')
    ax2.set_ylabel('Y坐标')
    
    plt.tight_layout()
    plt.savefig('comparison_test.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("对比测试完成，结果保存为 comparison_test.png")


def run_performance_test():
    """运行性能测试"""
    import time
    
    # 测试不同画布大小的性能
    sizes = [(100, 100), (200, 200), (500, 500), (1000, 1000)]
    
    print("性能测试结果:")
    print("画布大小\t绘制时间(秒)\t像素数量")
    print("-" * 40)
    
    for width, height in sizes:
        wu = WuAntialiasing(width, height)
        
        start_time = time.time()
        # 绘制多条直线
        for i in range(10):
            wu.draw_line(0, 0, width-1, height-1)
            wu.draw_line(0, height-1, width-1, 0)
        end_time = time.time()
        
        draw_time = end_time - start_time
        pixel_count = width * height
        
        print(f"{width}x{height}\t{draw_time:.4f}\t\t{pixel_count}")


if __name__ == "__main__":
    # 运行单元测试
    print("开始运行Wu反走样算法测试...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # 运行对比测试
    print("\n运行对比测试...")
    run_comparison_test()
    
    # 运行性能测试
    print("\n运行性能测试...")
    run_performance_test()
    
    print("\n所有测试完成！")
