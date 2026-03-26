from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class IDataPersistence(ABC):
    """数据持久化接口"""
    
    @abstractmethod
    def save(self, game_id: str, slot_name: str, data: Dict[str, Any]) -> bool:
        """保存游戏数据
        
        Args:
            game_id: 游戏ID
            slot_name: 存档槽名称
            data: 游戏数据
            
        Returns:
            是否保存成功
        """
        pass
    
    @abstractmethod
    def load(self, game_id: str, slot_name: str) -> Optional[Dict[str, Any]]:
        """加载游戏数据
        
        Args:
            game_id: 游戏ID
            slot_name: 存档槽名称
            
        Returns:
            游戏数据，不存在则返回None
        """
        pass
    
    @abstractmethod
    def delete(self, game_id: str, slot_name: str) -> bool:
        """删除存档
        
        Args:
            game_id: 游戏ID
            slot_name: 存档槽名称
            
        Returns:
            是否删除成功
        """
        pass
    
    @abstractmethod
    def list_saves(self, game_id: str) -> List[Dict[str, Any]]:
        """获取游戏的所有存档列表
        
        Args:
            game_id: 游戏ID
            
        Returns:
            存档信息列表
        """
        pass
    
    @abstractmethod
    def get_all_games(self) -> List[str]:
        """获取所有有存档的游戏ID列表
        
        Returns:
            游戏ID列表
        """
        pass
