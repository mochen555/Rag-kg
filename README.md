# Knowledge Graph Visualization from Markdown# Markdown的知识图谱可视化

这是一个从Markdown格式文本中提取结构化内容并生成交互式知识图谱可视化系统的工具。

## 项目概述

该工具能够：
1. 解析层级结构的Markdown文档
2. 自动生成知识图谱（实体和关系）
3. 创建直观的可视化界面展示内容结构
4. 提供交互式探索文档结构和知识图谱的能力

## 架构设计

```
project/   项目/   项目/
├── config.py             # 配置文件
├── data_structures.py    # 数据结构定义
├── text_processor.py     # 文本处理逻辑
├── kg_processor.py       # 知识图谱处理逻辑
├── visualization.py      # 可视化处理
└── main.py               # 主程序入口
```

## 安装说明

1. **克隆仓库**
```bash   ”“bash   ”“bash”“bash‘ ’ ' bash " " bash " " bash " “ bash ”
git clone https://github.com/your-username/knowledge-graph-visualization.gitGit克隆https://github.com/your-username/knowledge-graph-visualization.gitGit克隆https://github.com/your-username/knowledge-graph-visualization.git
cd knowledge-graph-visualization
```

2. **安装依赖**
```bash   ”“bash   ”“bash”“bash‘ ’ ' bash " " bash " " bash " “ bash ”
pip install -r requirements.txtPIP install -r requirements.txtPIP install -r要求。txtPIP install -r requirements.txt
```

> **requirements.txt** 内容:
> ```
> networkx
> pyvis
> jinja2
> requests   >请求
> tiktoken
> openai
> ```

## 配置设置

编辑 `config.py` 文件进行个性化配置：

```python   ”“python   ”“python”“python‘ ’ ' python " " python " " python " " python " " python
# 知识图谱生成配置
KG_CONFIG = {   Kg_config = {KG_CONFIG = {KG_CONFIG = {KG_CONFIG = {KG_CONFIG = {KG_CONFIG = {KG_CONFIG = {
    "MODEL_NAME": "deepseek/deepseek-chat",  # 使用的AI模型
    "TEMPERATURE": 0.0,                     # 生成温度参数
    "API_KEY": "your-api-key-here"           # 替换为您的API密钥
}

# 文件路径配置
FILE_PATHS = {   File_paths = {FILE_PATHS = {
    "INPUT_FILE": "input.md",    # 输入Markdown文件路径
    "OUTPUT_HTML": "output.html" # 输出HTML可视化文件路径
}

# 可视化配置
VIS_CONFIG = {
    "NODE_COLOR": "#97C2FC",     # 节点颜色 (蓝色)
    "EDGE_COLOR": "gray",         # 关系边颜色
    "NODE_SIZE": 20               # 节点尺寸
}
```

## 输入文件格式

输入应为遵循层级结构的Markdown文件：

```markdown   ”“减价
# 国际背景
美国在俄乌冲突初期试图...

## 欧盟立场
欧盟内部存在分歧...

### 法国立场
马克龙总统主张...

### 德国立场
朔尔茨总理更为谨慎...
```

## 运行程序

```bash   ”“bash   ”“bash”“bash‘ ’ ' bash " " bash " " bash " “ bash ”
python main.py
```

## 输出结果

程序将生成：
1. 交互式HTML可视化文件 (位于 `output.html`)
2. 左侧树状结构导航
3. 右侧知识图谱可视化区域
4. 点击节点可查看相关实体和关系

## 示例展示

[]



## 自定义选项

1. **修改知识图谱生成参数**
   - 在 `config.py` 中调整 `KG_CONFIG` 设置
   - 更改API密钥、模型或生成温度

2. **调整可视化样式**
   - 在 `config.py` 中修改 `VIS_CONFIG` 参数
   - 支持自定义节点颜色、大小和边颜色

3. **扩展功能**
   - 在 `visualization.py` 中添加自定义模板
   - 修改 `kg_processor.py` 调整知识图谱处理逻辑

## 注意事项

1. 确保提供有效的API密钥以访问AI模型
2. 输入文件应符合层级结构要求
3. 首次运行时需要安装所有依赖项
4. 大型文档处理可能需要较长时间（取决于API调用）

## 贡献指南

欢迎贡献代码！请遵循以下流程：
1. Fork项目仓库
2. 在分支上开发新功能
3. 编写单元测试
4. 提交Pull Request



