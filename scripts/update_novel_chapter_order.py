#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新小说章节文件的 chapter_order
"""

import os
import re
from pathlib import Path

def extract_chapter_number(filename):
    """从文件名中提取章节号"""
    # 匹配中文数字：第一章、第二章等
    chinese_numbers = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '十一': 11, '十二': 12, '十三': 13, '十四': 14,
        '十五': 15, '十六': 16, '十七': 17, '十八': 18,
        '十九': 19, '二十': 20
    }
    
    # 先尝试匹配中文数字
    match = re.search(r'第([一二三四五六七八九十]+)章', filename)
    if match:
        chinese_num = match.group(1)
        if chinese_num in chinese_numbers:
            return chinese_numbers[chinese_num]
        # 处理"十X"的情况
        if chinese_num.startswith('十') and len(chinese_num) > 1:
            base = 10
            if chinese_num[1:] in chinese_numbers:
                return base + chinese_numbers[chinese_num[1:]] - 1
    
    # 匹配阿拉伯数字：第一章、第二章等
    match = re.search(r'第(\d+)章', filename)
    if match:
        return int(match.group(1))
    
    # 如果没有找到，尝试提取文件名开头的数字
    match = re.search(r'^(\d+)', filename)
    if match:
        return int(match.group(1))
    
    return 9999  # 默认排序到最后

def update_chapter_order(file_path):
    """更新章节文件的 chapter_order"""
    filename = os.path.basename(file_path)
    chapter_order = extract_chapter_number(filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有 chapter_order
        if 'chapter_order:' in content:
            # 更新现有的 chapter_order
            pattern = r'chapter_order:\s*\d+'
            replacement = f'chapter_order: {chapter_order}'
            updated_content = re.sub(pattern, replacement, content)
            
            if updated_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"已更新 {file_path} 的 chapter_order 为 {chapter_order}")
            else:
                print(f"{file_path} 的 chapter_order 已经是 {chapter_order}，跳过")
        else:
            # 如果没有 chapter_order，在 front matter 中添加
            # 找到 front matter 结束位置
            front_matter_end = content.find('---', 3)
            if front_matter_end != -1:
                # 在 front matter 结束前添加 chapter_order
                updated_content = content[:front_matter_end] + f'chapter_order: {chapter_order}\n' + content[front_matter_end:]
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"已为 {file_path} 添加 chapter_order: {chapter_order}")
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")

def process_novel_directory(novel_dir):
    """处理小说目录"""
    novel_path = Path(novel_dir)
    
    # 遍历所有子目录（分部）
    for part_dir in novel_path.iterdir():
        if part_dir.is_dir() and not part_dir.name.startswith('.'):
            # 处理该分部下的所有 markdown 文件
            for md_file in part_dir.glob('*.md'):
                update_chapter_order(str(md_file))

def main():
    """主函数"""
    # 小说目录路径
    novel_base_dir = Path('_Novel')
    
    if not novel_base_dir.exists():
        print(f"错误：目录 {novel_base_dir} 不存在")
        return
    
    # 遍历所有小说目录
    for novel_dir in novel_base_dir.iterdir():
        if novel_dir.is_dir() and not novel_dir.name.startswith('.'):
            print(f"处理小说：{novel_dir.name}")
            process_novel_directory(novel_dir)
    
    print("处理完成！")

if __name__ == '__main__':
    main()

