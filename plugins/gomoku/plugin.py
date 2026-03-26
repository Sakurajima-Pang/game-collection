import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional
from game.interfaces import IGame


class GomokuGame(IGame):
    """五子棋游戏插件"""
    
    BOARD_SIZE = 15
    CELL_SIZE = 35
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    
    def __init__(self):
        self._panel: Optional[tk.Frame] = None
        self._canvas: Optional[tk.Canvas] = None
        self._board: list = []
        self._current_player: int = self.BLACK
        self._game_over: bool = False
        self._winner: Optional[int] = None
        self._move_count: int = 0
        self._status_label: Optional[ttk.Label] = None
        self._reset_game()
    
    @property
    def game_id(self) -> str:
        return "gomoku"
    
    @property
    def game_name(self) -> str:
        return "五子棋"
    
    @property
    def game_description(self) -> str:
        return "经典五子棋对战，双人对战模式"
    
    @property
    def game_version(self) -> str:
        return "1.0.0"
    
    def _reset_game(self) -> None:
        self._board = [[self.EMPTY] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self._current_player = self.BLACK
        self._game_over = False
        self._winner = None
        self._move_count = 0
    
    def create_game_panel(self, parent: tk.Frame) -> tk.Frame:
        self._panel = ttk.Frame(parent)
        
        control_frame = ttk.Frame(self._panel)
        control_frame.pack(pady=10)
        
        self._status_label = ttk.Label(
            control_frame,
            text="⚫ 黑棋先行",
            font=('微软雅黑', 14, 'bold')
        )
        self._status_label.pack()
        
        canvas_size = self.BOARD_SIZE * self.CELL_SIZE + self.CELL_SIZE
        self._canvas = tk.Canvas(
            self._panel,
            width=canvas_size,
            height=canvas_size,
            bg='#DEB887',
            highlightthickness=0
        )
        self._canvas.pack(pady=10)
        
        self._draw_board()
        self._canvas.bind('<Button-1>', self._on_click)
        
        info_frame = ttk.Frame(self._panel)
        info_frame.pack(pady=5)
        
        ttk.Label(
            info_frame,
            text="点击棋盘落子，五子连珠获胜！",
            font=('微软雅黑', 10)
        ).pack()
        
        return self._panel
    
    def _draw_board(self) -> None:
        self._canvas.delete('all')
        
        for i in range(self.BOARD_SIZE):
            x = self.CELL_SIZE + i * self.CELL_SIZE
            y = self.CELL_SIZE + i * self.CELL_SIZE
            
            self._canvas.create_line(
                self.CELL_SIZE, y,
                self.CELL_SIZE * self.BOARD_SIZE, y,
                fill='#8B4513'
            )
            self._canvas.create_line(
                x, self.CELL_SIZE,
                x, self.CELL_SIZE * self.BOARD_SIZE,
                fill='#8B4513'
            )
        
        star_points = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7),
                       (3, 7), (11, 7), (7, 3), (7, 11)]
        for px, py in star_points:
            x = self.CELL_SIZE + px * self.CELL_SIZE
            y = self.CELL_SIZE + py * self.CELL_SIZE
            self._canvas.create_oval(
                x - 4, y - 4, x + 4, y + 4,
                fill='#8B4513', outline='#8B4513'
            )
        
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self._board[row][col] != self.EMPTY:
                    self._draw_piece(row, col, self._board[row][col])
    
    def _draw_piece(self, row: int, col: int, player: int) -> None:
        x = self.CELL_SIZE + col * self.CELL_SIZE
        y = self.CELL_SIZE + row * self.CELL_SIZE
        radius = self.CELL_SIZE // 2 - 2
        
        color = '#000000' if player == self.BLACK else '#FFFFFF'
        outline = '#333333' if player == self.WHITE else '#000000'
        
        self._canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color, outline=outline, width=2
        )
    
    def _on_click(self, event: tk.Event) -> None:
        if self._game_over:
            return
        
        col = round((event.x - self.CELL_SIZE) / self.CELL_SIZE)
        row = round((event.y - self.CELL_SIZE) / self.CELL_SIZE)
        
        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
            if self._board[row][col] == self.EMPTY:
                self._make_move(row, col)
    
    def _make_move(self, row: int, col: int) -> None:
        self._board[row][col] = self._current_player
        self._move_count += 1
        self._draw_piece(row, col, self._current_player)
        
        if self._check_win(row, col):
            self._game_over = True
            self._winner = self._current_player
            winner_name = "黑棋" if self._winner == self.BLACK else "白棋"
            self._status_label.config(text=f"🎉 {winner_name}获胜！")
            messagebox.showinfo("游戏结束", f"{winner_name}获胜！")
        elif self._move_count >= self.BOARD_SIZE * self.BOARD_SIZE:
            self._game_over = True
            self._status_label.config(text="🤝 平局！")
            messagebox.showinfo("游戏结束", "平局！")
        else:
            self._current_player = self.WHITE if self._current_player == self.BLACK else self.BLACK
            player_text = "⚫ 黑棋" if self._current_player == self.BLACK else "⚪ 白棋"
            self._status_label.config(text=f"{player_text} 落子")
    
    def _check_win(self, row: int, col: int) -> bool:
        player = self._board[row][col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            
            r, c = row + dr, col + dc
            while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and self._board[r][c] == player:
                count += 1
                r += dr
                c += dc
            
            r, c = row - dr, col - dc
            while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and self._board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            
            if count >= 5:
                return True
        
        return False
    
    def new_game(self) -> None:
        self._reset_game()
        if self._canvas:
            self._draw_board()
        if self._status_label:
            self._status_label.config(text="⚫ 黑棋先行")
    
    def save_game(self) -> Dict[str, Any]:
        return {
            'board': self._board,
            'current_player': self._current_player,
            'game_over': self._game_over,
            'winner': self._winner,
            'move_count': self._move_count
        }
    
    def load_game(self, data: Dict[str, Any]) -> bool:
        try:
            self._board = data['board']
            self._current_player = data['current_player']
            self._game_over = data['game_over']
            self._winner = data.get('winner')
            self._move_count = data.get('move_count', 0)
            
            if self._canvas:
                self._draw_board()
            
            if self._status_label:
                if self._game_over:
                    if self._winner:
                        winner_name = "黑棋" if self._winner == self.BLACK else "白棋"
                        self._status_label.config(text=f"🎉 {winner_name}获胜！")
                    else:
                        self._status_label.config(text="🤝 平局！")
                else:
                    player_text = "⚫ 黑棋" if self._current_player == self.BLACK else "⚪ 白棋"
                    self._status_label.config(text=f"{player_text} 落子")
            
            return True
        except Exception as e:
            print(f"加载游戏失败: {e}")
            return False
    
    def get_save_info(self) -> Optional[Dict[str, Any]]:
        return {
            '步数': self._move_count,
            '当前': '黑棋' if self._current_player == self.BLACK else '白棋'
        }
    
    def destroy(self) -> None:
        if self._panel:
            self._panel.destroy()
            self._panel = None
            self._canvas = None
            self._status_label = None
