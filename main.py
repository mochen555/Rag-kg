from text_processor import TextProcessor
from kg_processor import create_kg, create_map, merge_map
from visualization import generate_html
from config import FILE_PATHS

def main():
    # 文本处理
    processor = TextProcessor()
    processor.parse_file(FILE_PATHS["INPUT_FILE"])
    
    # 知识图谱处理
    kg = create_kg()
    create_map(processor.root, kg)
    merge_map(processor.root, kg)
    
    # 生成可视化
    generate_html(processor.root, FILE_PATHS["OUTPUT_HTML"])

if __name__ == "__main__":
    main()