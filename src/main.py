from textnode import *
from enum import Enum
from copyDir import copyDir
from generatePage import generate_page, generate_pages_recursive
import sys

def main():
    basepath = sys.argv[1]
    if basepath == "":
        basepath = "/"

    copyDir("./static", "./public")

    generate_pages_recursive("./content", "./template.html", basepath)

main()