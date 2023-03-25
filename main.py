import os
import mel_parser


def main():
    prog = mel_parser.parse('''
        select col1, col2, col3
        from table
        where col1 = 1 and col3 > 3
    ''')
    print(*prog.tree, sep=os.linesep)

print("AYE")

if __name__ == "__main__":
    main()
