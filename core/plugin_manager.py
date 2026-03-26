import importlib
import importlib.util
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Type
from ..interfaces import IGame


def get_base_path() -> Path:
    """获取基础路径，支持打包和开发环境"""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent.parent.parent


class PluginManager:
    """插件管理器 - 负责发现、加载和管理游戏插件"""
    
    def __init__(self, plugins_dir: str):
        """初始化插件管理器
        
        Args:
            plugins_dir: 插件目录路径
        """
        self._plugins_dir = Path(plugins_dir)
        self._games: Dict[str, IGame] = {}
        self._game_classes: Dict[str, Type[IGame]] = {}
    
    def discover_plugins(self) -> List[str]:
        """发现所有可用的插件
        
        Returns:
            发现的插件ID列表
        """
        discovered = []
        
        if not self._plugins_dir.exists():
            base_path = get_base_path()
            self._plugins_dir = base_path / 'game' / 'plugins'
        
        if not self._plugins_dir.exists():
            return discovered
        
        for item in self._plugins_dir.iterdir():
            if item.is_dir() and not item.name.startswith('_'):
                plugin_file = item / 'plugin.py'
                if plugin_file.exists():
                    try:
                        game_class = self._load_plugin(item.name)
                        if game_class:
                            self._game_classes[game_class.__name__] = game_class
                            discovered.append(game_class.__name__)
                    except Exception as e:
                        print(f"加载插件 {item.name} 失败: {e}")
        
        return discovered
    
    def _load_plugin(self, plugin_name: str) -> Optional[Type[IGame]]:
        """加载单个插件
        
        Args:
            plugin_name: 插件目录名
            
        Returns:
            游戏类，加载失败返回None
        """
        plugin_path = self._plugins_dir / plugin_name / 'plugin.py'
        
        if not plugin_path.exists():
            return None
        
        spec = importlib.util.spec_from_file_location(
            f"game.plugins.{plugin_name}.plugin",
            str(plugin_path)
        )
        
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"game.plugins.{plugin_name}.plugin"] = module
            spec.loader.exec_module(module)
            
            if hasattr(module, 'GameClass'):
                return module.GameClass
            
            for name in dir(module):
                obj = getattr(module, name)
                if (isinstance(obj, type) and 
                    issubclass(obj, IGame) and 
                    obj is not IGame):
                    return obj
        
        return None
    
    def get_game(self, game_class_name: str) -> Optional[IGame]:
        """获取游戏实例
        
        Args:
            game_class_name: 游戏类名
            
        Returns:
            游戏实例
        """
        if game_class_name not in self._games:
            if game_class_name in self._game_classes:
                self._games[game_class_name] = self._game_classes[game_class_name]()
        
        return self._games.get(game_class_name)
    
    def get_all_games(self) -> Dict[str, IGame]:
        """获取所有游戏实例
        
        Returns:
            游戏实例字典 {类名: 实例}
        """
        for class_name in self._game_classes:
            if class_name not in self._games:
                self._games[class_name] = self._game_classes[class_name]()
        return self._games.copy()
    
    def get_game_info_list(self) -> List[Dict[str, str]]:
        """获取所有游戏信息列表
        
        Returns:
            游戏信息列表
        """
        info_list = []
        for class_name, game_class in self._game_classes.items():
            temp_instance = game_class()
            info_list.append({
                'class_name': class_name,
                'game_id': temp_instance.game_id,
                'game_name': temp_instance.game_name,
                'description': temp_instance.game_description,
                'version': temp_instance.game_version
            })
        return info_list
    
    def unload_game(self, game_class_name: str) -> None:
        """卸载游戏实例
        
        Args:
            game_class_name: 游戏类名
        """
        if game_class_name in self._games:
            self._games[game_class_name].destroy()
            del self._games[game_class_name]
