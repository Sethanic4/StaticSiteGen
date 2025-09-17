from textnode import TextNode, TextType
class HTMLNode():
    def __init__(self,tag:str = None,value:str = None,children:list = None,props:dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        prop_text = ""
        for k, v in self.props.items():
            prop_text += f' {k}="{v}"'
        return prop_text
    
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

class LeafNode(HTMLNode):
    def __init__(self,tag:str, value:str,props:dict = None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value == None:
            raise ValueError("No Value")
        if self.tag == None:
            return self.value
        if self.props == None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self,tag:str,children:list,props:dict = None):
        super().__init__(tag,None,children,props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag")
        if self.children == None:
            raise ValueError("No child")
        htmlstring = f'<{self.tag}'
        if self.props:
            htmlstring += f'{self.props_to_html()}'
        htmlstring += ">"
        for child in self.children:
            htmlstring += child.to_html()
        htmlstring += f"</{self.tag}>"
        return htmlstring
        
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img","",{"src":text_node.url,"alt":text_node.text})
        case _:
            raise Exception("Not valid text type")
