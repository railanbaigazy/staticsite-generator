import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
