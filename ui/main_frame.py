import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional, Dict, Any
from ..interfaces import IGame
from ..core import PluginManager, JSONPersistence


class GameMainFrame:
    """游戏管理器主界面"""
    
    def __init__(self, root: tk.Tk, plugins_dir: str, data_dir: str):
        self._root = root
        self._root.title("游戏管理器")
        self._root.geometry("1000x700")
        self._root.minsize(800, 600)
        
        self._plugin_manager = PluginManager(plugins_dir)
        self._persistence = JSONPersistence(data_dir)
        
        self._current_game: Optional[IGame] = None
        self._current_game_class_name: Optional[str] = None
        self._current_game_panel: Optional[tk.Frame] = None
        
        self._setup_ui()
        self._load_plugins()
    
    def _setup_ui(self) -> None:
        self._setup_styles()
        
        self._main_container = ttk.PanedWindow(
            self._root, 
            orient=tk.HORIZONTAL
        )
        self._main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self._setup_left_panel()
        self._setup_right_panel()
    
    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.configure('Game.TButton', font=('微软雅黑', 10), padding=10)
        style.configure('Game.TLabel', font=('微软雅黑', 11))
        style.configure('Title.TLabel', font=('微软雅黑', 14, 'bold'))
        style.configure('Info.TLabel', font=('微软雅黑', 9))
    
    def _setup_left_panel(self) -> None:
        left_frame = ttk.Frame(self._main_container, width=250)
        left_frame.pack_propagate(False)
        
        title_label = ttk.Label(
            left_frame, 
            text="🎮 游戏列表", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(10, 5))
        
        self._game_list_frame = ttk.Frame(left_frame)
        self._game_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self._game_buttons: Dict[str, ttk.Button] = {}
        
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=10)
        
        self._setup_game_controls(left_frame)
        
        self._main_container.add(left_frame, weight=1)
    
    def _setup_game_controls(self, parent: ttk.Frame) -> None:
        controls_frame = ttk.LabelFrame(parent, text="游戏控制", padding=10)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self._btn_new_game = ttk.Button(
            controls_frame,
            text="🆕 新游戏",
            command=self._on_new_game,
            style='Game.TButton'
        )
        self._btn_new_game.pack(fill=tk.X, pady=2)
        
        self._btn_save_game = ttk.Button(
            controls_frame,
            text="💾 保存游戏",
            command=self._on_save_game,
            style='Game.TButton'
        )
        self._btn_save_game.pack(fill=tk.X, pady=2)
        
        self._btn_load_game = ttk.Button(
            controls_frame,
            text="📂 加载存档",
            command=self._on_load_game,
            style='Game.TButton'
        )
        self._btn_load_game.pack(fill=tk.X, pady=2)
        
        self._btn_delete_save = ttk.Button(
            controls_frame,
            text="🗑️ 删除存档",
            command=self._on_delete_save,
            style='Game.TButton'
        )
        self._btn_delete_save.pack(fill=tk.X, pady=2)
        
        self._set_buttons_state(False)
    
    def _setup_right_panel(self) -> None:
        right_frame = ttk.Frame(self._main_container)
        
        self._game_title_label = ttk.Label(
            right_frame,
            text="请选择一个游戏",
            style='Title.TLabel'
        )
        self._game_title_label.pack(pady=10)
        
        self._game_info_label = ttk.Label(
            right_frame,
            text="",
            style='Info.TLabel'
        )
        self._game_info_label.pack()
        
        self._game_container = ttk.Frame(right_frame)
        self._game_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._welcome_frame = ttk.Frame(self._game_container)
        self._welcome_frame.pack(fill=tk.BOTH, expand=True)
        
        welcome_text = """
        欢迎来到游戏管理器！
        
        👈 请从左侧选择一个游戏开始
        
        功能说明：
        • 点击游戏名称开始游戏
        • 新游戏 - 开始新一局
        • 保存游戏 - 保存当前进度
        • 加载存档 - 读取已保存的游戏
        • 删除存档 - 删除不需要的存档
        """
        
        welcome_label = ttk.Label(
            self._welcome_frame,
            text=welcome_text,
            style='Game.TLabel',
            justify=tk.CENTER
        )
        welcome_label.pack(expand=True)
        
        self._main_container.add(right_frame, weight=4)
    
    def _load_plugins(self) -> None:
        self._plugin_manager.discover_plugins()
        self._refresh_game_list()
    
    def _refresh_game_list(self) -> None:
        for widget in self._game_list_frame.winfo_children():
            widget.destroy()
        
        self._game_buttons.clear()
        
        games_info = self._plugin_manager.get_game_info_list()
        
        for info in games_info:
            btn = ttk.Button(
                self._game_list_frame,
                text=f"🎯 {info['game_name']}",
                command=lambda cn=info['class_name']: self._select_game(cn),
                style='Game.TButton'
            )
            btn.pack(fill=tk.X, pady=3)
            self._game_buttons[info['class_name']] = btn
            
            desc_label = ttk.Label(
                self._game_list_frame,
                text=f"   {info['description']}",
                style='Info.TLabel'
            )
            desc_label.pack(anchor=tk.W, padx=5)
    
    def _select_game(self, game_class_name: str) -> None:
        if self._current_game_class_name == game_class_name:
            return
        
        self._unload_current_game()
        
        self._current_game = self._plugin_manager.get_game(game_class_name)
        self._current_game_class_name = game_class_name
        
        if self._current_game:
            self._game_title_label.config(text=f"🎯 {self._current_game.game_name}")
            self._game_info_label.config(
                text=f"版本: {self._current_game.game_version} | {self._current_game.game_description}"
            )
            
            self._welcome_frame.pack_forget()
            
            self._current_game_panel = self._current_game.create_game_panel(
                self._game_container
            )
            self._current_game_panel.pack(fill=tk.BOTH, expand=True)
            
            self._set_buttons_state(True)
            
            for class_name, btn in self._game_buttons.items():
                if class_name == game_class_name:
                    btn.config(text=f"▶️ {self._current_game.game_name}")
                else:
                    game = self._plugin_manager.get_game(class_name)
                    if game:
                        btn.config(text=f"🎯 {game.game_name}")
    
    def _unload_current_game(self) -> None:
        if self._current_game:
            self._current_game.destroy()
            self._current_game = None
            self._current_game_class_name = None
        
        if self._current_game_panel:
            self._current_game_panel.pack_forget()
            self._current_game_panel = None
        
        self._set_buttons_state(False)
    
    def _set_buttons_state(self, enabled: bool) -> None:
        state = tk.NORMAL if enabled else tk.DISABLED
        self._btn_new_game.config(state=state)
        self._btn_save_game.config(state=state)
        self._btn_load_game.config(state=state)
        self._btn_delete_save.config(state=state)
    
    def _on_new_game(self) -> None:
        if self._current_game:
            self._current_game.new_game()
    
    def _on_save_game(self) -> None:
        if not self._current_game:
            return
        
        slot_name = simpledialog.askstring(
            "保存游戏",
            "请输入存档名称：",
            parent=self._root
        )
        
        if slot_name:
            save_data = self._current_game.save_game()
            save_data['info'] = self._current_game.get_save_info() or {}
            
            if self._persistence.save(
                self._current_game.game_id,
                slot_name,
                save_data
            ):
                messagebox.showinfo("成功", f"游戏已保存为: {slot_name}")
            else:
                messagebox.showerror("错误", "保存失败")
    
    def _on_load_game(self) -> None:
        if not self._current_game:
            return
        
        saves = self._persistence.list_saves(self._current_game.game_id)
        
        if not saves:
            messagebox.showinfo("提示", "没有找到存档")
            return
        
        save_window = tk.Toplevel(self._root)
        save_window.title("选择存档")
        save_window.geometry("400x300")
        save_window.transient(self._root)
        save_window.grab_set()
        
        ttk.Label(
            save_window,
            text="选择要加载的存档：",
            style='Title.TLabel'
        ).pack(pady=10)
        
        list_frame = ttk.Frame(save_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        save_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=('微软雅黑', 10)
        )
        save_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=save_listbox.yview)
        
        for save in saves:
            display_text = f"{save['slot_name']} - {save['timestamp'][:19]}"
            if save.get('info'):
                info_str = " | ".join(f"{k}: {v}" for k, v in save['info'].items())
                display_text += f" | {info_str}"
            save_listbox.insert(tk.END, display_text)
        
        def do_load():
            selection = save_listbox.curselection()
            if selection:
                idx = selection[0]
                slot_name = saves[idx]['slot_name']
                data = self._persistence.load(
                    self._current_game.game_id,
                    slot_name
                )
                if data and self._current_game.load_game(data):
                    messagebox.showinfo("成功", f"已加载存档: {slot_name}")
                    save_window.destroy()
                else:
                    messagebox.showerror("错误", "加载失败")
        
        ttk.Button(
            save_window,
            text="加载",
            command=do_load,
            style='Game.TButton'
        ).pack(pady=10)
    
    def _on_delete_save(self) -> None:
        if not self._current_game:
            return
        
        saves = self._persistence.list_saves(self._current_game.game_id)
        
        if not saves:
            messagebox.showinfo("提示", "没有找到存档")
            return
        
        save_window = tk.Toplevel(self._root)
        save_window.title("删除存档")
        save_window.geometry("400x300")
        save_window.transient(self._root)
        save_window.grab_set()
        
        ttk.Label(
            save_window,
            text="选择要删除的存档：",
            style='Title.TLabel'
        ).pack(pady=10)
        
        list_frame = ttk.Frame(save_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        save_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=('微软雅黑', 10)
        )
        save_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=save_listbox.yview)
        
        for save in saves:
            display_text = f"{save['slot_name']} - {save['timestamp'][:19]}"
            save_listbox.insert(tk.END, display_text)
        
        def do_delete():
            selection = save_listbox.curselection()
            if selection:
                idx = selection[0]
                slot_name = saves[idx]['slot_name']
                
                if messagebox.askyesno("确认", f"确定要删除存档 '{slot_name}' 吗？"):
                    if self._persistence.delete(
                        self._current_game.game_id,
                        slot_name
                    ):
                        messagebox.showinfo("成功", f"已删除存档: {slot_name}")
                        save_window.destroy()
                    else:
                        messagebox.showerror("错误", "删除失败")
        
        ttk.Button(
            save_window,
            text="删除",
            command=do_delete,
            style='Game.TButton'
        ).pack(pady=10)
    
    def run(self) -> None:
        self._root.mainloop()
