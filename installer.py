#!/usr/bin/env python3
"""
游戏合集安装程序
支持自定义安装路径
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil
import os
import sys
from pathlib import Path
import subprocess


class Installer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("游戏合集 - 安装程序")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.install_path = tk.StringVar(value=str(Path.home() / "GameCollection"))
        self.create_desktop_shortcut = tk.BooleanVar(value=True)
        self.create_start_menu = tk.BooleanVar(value=True)
        
        self.setup_ui()
        
    def setup_ui(self):
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 18, "bold"))
        style.configure("Info.TLabel", font=("Arial", 10))
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(
            main_frame, 
            text="🎮 游戏合集 安装向导", 
            style="Title.TLabel"
        )
        title_label.pack(pady=(0, 20))
        
        info_frame = ttk.LabelFrame(main_frame, text="安装信息", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(info_frame, text="包含游戏：", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        ttk.Label(info_frame, text="  • 2048 - 经典数字合并游戏", style="Info.TLabel").pack(anchor=tk.W)
        ttk.Label(info_frame, text="  • 五子棋 - 双人对弈棋类游戏", style="Info.TLabel").pack(anchor=tk.W)
        ttk.Label(info_frame, text="  • 华容道 - 经典滑块益智游戏", style="Info.TLabel").pack(anchor=tk.W)
        
        path_frame = ttk.LabelFrame(main_frame, text="安装路径", padding="10")
        path_frame.pack(fill=tk.X, pady=(0, 15))
        
        path_entry_frame = ttk.Frame(path_frame)
        path_entry_frame.pack(fill=tk.X)
        
        ttk.Entry(path_entry_frame, textvariable=self.install_path, width=50).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(path_entry_frame, text="浏览...", command=self.browse_path).pack(side=tk.LEFT)
        
        options_frame = ttk.LabelFrame(main_frame, text="安装选项", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Checkbutton(
            options_frame, 
            text="创建桌面快捷方式", 
            variable=self.create_desktop_shortcut
        ).pack(anchor=tk.W)
        
        ttk.Checkbutton(
            options_frame, 
            text="创建开始菜单快捷方式", 
            variable=self.create_start_menu
        ).pack(anchor=tk.W)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="安装", command=self.install, width=15).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="取消", command=self.root.quit, width=15).pack(side=tk.RIGHT)
        
    def browse_path(self):
        path = filedialog.askdirectory(
            title="选择安装路径",
            initialdir=self.install_path.get()
        )
        if path:
            self.install_path.set(path)
            
    def create_shortcut(self, shortcut_path, target_path, name):
        try:
            import pythoncom
            from win32com.shell import shell, shellcon
            
            shortcut = pythoncom.CoCreateInstance(
                shell.CLSID_ShellLink,
                None,
                pythoncom.CLSCTX_INPROC_SERVER,
                shell.IID_IShellLink
            )
            shortcut.SetPath(str(target_path))
            shortcut.SetWorkingDirectory(str(Path(target_path).parent))
            shortcut.SetDescription(f"游戏合集 - {name}")
            
            persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
            persist_file.Save(str(shortcut_path), 0)
            return True
        except ImportError:
            bat_path = Path(shortcut_path).with_suffix('.bat')
            with open(bat_path, 'w') as f:
                f.write(f'@echo off\nstart "" "{target_path}"\n')
            return True
        except Exception as e:
            print(f"创建快捷方式失败: {e}")
            return False
            
    def install(self):
        install_dir = Path(self.install_path.get())
        
        if install_dir.exists() and list(install_dir.iterdir()):
            if not messagebox.askyesno(
                "确认", 
                f"目录 {install_dir} 已存在且不为空，是否继续安装？"
            ):
                return
        
        progress_window = tk.Toplevel(self.root)
        progress_window.title("安装中...")
        progress_window.geometry("400x100")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        ttk.Label(progress_window, text="正在安装，请稍候...").pack(pady=10)
        progress = ttk.Progressbar(progress_window, mode='determinate', length=350)
        progress.pack(pady=10)
        
        def do_install():
            try:
                install_dir.mkdir(parents=True, exist_ok=True)
                progress['value'] = 10
                progress_window.update()
                
                if getattr(sys, 'frozen', False):
                    source_dir = Path(sys._MEIPASS)
                else:
                    source_dir = Path(__file__).parent
                
                exe_source = source_dir / 'GameCollection.exe'
                if exe_source.exists():
                    shutil.copy2(exe_source, install_dir / 'GameCollection.exe')
                    progress['value'] = 30
                    progress_window.update()
                
                for item in ['plugins', 'data', 'interfaces', 'core', 'ui']:
                    src = source_dir / item
                    dst = install_dir / item
                    if src.exists():
                        if dst.exists():
                            shutil.rmtree(dst)
                        shutil.copytree(src, dst)
                        progress['value'] += 10
                        progress_window.update()
                
                if self.create_desktop_shortcut.get():
                    desktop = Path.home() / 'Desktop'
                    if desktop.exists():
                        self.create_shortcut(
                            desktop / '游戏合集.lnk',
                            install_dir / 'GameCollection.exe',
                            '游戏合集'
                        )
                    progress['value'] = 85
                    progress_window.update()
                
                if self.create_start_menu.get():
                    start_menu = Path.home() / 'AppData' / 'Roaming' / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs'
                    if start_menu.exists():
                        self.create_shortcut(
                            start_menu / '游戏合集.lnk',
                            install_dir / 'GameCollection.exe',
                            '游戏合集'
                        )
                    progress['value'] = 95
                    progress_window.update()
                
                progress['value'] = 100
                progress_window.update()
                
                progress_window.destroy()
                
                messagebox.showinfo(
                    "安装完成", 
                    f"游戏合集已成功安装到：\n{install_dir}\n\n点击确定退出安装程序。"
                )
                self.root.quit()
                
            except Exception as e:
                progress_window.destroy()
                messagebox.showerror("安装失败", f"安装过程中发生错误：\n{str(e)}")
                
        self.root.after(100, do_install)
        
    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    installer = Installer()
    installer.run()
