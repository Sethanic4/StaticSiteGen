from textnode import TextNode,TextType
from htmlnode import *
from enum import Enum
import re
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown")
        for i in range(len(sections)):
            if sections[i] =="":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i],TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = re.split(r"(!\[.*?\]\(.*?\))",old_node.text)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown")
        for i in range(len(sections)):
            if sections[i] =="":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i],TextType.TEXT))
            else:
                linktext = re.findall(r"!\[(.*?)\]",sections[i])
                link = re.findall(r"\((.*?)\)",sections[i])
                split_nodes.append(TextNode(linktext[0], TextType.IMAGE,link[0]))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = re.split(r"(\[.*?\]\(.*?\))",old_node.text)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown")
        for i in range(len(sections)):
            if sections[i] =="":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i],TextType.TEXT))
            else:
                linktext = re.findall(r"\[(.*?)\]",sections[i])
                link = re.findall(r"\((.*?)\)",sections[i])
                split_nodes.append(TextNode(linktext[0], TextType.LINK,link[0]))
        new_nodes.extend(split_nodes)
    return new_nodes

def text_to_textnodes(text):
    new_nodes = TextNode(text,TextType.TEXT)
    new_nodes = split_nodes_delimiter([new_nodes],"**",TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes,"_",TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes,"`",TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    all_blocks = re.split(r"(```.*?```)", markdown.strip(), flags=re.DOTALL)
    new_markdown = []
    for block in all_blocks:
        if not block.strip():
            continue
        if block.startswith("```"):
            new_markdown.append(block)
        else:
            plain_blocks = block.strip().split("\n\n")
            for p in plain_blocks:
                if p.strip():
                    new_markdown.append(p.strip())
    return new_markdown
'''              
    for n in new_markdown:
        if len(n.split("\n")) > 1:
            singlines = n.split("\n")
            n = []
            for line in singlines:
                line = line.strip()
                n.append(line + "\n")
            n = "".join(n)
        if n !="":
            new_markdown2.append(n.strip())
            continue
'''

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    block_type = None
    if re.match(r"^#{1,6} ",block):
        return BlockType.HEADING
    if re.match(r"^```.*?```$", block, re.DOTALL):
        return BlockType.CODE
    list_length = len(block.split("\n"))
    if list_length > 1:
        lines = block.split("\n")
        quote = 0
        unordered_list = 0
        ordered_list = 0
        for line in lines:
            if re.match("^>",line):
                block_type = BlockType.QUOTE
                quote += 1
            if re.match("^- ",line):
                block_type = BlockType.UNORDERED_LIST
                unordered_list += 1
            if re.match("^\d+. ",line):
                block_type = BlockType.ORDERED_LIST
                ordered_list += 1
        if (quote != list_length and quote != 0) or (unordered_list != list_length and unordered_list != 0) or (ordered_list != list_length and ordered_list != 0):
            block_type = None
    if block_type == None:
        block_type = BlockType.PARAGRAPH
    return block_type

def text_to_children(s: str):
    return [text_node_to_html_node(tn) for tn in text_to_textnodes(s)]

def markdown_to_html_node(markdown):
    blocks= []
    for block in markdown_to_blocks(markdown):
        content = ""
        num = 0
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
               clean_block = block.replace("\n", " ")
               blocks.append(ParentNode("p",children=text_to_children(clean_block)))
            case BlockType.HEADING:
                match = re.match(r"^(#{1,6})\s+(.*)$",block)
                num = len(match.group(1))
                content = match.group(2)
                blocks.append(ParentNode(f"h{num}",children=text_to_children(content)))
            case BlockType.CODE:
                inner = block.strip('`').lstrip("\n").rstrip("\n")
                code = LeafNode("code", inner + "\n")
                blocks.append(ParentNode("pre", [code]))
            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                nblock = []
                for line in lines:
                    match = re.match(r"^\d+\.\s+(.*)$",line)
                    nblock.append(ParentNode("li",children=text_to_children(match.group(1))))
                blocks.append(ParentNode("ol",nblock))
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                nblock = []
                for line in lines:
                    match = re.match(r"^- (.+)$",line)
                    nblock.append(ParentNode("li",children=text_to_children(match.group(1))))
                blocks.append(ParentNode("ul",nblock))
            case BlockType.QUOTE:
                nblock = []
                lines = block.split("\n")
                for line in lines:
                    nblock.extend(text_to_children(line.lstrip('>').lstrip()))
                if nblock:
                    blocks.append(ParentNode("blockquote",nblock))

    root = ParentNode("div",blocks)
    return root

def extract_title(markdown):
    head_block = None
    for block in markdown_to_blocks(markdown):
        if block_to_block_type(block) == BlockType.HEADING:
            match = re.match(r"^(#{1,6})\s+(.*)$",block)
            head_block = match.group(2)
    if head_block == None:
        raise ValueError("No Title")
    return ""