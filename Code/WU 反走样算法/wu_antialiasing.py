"""
Wu反走样算法实现
Wu反走样算法是一种用于绘制平滑直线的算法，通过计算像素的覆盖度来实现反走样效果。
"""

import math
import numpy as np
from typing import Tuple, List


class WuAntialiasing:
    """Wu反走样算法类"""
    
    def __init__(self, width: int, height: int):
        """
        初始化画布
        
        Args:
            width: 画布宽度
            height: 画布高度
        """
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width), dtype=np.float32)
    
    def _fpart(self, x: float) -> float:
        """获取浮点数的小数部分"""
        return x - math.floor(x)
    
    def _rfpart(self, x: float) -> float:
        """获取浮点数的反向小数部分 (1 - 小数部分)"""
        return 1 - self._fpart(x)
    
    def _plot(self, x: int, y: int, brightness: float):
        """
        在指定位置绘制像素
        
        Args:
            x: x坐标
            y: y坐标
            brightness: 亮度值 (0.0-1.0)
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.canvas[y, x] = min(1.0, max(0.0, brightness))
    
    def draw_line(self, x0: float, y0: float, x1: float, y1: float, color: float = 1.0):
        """
        使用Wu反走样算法绘制直线
        
        Args:
            x0: 起点x坐标
            y0: 起点y坐标
            x1: 终点x坐标
            y1: 终点y坐标
            color: 颜色强度 (0.0-1.0)
        """
        # 计算直线参数
        dx = x1 - x0
        dy = y1 - y0
        
        # 如果dx和dy都很小，直接绘制单个像素
        if abs(dx) < 1e-6 and abs(dy) < 1e-6:
            self._plot(int(round(x0)), int(round(y0)), color)
            return
        
        # 确定主方向
        if abs(dx) > abs(dy):
            # x方向为主方向
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                dx = -dx
                dy = -dy
            
            gradient = dy / dx if dx != 0 else 0
            
            # 处理第一个端点
            xend = round(x0)
            yend = y0 + gradient * (xend - x0)
            xgap = self._rfpart(x0 + 0.5)
            xpxl1 = int(xend)
            ypxl1 = int(yend)
            
            self._plot(xpxl1, ypxl1, self._rfpart(yend) * xgap * color)
            self._plot(xpxl1, ypxl1 + 1, self._fpart(yend) * xgap * color)
            
            intery = yend + gradient
            
            # 处理第二个端点
            xend = round(x1)
            yend = y1 + gradient * (xend - x1)
            xgap = self._fpart(x1 + 0.5)
            xpxl2 = int(xend)
            ypxl2 = int(yend)
            
            self._plot(xpxl2, ypxl2, self._rfpart(yend) * xgap * color)
            self._plot(xpxl2, ypxl2 + 1, self._fpart(yend) * xgap * color)
            
            # 绘制中间部分
            for x in range(xpxl1 + 1, xpxl2):
                self._plot(x, int(intery), self._rfpart(intery) * color)
                self._plot(x, int(intery) + 1, self._fpart(intery) * color)
                intery += gradient
        else:
            # y方向为主方向
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                dx = -dx
                dy = -dy
            
            gradient = dx / dy if dy != 0 else 0
            
            # 处理第一个端点
            yend = round(y0)
            xend = x0 + gradient * (yend - y0)
            ygap = self._rfpart(y0 + 0.5)
            ypxl1 = int(yend)
            xpxl1 = int(xend)
            
            self._plot(xpxl1, ypxl1, self._rfpart(xend) * ygap * color)
            self._plot(xpxl1 + 1, ypxl1, self._fpart(xend) * ygap * color)
            
            interx = xend + gradient
            
            # 处理第二个端点
            yend = round(y1)
            xend = y1 + gradient * (yend - y1)
            ygap = self._fpart(y1 + 0.5)
            ypxl2 = int(yend)
            xpxl2 = int(xend)
            
            self._plot(xpxl2, ypxl2, self._rfpart(xend) * ygap * color)
            self._plot(xpxl2 + 1, ypxl2, self._fpart(xend) * ygap * color)
            
            # 绘制中间部分
            for y in range(ypxl1 + 1, ypxl2):
                self._plot(int(interx), y, self._rfpart(interx) * color)
                self._plot(int(interx) + 1, y, self._fpart(interx) * color)
                interx += gradient
    
    def clear(self):
        """清空画布"""
        self.canvas.fill(0.0)
    
    def get_canvas(self) -> np.ndarray:
        """获取画布数据"""
        return self.canvas.copy()
    
    def save_image(self, filename: str):
        """
        保存图像到文件
        
        Args:
            filename: 文件名
        """
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 8))
        plt.imshow(self.canvas, cmap='gray', origin='lower')
        plt.colorbar()
        plt.title('Wu反走样算法结果')
        plt.xlabel('X坐标')
        plt.ylabel('Y坐标')
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()


def draw_circle_points(wu: WuAntialiasing, center_x: float, center_y: float, radius: float, num_points: int = 100):
    """
    绘制圆形点集
    
    Args:
        wu: Wu反走样对象
        center_x: 圆心x坐标
        center_y: 圆心y坐标
        radius: 半径
        num_points: 点的数量
    """
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        wu.draw_line(center_x, center_y, x, y, 0.8)


def draw_star(wu: WuAntialiasing, center_x: float, center_y: float, outer_radius: float, inner_radius: float, num_points: int = 5):
    """
    绘制星形
    
    Args:
        wu: Wu反走样对象
        center_x: 中心x坐标
        center_y: 中心y坐标
        outer_radius: 外半径
        inner_radius: 内半径
        num_points: 星形点数
    """
    points = []
    for i in range(num_points * 2):
        angle = math.pi * i / num_points
        if i % 2 == 0:
            radius = outer_radius
        else:
            radius = inner_radius
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    
    # 连接所有点形成星形
    for i in range(len(points)):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % len(points)]
        wu.draw_line(x0, y0, x1, y1, 0.9)
