from textnode import TextNode,TextType
from htmlnode import *
from delimit import *
import shutil
import os
import sys
base_file_path = os.path.join("..","StaticSiteGen")
def publish_site(source:str,destin:str):
    if not os.path.exists(destin):
        print(f"Created directory: {destin}")
        os.makedirs(destin)
    list = os.listdir(source)
    for l in list:
        lsource = os.path.join(source,l)
        ldestin = os.path.join(destin,l) 
        if os.path.isfile(lsource):
            shutil.copy(lsource,ldestin)
            print(f"Copied file to: {ldestin}")
        elif os.path.isdir(lsource):
            publish_site(lsource,ldestin)

def generate_page(from_path,template_path,dest_path,base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r', encoding='utf-8') as file:
        from_markdown = file.read()
    with open(template_path,'r',encoding='utf-8') as tfile:
        template = tfile.read()
    content = markdown_to_html_node(from_markdown).to_html()
    title = extract_title(from_markdown)
    final_html = template.replace("{{ Title }}",title)
    final_html = final_html.replace("{{ Content }}",content)
    final_html = final_html.replace(f'href="/',f'href="{base_path}')
    final_html = final_html.replace(f'src="/',f'src="{base_path}')
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        print(f"Created directory: {dest_dir}")
        os.makedirs(dest_dir)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
def generate_page_recursive(base_path):
    c_path = os.path.join(base_file_path,"content")
    template_path = os.path.join(base_file_path,"template.html")
    dest_path = os.path.join(base_file_path, "docs")
    content_path = os.walk(os.path.join(base_file_path,"content"))
    for dirpath, dirnames, filenames in content_path:
        for file in filenames:
            if file.endswith(".md"):
                from_path = os.path.join(dirpath,file)
                html_path = os.path.relpath(from_path,c_path)
                file_dest_path = os.path.join(dest_path,html_path).replace(".md",".html")
                generate_page(from_path,template_path,file_dest_path,base_path)

def main():
    if os.path.exists(os.path.join(base_file_path,"docs")):
        shutil.rmtree("docs")
    os.mkdir("docs")
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    file_path = os.path.join(base_file_path, "static")
    dest_path = os.path.join(base_file_path, "docs")

    publish_site(file_path,dest_path)
    generate_page_recursive(basepath)

if __name__ == "__main__":
    main()

