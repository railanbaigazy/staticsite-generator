import unittest
from htmlnode import (
    HTMLNode, LeafNode, ParentNode, 
    BlockTypes, 
    markdown_to_blocks, block_to_block_type, markdown_to_html_node
)

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

    
    # Test block_to_block_type function
    def test_block_to_paragraph_type(self):
        block = "A simple paragraph"
        actual_type = block_to_block_type(block)
        expected_type = BlockTypes.PARAGRAPH
        self.assertEqual(actual_type, expected_type)

    def test_block_to_heading_type(self):
        block = "## Heading"
        actual_type = block_to_block_type(block)
        expected_type = BlockTypes.HEADING
        self.assertEqual(actual_type, expected_type)

    def test_block_to_code_type(self):
        block = "```Code```"
        actual_type = block_to_block_type(block)
        expected_type = BlockTypes.CODE
        self.assertEqual(actual_type, expected_type)
    
    def test_block_to_quote_type(self):
        block = ">It is a quote\n>That says something cool\n>by Someone"
        actual_type = block_to_block_type(block)
        expected_type = BlockTypes.QUOTE
        self.assertEqual(actual_type, expected_type)

    def test_block_to_ul_type_stars(self):
        block = "* Item 1\n* Item 2"
        actual_type = block_to_block_type(block)
        expected_type = BlockTypes.UL
        self.assertEqual(actual_type, expected_type)

    def test_block_to_ul_type_dash(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        actual_type = block_to_block_type(block)
        expected_type = BlockTypes.UL
        self.assertEqual(actual_type, expected_type)

    def test_block_to_ol_type(self):
        block = "1. Item\n2. Second\n3. Third"
        actual_type = block_to_block_type(block)
        expected_type = BlockTypes.OL
        self.assertEqual(actual_type, expected_type)
        
    def test_block_to_not_ol_type(self):
        block = "1. Item\n3. Second\n2. Third"
        actual_type = block_to_block_type(block)
        expected_type = BlockTypes.PARAGRAPH
        self.assertEqual(actual_type, expected_type)

    
    # Test markdown_to_html_node function
    def test_heading_conversion(self):
        markdown = "# Heading 1\n## Heading 2\n### Heading 3"
        html_node = markdown_to_html_node(markdown)
        expected_html = "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_code_conversion(self):
        markdown = "```\nprint('Hello, world!')\n```"
        html_node = markdown_to_html_node(markdown)
        expected_html = "<div><pre><code>print('Hello, world!')</code></pre></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_quote_conversion(self):
        markdown = "> This is a quote\n> Second line of the quote"
        html_node = markdown_to_html_node(markdown)
        expected_html = "<div><blockquote><p>This is a quote</p><p>Second line of the quote</p></blockquote></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_unordered_list_conversion(self):
        markdown = "* Item 1\n* Item 2\n* Item 3"
        html_node = markdown_to_html_node(markdown)
        expected_html = "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_ordered_list_conversion(self):
        markdown = "1. First item\n2. Second item\n3. Third item"
        html_node = markdown_to_html_node(markdown)
        expected_html = "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_paragraph_conversion(self):
        markdown = "This is a paragraph.\n\nThis is another paragraph."
        html_node = markdown_to_html_node(markdown)
        expected_html = "<div><p>This is a paragraph.</p><p>This is another paragraph.</p></div>"
        self.assertEqual(html_node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()
