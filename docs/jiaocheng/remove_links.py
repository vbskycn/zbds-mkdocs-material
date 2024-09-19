import os
import re

def remove_markdown_links(content):
    # 保留链接文字，去除链接URL，但保留本地图片链接和指定域名的链接
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    def replacement(match):
        text, url = match.groups()
        if url.startswith('/') or url.endswith(('.png', '.jpg', '.jpeg', '.gif')) or 'zbds.top' in url or 'zhoujie218.top' in url:
            return f'[{text}]({url})'
        return text
    
    clean_content = re.sub(pattern, replacement, content)
    return clean_content

def process_markdown_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            file_path = os.path.join(directory, filename)
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 处理内容
            clean_content = remove_markdown_links(content)
            
            # 检查内容是否发生变化
            if clean_content != content:
                # 将处理后的内容写回文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(clean_content)
                print(f"已处理文件: {filename}")
            else:
                print(f"文件无需修改: {filename}")

if __name__ == "__main__":
    # 获取当前目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # 处理当前目录下的所有 Markdown 文件
    process_markdown_files(current_directory)
    
    print("所有 Markdown 文件处理完成")
