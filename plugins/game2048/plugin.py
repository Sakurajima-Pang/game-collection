import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional
import random
from game.interfaces import IGame


class Game2048(IGame):
    """2048游戏插件"""
    
    GRID_SIZE = 4
    CELL_SIZE = 100
    CELL_GAP = 10
    
    COLORS = {
        0: '#CDC1B4',
        2: '#EEE4DA',
        4: '#EDE0C8',
        8: '#F2B179',
        16: '#F59563',
        32: '#F67C5F',
        64: '#F65E3B',
        128: '#EDCF72',
        256: '#EDCC61',
        512: '#EDC850',
        1024: '#EDC53F',
        2048: '#EDC22E',
        4096: '#3C3A32',
        8192: '#3C3A32',
    }
    
    TEXT_COLORS = {
        2: '#776E65',
        4: '#776E65',
    }
    
    def __init__(self):
        self._panel: Optional[tk.Frame] = None
        self._canvas: Optional[tk.Canvas] = None
        self._grid: list = []
        self._score: int = 0
        self._best_score: int = 0
        self._game_over: bool = False
        self._score_label: Optional[ttk.Label] = None
        self._best_label: Optional[ttk.Label] = None
        self._status_label: Optional[ttk.Label] = None
        self._reset_game()
    
    @property
    def game_id(self) -> str:
        return "game2048"
    
    @property
    def game_name(self) -> str:
        return "2048"
    
    @property
    def game_description(self) -> str:
        return "经典数字合并游戏，挑战2048！"
    
    @property
    def game_version(self) -> str:
        return "1.0.0"
    
    def _reset_game(self) -> None:
        self._grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self._score = 0
        self._game_over = False
        self._add_random_tile()
        self._add_random_tile()
    
    def _add_random_tile(self) -> bool:
        empty_cells = []
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                if self._grid[r][c] == 0:
                    empty_cells.append((r, c))
        
        if empty_cells:
            r, c = random.choice(empty_cells)
            self._grid[r][c] = 4 if random.random() < 0.1 else 2
            return True
        return False
    
    def create_game_panel(self, parent: tk.Frame) -> tk.Frame:
        self._panel = ttk.Frame(parent)
        
        score_frame = ttk.Frame(self._panel)
        score_frame.pack(pady=10)
        
        score_box1 = ttk.Frame(score_frame, relief='ridge')
        score_box1.pack(side=tk.LEFT, padx=10)
        ttk.Label(score_box1, text="分数", font=('微软雅黑', 10)).pack(padx=15, pady=2)
        self._score_label = ttk.Label(score_box1, text="0", font=('微软雅黑', 14, 'bold'))
        self._score_label.pack(padx=15, pady=2)
        
        score_box2 = ttk.Frame(score_frame, relief='ridge')
        score_box2.pack(side=tk.LEFT, padx=10)
        ttk.Label(score_box2, text="最高分", font=('微软雅黑', 10)).pack(padx=15, pady=2)
        self._best_label = ttk.Label(score_box2, text=str(self._best_score), font=('微软雅黑', 14, 'bold'))
        self._best_label.pack(padx=15, pady=2)
        
        self._status_label = ttk.Label(self._panel, text="使用方向键移动方块", font=('微软雅黑', 11))
        self._status_label.pack(pady=5)
        
        canvas_size = self.GRID_SIZE * (self.CELL_SIZE + self.CELL_GAP) + self.CELL_GAP
        self._canvas = tk.Canvas(
            self._panel,
            width=canvas_size,
            height=canvas_size,
            bg='#BBADA0',
            highlightthickness=0
        )
        self._canvas.pack(pady=10)
        
        self._draw_grid()
        
        self._panel.bind_all('<Key>', self._on_key)
        self._panel.bind('<Button-1>', lambda e: self._panel.focus_set())
        self._panel.focus_set()
        
        info_frame = ttk.Frame(self._panel)
        info_frame.pack(pady=5)
        ttk.Label(
            info_frame,
            text="方向键或WASD移动，合并相同数字达到2048！",
            font=('微软雅黑', 10)
        ).pack()
        
        return self._panel
    
    def _draw_grid(self) -> None:
        self._canvas.delete('all')
        
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                x = self.CELL_GAP + c * (self.CELL_SIZE + self.CELL_GAP)
                y = self.CELL_GAP + r * (self.CELL_SIZE + self.CELL_GAP)
                
                value = self._grid[r][c]
                color = self.COLORS.get(value, self.COLORS[4096])
                
                self._canvas.create_rectangle(
                    x, y,
                    x + self.CELL_SIZE, y + self.CELL_SIZE,
                    fill=color, outline=color
                )
                
                if value != 0:
                    text_color = self.TEXT_COLORS.get(value, '#F9F6F2')
                    font_size = 40 if value < 100 else 35 if value < 1000 else 28
                    self._canvas.create_text(
                        x + self.CELL_SIZE // 2,
                        y + self.CELL_SIZE // 2,
                        text=str(value),
                        font=('微软雅黑', font_size, 'bold'),
                        fill=text_color
                    )
        
        if self._score_label:
            self._score_label.config(text=str(self._score))
        if self._best_label and self._score > self._best_score:
            self._best_score = self._score
            self._best_label.config(text=str(self._best_score))
    
    def _on_key(self, event: tk.Event) -> None:
        if self._game_over:
            return
        
        key = event.keysym.lower()
        
        if key in ('up', 'w'):
            moved = self._move_up()
        elif key in ('down', 's'):
            moved = self._move_down()
        elif key in ('left', 'a'):
            moved = self._move_left()
        elif key in ('right', 'd'):
            moved = self._move_right()
        else:
            return
        
        if moved:
            self._add_random_tile()
            self._draw_grid()
            
            if self._check_win():
                self._game_over = True
                self._status_label.config(text="🎉 恭喜达到2048！")
                messagebox.showinfo("胜利", "恭喜你达到了2048！")
            elif self._check_game_over():
                self._game_over = True
                self._status_label.config(text="💀 游戏结束！")
                messagebox.showinfo("游戏结束", f"游戏结束！最终得分: {self._score}")
    
    def _compress(self, row: list) -> tuple:
        new_row = [x for x in row if x != 0]
        new_row += [0] * (self.GRID_SIZE - len(new_row))
        return new_row
    
    def _merge(self, row: list) -> list:
        for i in range(self.GRID_SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self._score += row[i]
                row[i + 1] = 0
        return row
    
    def _move_left(self) -> bool:
        moved = False
        for r in range(self.GRID_SIZE):
            original = self._grid[r][:]
            row = self._compress(self._grid[r])
            row = self._merge(row)
            row = self._compress(row)
            self._grid[r] = row
            if row != original:
                moved = True
        return moved
    
    def _move_right(self) -> bool:
        moved = False
        for r in range(self.GRID_SIZE):
            original = self._grid[r][:]
            row = self._grid[r][::-1]
            row = self._compress(row)
            row = self._merge(row)
            row = self._compress(row)
            self._grid[r] = row[::-1]
            if self._grid[r] != original:
                moved = True
        return moved
    
    def _move_up(self) -> bool:
        moved = False
        for c in range(self.GRID_SIZE):
            col = [self._grid[r][c] for r in range(self.GRID_SIZE)]
            original = col[:]
            col = self._compress(col)
            col = self._merge(col)
            col = self._compress(col)
            for r in range(self.GRID_SIZE):
                self._grid[r][c] = col[r]
            if col != original:
                moved = True
        return moved
    
    def _move_down(self) -> bool:
        moved = False
        for c in range(self.GRID_SIZE):
            col = [self._grid[r][c] for r in range(self.GRID_SIZE)][::-1]
            original = [self._grid[r][c] for r in range(self.GRID_SIZE)]
            col = self._compress(col)
            col = self._merge(col)
            col = self._compress(col)
            col = col[::-1]
            for r in range(self.GRID_SIZE):
                self._grid[r][c] = col[r]
            if col != original:
                moved = True
        return moved
    
    def _check_win(self) -> bool:
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                if self._grid[r][c] >= 2048:
                    return True
        return False
    
    def _check_game_over(self) -> bool:
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                if self._grid[r][c] == 0:
                    return False
                if c < self.GRID_SIZE - 1 and self._grid[r][c] == self._grid[r][c + 1]:
                    return False
                if r < self.GRID_SIZE - 1 and self._grid[r][c] == self._grid[r + 1][c]:
                    return False
        return True
    
    def new_game(self) -> None:
        self._reset_game()
        if self._canvas:
            self._draw_grid()
        if self._status_label:
            self._status_label.config(text="使用方向键移动方块")
        if self._panel:
            self._panel.focus_set()
    
    def save_game(self) -> Dict[str, Any]:
        return {
            'grid': self._grid,
            'score': self._score,
            'best_score': self._best_score,
            'game_over': self._game_over
        }
    
    def load_game(self, data: Dict[str, Any]) -> bool:
        try:
            self._grid = data['grid']
            self._score = data['score']
            self._best_score = max(data.get('best_score', 0), self._best_score)
            self._game_over = data.get('game_over', False)
            
            if self._canvas:
                self._draw_grid()
            
            if self._status_label:
                if self._game_over:
                    self._status_label.config(text="游戏已结束")
                else:
                    self._status_label.config(text="使用方向键移动方块")
            
            if self._panel:
                self._panel.focus_set()
            
            return True
        except Exception as e:
            print(f"加载游戏失败: {e}")
            return False
    
    def get_save_info(self) -> Optional[Dict[str, Any]]:
        return {
            '分数': self._score,
            '最高方块': max(max(row) for row in self._grid)
        }
    
    def destroy(self) -> None:
        if self._panel:
            self._panel.unbind_all('<Key>')
            self._panel.destroy()
            self._panel = None
            self._canvas = None
            self._score_label = None
            self._best_label = None
            self._status_label = None
