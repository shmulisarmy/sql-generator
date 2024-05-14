"""
this package gives you the option to get any text colored

code sample:
print(blue("hello")) => blue hello string
same goes for grey, red, green, yellow, purple and violet
"""

grey = lambda text: f"\x1b[30m{text}\x1b[39m"
red = lambda text: f"\x1b[31m{text}\x1b[39m"
green = lambda text: f"\x1b[32m{text}\x1b[39m"
yellow = lambda text: f"\x1b[33m{text}\x1b[39m"
blue = lambda text: f"\x1b[34m{text}\x1b[39m"
purple = lambda text: f"\x1b[35m{text}\x1b[39m"
violet = lambda text: f"\x1b[36m{text}\x1b[39m"