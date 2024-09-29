import os
import re
import yaml
import datetime

# 定义要检测的文件夹根目录
root_directory = "I:\\B-MioBlogSites"

# 定义符合条件的文件夹前缀（_开头，首字母大写）
folder_prefix = "_"

# 定义 Front Matter 模板
front_matter_template = """---
layout: article
title: {title}
date: {date}
tags: [""]
---
"""

# 文件路径配置
config_file = os.path.join(root_directory, "_config.yml")
categories_file = os.path.join(root_directory, "_includes/categories.html")
tag_file = os.path.join(root_directory, "tag.html")

# --- Step 1: 定义 auto_front_matter 的相关函数和逻辑 ---
def find_markdown_files(directory):
    """遍历指定目录，查找所有 .md 文件，并返回文件路径列表。"""
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def has_front_matter(file_path):
    """检查文件是否包含 Front Matter（以 --- 开头）。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            return first_line == "---"
    except UnicodeDecodeError:
        print(f"无法解码文件：{file_path}，跳过该文件。")
        return False

def add_front_matter_to_file(file_path):
    """为没有 Front Matter 的文件添加 Front Matter 信息。"""
    # 获取文件名并去掉 .md 后缀作为标题
    file_name = os.path.basename(file_path)
    title = os.path.splitext(file_name)[0]

    # 获取当前日期
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    # 创建 Front Matter 内容
    front_matter = front_matter_template.format(title=title, date=date)

    try:
        # 读取原文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 在文件开头添加 Front Matter 信息，并写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(front_matter + "\n" + content)
        print(f"已为文件 {file_path} 添加 Front Matter 信息。")

    except UnicodeDecodeError:
        print(f"无法解码文件：{file_path}，跳过该文件。")

def auto_front_matter():
    """自动为符合条件的文件夹中的 .md 文件添加 Front Matter。"""
    # 遍历指定根目录，查找符合条件的文件夹
    for folder in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder)
        # 检查文件夹是否以 _ 开头，且首字母大写
        if os.path.isdir(folder_path) and folder.startswith(folder_prefix) and folder[1].isupper():
            print(f"正在处理文件夹：{folder_path}")
            
            # 查找该文件夹及其子文件夹中的所有 .md 文件
            markdown_files = find_markdown_files(folder_path)

            # 为没有 Front Matter 的 .md 文件添加 Front Matter 信息
            for md_file in markdown_files:
                if not has_front_matter(md_file):
                    add_front_matter_to_file(md_file)

# --- Step 2: 定义 auto_update 的相关函数和逻辑 ---
def read_existing_collections():
    """从 _config.yml 中读取现有的 collections 配置，返回已存在的分类名列表。"""
    with open(config_file, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
        
    # 提取现有 collections 中的分类名称（大写形式）
    existing_collections = list(config.get("collections", {}).keys())
    return existing_collections

def find_new_categories(existing_collections):
    """查找所有以 _ 开头且首字母为大写的文件夹，并且该文件夹中包含 .md 文件。
    与 existing_collections 进行对比，返回新建的分类文件夹。
    """
    categories = []
    for folder in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder)
        if os.path.isdir(folder_path) and folder.startswith(folder_prefix) and folder[1].isupper():
            # 去掉文件夹前缀 `_`，得到分类名称（如 `_Algorithm` -> `Algorithm`）
            category = folder[1:]

            # 检查文件夹中是否存在 .md 文件
            md_files = [f for f in os.listdir(folder_path) if f.endswith(".md")]
            if md_files and category not in existing_collections:
                categories.append(category)
    return categories

from ruamel.yaml import YAML

def update_config_yaml(new_categories):
    """将新的分类添加到 _config.yml 文件的 collections 中，并确保格式正确。"""
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)  # 控制映射（字典）和序列（列表）的缩进格式

    with open(config_file, "r", encoding="utf-8") as file:
        config = yaml.load(file)

    if "collections" not in config:
        config["collections"] = {}

    # 添加新分类到 collections 中
    for category in new_categories:
        lowercase_category = category.lower()
        if lowercase_category not in config["collections"]:
            config["collections"][category] = {
                "output": True,
                "permalink": f"/:collection/:path"
            }
            print(f"添加分类到 _config.yml: {category}")

    # 使用 `ruamel.yaml` 写入时，保持原有格式和缩进
    with open(config_file, "w", encoding="utf-8") as file:
        yaml.dump(config, file)
    print(f"已更新 _config.yml 文件。")



def create_html_files(new_categories):
    """为每个新的分类文件夹创建对应的小写 HTML 文件（如 algorithm.html）。"""
    for category in new_categories:
        lowercase_category = category.lower()
        html_content = f"""---
