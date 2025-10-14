from textnode import TextNode, TextType
from blockType import block_to_block_type, BlockType
import re

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props != None:
            props_string = ""

            for key in self.props: 
                props_string += f' {key}="{self.props[key]}"'

            return props_string
        else:
            return None
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("missing value")
        else:
            if self.tag == None:
                return self.value
            else:
                if self.props_to_html() != None:
                    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
                else:
                    return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent Node has no tag")
        elif self.children == None:
            raise ValueError("Parent Node has no children")
        else:
            if self.props == None:
                html = f"<{self.tag}>"
            else:
                html = f"<{self.tag}{self.props_to_html()}"

            for child in self.children:
                html = html +child.to_html()

            html += f"</{self.tag}>"

            return html
        
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            node = LeafNode(None, text_node.text)
            return node

        case TextType.BOLD:
            node = LeafNode("b", text_node.text)
            return node

        case TextType.ITALIC:
            node = LeafNode("i", text_node.text)
            return node

        case TextType.CODE:
            node = LeafNode("code", text_node.text)
            return node

        case TextType.LINK:
            props = {"href": text_node.url}
            node = LeafNode("a", text_node.text, props)
            return node

        case TextType.IMAGE:
            props = {"src": text_node.url, "alt": text_node.text}
            node = LeafNode("img", "", props)
            return node

        case _:
            raise ValueError("invalid text type")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            split_string = node.text.split(delimiter)

            if len(split_string) % 2 == 0:
                raise Exception("invalid Mardown syntax")
            else:
                for i in range(0, len(split_string)):
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_string[i], TextType.NORMAL))
                    else:
                        new_nodes.append(TextNode(split_string[i], text_type))

    return new_nodes

def extract_markdown_images(text):
        alt_url = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return alt_url

def extract_markdown_links(text):
        links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return links

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
        else:
            original_text = node.text

            for image in images:
                image_alt = image[0]
                image_link = image[1]

                sections = original_text.split(f"![{image_alt}]({image_link})", 1)
                
                if sections[0] != "":
                    text_node = TextNode(sections[0], TextType.NORMAL)
                    new_nodes.append(text_node)

                image_node = TextNode(image_alt, TextType.IMAGE, image_link)
                new_nodes.append(image_node)

                original_text = sections[1]
            
            if original_text != "":
                final_node = TextNode(original_text, TextType.NORMAL)
                new_nodes.append(final_node)
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
        else:
            original_text = node.text

            for link in links:
                link_text = link[0]
                link_url = link[1]

                sections = original_text.split(f"[{link_text}]({link_url})", 1)
                
                if sections[0] != "":
                    text_node = TextNode(sections[0], TextType.NORMAL)
                    new_nodes.append(text_node)

                link_node = TextNode(link_text, TextType.LINK, link_url)
                new_nodes.append(link_node)

                original_text = sections[1]
            
            if original_text != "":
                final_node = TextNode(original_text, TextType.NORMAL)
                new_nodes.append(final_node)
    
    return new_nodes

def text_to_textnodes(text):
    # Put text in a textnode
    nodes = [
        TextNode(text, TextType.NORMAL)
    ]

    # Look for bold text
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # Look for italic text
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # Look for code text
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Look for images
    nodes = split_nodes_image(nodes)

    # Look for links
    nodes = split_nodes_link(nodes)

    # Return split nodes
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    #### THIS IS WHERE YOU ARE ######
    #print(f"Split Blocks: {blocks}")
    stripped = []

    for block in blocks:
        stripped.append(block.strip())

    #print(f"Stripped Blocks: {stripped}")

    return stripped

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    print(f"Blocks in markdown_to_html_node: {blocks}")

    children = []

    for block in blocks:
        print("#####\nLOOP BEGIN\n######")
        if (block == ""):
            continue

        block_type = block_to_block_type(block)
        print(f"Block Type: {block_type}")
        print(f"Block: {block}")
        
        match block_type:
            case BlockType.PARAGRAPH:
                block = block.replace('\n', ' ')
                node_children = text_to_children(block)
                node = ParentNode("p", node_children)
                children.append(node)
            case BlockType.HEADING:
                # What kind of heading?
                hashCount = block.count("#")

                # Remove hashes from block
                stripped = block.strip("#")
                stripped = stripped[1:]
                
                # Get node children
                node_children = text_to_children(stripped)

                # Make a heading node
                node = ParentNode(f"h{hashCount}", node_children)

                # Append with rest of children
                children.append(node)

            case BlockType.CODE:
                block = block.strip("`")
                block = block[1:]

                # Create a LeafNode with the text content
                text_node = LeafNode(None, block)
                
                # Put the text node in a list for the code tag
                code_node = ParentNode("code", [text_node])
                
                # Put the code node in a list for the pre tag
                node = ParentNode("pre", [code_node])

                children.append(node)
                
            case BlockType.QUOTE:
                block = block.replace('>', '')
                block = block.strip()
                node_children = text_to_children(block)
                node = ParentNode("blockquote", node_children)
                children.append(node)

            case BlockType.UNORDERED_LIST:
                block = block_to_list_items(block)
                node_children = text_to_children(block)
                node = ParentNode("ul", node_children)
                children.append(node)

            case BlockType.ORDERED_LIST:
                block = block_to_list_items(block)
                node_children = text_to_children(block)
                node = ParentNode("ol", node_children)
                children.append(node)

    main = ParentNode("div", children)
    print(f"Main: {main.to_html()}")
    return main

def block_to_list_items(block):
    lines = block.split("\n")
    new_block = ""

    for l in range(0, len(lines)):
        space_index = lines[l].find(" ")
        new_line = lines[l][space_index+1:]
        new_block += f"<li>{new_line}</li>\n" 
    
    return new_block
    

def text_to_children(text):
    text_children = text_to_textnodes(text)
    html_children = []

    for text_child in text_children:
        html_child = text_node_to_html_node(text_child)
        html_children.append(html_child)

    return html_children


def extract_title(markdown):
    lines = markdown.split('\n')

    for line in lines:
        if line[0:2] == "# ":
            return line.strip("# ")
        else:
            continue

    # If it's made it this far there's a problem
    raise ValueError("No Header")