import json
import csv
import uuid
import os
import html
from collections import defaultdict

class KGCsvExporter:
    def __init__(self, input_json_path):
        self.input_json_path = input_json_path
        self.output_dir = os.path.dirname(input_json_path)
        self.entities = defaultdict(set)
        self.relations = defaultdict(set)
        self.node_ids = {}  # {node_path: unique_id}
        
        # 安全生成输出路径
        base_name = os.path.basename(input_json_path)
        name, ext = os.path.splitext(base_name)
        self.output_json_path = os.path.join(self.output_dir, f"{name}_indexed{ext}")
        self.entities_csv_path = os.path.join(self.output_dir, f"{name}_entities.csv")
        self.relations_csv_path = os.path.join(self.output_dir, f"{name}_relations.csv")
    
    def _sanitize_string(self, s):
        """清理字符串，移除特殊字符和引号"""
        return html.unescape(s).replace('"', '').replace('\\', '')
    
    def _generate_node_id(self, node_path):
        """为节点生成唯一ID"""
        if node_path not in self.node_ids:
            self.node_ids[node_path] = str(uuid.uuid4())
        return self.node_ids[node_path]
    
    def _traverse_tree(self, node, parent_path=""):
        """递归遍历树结构，清洗数据"""
        # 生成当前节点完整路径
        current_path = f"{parent_path}/{node['name']}" if parent_path else node['name']
        current_id = self._generate_node_id(current_path)
        
        # 清理节点数据
        clean_node = {
            "node_id": current_id,
            "name": self._sanitize_string(node['name']),
            "text": self._sanitize_string(node.get('text', '')),
            "is_leaf": node.get('is_leaf', False),
            "children": []  # 初始化为空列表
        }
        
        # 处理知识图谱数据
        if node.get('graph'):
            # 清理实体
            entities = [self._sanitize_string(e) for e in node['graph'].get('entities', [])]
            if entities:
                self.entities[current_id].update(entities)
            
            # 清理关系
            for rel in node['graph'].get('relations', []):
                if len(rel) == 3:  # 确保是三元组
                    clean_rel = tuple(self._sanitize_string(r) for r in rel)
                    self.relations[current_id].add(clean_rel)
        
        # 递归处理子节点
        for child in node.get('children', []):
            child_node = self._traverse_tree(child, current_path)
            clean_node["children"].append(child_node["name"])
        
        return clean_node
    
    def export(self):
        # 加载原始JSON结构树
        try:
            with open(self.input_json_path, 'r', encoding='utf-8') as f:
                tree_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            print("尝试修复可能的引号问题...")
            # 尝试清理文件中的非法引号
            with open(self.input_json_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # 移除JSON字符串外的非法引号
            fixed_content = content.replace("\",", ",").replace(",\"", ",").replace("\":", ":")
            tree_data = json.loads(fixed_content)
        
        # 遍历并清洗树结构
        indexed_tree = self._traverse_tree(tree_data)
        
        # 安全保存转换后的JSON
        try:
            with open(self.output_json_path, 'w', encoding='utf-8') as f:
                json.dump(indexed_tree, f, indent=2, ensure_ascii=False)
            print(f"成功生成索引化JSON: {self.output_json_path}")
        except Exception as e:
            print(f"保存JSON时出错: {e}")
            # 备用写入方法
            with open(self.output_json_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(indexed_tree, ensure_ascii=False))
        
        # 保存实体CSV（安全方法）
        try:
            with open(self.entities_csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['entity_id', 'entity', 'node_id'])
                
                entity_id = 1
                for node_id, entities in self.entities.items():
                    for entity in entities:
                        # 确保实体中没有双引号
                        clean_entity = entity.replace('"', '')
                        writer.writerow([entity_id, clean_entity, node_id])
                        entity_id += 1
            print(f"成功生成实体CSV: {self.entities_csv_path}")
        except Exception as e:
            print(f"保存实体CSV时出错: {e}")
        
        # 保存关系CSV（安全方法）
        try:
            with open(self.relations_csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['relation_id', 'source', 'relation', 'target', 'node_id'])
                
                relation_id = 1
                for node_id, relations in self.relations.items():
                    for rel in relations:
                        source, relation, target = rel
                        # 清理每个字段
                        clean_source = source.replace('"', '')
                        clean_relation = relation.replace('"', '')
                        clean_target = target.replace('"', '')
                        writer.writerow([relation_id, clean_source, clean_relation, clean_target, node_id])
                        relation_id += 1
            print(f"成功生成关系CSV: {self.relations_csv_path}")
        except Exception as e:
            print(f"保存关系CSV时出错: {e}")
        
        return {
            "indexed_json": self.output_json_path,
            "entities_csv": self.entities_csv_path,
            "relations_csv": self.relations_csv_path
        }

# 使用示例
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python kg_csv_exporter.py <input_json_path>")
        sys.exit(1)
    
    input_json_path = sys.argv[1]
    print(f"开始处理: {input_json_path}")
    
    exporter = KGCsvExporter(input_json_path)
    result = exporter.export()
    
    print("\n处理完成，生成文件:")
    for key, path in result.items():
        print(f"- {key}: {path}")