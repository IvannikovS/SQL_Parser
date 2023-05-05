import os

import mel_parser


def main():
    prog = mel_parser.parse('''
        SELECT col3 , col4, tab4
        FROM table1
        WHERE table1 = 10 or col3 > 10
        GROUP BY col1
        HAVING col2 like "_like%"
    ''')

    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()
