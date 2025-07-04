# 知识图谱生成配置
KG_CONFIG = {
    "MODEL_NAME": "deepseek/deepseek-chat",
    "TEMPERATURE": 0.0,
    "API_KEY": "sk-c0ff37fca9f3439fab7ca60ef6819cef",
    "CONNECTIVITY_THRESHOLD": 1,  # 新增连通度阈值 (0-1之间)
    "MIN_CONNECTIONS": 1  # 最小连接数阈值
}

# 文件路径配置
FILE_PATHS = {
    "INPUT_FILE": "passage copy/俄乌冲突背景下的法国应对：动因及影响_张红.md",
    "OUTPUT_HTML": "俄乌冲突背景下的法国应对：动因及影响_张红.html"
}

# 可视化配置
VIS_CONFIG = {
    "NODE_COLOR": "#97C2FC",
    "EDGE_COLOR": "gray",
    "NODE_SIZE": 20
}