import re
import click

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
def clean_tex_comments(input_path):
    """清理TEX文件中的注释并保存到新文件。
    新文件名将在原文件名后添加.clean后缀。
    
    INPUT_PATH: TEX文件的路径
    """
    # 读取输入文件
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除行内注释 (% 开头直到行尾，但保留换行符)
    content = re.sub(r'(?<!\\)%.*?(?=\n|$)', '', content)
    
    # 移除多余的空行
    content = re.sub(r'\n\s*\n+', '\n\n', content)
    
    # 生成输出文件名
    output_file = input_path.rsplit('.', 1)[0] + '.clean.' + input_path.rsplit('.', 1)[1]
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    
    click.echo(f"已清理注释并保存到: {output_file}")

if __name__ == '__main__':
    clean_tex_comments()

# 使用方法: python script.py your_file.tex