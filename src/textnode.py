from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
"""
**Bold text**
_Italic text_
`Code text`
Links, in this format: [anchor text](url)
Images, in this format: ![alt text](url)
"""

class TextNode():
    def __init__(self,text, text_type:TextType,url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self,node2):
        if self.text == node2.text and self.text_type == node2.text_type and self.url == node2.url:
            return True
        else:
            return False
    
    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.value},{self.url})"