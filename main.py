import os

import mel_parser


def main():
    prog = mel_parser.parse('''
        SELECT col3, col4, tab4
        FROM table JOIN table7 ON col3 = col4 
        WHERE col3 > 10
        GROUP BY col4
        HAVING col4 like "_hi" ( SELECT * FROM col3 WHERE col4 > 10 )
    ''')

    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()
