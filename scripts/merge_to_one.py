r"""
given a main tex file: main.tex
it contains several other tex files with \input or \include
this script will merge all the tex files into one, and output to a new file: merged.tex

Options:
--ignore-method-exp: Ignore method and experiment sections in chapters
--ignore-appendix: Ignore appendix content
"""

import os
import re
import argparse

def remove_comments(content):
    """Remove LaTeX comments from the content."""
    # 保留行内容，去掉注释部分
    lines = []
    for line in content.split('\n'):
        # 跳过完全是注释的行
        if line.lstrip().startswith('%'):
            continue
        # 处理行内注释
        # 但要保留 \% 转义的百分号
        result = ''
        i = 0
        while i < len(line):
            if line[i] == '\\' and i + 1 < len(line) and line[i + 1] == '%':
                result += '\\%'
                i += 2
            elif line[i] == '%':
                break
            else:
                result += line[i]
                i += 1
        # 只添加非空行
        if result.strip():
            lines.append(result.rstrip())
    return '\n'.join(lines)

def read_tex_file(file_path):
    """Read a tex file and return its content."""
    if not file_path.endswith('.tex'):
        file_path += '.tex'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 去除注释
            return remove_comments(content)
    except FileNotFoundError:
        print(f"Warning: Could not find file {file_path}")
        return f"% Could not find file {file_path}"

def remove_method_exp_sections(content):
    """Remove method, experiment and related work sections from the content."""
    # Pattern to match sections starting with method, experiment or related work (including Chinese equivalents)
    section_pattern = r'\\section\{(方法|实验|相关工作|Method|Experiment|Experiments|Related Work)[^\}]*\}.*?(?=\\section\{|$)'
    # Remove these sections using regex
    content = re.sub(section_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    return content

def process_content(content, base_dir, ignore_method_exp=False):
    """Process the content and replace \input and \include statements with file contents."""
    # Find all \input{...} and \include{...} statements
    input_pattern = r'\\input\{([^}]+)\}'
    include_pattern = r'\\include\{([^}]+)\}'
    
    # Process \input statements
    while re.search(input_pattern, content):
        match = re.search(input_pattern, content)
        if match:
            file_path = match.group(1)
            full_path = os.path.join(base_dir, file_path)
            file_content = read_tex_file(full_path)
            # Recursively process the included content
            file_content = process_content(file_content, os.path.dirname(full_path), ignore_method_exp)
            # Remove method and experiment sections if flag is set
            if ignore_method_exp:
                file_content = remove_method_exp_sections(file_content)
            content = content[:match.start()] + file_content + content[match.end():]

    # Process \include statements
    while re.search(include_pattern, content):
        match = re.search(include_pattern, content)
        if match:
            file_path = match.group(1)
            full_path = os.path.join(base_dir, file_path)
            file_content = read_tex_file(full_path)
            # Recursively process the included content
            file_content = process_content(file_content, os.path.dirname(full_path), ignore_method_exp)
            # Remove method and experiment sections if flag is set
            if ignore_method_exp:
                file_content = remove_method_exp_sections(file_content)
            content = content[:match.start()] + file_content + content[match.end():]

    return content

def remove_appendix(content):
    """Remove appendix content from the tex file."""
    # Pattern to match appendix content
    appendix_pattern = r'\\appendix.*?(?=\\end\{document\}|$)'
    # Remove appendix using regex
    content = re.sub(appendix_pattern, '', content, flags=re.DOTALL)
    return content

def merge_tex_files(main_tex_file='main.tex', output_file='merged.tex', ignore_method_exp=False, ignore_appendix=False):
    """
    Merge all tex files referenced in the main tex file into a single file.
    
    Args:
        main_tex_file (str): Path to the main tex file
        output_file (str): Path to the output merged file
        ignore_method_exp (bool): Whether to ignore method and experiment sections
        ignore_appendix (bool): Whether to ignore appendix content
    """
    # Get the base directory of the main tex file
    base_dir = os.path.dirname(main_tex_file)
    if not base_dir:
        base_dir = '.'

    # Read the main tex file
    with open(main_tex_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Process the content
    merged_content = process_content(content, base_dir, ignore_method_exp)
    
    # Remove appendix if requested
    if ignore_appendix:
        merged_content = remove_appendix(merged_content)
    
    # Final pass to remove any remaining comments
    merged_content = remove_comments(merged_content)

    # Write the merged content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(merged_content)
    
    print(f"Successfully merged all files into {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge LaTeX files into one.')
    parser.add_argument('--ignore-method-exp', action='store_true',
                      help='Ignore method and experiment sections in chapters')
    parser.add_argument('--ignore-appendix', action='store_true',
                      help='Ignore appendix content')
    parser.add_argument('--input', default='main.tex',
                      help='Input main tex file (default: main.tex)')
    parser.add_argument('--output', default='merged.tex',
                      help='Output merged tex file (default: merged.tex)')
    
    args = parser.parse_args()
    
    merge_tex_files(args.input, args.output, 
                   args.ignore_method_exp, 
                   args.ignore_appendix)
