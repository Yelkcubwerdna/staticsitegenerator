from textnode import *
from enum import Enum
from copyDir import copyDir
from generatePage import generate_page, generate_pages_recursive

def main():
    
    copyDir("./static", "./public")

    generate_pages_recursive("./content", "./template.html", "./public")

main()