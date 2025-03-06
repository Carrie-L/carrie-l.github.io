import os
import re
import yaml
import datetime
from pypinyin import lazy_pinyin  # 添加拼音转换库
import shutil  # 用于文件操作

# 定义要检测的文件夹根目录
root_directory = "I:\\B-MioBlogSites"

# 定义符合条件的文件夹前缀（_开头，首字母大写）
folder_prefix = "_"

# 文件名长度限制
MAX_FILENAME_LENGTH = 50

# 定义 Front Matter 模板 - 注意结束标记后有空行
front_matter_template = """---
layout: article
title: "{title}"
date: {date}
permalink: {permalink}
tags: []
---

"""

# 文件路径配置
config_file = os.path.join(root_directory, "_config.yml")
categories_file = os.path.join(root_directory, "_includes/categories.html")
tag_file = os.path.join(root_directory, "tag.html")
index_file = os.path.join(root_directory, "index.html")

def convert_to_pinyin(text):
    """将中文文本转换为拼音，用短横线连接"""
    # 转换为拼音
    pinyin_list = lazy_pinyin(text)
    # 过滤无效字符，只保留字母、数字和短横线
    filtered_pinyin = []
    for word in pinyin_list:
        # 将非字母数字字符替换为短横线
        cleaned_word = re.sub(r'[^a-zA-Z0-9]', '-', word)
        if cleaned_word:  # 确保不添加空字符串
            filtered_pinyin.append(cleaned_word)
    
    # 用短横线连接所有拼音
    result = '-'.join(filtered_pinyin)
    
    # 替换多个连续短横线为单个短横线
    result = re.sub(r'-+', '-', result)
    
    # 去除首尾的短横线
    result = result.strip('-')
    
    # 截断超长文件名
    if len(result) > MAX_FILENAME_LENGTH:
        result = result[:MAX_FILENAME_LENGTH].rstrip('-')
    
    return result.lower()  # 转为小写

def get_original_title(file_path):
    """获取文件的原始标题（不再重命名文件）"""
    file_name = os.path.basename(file_path)
    original_title = os.path.splitext(file_name)[0]
    return file_path, original_title

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

def add_front_matter_to_file(file_path, original_title=None):
    """为没有 Front Matter 的文件添加 Front Matter 信息。"""
    # 获取文件名并去掉 .md 后缀作为标题
    if not original_title:
        original_title = os.path.splitext(os.path.basename(file_path))[0]

    # 获取当前日期
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 获取文件所在的文件夹名称（不带前缀）用于permalink
    folder_path = os.path.dirname(file_path)
    folder_name = os.path.basename(folder_path)
    category = folder_name[1:] if folder_name.startswith('_') else folder_name
    
    # 生成permalink（格式: /分类/拼音文件名/）- 仍然使用拼音形式
    file_name_pinyin = convert_to_pinyin(original_title)
    permalink = f"/{category.lower()}/{file_name_pinyin}/"
    
    # 创建 Front Matter 内容，包含permalink和标题
    # 替换标题中的引号以避免YAML解析错误
    title_escaped = original_title.replace('"', '\\"')
    front_matter = front_matter_template.format(
        title=title_escaped, 
        date=date,
        permalink=permalink
    )

    try:
        # 读取原文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 在文件开头添加 Front Matter 信息，并写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(front_matter + content)  # front_matter已包含结束换行符
        print(f"已为文件 {file_path} 添加 Front Matter 信息。")

    except UnicodeDecodeError:
        print(f"无法解码文件：{file_path}，跳过该文件。")

