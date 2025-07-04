import re
from data_structures import Node
from config import KG_CONFIG
from kg_gen import KGGen  # 假设kg_gen是外部模块

def create_kg():
    return KGGen(
        model=KG_CONFIG["MODEL_NAME"],
        temperature=KG_CONFIG["TEMPERATURE"],
        api_key=KG_CONFIG["API_KEY"]
    )

def clean_text(text):
    return re.sub(r'[",...]', '', text)

def build_graph(node, kg):
    text = clean_text(node.get_text())
    graph = kg.generate(input_data=text, context=node.get_name())
    node.graph = graph

def merge_tree(node, kg):
    if not node.children:
        return
    temp = []
    for child in node.get_children():
        temp.append(child.graph)
    combined_graph = kg.aggregate(temp)
    node.graph = combined_graph

def create_map(node, kg):
    for child in node.get_children():
        create_map(child, kg)
    if not node.children:
        build_graph(node, kg)

def merge_map(node, kg):
    for child in node.get_children():
        if not child.is_leaf:
            merge_map(child, kg)
    merge_tree(node, kg)