import bibtexparser
from difflib import SequenceMatcher
import re

def clean_title(title):
    """清理标题文本，移除特殊字符和多余空格"""
    # 移除花括号
    title = re.sub(r'{|}', '', title)
    # 移除多余空格
    title = ' '.join(title.split())
    # 转换为小写
    return title.lower().strip()

def similar(a, b):
    """计算两个字符串的相似度"""
    return SequenceMatcher(None, a, b).ratio()

def analyze_bib_files(file1_path, file2_path, similarity_threshold=0.95):
    # 读取第一个bib文件
    with open(file1_path, 'r', encoding='utf-8') as file:
        bib1 = bibtexparser.load(file)
    
    # 读取第二个bib文件
    with open(file2_path, 'r', encoding='utf-8') as file:
        bib2 = bibtexparser.load(file)
    
    entries1 = bib1.entries
    entries2 = bib2.entries
    
    # 存储结果
    duplicates = []  # 重复条目
    unique_in_first = []  # 仅在第一个文件中的条目
    
    # 为第二个文件中的所有条目创建清理后的标题列表
    titles2 = [clean_title(entry.get('title', '')) for entry in entries2]
    
    # 检查第一个文件中的每个条目
    for entry1 in entries1:
        title1 = clean_title(entry1.get('title', ''))
        found_match = False
        
        # 与第二个文件中的所有条目比较
        for i, title2 in enumerate(titles2):
            if similar(title1, title2) >= similarity_threshold:
                duplicates.append({
                    'file1_entry': entry1,
                    'file2_entry': entries2[i]
                })
                found_match = True
                break
        
        if not found_match:
            unique_in_first.append(entry1)
    
    return duplicates, unique_in_first


def format_bib_entry(entry):
    """将条目格式化为BibTeX格式的字符串"""
    entry_type = entry.get('ENTRYTYPE', 'article')
    entry_id = entry.get('ID', 'unknown')
    
    lines = [f'@{entry_type}{{{entry_id},']
    
    # 获取所有字段（除了ENTRYTYPE和ID）
    fields = {k: v for k, v in entry.items() if k not in ['ENTRYTYPE', 'ID']}
    
    # 格式化每个字段
    for key, value in fields.items():
        lines.append(f'  {key} = {{{value}}},')
    
    lines.append('}')
    return '\n'.join(lines)


def print_results(duplicates, unique_in_first):
    print("\n=== 重复的条目 ===")
    for i, dup in enumerate(duplicates, 1):
        # print(f"\n重复项 #{i}:")
        # print(f"文件1中的标识符: {dup['file1_entry'].get('ID', 'N/A')}")
        # print(f"文件2中的标识符: {dup['file2_entry'].get('ID', 'N/A')}")
        # print(f"标题: {dup['file1_entry'].get('title', 'N/A')}")

        # 如果标识符不一样，打印
        if dup['file1_entry'].get('ID') != dup['file2_entry'].get('ID'):
            print(f"文件1中的标识符: {dup['file1_entry'].get('ID', 'N/A')}")
            print(f"文件2中的标识符: {dup['file2_entry'].get('ID', 'N/A')}")
            print(f"标识符不一样: {dup['file1_entry'].get('ID')} vs {dup['file2_entry'].get('ID')}")

    print("\n=== 仅在第一个文件中的条目 ===")
    for i, entry in enumerate(unique_in_first, 1):
        print()
        print(format_bib_entry(entry))

def main():
    # 替换为实际的文件路径
    file1_path = '/home/t-thang/code_base/cache/202412/ref.bib'
    file2_path = '/home/t-thang/code_base/phd-thesis/seuthesix.bib'
    
    try:
        duplicates, unique_in_first = analyze_bib_files(file1_path, file2_path)
        print_results(duplicates, unique_in_first)
    except Exception as e:
        print(f"处理文件时发生错误: {str(e)}")

if __name__ == "__main__":
    main()