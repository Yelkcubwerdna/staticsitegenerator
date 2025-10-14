from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    
    block = block.strip()

    # Check if it is a heading
    if (block[0] == "#"):
        # Split up string
        split = block.split(" ")

        # Get length of first split string
        first_len = len(split[0])

        # If it's a length of 6 or lower, it could be a heading
        if (first_len <= 6):
            # Check if all the characters are '#'
            all_hash = True

            for char in split[0]:
                if char != '#':
                    all_hash = False

            if all_hash == True:
                return BlockType.HEADING
    
    # Check if it's a code block, first 3 characters must be backticks
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    
    # Check if it's a quote block
    if block[0] == ">":
        lines = block.split("\n")
        quote = True

        for line in lines:
            if line[0] != ">":
                quote = False
        
        if quote == True:
            return BlockType.QUOTE

    # Check if it's an unordered list
    if block[0:2] == "- ":
        lines = block.split("\n")
        ul = True

        for line in lines:
            if line[0:2] != "- ":
                ul = False

        if ul == True:
            return BlockType.UNORDERED_LIST
        
    # Check if it's an ordered list
    if block[0:3] == "1. ":
        lines = block.split("\n")
        ol = True
        count = 1

        for line in lines:
            split = line.split(". ", 1)

            if len(split) == 1:
                ol = False
                break
            elif int(split[0]) != count:
                ol = False
                break
            else:
                count += 1

        if ol == True:
            return BlockType.ORDERED_LIST


    # If nothing fits, it's a paragraph
    return BlockType.PARAGRAPH