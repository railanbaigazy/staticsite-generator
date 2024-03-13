import unittest

from textnode import TextNode, TextTypes, split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_type(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_not_eq_none_url(self):
        node = TextNode("This is a text node", "bold", "url")
        node2 = TextNode("This is a text node", "bold", url=None)
        self.assertNotEqual(node, node2)

    def test_eq_same_url(self):
        node = TextNode("This is a text node", "bold", "https://example.com")
        node2 = TextNode("This is a text node", "bold", "https://example.com")
        self.assertEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("This is a text node", "bold", "https://example.com")
        node2 = TextNode("This is a text node", "bold", "https://different-example.com")
        self.assertNotEqual(node, node2)
    

    def test_split_single_node(self):
        node = TextNode("This is text with a `code block` word", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextTypes.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextTypes.TEXT),
            TextNode("code block", TextTypes.CODE),
            TextNode(" word", TextTypes.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_no_text_nodes(self):
        node1 = TextNode("This is text", TextTypes.BOLD)
        node2 = TextNode("with a `code block`", TextTypes.ITALIC)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextTypes.CODE)
        expected_nodes = [node1, node2]
        self.assertEqual(new_nodes, expected_nodes)

    def test_empty_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "", TextTypes.CODE)
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_delimiters(self):
        node = TextNode("This is text with a `code block` and *italic* word", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextTypes.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextTypes.TEXT),
            TextNode("code block", TextTypes.CODE),
            TextNode(" and *italic* word", TextTypes.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_no_matching_delimiter(self):
        node = TextNode("This is text with a `code block word", TextTypes.TEXT)
        try:
            split_nodes_delimiter([node], "`", TextTypes.CODE)
        except ValueError as e:
            self.assertEqual(str(e), "No matching closing delimiter")
        else:
            self.fail("Expected ValueError not raised")


    # Test extract_markdown_images function
    def test_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        expected_result = [("image", "https://i.imgur.com/zjjcJKZ.png"), ("another", "https://i.imgur.com/dfsdkjfd.png")]
        actual_result = extract_markdown_images(text)
        self.assertEqual(expected_result, actual_result)


    # Test extract_markdown_links function
    def test_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected_result = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        actual_result = extract_markdown_links(text)
        self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()
