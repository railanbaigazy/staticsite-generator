import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, markdown_to_blocks

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("a", "some link", None, {"href": "https://www.google.com", "target": "_blank"})
        expected_html = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_html)

    def test_no_props(self):
        node = HTMLNode("p", "some text")
        expected_html = ""
        self.assertEqual(node.props_to_html(), expected_html)

    def test_empty_props(self):
        node = HTMLNode("div", "some text", None, {})
        expected_html = ""
        self.assertEqual(node.props_to_html(), expected_html)

    def test_none_props(self):
        node = HTMLNode("span", "some text", None, None)
        expected_html = ""
        self.assertEqual(node.props_to_html(), expected_html)

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

    
    # Test markdown_to_blocks function
    def test_markdown_to_blocks(self):
        try:
            with open("src/test_markdowns/test_1.md", "r") as file:
                markdown = file.read()
            actual_blocks = markdown_to_blocks(markdown)
            expected_blocks = [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item"
            ]
            self.assertEqual(actual_blocks, expected_blocks)
        except FileNotFoundError:
            self.fail("test_markdown.md file not found")
        except Exception as e:
            self.fail(f"An error occurred: {e}")


if __name__ == "__main__":
    unittest.main()
