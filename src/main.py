import os
import shutil
import logging
from htmlnode import markdown_to_html_node 

def copy_directory_contents(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        logging.error(f"Source directory '{source_dir}' does not exist.")
        return

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        dest_item = os.path.join(dest_dir, item)
        
        if os.path.isdir(source_item):
            copy_directory_contents(source_item, dest_item)
        elif os.path.isfile(source_item):
            shutil.copy(source_item, dest_item)
            logging.info(f"Copied file: {source_item} -> {dest_item}")
        else:
            logging.warning(f"Ignoring item: {source_item}")

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    raise ValueError("No h1 header found in the markdown.")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    html_content = markdown_to_html_node(markdown_content).to_html()

    title = extract_title(markdown_content)

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_content)


def main():
    source_dir = "static"
    dest_dir = "public"
    
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
        logging.info(f"Deleted contents of {dest_dir}")
    
    copy_directory_contents(source_dir, dest_dir)

    markdown_file = os.path.join("content", "index.md")

    generate_page(markdown_file, "template.html", "public/index.html")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
