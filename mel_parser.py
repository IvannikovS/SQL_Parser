from contextlib import suppress
import inspect

import pyparsing as pp
from pyparsing import pyparsing_common as ppc

from mel_ast import *


def _make_parser():
    num = ppc.fnumber
    ident = ppc.identifier

    COMPARE = pp.oneOf(('= > <'))
    BOOL = pp.oneOf(('and or'))

    stmt = pp.Forward()

    group = ident
    cols = group + pp.ZeroOrMore(pp.Literal((',')).suppress() + group)

    bool_op = pp.Forward()

    group_where = ident | num | pp.Literal('(').suppress() + bool_op + pp.Literal(')').suppress()
    compare = group_where + pp.Optional(COMPARE + group_where)
    bool_op << compare + pp.ZeroOrMore(BOOL + compare)

    select_ = pp.Group(pp.Keyword("select").suppress() + (pp.Char('*').suppress() | cols)).setName('select')
    from_ = pp.Group(pp.Keyword("from").suppress() + cols).setName('from')
    where_ = pp.Group(pp.Keyword("where").suppress() + bool_op).setName('where')
    stmt_list = pp.Forward()
    stmt << (
            select_ | from_ | where_
    )
    stmt_list << pp.ZeroOrMore(stmt)
    program = stmt_list.ignore(pp.cStyleComment).ignore(pp.dblSlashComment) + pp.StringEnd()

    start = program

    def set_parse_action_magic(rule_name: str, parser: pp.ParserElement) -> None:
        if rule_name == rule_name.upper():
            return
        if rule_name in ('compare', 'bool_op'):
            def bin_op_parse_action(s, loc, tocs):
                rn = rule_name
                node = tocs[0]
                for i in range(1, len(tocs) - 1, 2):
                    node = BinOpNode(BinOp(tocs[i]), node, tocs[i + 1])
                return node

            parser.setParseAction(bin_op_parse_action)
        else:
            cls = ''.join(x.capitalize() for x in rule_name.split('_')) + 'Node'
            with suppress(NameError):
                cls = eval(cls)
                if not inspect.isabstract(cls):
                    def parse_action(s, loc, tocs):
                        return cls(*tocs)

                    parser.setParseAction(parse_action)

    for var_name, value in locals().copy().items():
        if isinstance(value, pp.ParserElement):
            set_parse_action_magic(var_name, value)

    return start


parser = _make_parser()


def parse(prog: str) -> StmtListNode:
    return parser.parseString(str(prog))[0]
