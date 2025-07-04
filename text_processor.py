from data_structures import Node
from config import FILE_PATHS

class TextProcessor:
    def __init__(self):
        self.root = Node("ROOT")
        self.stack = [self.root]
    
    def parse_file(self, file_path=None):
        if not file_path:
            file_path = FILE_PATHS["INPUT_FILE"]
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                self._process_line(line.strip('\n'))
        self._post_process(self.root)
    
    def _process_line(self, line):
        if line.startswith('#'):
            level = 0
            while line.startswith('#'):
                level += 1
                line = line[1:].lstrip()
            name = line.strip()
            self._update_hierarchy(level, name)
        else:
            if self.stack:
                current_node = self.stack[-1]
                current_node.text += line + '\n'
    
    def _update_hierarchy(self, level, name):
        if level < 1 or level > 6:
            return
            
        while len(self.stack) > level:
            self.stack.pop()
            
        if len(self.stack) == level:
            new_node = Node(name)
            self.stack[-1].add_child(new_node)
            self.stack.append(new_node)
    
    def _post_process(self, node):
        # 后处理逻辑（当前留空）
        pass