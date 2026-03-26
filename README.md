# 🎮 游戏合集 (Game Collection)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个基于 Python + Tkinter 开发的桌面游戏合集，包含三款经典益智游戏。

> **本项目由 [Trae](https://trae.ai/) 和 [GLM-5](https://www.zhipuai.cn/) 生成**

## 🎯 包含游戏

| 游戏 | 描述 | 特色 |
|------|------|------|
| **2048** | 经典数字合并游戏 | 方向键/WASD控制，挑战2048！ |
| **五子棋** | 双人对弈棋类游戏 | 15×15棋盘，五子连珠获胜 |
| **华容道** | 经典滑块益智游戏 | 5个关卡，让曹操逃出重围 |

## ✨ 功能特点

- 🎨 现代化 GUI 界面
- 🔌 插件化架构，易于扩展新游戏
- 💾 游戏存档/读档功能
- 📦 支持打包为独立可执行文件
- 🖥️ Windows 安装程序（支持自定义安装路径）

## 📦 安装与运行

### 方式一：直接运行（需要Python环境）

```bash
# 克隆仓库
git clone https://github.com/Sakurajima-Pang/game-collection.git
cd game-collection

# 运行游戏
python main.py
```

### 方式二：打包为可执行文件

```bash
# 安装 PyInstaller
pip install pyinstaller

# 运行打包脚本
build.bat
```

打包完成后：
- 主程序：`dist/GameCollection.exe`
- 安装程序：`dist/GameCollectionInstaller.exe`

## 🎮 游戏操作

### 2048
- **方向键** 或 **WASD**：移动方块
- 合并相同数字，目标是达到2048！

### 五子棋
- **鼠标点击**：落子
- 黑棋先行，五子连珠获胜

### 华容道
- **鼠标点击**：选择方块
- **方向键** 或 **WASD**：移动方块
- 目标：让曹操（红色大方块）从底部出口逃出

## 🏗️ 项目结构

```
game/
├── main.py              # 程序入口
├── build.spec           # PyInstaller配置
├── build.bat            # 打包脚本
├── installer.py         # 安装程序
├── core/                # 核心模块
│   ├── plugin_manager.py    # 插件管理器
│   └── persistence.py       # 数据持久化
├── interfaces/          # 接口定义
│   ├── game_interface.py    # 游戏接口
│   └── persistence_interface.py  # 持久化接口
├── ui/                  # 用户界面
│   └── main_frame.py        # 主界面
├── plugins/             # 游戏插件
│   ├── game2048/            # 2048游戏
│   ├── gomoku/              # 五子棋
│   └── huarongdao/          # 华容道
└── data/                # 数据目录
    └── saves/               # 存档文件
```

## 🔌 开发新游戏插件

1. 在 `plugins/` 目录下创建新文件夹
2. 创建 `plugin.py` 文件，实现 `IGame` 接口
3. 创建 `__init__.py`，导出 `GameClass`

```python
from game.interfaces import IGame

class MyGame(IGame):
    @property
    def game_id(self) -> str:
        return "my_game"
    
    @property
    def game_name(self) -> str:
        return "我的游戏"
    
    # ... 实现其他接口方法
```

## 📝 系统要求

- Python 3.8+
- Windows / macOS / Linux
- 无需额外依赖（仅使用Python标准库）

## 📄 许可证

MIT License

---

**本项目由 [Trae](https://trae.ai/) 和 [GLM-5](https://www.zhipuai.cn/) 生成**
