import os
import mel_parser


def main():
    prog = mel_parser.parse('''
        select col1 col2 col3
        from table
    ''')
    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()
