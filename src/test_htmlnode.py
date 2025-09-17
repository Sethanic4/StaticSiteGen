import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("href","paragraph/URL",["obj1","obj2"],{"href": "www.google.com","body_color": "AABBCC"})  
        self.assertEqual(isinstance(node.props_to_html(),str), True)

    def test_noteq(self):
        node = HTMLNode("href",["obj1","obj2"],{"href": "www.google.com","body_color": "AABBCC"})
        self.assertNotEqual(node.tag, node.value)

    def test_urldefault(self):
        node = HTMLNode()
        self.assertEqual(node.props, node.value)

    def test_leafnode(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leafnode2(self):
        node = LeafNode("a","link here",{"href": "www.google.com","body_color": "AABBCC"})
        self.assertEqual(node.to_html(), '<a href="www.google.com" body_color="AABBCC">link here</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)

    def test_to_html_with_boots(self):
        # Define the nodes
        title_node = LeafNode("h1", "Title")
        bold_node = LeafNode("b", "bold")
        text_node1 = LeafNode(None, "Some ")
        text_node2 = LeafNode(None, " text")
        paragraph_node = ParentNode("p", [text_node1, bold_node, text_node2])
        div_node = ParentNode("div", [title_node, paragraph_node])
        self.assertEqual(div_node.to_html(),"<div><h1>Title</h1><p>Some <b>bold</b> text</p></div>")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_image(self):
        node = TextNode("Alternate text", TextType.IMAGE,"www.google.com")  
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src":"www.google.com","alt":"Alternate text"})    

if __name__ == "__main__":
    unittest.main()