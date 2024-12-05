import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting","href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            'class="greeting"href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )
class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")

    def test_to_html_with_tag(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_without_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_empty_value(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_to_html_with_none_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_zero_value(self):
        node = LeafNode("p", 0)
        with self.assertRaises(ValueError):
            node.to_html()


class TestParentNode(unittest.TestCase):
    def test_init(self):
        node = ParentNode("p", [LeafNode("b", "Bold text")])
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.children, [LeafNode("b", "Bold text")])
        self.assertIsNone(node.value)

    def test_init_with_props(self):
        node = ParentNode("p", [LeafNode("b", "Bold text")], props={"class": "container"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.children, [LeafNode("b", "Bold text")])
        self.assertEqual(node.props, {"class": "container"})

    def test_to_html(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")])
        expected_html = "<p><b>Bold text</b>Normal text</p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_props(self):
        node = ParentNode("p", [LeafNode("b", "Bold text")], props={"class": "container"})
        expected_html = '<p class="container"><b>Bold text</b></p>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_empty_children(self):
        node = ParentNode("p", [])
        expected_html = "<p></p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_init_raises_error_if_tag_is_none(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("b", "Bold text")])

    def test_init_raises_error_if_tag_is_empty(self):
        with self.assertRaises(ValueError):
            ParentNode("", [LeafNode("b", "Bold text")])

    def test_init_raises_error_if_children_is_none(self):
        with self.assertRaises(ValueError):
            ParentNode("p", None)





if __name__ == "__main__":
    unittest.main()
