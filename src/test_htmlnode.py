import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, markdown_to_html_node, extract_title

class TestHTMLNode(unittest.TestCase):
    def test_default(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_propstohtml(self):
        node = HTMLNode("p", "Google", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_emptyprops(self):
        node = HTMLNode("p", "Google")
        self.assertEqual(node.props_to_html(), None)

    def test_leafnodenovalue(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_leafnodenotag(self):
        node = LeafNode(None, "This is untagged text.")
        self.assertEqual(node.to_html(), "This is untagged text.")

    def test_leafnodetagandvalue(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leafnodetagvalueandprops(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_parentnodebootdevexample(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parentnodenotag(self):
        node = ParentNode(None, [LeafNode(None, "Normal Text")])
        self.assertRaises(ValueError, node.to_html)

    def test_parentnodenochildren(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_parentnodenestmageddon(self):
        node = ParentNode(
            "p",
            [
                ParentNode("h1", [LeafNode("p", "TextyText")]),
                ParentNode("p",
                           [
                               ParentNode("i", [
                                   LeafNode("b", "AAAAAAAA")
                               ]),
                               LeafNode("i", "Wow")
                           ]),
                LeafNode(None, "I'm just a baby!")
            ]
        )
        self.assertEqual(node.to_html(), "<p><h1><p>TextyText</p></h1><p><i><b>AAAAAAAA</b></i><i>Wow</i></p>I'm just a baby!</p>")

    def test_normaltexttohtmlnode(self):
        text_node = TextNode("This is normal text.", TextType.NORMAL)
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), "This is normal text.")

    def test_boldtexttohtmlnode(self):
        text_node = TextNode("This is bold text!", TextType.BOLD)
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), "<b>This is bold text!</b>")

    def test_italictexttohtmlnode(self):
        text_node = TextNode("This is italic text?", TextType.ITALIC)
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), "<i>This is italic text?</i>")

    def test_codetexttohtmlnode(self):
        text_node = TextNode("print(This is code text.)", TextType.CODE)
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), "<code>print(This is code text.)</code>")

    def test_linktohtmlnode(self):
        text_node = TextNode("Google it!", TextType.LINK, "https://www.google.com")
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Google it!</a>')

    def test_imagetohtmlnode(self):
        text_node = TextNode("A cute kitten in grass", TextType.IMAGE, "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Stray_kitten_Rambo002.jpg/1200px-Stray_kitten_Rambo002.jpg")
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Stray_kitten_Rambo002.jpg/1200px-Stray_kitten_Rambo002.jpg" alt="A cute kitten in grass"></img>')

    def test_invalidtexttypetohtmlnode(self):
        text_node = TextNode("This shouldn't work", "Normal Text")
        self.assertRaises(ValueError, text_node_to_html_node, text_node)

    def test_givensplitnodeexamp(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
            ])
        
    def test_splitdelimitnotnormaltext(self):
        node = TextNode("This is **bold** text.", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is **bold** text.", TextType.BOLD)])

    def test_splitdelimitbadmarkdown(self):
        node = TextNode("This is **bad* markdown text.", TextType.NORMAL)
        self.assertRaises(Exception, split_nodes_delimiter, ([node], "**", TextType.BOLD))

    def test_splitdelimitboldtwice(self):
        node = TextNode("**Wow!** That's **bold** text!", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("", TextType.NORMAL),
            TextNode("Wow!", TextType.BOLD),
            TextNode(" That's ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text!", TextType.NORMAL)])
        
    def test_splitdelimititalic(self):
        node = TextNode("This is *italic* text.", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.NORMAL)
        ])

    def test_extractimage(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])

    def test_extractimagebadmd(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and !(https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_extractlinks(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extractlinksbadmd(self):
        text = "This is text with a link (https://www.boot.dev) and [to youtube]"
        self.assertEqual(extract_markdown_links(text), [])

    def test_splitnodeimage(self):
        node = TextNode("This is an image ![rick_roll](https://i.imgur.com/aKaOqIh.gif)!", TextType.NORMAL)
        expected = [
            TextNode("This is an image ", TextType.NORMAL),
            TextNode("rick_roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("!", TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_splitnodeimagestart(self):
        node = TextNode("![rick_roll](https://i.imgur.com/aKaOqIh.gif) This is an image!", TextType.NORMAL)
        expected = [
            TextNode("rick_roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" This is an image!", TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_splitnodeimageend(self):
        node = TextNode("This is an image! ![rick_roll](https://i.imgur.com/aKaOqIh.gif)", TextType.NORMAL)
        expected = [
            TextNode("This is an image! ", TextType.NORMAL),
            TextNode("rick_roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_splitnodeimagenone(self):
        node = TextNode("This is no image!", TextType.NORMAL)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_splitnodeimagemulti(self):
        nodes = [
            TextNode("This is an image ![rick_roll](https://i.imgur.com/aKaOqIh.gif)!", TextType.NORMAL),
            TextNode("![rick_roll](https://i.imgur.com/aKaOqIh.gif) This is an image!", TextType.NORMAL),
            TextNode("This is an image! ![rick_roll](https://i.imgur.com/aKaOqIh.gif)", TextType.NORMAL),
            TextNode("This is no image!", TextType.NORMAL)
        ]
        expected = [
            TextNode("This is an image ", TextType.NORMAL),
            TextNode("rick_roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("!", TextType.NORMAL),
            TextNode("rick_roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" This is an image!", TextType.NORMAL),
            TextNode("This is an image! ", TextType.NORMAL),
            TextNode("rick_roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("This is no image!", TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_splitnodelinkexam(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL
        )
        expected = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            )
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_splitnodelinkfront(self):
        node = TextNode(
            "[Boot dev](https://www.boot.dev) is a website.",
            TextType.NORMAL
        )
        expected = [
            TextNode("Boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" is a website.", TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_splitnodelinkbadmd(self):
        node = TextNode(
            "Boot dev(https://www.boot.dev) is a website.",
            TextType.NORMAL
        )
        self.assertEqual(split_nodes_link([node]), [node])

    def test_texttonodeexample(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
     )    
        
    def test_markdown_to_blocks_2(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ]
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headingblock(self):
        md = """
### This is a heading 3 heading"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading 3 heading</h3></div>"
        )

    def test_quoteblock(self):
        md = """
>This is a quote!"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote!</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- Ichi
- Ni
- San"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Ichi</li>\n<li>Ni</li>\n<li>San</li>\n</ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. Play video games
2. ?????
3. Profit"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Play video games</li>\n<li>?????</li>\n<li>Profit</li>\n</ol></div>"
        )

    def test_extract_title(self):
        self.assertEqual("Hello", extract_title("# Hello"))

    def test_extract_title_no_header(self):
        self.assertRaises(ValueError, extract_title, "## Hello")

    def test_extract_title_end(self):
        md = """
<!-- Empty Space -->
### Not the Title
# Hello"""
        self.assertEqual("Hello", extract_title(md))