layout: list
title: {lowercase_category}
---
<main class="container">
  <div class="article-list">
    {{% for post in site.{category} %}}
    <article class="post-preview">
      <div class="post-content">
        <h3><a href="{{{{ post.url | relative_url }}}}">{{{{ post.title }}}}</a></h3>
        {{{{ post.excerpt }}}}
      </div>
    </article>
    {{% endfor %}}
  </div>
  {{% include categories.html posts=site.{category} %}}
</main>
"""
        # 写入新的 HTML 文件
        with open(f"{lowercase_category}.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"创建 HTML 文件: {lowercase_category}.html")

def update_categories_html(new_categories):
    """在 _includes/categories.html 中手动添加新的 HTML 引用。"""
    with open(categories_file, "r", encoding="utf-8") as file:
        categories_content = file.read()

    # 查找 if 条件中的 HTML 文件引用部分
    match = re.search(r"{% if page.name == '[\w.]+?'", categories_content)
    if match:
        original_condition = match.group(0)

        # 为 if 条件中添加新的 HTML 文件名（小写形式）
        for category in new_categories:
            lowercase_category = category.lower()
            new_condition = f"or page.name == '{lowercase_category}.html'"
            if new_condition not in categories_content:
                original_condition += f" {new_condition}"
                print(f"在 categories.html 中添加: {new_condition}")

        # 替换原始的 if 条件语句
        categories_content = categories_content.replace(match.group(0), original_condition)

    # 写回 categories.html
    with open(categories_file, "w", encoding="utf-8") as file:
        file.write(categories_content)
    print(f"已更新 {categories_file} 文件。")

def update_tag_html(new_categories):
    """在 tag.html 中更新 all_posts 的 concat 配置。"""
    with open(tag_file, "r", encoding="utf-8") as file:
        tag_content = file.read()

    # 查找并替换 all_posts 变量的 concat 配置
    match = re.search(r"{% assign all_posts = site\.[\w\W]*? %}", tag_content)
    if match:
        original_assign = match.group(0)
        new_assign = original_assign

        # 添加新分类到 all_posts 中，使用大写的分类名，如 `site.Algorithm`
        for category in new_categories:
            if f"| concat: site.{category}" not in new_assign:
                new_assign = new_assign.replace(" %}", f" | concat: site.{category} %}}")
                print(f"在 tag.html 中添加: | concat: site.{category}")

        # 替换原有 assign 语句
        tag_content = tag_content.replace(original_assign, new_assign)

    # 写回 tag.html
    with open(tag_file, "w", encoding="utf-8") as file:
        file.write(tag_content)
    print(f"已更新 {tag_file} 文件。")

def auto_update():
    """自动更新 _config.yml、创建 HTML 文件和更新其他相关文件。"""
    # 从 _config.yml 中读取现有的 collections
    existing_collections = read_existing_collections()
    print(f"现有的 collections: {existing_collections}")

    # 查找新分类（与现有 collections 对比）
    new_categories = find_new_categories(existing_collections)
    if not new_categories:
        print("未检测到新的分类文件夹，脚本终止。")
        return

    print(f"检测到以下新分类文件夹: {new_categories}")

    # 更新 _config.yml 文件
    update_config_yaml(new_categories)

    # 创建新的 HTML 文件
    create_html_files(new_categories)

    # 更新 _includes/categories.html 文件
    update_categories_html(new_categories)

    # 更新 tag.html 文件
    update_tag_html(new_categories)

# --- Main Entry ---
def main():
    # 先执行 auto_front_matter 操作
    auto_front_matter()
    # 再执行 auto_update 操作
    auto_update()

if __name__ == "__main__":
    main()
