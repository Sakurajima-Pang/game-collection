@echo off
chcp 65001 >nul
echo ========================================
echo    游戏合集 - 打包脚本
echo ========================================
echo.

echo [1/3] 清理旧的构建文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo [2/3] 打包主程序...
pyinstaller build.spec --clean

echo [3/3] 打包安装程序...
pyinstaller --onefile --windowed --name "GameCollectionInstaller" installer.py

echo.
echo ========================================
echo 打包完成！
echo 主程序: dist\GameCollection.exe
echo 安装程序: dist\GameCollectionInstaller.exe
echo ========================================
pause
