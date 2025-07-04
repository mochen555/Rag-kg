import json
from collections import OrderedDict

class Node:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.parent = None
        self.text = ""
        self.graph = None
        self.is_leaf = False
    
    def add_child(self, child):
        if child.name in self.children:
            raise ValueError(f"Duplicate child name: {child.name}")
        self.children[child.name] = child
        child.parent = self
    
    def get_child(self, name):
        return self.children.get(name)
    
    def get_children(self):
        return list(self.children.values())
    
    def get_parent(self):
        return self.parent
    
    def get_name(self):
        return self.name
    
    def get_text(self):
        return self.text
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.name == other.name
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<Node: {self.name}>"
    def to_dict(self):
        """将节点转换为字典结构（可序列化）"""
        return OrderedDict([
            ('name', self.name),
            ('text', self.text),
            ('is_leaf', self.is_leaf),
            ('graph', self._graph_to_dict()),
            ('children', [child.to_dict() for child in self.get_children()])
        ])
    
    def _graph_to_dict(self):
        """将graph对象转换为可序列化的字典结构，确保entities和relations不换行"""
        if not self.graph:
            return None
            
        # 确保entities和relations不换行
        entities_str = json.dumps(list(self.graph.entities), ensure_ascii=False)
        relations_str = json.dumps([list(rel) for rel in self.graph.relations], ensure_ascii=False)
        
        return {
            'entities': entities_str,
            'relations': relations_str
        }
    
    def to_json(self, file_path, indent=2):
        """将整个树结构保存为JSON文件"""
        tree_dict = self.to_dict()
        with open(file_path, 'w', encoding='utf-8') as f:
            # 手动序列化以确保entities和relations不换行
            json_str = json.dumps(tree_dict, ensure_ascii=False, indent=indent)
            
            # 处理entities和relations的换行问题
            json_str = json_str.replace('"entities": "', '"entities": ')
            json_str = json_str.replace('"relations": "', '"relations": ')
            json_str = json_str.replace('"}]",', '"}]",')
            json_str = json_str.replace('"]"', '"]')
            
            f.write(json_str)