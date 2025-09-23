# Wu 反走样算法实现

这是一个用 Python 实现的 Wu 反走样算法库，用于绘制平滑的直线和图形。

## 算法简介

Wu 反走样算法（Wu's line algorithm）是一种用于绘制平滑直线的算法，由 Xiaolin Wu 在 1991 年提出。该算法通过计算像素的覆盖度来实现反走样效果，使得绘制的直线看起来更加平滑，没有锯齿状边缘。

## 主要特性

- ✅ 完整的 Wu 反走样算法实现
- ✅ 支持任意角度的直线绘制
- ✅ 可调节颜色强度
- ✅ 提供多种图形绘制功能（圆形、星形等）
- ✅ 完整的测试用例
- ✅ 可视化演示程序
- ✅ 性能测试功能

## 文件结构

```
WU 反走样算法/
├── wu_antialiasing.py      # 核心算法实现
├── test_wu_antialiasing.py # 测试用例
├── demo.py                 # 演示程序
└── README.md              # 说明文档
```

## 安装依赖

```bash
pip install numpy matplotlib
```

## 快速开始

### 基本使用

```python
from wu_antialiasing import WuAntialiasing

# 创建画布
wu = WuAntialiasing(400, 400)

# 绘制直线
wu.draw_line(10, 10, 390, 390)

# 保存图像
wu.save_image("output.png")
```

### 绘制复杂图形

```python
from wu_antialiasing import WuAntialiasing, draw_circle_points, draw_star

wu = WuAntialiasing(400, 400)

# 绘制星形
draw_star(wu, 200, 200, 100, 50, 5)

# 绘制圆形点集
draw_circle_points(wu, 200, 200, 80, 50)

# 保存图像
wu.save_image("complex_shapes.png")
```

## API 文档

### WuAntialiasing 类

#### 构造函数

```python
WuAntialiasing(width: int, height: int)
```

- `width`: 画布宽度
- `height`: 画布高度

#### 主要方法

##### draw_line(x0, y0, x1, y1, color=1.0)

绘制反走样直线

- `x0, y0`: 起点坐标
- `x1, y1`: 终点坐标
- `color`: 颜色强度 (0.0-1.0)

##### clear()

清空画布

##### get_canvas()

获取画布数据（numpy 数组）

##### save_image(filename)

保存图像到文件

### 辅助函数

#### draw_circle_points(wu, center_x, center_y, radius, num_points=100)

绘制圆形点集

- `wu`: WuAntialiasing 对象
- `center_x, center_y`: 圆心坐标
- `radius`: 半径
- `num_points`: 点的数量

#### draw_star(wu, center_x, center_y, outer_radius, inner_radius, num_points=5)

绘制星形

- `wu`: WuAntialiasing 对象
- `center_x, center_y`: 中心坐标
- `outer_radius`: 外半径
- `inner_radius`: 内半径
- `num_points`: 星形点数

## 运行测试

```bash
python test_wu_antialiasing.py
```

测试包括：

- 基本直线绘制测试
- 边界情况测试
- 反走样质量测试
- 性能测试
- 对比测试（与简单直线算法对比）

## 运行演示

```bash
python demo.py
```

演示程序会生成多个图像文件，展示不同的图形效果：

- `demo_basic_lines.png`: 基本直线演示
- `demo_complex_shapes.png`: 复杂图形演示
- `demo_antialiasing_comparison.png`: 反走样效果对比
- `demo_gradient_lines.png`: 渐变直线演示
- `demo_spiral.png`: 螺旋图形演示
- `demo_geometric_patterns.png`: 几何图案演示
- `demo_artistic_design.png`: 艺术设计演示
- `summary_demo.png`: 总结图像

## 算法原理

Wu 反走样算法的核心思想是：

1. **主方向确定**: 根据直线的斜率确定主要绘制方向（x 方向或 y 方向）
2. **端点处理**: 对直线的两个端点进行特殊处理，计算部分像素的覆盖度
3. **中间像素**: 对于中间像素，根据与理想直线的距离计算覆盖度
4. **亮度计算**: 根据覆盖度计算像素的亮度值

### 关键公式

- 小数部分: `fpart(x) = x - floor(x)`
- 反向小数部分: `rfpart(x) = 1 - fpart(x)`
- 像素亮度: `brightness = coverage * color_intensity`

## 性能特点

- **时间复杂度**: O(max(|dx|, |dy|))，其中 dx 和 dy 是直线的坐标差
- **空间复杂度**: O(width × height)
- **适用场景**: 适合绘制平滑的直线和简单图形

## 扩展功能

### 自定义图形绘制

```python
def draw_custom_shape(wu):
    """绘制自定义图形"""
    # 绘制多边形
    points = [(100, 100), (200, 100), (250, 150), (200, 200), (100, 200)]
    for i in range(len(points)):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % len(points)]
        wu.draw_line(x0, y0, x1, y1, 0.8)
```

### 动画效果

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def create_animation():
    """创建动画效果"""
    fig, ax = plt.subplots()

    def animate(frame):
        wu = WuAntialiasing(200, 200)
        angle = frame * 0.1
        x = 100 + 80 * math.cos(angle)
        y = 100 + 80 * math.sin(angle)
        wu.draw_line(100, 100, x, y)

        ax.clear()
        ax.imshow(wu.get_canvas(), cmap='gray', origin='lower')
        ax.set_title(f'Frame {frame}')

    anim = animation.FuncAnimation(fig, animate, frames=100, interval=50)
    anim.save('animation.gif', writer='pillow')
```

## 注意事项

1. **坐标系统**: 使用标准的计算机图形学坐标系统，原点在左下角
2. **颜色值**: 颜色强度范围为 0.0 到 1.0
3. **边界检查**: 算法会自动处理超出画布边界的像素
4. **浮点精度**: 使用浮点坐标可以获得更精确的绘制效果

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 参考文献

- Wu, Xiaolin. "An efficient antialiasing technique." ACM SIGGRAPH Computer Graphics 25.4 (1991): 143-152.
