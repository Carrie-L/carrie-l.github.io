import os
import re
import shutil
from ruamel.yaml import YAML

# --- Configuration ---
ROOT_DIRECTORY = "I:\\B-MioBlogSites"
CONFIG_FILE = os.path.join(ROOT_DIRECTORY, "_config.yml")
CATEGORIES_HTML_FILE = os.path.join(ROOT_DIRECTORY, "_includes/categories.html")
TAG_HTML_FILE = os.path.join(ROOT_DIRECTORY, "tag.html")
INDEX_HTML_FILE = os.path.join(ROOT_DIRECTORY, "index.html")
MONITOR_SERVICE_FILE = os.path.join(ROOT_DIRECTORY, "scripts/blog_monitor_service.py")

def remove_category_folder(category_name):
    """Safely removes the specified category folder."""
    folder_path = os.path.join(ROOT_DIRECTORY, f"_{category_name}")
    if os.path.isdir(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"✅ Successfully removed folder: {folder_path}")
        except OSError as e:
            print(f"❌ Error removing folder {folder_path}: {e}")
            return False
    else:
        print(f"ℹ️ Folder not found, skipping: {folder_path}")
    return True

def remove_from_config(category_name):
    """Removes the specified category from the _config.yml collections."""
    yaml = YAML()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = yaml.load(f)

        if "collections" in config and category_name in config["collections"]:
            del config["collections"][category_name]
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                yaml.dump(config, f)
            print(f"✅ Successfully removed '{category_name}' from {CONFIG_FILE}")
        else:
            print(f"ℹ️ Category '{category_name}' not found in {CONFIG_FILE}, skipping.")
    except Exception as e:
        print(f"❌ Error updating {CONFIG_FILE}: {e}")

def remove_category_html_file(category_name):
    """Removes the category's corresponding HTML file."""
    file_path = os.path.join(ROOT_DIRECTORY, f"{category_name.lower()}.html")
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            print(f"✅ Successfully removed file: {file_path}")
        except OSError as e:
            print(f"❌ Error removing file {file_path}: {e}")
    else:
        print(f"ℹ️ HTML file not found, skipping: {file_path}")

def remove_from_includes_html(category_name):
    """Removes the link from _includes/categories.html."""
    try:
        with open(CATEGORIES_HTML_FILE, "r+", encoding="utf-8") as f:
            content = f.read()
            # Regex to find "or page.name == 'category.html'" with optional spaces
            pattern = re.compile(r"\s*or\s+page\.name\s*==\s*'"+ re.escape(category_name.lower()) + r"\.html'")
            if pattern.search(content):
                new_content = pattern.sub("", content)
                f.seek(0)
                f.write(new_content)
                f.truncate()
                print(f"✅ Successfully removed link for '{category_name}' from {CATEGORIES_HTML_FILE}")
            else:
                print(f"ℹ️ Link for '{category_name}' not found in {CATEGORIES_HTML_FILE}, skipping.")
    except Exception as e:
        print(f"❌ Error updating {CATEGORIES_HTML_FILE}: {e}")

def remove_from_concat_config(file_path, category_name):
    """Removes the category from the 'all_posts' concat line in a given file."""
    try:
        with open(file_path, "r+", encoding="utf-8") as f:
            content = f.read()
            # Regex to find "| concat: site.CategoryName" with optional spaces
            pattern = re.compile(r"\s*\|\s*concat:\s*site\." + re.escape(category_name))
            if pattern.search(content):
                new_content = pattern.sub("", content)
                f.seek(0)
                f.write(new_content)
                f.truncate()
                print(f"✅ Successfully removed concat for 'site.{category_name}' from {file_path}")
            else:
                print(f"ℹ️ Concat for 'site.{category_name}' not found in {file_path}, skipping.")
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")

def remove_from_monitor_service(category_name):
    """Removes the category folder path from the blog_monitor_service.py script."""
    try:
        with open(MONITOR_SERVICE_FILE, "r+", encoding="utf-8") as f:
            lines = f.readlines()
            # Construct the exact path string to look for
            path_to_remove = f'r"I:\\\\B-MioBlogSites\\\\_{category_name}"'
            
            new_lines = [line for line in lines if path_to_remove not in line]

            if len(new_lines) < len(lines):
                # Clean up potential trailing commas from the previous line
                for i in range(len(new_lines)):
                    if new_lines[i].strip().endswith(',') and (i + 1 >= len(new_lines) or ']' in new_lines[i+1]):
                         new_lines[i] = new_lines[i].rstrip().rstrip(',') + '\n'

                f.seek(0)
                f.writelines(new_lines)
                f.truncate()
                print(f"✅ Successfully removed monitoring path for '_{category_name}' from {MONITOR_SERVICE_FILE}")
            else:
                print(f"ℹ️ Monitoring path for '_{category_name}' not found in {MONITOR_SERVICE_FILE}, skipping.")
    except Exception as e:
        print(f"❌ Error updating {MONITOR_SERVICE_FILE}: {e}")

def main():
    """Main function to drive the category removal process."""
    category_to_remove = input("Enter the Category name to remove (e.g., 'Git', 'DSA'): ")

    if not category_to_remove:
        print("No category name provided. Exiting.")
        return
        
    print(f"--- Starting removal process for category: {category_to_remove} ---")
    
    # 1. Remove from _config.yml
    remove_from_config(category_to_remove)
    
    # 2. Remove from _includes/categories.html
    remove_from_includes_html(category_to_remove)
    
    # 3. Remove from tag.html
    remove_from_concat_config(TAG_HTML_FILE, category_to_remove)
    
    # 4. Remove from index.html
    remove_from_concat_config(INDEX_HTML_FILE, category_to_remove)
    
    # 5. Remove from monitor service
    remove_from_monitor_service(category_to_remove)
    
    # 6. Remove the category's HTML file
    remove_category_html_file(category_to_remove)
    
    # 7. Finally, remove the category folder itself
    remove_category_folder(category_to_remove)
    
    print(f"--- Removal process for category '{category_to_remove}' completed. ---")

if __name__ == "__main__":
    main() 