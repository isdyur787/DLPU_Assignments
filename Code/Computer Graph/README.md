# 直线绘制演示（DDA、中点算法与 Bresenham 算法）

该项目提供一个 Java Swing 图形界面，输入两点 (x1, y1) 与 (x2, y2)，选择算法（DDA、中点算法或 Bresenham 算法），在画布中绘制直线。支持鼠标在画布上选点：左键两次选两点后自动绘制；右键清空。坐标系默认以左下角为原点，支持缩放与平移，支持全象限绘制（包括负数坐标）。

## 编译与运行

要求：JDK 8+。

```bash
# 进入项目根目录
cd "/Users/shaoyuming/Desktop/DLPU/Code/Computer Graph"

# 编译（会生成 out 目录）
mkdir -p out && javac -encoding UTF-8 -d out src/LineDrawingApp.java

# 运行
java -cp out LineDrawingApp
```

## 使用说明

- 左侧面板：选择算法（DDA、中点、Bresenham）、输入 x1 y1 x2 y2（支持负数），点击"绘制直线"。
- 右侧画布：展示以像素为单位的绘制结果，带自适应网格、坐标轴与刻度。
- 鼠标交互：
  - 左键第一次点击设置 (x1,y1)，第二次点击设置 (x2,y2) 并按当前算法绘制
  - 右键点击清空所选点与绘制内容
  - 中键拖拽进行平移
  - 滚轮缩放（以鼠标为中心）。状态栏会显示世界坐标与当前缩放
- 算法说明：
  - DDA：使用浮点增量，蓝色显示
  - 中点算法：Bresenham 变体，红色显示
  - Bresenham：经典 Bresenham 算法，绿色显示
- 支持全象限绘制，包括负数坐标输入。

## 目录结构

```
/Users/shaoyuming/Desktop/DLPU/Code/Computer Graph
├── src
│  └── LineDrawingApp.java
└── README.md
```
