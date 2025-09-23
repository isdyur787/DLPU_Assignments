#!/usr/bin/env python3
"""
Wu反走样算法测试运行脚本
"""

import sys
import os

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import numpy
        import matplotlib
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def run_basic_test():
    """运行基本测试"""
    print("\n🧪 运行基本功能测试...")
    try:
        from wu_antialiasing import WuAntialiasing
        
        # 创建画布并绘制测试直线
        wu = WuAntialiasing(200, 200)
        wu.draw_line(10, 10, 190, 190)
        wu.draw_line(10, 190, 190, 10)
        
        # 检查是否有像素被绘制
        if wu.canvas.sum() > 0:
            print("✅ 基本绘制功能正常")
            return True
        else:
            print("❌ 基本绘制功能异常")
            return False
    except Exception as e:
        print(f"❌ 基本测试失败: {e}")
        return False

def run_visual_test():
    """运行可视化测试"""
    print("\n🎨 运行可视化测试...")
    try:
        from wu_antialiasing import WuAntialiasing, draw_star, draw_circle_points
        
        wu = WuAntialiasing(300, 300)
        
        # 绘制测试图形
        draw_star(wu, 150, 150, 80, 40, 5)
        draw_circle_points(wu, 150, 150, 60, 30)
        
        # 保存测试图像
        wu.save_image("test_output.png")
        
        if os.path.exists("test_output.png"):
            print("✅ 可视化功能正常，测试图像已保存为 test_output.png")
            return True
        else:
            print("❌ 可视化功能异常")
            return False
    except Exception as e:
        print(f"❌ 可视化测试失败: {e}")
        return False

def main():
    """主函数"""
    print("Wu反走样算法测试程序")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 运行基本测试
    if not run_basic_test():
        sys.exit(1)
    
    # 运行可视化测试
    if not run_visual_test():
        sys.exit(1)
    
    print("\n🎉 所有测试通过！")
    print("\n可用的命令:")
    print("- python test_wu_antialiasing.py  # 运行完整测试套件")
    print("- python demo.py                  # 运行演示程序")
    print("- python wu_antialiasing.py       # 查看核心算法代码")

if __name__ == "__main__":
    main()
