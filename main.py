import os

import mel_parser


def main():
    prog = mel_parser.parse('''
        SELECT col3, col4, tab4
        FROM table
        JOIN table5 ON col4 = col5
        WHERE col3 > 10 and col5 not NULL 
        GROUP BY col4
        HAVING col4 like "_hi"
        
    ''')

    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()
