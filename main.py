import tkinter as tk
import os
import sys
from pathlib import Path


def get_base_path() -> Path:
    """获取基础路径，支持打包和开发环境"""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent.parent


def main():
    base_path = get_base_path()
    
    if base_path.name == 'game':
        game_dir = base_path
    else:
        game_dir = base_path / 'game'
    
    if str(base_path) not in sys.path:
        sys.path.insert(0, str(base_path))
    
    from game.ui.main_frame import GameMainFrame
    
    plugins_dir = game_dir / 'plugins'
    data_dir = game_dir / 'data'
    
    plugins_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    root = tk.Tk()
    
    app = GameMainFrame(
        root=root,
        plugins_dir=str(plugins_dir),
        data_dir=str(data_dir)
    )
    
    app.run()


if __name__ == '__main__':
    main()
