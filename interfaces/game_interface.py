from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from tkinter import Frame


class IGame(ABC):
    """游戏插件接口 - 所有游戏插件必须实现此接口"""
    
    @property
    @abstractmethod
    def game_id(self) -> str:
        """游戏唯一标识符"""
        pass
    
    @property
    @abstractmethod
    def game_name(self) -> str:
        """游戏显示名称"""
        pass
    
    @property
    @abstractmethod
    def game_description(self) -> str:
        """游戏描述"""
        pass
    
    @property
    @abstractmethod
    def game_version(self) -> str:
        """游戏版本号"""
        pass
    
    @abstractmethod
    def create_game_panel(self, parent: Frame) -> Frame:
        """创建游戏面板
        
        Args:
            parent: 父容器
            
        Returns:
            游戏面板Frame
        """
        pass
    
    @abstractmethod
    def new_game(self) -> None:
        """开始新游戏"""
        pass
    
    @abstractmethod
    def save_game(self) -> Dict[str, Any]:
        """保存游戏状态
        
        Returns:
            游戏状态数据字典
        """
        pass
    
    @abstractmethod
    def load_game(self, data: Dict[str, Any]) -> bool:
        """加载游戏状态
        
        Args:
            data: 游戏状态数据字典
            
        Returns:
            是否加载成功
        """
        pass
    
    @abstractmethod
    def get_save_info(self) -> Optional[Dict[str, Any]]:
        """获取当前存档信息（用于显示存档列表）
        
        Returns:
            存档信息字典，包含如：分数、时间、进度等
        """
        pass
    
    @abstractmethod
    def destroy(self) -> None:
        """销毁游戏面板，释放资源"""
        pass
