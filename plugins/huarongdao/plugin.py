import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional, List, Tuple
from game.interfaces import IGame


class Block:
    """华容道方块类"""
    
    def __init__(self, block_id: str, x: int, y: int, width: int, height: int, color: str, name: str):
        self.block_id = block_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.name = name
    
    def get_cells(self) -> List[Tuple[int, int]]:
        """获取方块占用的所有格子"""
        cells = []
        for dy in range(self.height):
            for dx in range(self.width):
                cells.append((self.x + dx, self.y + dy))
        return cells
    
    def copy(self) -> 'Block':
        return Block(self.block_id, self.x, self.y, self.width, self.height, self.color, self.name)


class HuarongdaoGame(IGame):
    """华容道游戏插件"""
    
    BOARD_WIDTH = 4
    BOARD_HEIGHT = 5
    CELL_SIZE = 80
    EXIT_X = 1
    EXIT_Y = 3
    
    LEVELS = {
        '横刀立马': {
            'blocks': [
                ('caocao', 1, 0, 2, 2, '#E74C3C', '曹操'),
                ('guanyu', 0, 2, 2, 1, '#27AE60', '关羽'),
                ('zhangfei', 0, 0, 1, 2, '#3498DB', '张飞'),
                ('zhaoyun', 3, 0, 1, 2, '#9B59B6', '赵云'),
                ('machao', 0, 3, 1, 2, '#F39C12', '马超'),
                ('huangzhong', 3, 2, 1, 2, '#1ABC9C', '黄忠'),
                ('soldier1', 2, 2, 1, 1, '#95A5A6', '兵'),
                ('soldier2', 3, 4, 1, 1, '#95A5A6', '兵'),
                ('soldier3', 1, 3, 1, 1, '#95A5A6', '兵'),
                ('soldier4', 2, 3, 1, 1, '#95A5A6', '兵'),
            ],
            'min_moves': 81
        },
        '指挥若定': {
            'blocks': [
                ('caocao', 1, 0, 2, 2, '#E74C3C', '曹操'),
                ('guanyu', 1, 2, 2, 1, '#27AE60', '关羽'),
                ('zhangfei', 0, 0, 1, 2, '#3498DB', '张飞'),
                ('zhaoyun', 3, 0, 1, 2, '#9B59B6', '赵云'),
                ('machao', 0, 2, 1, 2, '#F39C12', '马超'),
                ('huangzhong', 3, 2, 1, 2, '#1ABC9C', '黄忠'),
                ('soldier1', 0, 4, 1, 1, '#95A5A6', '兵'),
                ('soldier2', 1, 3, 1, 1, '#95A5A6', '兵'),
                ('soldier3', 2, 3, 1, 1, '#95A5A6', '兵'),
                ('soldier4', 3, 4, 1, 1, '#95A5A6', '兵'),
            ],
            'min_moves': 70
        },
        '将拥曹营': {
            'blocks': [
                ('caocao', 1, 0, 2, 2, '#E74C3C', '曹操'),
                ('guanyu', 1, 2, 2, 1, '#27AE60', '关羽'),
                ('zhangfei', 0, 0, 1, 2, '#3498DB', '张飞'),
                ('zhaoyun', 3, 0, 1, 2, '#9B59B6', '赵云'),
                ('machao', 0, 2, 1, 2, '#F39C12', '马超'),
                ('huangzhong', 3, 2, 1, 2, '#1ABC9C', '黄忠'),
                ('soldier1', 0, 4, 1, 1, '#95A5A6', '兵'),
                ('soldier2', 1, 3, 1, 1, '#95A5A6', '兵'),
                ('soldier3', 2, 3, 1, 1, '#95A5A6', '兵'),
                ('soldier4', 3, 4, 1, 1, '#95A5A6', '兵'),
            ],
            'min_moves': 72
        },
        '齐头并进': {
            'blocks': [
                ('caocao', 1, 0, 2, 2, '#E74C3C', '曹操'),
                ('guanyu', 1, 4, 2, 1, '#27AE60', '关羽'),
                ('zhangfei', 0, 0, 1, 2, '#3498DB', '张飞'),
                ('zhaoyun', 3, 0, 1, 2, '#9B59B6', '赵云'),
                ('machao', 0, 2, 1, 2, '#F39C12', '马超'),
                ('huangzhong', 3, 2, 1, 2, '#1ABC9C', '黄忠'),
                ('soldier1', 1, 2, 1, 1, '#95A5A6', '兵'),
                ('soldier2', 2, 2, 1, 1, '#95A5A6', '兵'),
                ('soldier3', 1, 3, 1, 1, '#95A5A6', '兵'),
                ('soldier4', 2, 3, 1, 1, '#95A5A6', '兵'),
            ],
            'min_moves': 60
        },
        '兵分三路': {
            'blocks': [
                ('caocao', 0, 0, 2, 2, '#E74C3C', '曹操'),
                ('guanyu', 1, 2, 2, 1, '#27AE60', '关羽'),
                ('zhangfei', 2, 0, 1, 2, '#3498DB', '张飞'),
                ('zhaoyun', 3, 0, 1, 2, '#9B59B6', '赵云'),
                ('machao', 2, 2, 1, 2, '#F39C12', '马超'),
                ('huangzhong', 3, 2, 1, 2, '#1ABC9C', '黄忠'),
                ('soldier1', 0, 2, 1, 1, '#95A5A6', '兵'),
                ('soldier2', 0, 3, 1, 1, '#95A5A6', '兵'),
                ('soldier3', 0, 4, 1, 1, '#95A5A6', '兵'),
                ('soldier4', 3, 4, 1, 1, '#95A5A6', '兵'),
            ],
            'min_moves': 100
        },
    }
    
    def __init__(self):
        self._panel: Optional[tk.Frame] = None
        self._canvas: Optional[tk.Canvas] = None
        self._blocks: Dict[str, Block] = {}
        self._selected_block: Optional[Block] = None
        self._move_count: int = 0
        self._game_over: bool = False
        self._current_level: str = '横刀立马'
        self._status_label: Optional[ttk.Label] = None
        self._level_label: Optional[ttk.Label] = None
        self._level_window: Optional[tk.Toplevel] = None
    
    @property
    def game_id(self) -> str:
        return "huarongdao"
    
    @property
    def game_name(self) -> str:
        return "华容道"
    
    @property
    def game_description(self) -> str:
        return "经典滑块益智游戏，让曹操从底部逃出"
    
    @property
    def game_version(self) -> str:
        return "1.0.0"
    
    def _load_level(self, level_name: str) -> None:
        self._blocks.clear()
        self._current_level = level_name
        level_data = self.LEVELS.get(level_name, self.LEVELS['横刀立马'])
        
        for block_data in level_data['blocks']:
            block = Block(*block_data)
            self._blocks[block.block_id] = block
        
        self._move_count = 0
        self._game_over = False
        self._selected_block = None
    
    def create_game_panel(self, parent: tk.Frame) -> tk.Frame:
        self._panel = ttk.Frame(parent)
        
        top_frame = ttk.Frame(self._panel)
        top_frame.pack(pady=10)
        
        self._level_label = ttk.Label(
            top_frame,
            text=f"关卡: {self._current_level}",
            font=('微软雅黑', 14, 'bold')
        )
        self._level_label.pack(side=tk.LEFT, padx=20)
        
        ttk.Button(
            top_frame,
            text="选择关卡",
            command=self._show_level_selector
        ).pack(side=tk.LEFT, padx=10)
        
        self._status_label = ttk.Label(
            top_frame,
            text="步数: 0",
            font=('微软雅黑', 12)
        )
        self._status_label.pack(side=tk.LEFT, padx=20)
        
        canvas_width = self.BOARD_WIDTH * self.CELL_SIZE + 20
        canvas_height = self.BOARD_HEIGHT * self.CELL_SIZE + 20
        
        self._canvas = tk.Canvas(
            self._panel,
            width=canvas_width,
            height=canvas_height,
            bg='#8B4513',
            highlightthickness=2,
            highlightbackground='#5D3A1A'
        )
        self._canvas.pack(pady=10)
        
        self._load_level(self._current_level)
        self._draw_board()
        
        self._canvas.bind('<Button-1>', self._on_click)
        self._panel.bind_all('<Key>', self._on_key)
        self._panel.bind('<Button-1>', lambda e: self._panel.focus_set())
        self._panel.focus_set()
        
        info_frame = ttk.Frame(self._panel)
        info_frame.pack(pady=5)
        
        ttk.Label(
            info_frame,
            text="点击选择方块，WASD或方向键移动。目标：让曹操(红色)从底部出口逃出！",
            font=('微软雅黑', 10)
        ).pack()
        
        return self._panel
    
    def _draw_board(self) -> None:
        self._canvas.delete('all')
        
        for x in range(self.BOARD_WIDTH + 1):
            self._canvas.create_line(
                10 + x * self.CELL_SIZE, 10,
                10 + x * self.CELL_SIZE, 10 + self.BOARD_HEIGHT * self.CELL_SIZE,
                fill='#5D3A1A', width=1
            )
        
        for y in range(self.BOARD_HEIGHT + 1):
            self._canvas.create_line(
                10, 10 + y * self.CELL_SIZE,
                10 + self.BOARD_WIDTH * self.CELL_SIZE, 10 + y * self.CELL_SIZE,
                fill='#5D3A1A', width=1
            )
        
        exit_x1 = 10 + self.EXIT_X * self.CELL_SIZE
        exit_x2 = 10 + (self.EXIT_X + 2) * self.CELL_SIZE
        exit_y = 10 + self.BOARD_HEIGHT * self.CELL_SIZE
        
        self._canvas.create_rectangle(
            exit_x1, exit_y - 5,
            exit_x2, exit_y + 5,
            fill='#FFD700', outline='#FFA500', width=2
        )
        self._canvas.create_text(
            (exit_x1 + exit_x2) / 2, exit_y,
            text="出口", font=('微软雅黑', 10, 'bold'), fill='#8B4513'
        )
        
        for block in self._blocks.values():
            self._draw_block(block)
        
        if self._status_label:
            self._status_label.config(text=f"步数: {self._move_count}")
    
    def _draw_block(self, block: Block) -> None:
        x1 = 10 + block.x * self.CELL_SIZE + 2
        y1 = 10 + block.y * self.CELL_SIZE + 2
        x2 = 10 + (block.x + block.width) * self.CELL_SIZE - 2
        y2 = 10 + (block.y + block.height) * self.CELL_SIZE - 2
        
        outline_color = '#FFD700' if self._selected_block and self._selected_block.block_id == block.block_id else '#333333'
        outline_width = 3 if self._selected_block and self._selected_block.block_id == block.block_id else 1
        
        self._canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=block.color,
            outline=outline_color,
            width=outline_width
        )
        
        font_size = 16 if block.width == 2 and block.height == 2 else 12
        self._canvas.create_text(
            (x1 + x2) / 2, (y1 + y2) / 2,
            text=block.name,
            font=('微软雅黑', font_size, 'bold'),
            fill='white'
        )
    
    def _get_block_at(self, canvas_x: int, canvas_y: int) -> Optional[Block]:
        board_x = (canvas_x - 10) // self.CELL_SIZE
        board_y = (canvas_y - 10) // self.CELL_SIZE
        
        for block in self._blocks.values():
            if (block.x <= board_x < block.x + block.width and
                block.y <= board_y < block.y + block.height):
                return block
        return None
    
    def _can_move(self, block: Block, dx: int, dy: int) -> bool:
        new_x = block.x + dx
        new_y = block.y + dy
        
        if new_x < 0 or new_x + block.width > self.BOARD_WIDTH:
            return False
        if new_y < 0 or new_y + block.height > self.BOARD_HEIGHT:
            return False
        
        occupied = set()
        for other in self._blocks.values():
            if other.block_id != block.block_id:
                for cell in other.get_cells():
                    occupied.add(cell)
        
        for dx_b in range(block.width):
            for dy_b in range(block.height):
                if (new_x + dx_b, new_y + dy_b) in occupied:
                    return False
        
        return True
    
    def _on_click(self, event: tk.Event) -> None:
        if self._game_over:
            return
        
        block = self._get_block_at(event.x, event.y)
        if block:
            self._selected_block = block
            self._draw_board()
    
    def _on_key(self, event: tk.Event) -> None:
        if self._game_over or not self._selected_block:
            return
        
        key = event.keysym.lower()
        dx, dy = 0, 0
        
        if key in ('up', 'w'):
            dy = -1
        elif key in ('down', 's'):
            dy = 1
        elif key in ('left', 'a'):
            dx = -1
        elif key in ('right', 'd'):
            dx = 1
        else:
            return
        
        if self._can_move(self._selected_block, dx, dy):
            self._selected_block.x += dx
            self._selected_block.y += dy
            self._move_count += 1
            self._draw_board()
            self._check_win()
    
    def _check_win(self) -> None:
        caocao = self._blocks.get('caocao')
        if caocao and caocao.x == self.EXIT_X and caocao.y == self.BOARD_HEIGHT - 2:
            self._game_over = True
            self._status_label.config(text=f"胜利！步数: {self._move_count}")
            messagebox.showinfo("恭喜", f"曹操成功逃出！\n总步数: {self._move_count}")
    
    def _show_level_selector(self) -> None:
        if self._level_window:
            self._level_window.destroy()
        
        self._level_window = tk.Toplevel(self._panel)
        self._level_window.title("选择关卡")
        self._level_window.geometry("300x400")
        self._level_window.transient(self._panel.winfo_toplevel())
        self._level_window.grab_set()
        
        ttk.Label(
            self._level_window,
            text="选择关卡",
            font=('微软雅黑', 14, 'bold')
        ).pack(pady=10)
        
        for level_name, level_data in self.LEVELS.items():
            level_frame = ttk.Frame(self._level_window)
            level_frame.pack(fill=tk.X, padx=10, pady=5)
            
            btn = ttk.Button(
                level_frame,
                text=level_name,
                command=lambda ln=level_name: self._select_level(ln)
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(
                level_frame,
                text=f"最少步数: {level_data['min_moves']}",
                font=('微软雅黑', 9)
            ).pack(side=tk.LEFT, padx=10)
    
    def _select_level(self, level_name: str) -> None:
        self._load_level(level_name)
        self._level_label.config(text=f"关卡: {level_name}")
        self._draw_board()
        if self._level_window:
            self._level_window.destroy()
            self._level_window = None
    
    def new_game(self) -> None:
        self._load_level(self._current_level)
        self._level_label.config(text=f"关卡: {self._current_level}")
        self._draw_board()
        self._panel.focus_set()
    
    def save_game(self) -> Dict[str, Any]:
        blocks_data = {}
        for block_id, block in self._blocks.items():
            blocks_data[block_id] = {
                'x': block.x,
                'y': block.y,
                'width': block.width,
                'height': block.height,
                'color': block.color,
                'name': block.name
            }
        
        return {
            'level': self._current_level,
            'blocks': blocks_data,
            'move_count': self._move_count,
            'game_over': self._game_over
        }
    
    def load_game(self, data: Dict[str, Any]) -> bool:
        try:
            self._current_level = data.get('level', '横刀立马')
            self._move_count = data.get('move_count', 0)
            self._game_over = data.get('game_over', False)
            
            self._blocks.clear()
            blocks_data = data.get('blocks', {})
            
            level_data = self.LEVELS.get(self._current_level, self.LEVELS['横刀立马'])
            for block_data in level_data['blocks']:
                block = Block(*block_data)
                if block.block_id in blocks_data:
                    saved = blocks_data[block.block_id]
                    block.x = saved['x']
                    block.y = saved['y']
                self._blocks[block.block_id] = block
            
            if self._level_label:
                self._level_label.config(text=f"关卡: {self._current_level}")
            
            if self._canvas:
                self._draw_board()
            
            return True
        except Exception as e:
            print(f"加载游戏失败: {e}")
            return False
    
    def get_save_info(self) -> Optional[Dict[str, Any]]:
        return {
            '关卡': self._current_level,
            '步数': self._move_count
        }
    
    def destroy(self) -> None:
        if self._level_window:
            self._level_window.destroy()
            self._level_window = None
        if self._panel:
            self._panel.unbind_all('<Key>')
            self._panel.destroy()
            self._panel = None
            self._canvas = None
            self._status_label = None
            self._level_label = None
