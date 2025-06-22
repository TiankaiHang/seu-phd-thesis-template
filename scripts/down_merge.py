import requests
import tarfile
import os
import re
import shutil
from io import BytesIO

def download_source(arxiv_id):
    if "arxiv.org" in arxiv_id:
        arxiv_id = arxiv_id.split('/')[-1]
    
    url = f"https://arxiv.org/e-print/{arxiv_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("下载失败")
    
    return response.content

def extract_tar(content, output_dir):
    # 如果目录已存在，先删除
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    # 解压文件
    with tarfile.open(fileobj=BytesIO(content), mode='r:*') as tar:
        tar.extractall(output_dir)
    
    return output_dir

def find_main_tex(directory):
    tex_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))
    
    for tex_file in tex_files:
        with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if '\\documentclass' in content:
                return tex_file
    
    return None

def process_input_commands(content, base_path):
    def replace_input(match):
        filename = match.group(1)
        if not filename.endswith('.tex'):
            filename += '.tex'
        filepath = os.path.join(os.path.dirname(base_path), filename)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except:
            return match.group(0)
    
    def replace_include(match):
        filename = match.group(1)
        if not filename.endswith('.tex'):
            filename += '.tex'
        filepath = os.path.join(os.path.dirname(base_path), filename)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except:
            return match.group(0)
    
    content = re.sub(r'\\input\{([^}]+)\}', replace_input, content)
    content = re.sub(r'\\include\{([^}]+)\}', replace_include, content)
    
    return content

def create_project_directory(arxiv_id):
    # 创建以arxiv_id命名的项目目录
    if "arxiv.org" in arxiv_id:
        arxiv_id = arxiv_id.split('/')[-1]
    
    project_dir = f"arxiv_{arxiv_id}"
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
    return project_dir

def main(arxiv_url):
    # 创建项目目录
    project_dir = create_project_directory(arxiv_url)
    
    # 下载源文件
    content = download_source(arxiv_url)
    
    # 解压文件到项目目录
    temp_dir = extract_tar(content, os.path.join(project_dir, "source"))
    
    # 查找主tex文件
    main_tex = find_main_tex(temp_dir)
    if not main_tex:
        raise Exception("未找到主tex文件")
    
    # 读取主文件内容
    with open(main_tex, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 处理 input 和 include 命令
    content = process_input_commands(content, main_tex)
    
    # 保存合并后的文件到项目目录
    output_file = os.path.join(project_dir, "merged.tex")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"项目文件夹: {project_dir}")
    print(f"源文件位置: {os.path.join(project_dir, 'source')}")
    print(f"合并后的tex文件: {output_file}")


if __name__ == "__main__":
    # 使用示例
    # arxiv_url = "https://arxiv.org/src/2407.03297"
    arxiv_url = "https://arxiv.org/src/2303.09556"
    main(arxiv_url)
