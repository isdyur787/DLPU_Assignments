@echo off
REM 递归下降语法分析器 - Windows启动脚本

echo ==================================
echo   递归下降语法分析器
echo   编译原理小组作业3
echo ==================================
echo.

REM 尝试使用python3
where python3 >nul 2>nul
if %errorlevel% == 0 (
    echo 使用 python3 启动图形界面...
    python3 gui.py
    goto :end
)

REM 尝试使用python
where python >nul 2>nul
if %errorlevel% == 0 (
    echo 使用 python 启动图形界面...
    python gui.py
    goto :end
)

REM 没有找到Python
echo 错误：未找到 Python！请先安装 Python 3.6 或更高版本。
pause
exit /b 1

:end
pause

