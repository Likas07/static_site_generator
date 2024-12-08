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
    """Test suite for ParentNode class"""

    # Initialization Tests
    def test_basic_initialization(self):
        """Test basic initialization with required parameters"""
        node = ParentNode("div", [LeafNode("p", "text")])
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        self.assertIsNone(node.value)
        self.assertIsNone(node.props)

    def test_initialization_with_props(self):
        """Test initialization with props"""
        props = {"class": "container", "id": "main"}
        node = ParentNode("div", [LeafNode("p", "text")], props=props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.props, props)

    def test_initialization_preserves_children_order(self):
        """Test that children maintain their order"""
        children = [
            LeafNode("p", "first"),
            LeafNode("p", "second"),
            LeafNode("p", "third")
        ]
        node = ParentNode("div", children)
        self.assertEqual(node.children, children)

    # Validation Tests - Tag
    def test_none_tag_raises_error(self):
        """Test that None tag raises ValueError"""
        with self.assertRaisesRegex(ValueError, "Tag cannot be empty"):
            ParentNode(None, [LeafNode("p", "text")])

    def test_empty_tag_raises_error(self):
        """Test that empty string tag raises ValueError"""
        with self.assertRaisesRegex(ValueError, "Tag cannot be empty"):
            ParentNode("", [LeafNode("p", "text")])

    # Validation Tests - Children
    def test_none_children_raises_error(self):
        """Test that None children raises ValueError"""
        with self.assertRaisesRegex(ValueError, "Children cannot be empty"):
            ParentNode("div", None)

    def test_empty_children_list_raises_error_in_to_html(self):
        """Test that empty children list raises ValueError in to_html"""
        node = ParentNode("div", [])
        with self.assertRaisesRegex(ValueError, "Children cannot be empty"):
            node.to_html()

    def test_invalid_child_type_raises_error(self):
        """Test that non-HTMLNode children raise ValueError"""
        node = ParentNode("div", ["not a node"])
        with self.assertRaisesRegex(ValueError, "Children must be of type HTMLNode"):
            node.to_html()

    # HTML Generation Tests - Basic
    def test_basic_html_generation(self):
        """Test basic HTML generation with single child"""
        node = ParentNode("div", [LeafNode("p", "text")])
        expected = "<div><p>text</p></div>"
        self.assertEqual(node.to_html(), expected)

    def test_html_generation_with_props(self):
        """Test HTML generation with properties"""
        node = ParentNode(
            "div",
            [LeafNode("p", "text")],
            props={"class": "container", "id": "main"}
        )
        expected = '<div class="container" id="main"><p>text</p></div>'
        self.assertEqual(node.to_html(), expected)

    # HTML Generation Tests - Complex
    def test_multiple_children_html_generation(self):
        """Test HTML generation with multiple children"""
        node = ParentNode("div", [
            LeafNode("p", "first"),
            LeafNode("span", "second"),
            LeafNode(None, "text"),
            LeafNode("b", "bold")
        ])
        expected = "<div><p>first</p><span>second</span>text<b>bold</b></div>"
        self.assertEqual(node.to_html(), expected)

    def test_nested_nodes_html_generation(self):
        """Test HTML generation with nested ParentNodes"""
        node = ParentNode("section", [
            ParentNode("div", [
                LeafNode("p", "text")
            ])
        ])
        expected = "<section><div><p>text</p></div></section>"
        self.assertEqual(node.to_html(), expected)

    def test_deep_nesting_html_generation(self):
        """Test HTML generation with deep nesting"""
        node = ParentNode("main", [
            ParentNode("section", [
                ParentNode("article", [
                    ParentNode("div", [
                        LeafNode("p", "deep")
                    ])
                ])
            ])
        ])
        expected = "<main><section><article><div><p>deep</p></div></article></section></main>"
        self.assertEqual(node.to_html(), expected)

    def test_mixed_content_html_generation(self):
        """Test HTML generation with mixed content types"""
        node = ParentNode("div", [
            LeafNode(None, "text"),
            ParentNode("p", [LeafNode("b", "bold")]),
            LeafNode("i", "italic"),
            ParentNode("span", [LeafNode(None, "more")])
        ])
        expected = "<div>text<p><b>bold</b></p><i>italic</i><span>more</span></div>"
        self.assertEqual(node.to_html(), expected)

    # Edge Cases
    def test_special_characters_in_props(self):
        """Test handling of special characters in props"""
        node = ParentNode(
            "div",
            [LeafNode("p", "text")],
            props={"data-test": "hello & goodbye", "class": "a < b > c"}
        )
        expected = '<div data-test="hello & goodbye" class="a < b > c"><p>text</p></div>'
        self.assertEqual(node.to_html(), expected)

    def test_special_characters_in_content(self):
        """Test handling of special characters in content"""
        node = ParentNode("div", [
            LeafNode("p", "Hello & goodbye < > \" '")
        ])
        expected = '<div><p>Hello & goodbye < > " \'</p></div>'
        self.assertEqual(node.to_html(), expected)





if __name__ == "__main__":
    unittest.main()