def process_markdown_file(file_path, original_title=None):
    """处理Markdown文件，提取#标签并修改图片路径格式，确保格式正确"""
    # 获取文件所在的文件夹名称作为类别标签
    folder_path = os.path.dirname(file_path)
    folder_name = os.path.basename(folder_path)
    category_tag = folder_name[1:] if folder_name.startswith('_') else folder_name
    category_lower = category_tag.lower()
    
    # 如果没有提供原始标题，则使用文件名
    if not original_title:
        original_title = os.path.splitext(os.path.basename(file_path))[0]
        
    # 获取文件名拼音形式（用于permalink）- 只有permalink使用拼音
    file_name_pinyin = convert_to_pinyin(original_title)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        print(f"无法解码文件：{file_path}，跳过该文件。")
        return None

    # 提取并删除 #标签 (确保只匹配 # 后面的有效文字，避免标题符号)
    tags_pattern = r"(?<!\S)#([a-zA-Z0-9_\u4e00-\u9fa5]+)"  # 匹配以#开头且是有效字符的标签
    new_tags = re.findall(tags_pattern, content)  # 提取所有 #标签
    new_tags = list(set(new_tags))  # 去重
    # 清理可能存在的无效标签
    new_tags = [tag for tag in new_tags if tag and not tag.endswith(')') and len(tag) > 1]

    # 删除文件中的 #标签（避免误删其他内容）
    content = re.sub(r"(?<!\S)#([a-zA-Z0-9_\u4e00-\u9fa5]+)", '', content)

    # 替换 ![[]] 格式图片路径为 ![]() 格式
    image_pattern = r"!\[\[(.*?)\]\]"
    updated_content = re.sub(image_pattern, r'![](\1)', content)
    # 避免重复替换 ../assets/blogimages/ 开头的路径
    updated_content = re.sub(r'!\[]\((?!../assets/blogimages/)(.*?)\)', r'![](../assets/blogimages/\1)', updated_content)

    # 检查是否有Front Matter
    has_front_matter = False
    front_matter_pattern = r"^---\s*\n(.*?)\n\s*---"
    front_matter = re.search(front_matter_pattern, content, re.DOTALL)

    if front_matter:
        front_matter_content = front_matter.group(1).strip()

        # 提取已有的tags - 更精确的正则表达式处理
        existing_tags = []
        tags_match = re.search(r'tags:\s*\[(.*?)\]', front_matter_content, re.DOTALL)
        if tags_match and tags_match.group(1).strip():
            # 使用更可靠的方式拆分标签
            tag_content = tags_match.group(1).strip()
            # 提取引号中的内容作为标签
            tag_matches = re.findall(r'["\'](.*?)["\']', tag_content)
            if tag_matches:
                existing_tags = [tag.strip() for tag in tag_matches if tag.strip()]
            else:
                # 尝试普通拆分
                existing_tags = [tag.strip().strip('"').strip("'") for tag in tag_content.split(",") if tag.strip()]
        
        # 添加分类文件夹名称作为标签（如果不存在）
        if category_tag and category_tag not in existing_tags:
            existing_tags.append(category_tag)
            
        # 过滤掉可能的错误标签
        filtered_tags = []
        for tag in existing_tags + new_tags:
            # 排除 "0)" 等无效标签
            if tag and not tag.endswith(')') and len(tag) > 1:
                filtered_tags.append(tag)
                
        # 合并标签并去重
        combined_tags = list(set(filtered_tags))
        
        # 构建新的tags字段
        if combined_tags:
            new_tags_line = f'tags: ["' + '", "'.join(combined_tags) + '"]'
        else:
            new_tags_line = 'tags: []'
            
        # 确保标题是原始标题
        title_escaped = original_title.replace('"', '\\"')
        title_line = f'title: "{title_escaped}"'
        
        # 处理标题和tags
        new_front_matter = []
        lines = front_matter_content.split('\n')
        title_added = False
        tags_added = False
        permalink_added = False
        
        for line in lines:
            if line.strip().startswith('title:'):
                new_front_matter.append(title_line)
                title_added = True
            elif line.strip().startswith('tags:'):
                new_front_matter.append(new_tags_line)
                tags_added = True
            elif line.strip().startswith('permalink:'):
                permalink = f"/{category_lower}/{file_name_pinyin}/"
                new_front_matter.append(f"permalink: {permalink}")
                permalink_added = True
            else:
                new_front_matter.append(line)
        
        # 如果没有添加标题，添加标题
        if not title_added:
            new_front_matter.insert(0, title_line)
            
        # 如果没有添加标签，添加标签
        if not tags_added:
            new_front_matter.append(new_tags_line)
            
        # 如果没有添加permalink，添加permalink
        if not permalink_added:
            permalink = f"/{category_lower}/{file_name_pinyin}/"
            new_front_matter.append(f"permalink: {permalink}")
            
        # 组合新的Front Matter内容
        new_front_matter_content = '\n'.join(new_front_matter)
        
        # 替换原有Front Matter
        updated_content = updated_content.replace(front_matter.group(0), f"---\n{new_front_matter_content}\n---\n\n")
        
    else:
        # 如果没有Front Matter，添加新的Front Matter
        # 确保分类标签被添加
        if category_tag and category_tag not in new_tags:
            new_tags.append(category_tag)
            
        # 格式化标签列表
        if new_tags:
            tags_str = f'["' + '", "'.join(new_tags) + '"]'
        else:
            tags_str = '[]'
            
        # 生成permalink
        permalink = f"/{category_lower}/{file_name_pinyin}/"
        
        # 准备标题，确保正确转义
        title_escaped = original_title.replace('"', '\\"')
            
        # 明确指定格式确保每个部分都在自己的行上
        front_matter = f"""---
layout: article
title: "{title_escaped}"
date: {datetime.datetime.now().strftime('%Y-%m-%d')}
permalink: {permalink}
tags: {tags_str}
---

"""
        updated_content = front_matter + updated_content

    # 最后的修复，确保YAML标记格式正确
    # 确保开头的 --- 单独占一行
    updated_content = re.sub(r"^([^\n-]*)---", r"\1---", updated_content)
    
    # 确保结尾的 --- 单独占一行并且后面有空行
    updated_content = re.sub(r"([^\n])---(\s*\n)", r"\1\n---\n\n", updated_content)
    
    # 去除可能的多余空行
    updated_content = re.sub(r"\n{3,}", "\n\n", updated_content)

    # 保存修改后的文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    return updated_content

