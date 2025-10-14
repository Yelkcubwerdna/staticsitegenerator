import unittest
from blockType import BlockType, block_to_block_type
from htmlnode import markdown_to_html_node, markdown_to_blocks

class TestBlockType(unittest.TestCase):
    def test_heading1(self):
        block =  "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading2(self):
        block = "## This is a h2"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading3(self):
        block = "### This is a h3 heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading4(self):
        block = "#### This is a h4 heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading5(self):
        block = "##### This is a h5 heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading6(self):
        block = "###### This is a h6 heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading7(self):
        block = "####### H7 heading is not a thing"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_headingE(self):
        block = "###This is bad markdown"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_headingE2(self):
        block = "######This is also bad markdown"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_code(self):
        block = "```code```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_codeerror(self):
        block ="```Not code"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_coderror2(self):
        block = "Not code```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_singlequote(self):
        block = ">Testing"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_doublequote(self):
        block = ">First Line\n>Second Line"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_mixedlines(self):
        block = ">First Line\nNot a Quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_unorderedlist(self):
        block = "- First Item\n- Second Item\n- 3rd Item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_unorderedlistbad(self):
        block = "- First Item\nSecond item\n- 3rd Item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_orderedlist(self):
        block = "1. First Item\n2. Second Item\n3. Third Item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_orderedlistbad1(self):
        block = "1. FirstItem\nSecond Item\n3. Third Item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_orderedlistbad2(self):
        block = "1. FirstItem\n3. Second Item\n4. Third Item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_orderedlistbad3(self):
        block = "1. First Item\n2. Second Item\n3.Third Item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_orderedlistdoubledigit(self):
        block = "1. First Item\n2. Second Item\n3. Third Item\n4. Fourth Item\n5. Fifth Item\n6. Sixth Item\n7. Seventh Item\n8. Eighth Item\n9. Ninth Item\n10. Tenth Item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

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