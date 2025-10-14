from htmlnode import markdown_to_html_node, extract_title
import os

def generate_page(from_path, template_path, dest_path):
    # Print a message
    print(f"Generate page from {from_path} to {dest_path} using {template_path}")

    # Get the markdown
    markdown_file = open(from_path)
    markdown = markdown_file.read()
    markdown_file.close()

    # Get the template
    template_file = open(template_path)
    template = template_file.read()
    template_file.close()

    # Convert markdown to html
    nodes = markdown_to_html_node(markdown)
    content = nodes.to_html()

    # Get the title
    title = extract_title(markdown)

    # Replace the title in content in the template
    html_file = template.replace("{{ Title }}", title)
    html_file = html_file.replace("{{ Content }}", content)

    # Write html to destination
    # Make path if it doesn't exist
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    dest_file = open(dest_path, 'w')
    dest_file.write(html_file)
    dest_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Print a message
    print(f"Generate page from {dir_path_content} to {dest_dir_path} using {template_path}")

    ls = os.listdir(dir_path_content)

    for path in ls:
        if os.path.isfile(os.path.join(dir_path_content, path)):
            print(f"{path} is a file")
            content = os.path.join(dir_path_content, path)
            public = path.replace(".md", ".html")
            public = os.path.join(dest_dir_path, public)
            generate_page(content, template_path, public)
        else:
            print(f"{path} is a directory")
            generate_pages_recursive(os.path.join(dir_path_content, path), template_path, os.path.join(dest_dir_path, path))