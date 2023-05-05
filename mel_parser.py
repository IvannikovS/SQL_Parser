import inspect
from contextlib import suppress

import pyparsing as pp
from pyparsing import pyparsing_common as ppc

from mel_ast import *


def _make_parser():
    num = ppc.fnumber
    ident = ppc.identifier | (pp.Literal('"').suppress() + ppc.identifier + pp.Literal('"').suppress()) | \
            (pp.Literal('"').suppress() + ppc.identifier + pp.Char('%').suppress() + pp.Literal('"').suppress())

    COMPARE = pp.oneOf(('=', '>', '<', '!=', '<>'))
    join_type = pp.oneOf(('inner', 'left', 'right', 'full', 'cross', 'natural'))
    BOOL = pp.oneOf(('and', 'or', 'between', 'in', 'like', 'not', 'is'))
    stmt = pp.Forward()

    group = ident + pp.Optional(pp.Char('.').suppress() + ident)
    cols = group + pp.ZeroOrMore(pp.Literal(',').suppress() + group)

    bool_op = pp.Forward()

    group_where = ident | num | pp.Literal('(').suppress() + bool_op + pp.Literal(')').suppress()

    compare = group_where + pp.Optional(COMPARE + group_where)
    bool_op << compare + pp.ZeroOrMore(BOOL + compare)

    select_ = pp.Group(pp.CaselessKeyword("select").suppress() + (pp.Char('*').suppress() | cols)).setName('select')
    from_ = pp.Group(pp.CaselessKeyword("from").suppress() + bool_op).setName('from')
    where_ = pp.Group(pp.CaselessKeyword("where").suppress() + bool_op).setName('where')
    group_by_ = pp.Group(pp.CaselessKeyword('group by').suppress() + cols).setName('group by')
    order_by_ = pp.Group(pp.CaselessKeyword('order by').suppress() + cols).setName('order by')
    having_ = pp.Group(pp.CaselessKeyword('having').suppress() + bool_op).setName('having')
    join_ = pp.Group(pp.CaselessKeyword("join").suppress() + group + pp.CaselessKeyword("on").suppress() + bool_op | group).setName('join')

    stmt_list = pp.Forward()
    stmt << (
            select_ | from_ | where_ | order_by_ | group_by_ | having_ | join_
    )

    stmt_list << pp.ZeroOrMore(stmt)
    program = stmt_list.ignore(pp.cStyleComment).ignore(pp.dblSlashComment) + pp.StringEnd()

    start = program

    def set_parse_action_magic(rule_name: str, parser: pp.ParserElement) -> None:
        if rule_name == rule_name.upper():
            return
        if rule_name in ('compare', 'bool_op', 'group by'):
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


def hello():
    print("Hello world!")
