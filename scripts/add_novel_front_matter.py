#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为小说章节文件添加 Front Matter
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

def get_title_from_filename(filename):
    """从文件名获取标题（去掉扩展名）"""
    return os.path.splitext(filename)[0]

def has_front_matter(file_path):
    """检查文件是否已有 Front Matter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            return first_line == '---'
    except:
        return False

def add_front_matter_to_chapter(file_path, novel_name, part_name):
    """为章节文件添加 Front Matter"""
    filename = os.path.basename(file_path)
    title = get_title_from_filename(filename)
    chapter_order = extract_chapter_number(filename)
    
    # 构建路径信息
    relative_path = file_path.replace('\\', '/')
    path_parts = relative_path.split('/')
    
    # 生成 permalink
    novel_slug = novel_name.replace(' ', '-')
    part_slug = part_name.replace(' ', '-')
    title_slug = title.replace(' ', '-').replace('「', '').replace('」', '').replace('：', '-')
    permalink = f"/Novel/{novel_slug}/{part_slug}/{title_slug}/"
    
    front_matter = f"""---
layout: novel-reader
title: "{title}"
novel_title: "{novel_name}"
part_title: "{part_name}"
part_path: "{novel_name}/{part_name}"
chapter_order: {chapter_order}
permalink: {permalink}
---

"""
    
    try:
        # 读取原文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果已有 front matter，跳过
        if has_front_matter(file_path):
            print(f"文件 {file_path} 已有 Front Matter，跳过")
            return
        
        # 在文件开头添加 Front Matter
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(front_matter + content)
        
        print(f"已为文件 {file_path} 添加 Front Matter")
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")

def process_novel_directory(novel_dir):
    """处理小说目录"""
    novel_path = Path(novel_dir)
    novel_name = novel_path.name
    
    # 遍历所有子目录（分部）
    for part_dir in novel_path.iterdir():
        if part_dir.is_dir() and not part_dir.name.startswith('.'):
            part_name = part_dir.name
            
            # 处理该分部下的所有 markdown 文件
            for md_file in part_dir.glob('*.md'):
                add_front_matter_to_chapter(str(md_file), novel_name, part_name)

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

