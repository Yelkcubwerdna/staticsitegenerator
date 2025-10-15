from textnode import *
from enum import Enum
from copyDir import copyDir
from generatePage import generate_page, generate_pages_recursive
import sys

def main():
    
    try:
        basepath = sys.argv[1]
    except:
        basepath = "/"

    copyDir("./static", "./docs")

    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

main()