def auto_front_matter():
    """自动为符合条件的文件夹中的 .md 文件添加 Front Matter，不再重命名文件。"""
    # 遍历指定根目录，查找符合条件的文件夹
    for folder in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder)
        # 检查文件夹是否以 _ 开头，且首字母大写
        if os.path.isdir(folder_path) and folder.startswith(folder_prefix) and folder[1].isupper():
            print(f"正在处理文件夹：{folder_path}")
            
            # 查找该文件夹及其子文件夹中的所有 .md 文件
            markdown_files = find_markdown_files(folder_path)

            # 为每个 .md 文件执行处理
            for md_file in markdown_files:
                try:
                    # 获取原始标题，不再重命名文件
                    file_path, original_title = get_original_title(md_file)
                    
                    # 检查文件是否已有Front Matter
                    if not has_front_matter(file_path):
                        # 只为没有Front Matter的文件添加Front Matter
                        add_front_matter_to_file(file_path, original_title)
                    else:
                        # 对于已有Front Matter的文件，只在原有基础上修改
                        print(f"文件 {file_path} 已有Front Matter，修改现有内容...")
                    
                    # 处理文件内容
                    process_markdown_file(file_path, original_title)
                    
                except Exception as e:
                    print(f"处理文件 {md_file} 时出错: {str(e)}")

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
    try:
        # 先读取文件内容
        with open(config_file, "r", encoding="utf-8") as file:
            content = file.read()

        # 手动解析 collections 部分
        collections_start = content.find("collections:")
        if collections_start == -1:
            # 如果没有 collections，添加它
            content += "\n\ncollections:\n"

        # 添加新分类
        for category in new_categories:
            collection_entry = f"""  {category}:
    output: true
    permalink: /:collection/:path
"""
            # 检查该分类是否已存在
            if category not in content:
                # 找到 collections 部分的末尾
                collections_end = content.find("\n\n", collections_start)
                if collections_end == -1:
                    collections_end = len(content)
                
                # 在 collections 部分末尾插入新分类
                content = content[:collections_end] + "\n" + collection_entry + content[collections_end:]
                print(f"添加分类到 _config.yml: {category}")

        # 写回文件
        with open(config_file, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"已更新 _config.yml 文件。")

    except Exception as e:
        print(f"更新 _config.yml 时发生错误: {str(e)}")
        raise


def create_html_files(new_categories):
    """为每个新的分类文件夹创建对应的小写 HTML 文件（如 algorithm.html）。"""
    for category in new_categories:
        lowercase_category = category.lower()
        html_content = f"""---
layout: list
title: {lowercase_category}
---
    {{% for post in site.{category} %}}
    <article class="post-preview">
      <div class="list-post-content">
        <h3><a href="{{{{ post.url | relative_url }}}}">{{{{ post.title }}}}</a></h3>
        <div class="item-text">{{{{ post.excerpt | strip_html | truncatewords: 100 }}}}</div>
      </div>
    </article>
    {{% endfor %}}
  </div>
  {{% include categories.html posts=site.{category} %}}
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

def update_index_html(new_categories):
    """在 index.html 中更新 all_posts 的 concat 配置。"""
    with open(index_file, "r", encoding="utf-8") as file:
        index_content = file.read()

    # 查找并替换 all_posts 变量的 concat 配置
    match = re.search(r"{% assign all_posts = site\.[\w\W]*? %}", index_content)
    if match:
        original_assign = match.group(0)
        new_assign = original_assign

        # 添加新分类到 all_posts 中，使用大写的分类名，如 `site.Algorithm`
        for category in new_categories:
            if f"| concat: site.{category}" not in new_assign:
                new_assign = new_assign.replace(" %}", f" | concat: site.{category} %}}")
                print(f"在 tag.html 中添加: | concat: site.{category}")

        # 替换原有 assign 语句
        index_content = index_content.replace(original_assign, new_assign)

    # 写回 tag.html
    with open(index_file, "w", encoding="utf-8") as file:
        file.write(index_content)
    print(f"已更新 {index_file} 文件。")

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

    # 更新 index.html 文件
    update_index_html(new_categories)

# --- Main Entry ---
def main():
    # 先执行 auto_front_matter 操作
    auto_front_matter()
    # 再执行 auto_update 操作
    auto_update()

if __name__ == "__main__":
    main()
