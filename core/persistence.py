import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from ..interfaces import IDataPersistence


class JSONPersistence(IDataPersistence):
    """JSON文件持久化实现"""
    
    def __init__(self, data_dir: str):
        """初始化持久化服务
        
        Args:
            data_dir: 数据存储目录
        """
        self._data_dir = Path(data_dir)
        self._saves_dir = self._data_dir / 'saves'
        self._saves_dir.mkdir(parents=True, exist_ok=True)
        self._index_file = self._saves_dir / 'index.json'
        self._index = self._load_index()
    
    def _load_index(self) -> Dict[str, Any]:
        """加载存档索引"""
        if self._index_file.exists():
            try:
                with open(self._index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_index(self) -> None:
        """保存存档索引"""
        with open(self._index_file, 'w', encoding='utf-8') as f:
            json.dump(self._index, f, ensure_ascii=False, indent=2)
    
    def _get_save_path(self, game_id: str, slot_name: str) -> Path:
        """获取存档文件路径"""
        safe_slot = slot_name.replace('/', '_').replace('\\', '_')
        return self._saves_dir / f"{game_id}_{safe_slot}.json"
    
    def save(self, game_id: str, slot_name: str, data: Dict[str, Any]) -> bool:
        """保存游戏数据"""
        try:
            save_path = self._get_save_path(game_id, slot_name)
            
            save_data = {
                'game_id': game_id,
                'slot_name': slot_name,
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            if game_id not in self._index:
                self._index[game_id] = {}
            
            self._index[game_id][slot_name] = {
                'timestamp': save_data['timestamp'],
                'save_file': str(save_path.name)
            }
            self._save_index()
            
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False
    
    def load(self, game_id: str, slot_name: str) -> Optional[Dict[str, Any]]:
        """加载游戏数据"""
        try:
            save_path = self._get_save_path(game_id, slot_name)
            
            if not save_path.exists():
                return None
            
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            return save_data.get('data')
        except Exception as e:
            print(f"加载失败: {e}")
            return None
    
    def delete(self, game_id: str, slot_name: str) -> bool:
        """删除存档"""
        try:
            save_path = self._get_save_path(game_id, slot_name)
            
            if save_path.exists():
                save_path.unlink()
            
            if game_id in self._index and slot_name in self._index[game_id]:
                del self._index[game_id][slot_name]
                if not self._index[game_id]:
                    del self._index[game_id]
                self._save_index()
            
            return True
        except Exception as e:
            print(f"删除失败: {e}")
            return False
    
    def list_saves(self, game_id: str) -> List[Dict[str, Any]]:
        """获取游戏的所有存档列表"""
        saves = []
        
        if game_id in self._index:
            for slot_name, info in self._index[game_id].items():
                save_data = self.load(game_id, slot_name)
                saves.append({
                    'slot_name': slot_name,
                    'timestamp': info['timestamp'],
                    'info': save_data.get('info', {}) if save_data else {}
                })
        
        saves.sort(key=lambda x: x['timestamp'], reverse=True)
        return saves
    
    def get_all_games(self) -> List[str]:
        """获取所有有存档的游戏ID列表"""
        return list(self._index.keys())
