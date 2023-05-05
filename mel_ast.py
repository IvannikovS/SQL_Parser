from abc import ABC, abstractmethod
from typing import Callable, Tuple
from enum import Enum


class AstNode(ABC):
    @property
    def childs(self) -> Tuple['AstNode', ...]:
        return ()

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def tree(self) -> [str, ...]:
        res = [str(self)]
        childs = self.childs
        for i, child in enumerate(childs):
            ch0, ch = '├', '│'
            if i == len(childs) - 1:
                ch0, ch = '└', ' '
            res.extend(((ch0 if j == 0 else ch) + ' ' + s for j, s in enumerate(child.tree)))
        return res

    def visit(self, func: Callable[['AstNode'], None]) -> None:
        func(self)
        map(func, self.childs)

    def __getitem__(self, index):
        return self.childs[index] if index < len(self.childs) else None


class ExprNode(AstNode):
    pass


class NumNode(ExprNode):
    def __init__(self, num: float):
        super().__init__()
        self.num = float(num)

    def __str__(self) -> str:
        return str(self.num)


class IdentNode(ExprNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = str(name)

    def __str__(self) -> str:
        return str(self.name)


class BinOp(Enum):
    MORE = '>'
    LESS = '<'
    EQUALS = '='
    AND = 'and'
    OR = 'or'
    BETWEEN = 'between'
    IN = 'in'
    LIKE = 'like'
    NOT = 'not'
    IS = 'is'


class BinOpNode(ExprNode):
    def __init__(self, op: BinOp, arg1: ExprNode, arg2: ExprNode):
        super().__init__()
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    @property
    def childs(self) -> Tuple[ExprNode, ExprNode]:
        return self.arg1, self.arg2

    def __str__(self) -> str:
        return str(self.op.value)


class InputNode(AstNode):
    def __init__(self, var: IdentNode):
        self.var = var

    @property
    def childs(self) -> Tuple[IdentNode]:
        return self.var,

    def __str__(self) -> str:
        return 'input'


class OutputNode(AstNode):
    def __init__(self, arg: ExprNode):
        self.arg = arg

    @property
    def childs(self) -> Tuple[ExprNode]:
        return self.arg,

    def __str__(self) -> str:
        return 'output'


class StmtNode(AstNode):
    pass


class AssignNode(StmtNode):
    def __init__(self, var: IdentNode, val: ExprNode):
        super().__init__()
        self.var = var
        self.val = val

    @property
    def childs(self) -> Tuple[IdentNode, ExprNode]:
        return self.var, self.val

    def __str__(self) -> str:
        return '='


class SelectNode(StmtNode):
    def __init__(self, cond: ExprNode):
        super().__init__()
        self.cond = cond

    @property
    def childs(self) -> ExprNode:
        return self.cond

    def __str__(self) -> str:
        return 'select'


class FromNode(StmtNode):
    def __init__(self, cond: ExprNode):
        super().__init__()
        self.cond = cond

    @property
    def childs(self) -> ExprNode:
        return self.cond

    def __str__(self) -> str:
        return 'from'


class WhereNode(StmtNode):
    def __init__(self, cond: ExprNode):
        super().__init__()
        self.cond = cond

    @property
    def childs(self) -> ExprNode:
        return self.cond

    def __str__(self) -> str:
        return 'where'


class GroupByNode(StmtNode):
    def __init__(self, cond: ExprNode):
        super().__init__()
        self.cond = cond

    @property
    def childs(self) -> ExprNode:
        return self.cond

    def __str__(self) -> str:
        return 'group by'


class HavingNode(StmtNode):
    def __init__(self, cond: ExprNode):
        super().__init__()
        self.cond = cond

    @property
    def childs(self) -> ExprNode:
        return self.cond

    def __str__(self) -> str:
        return 'having'


class SortOrder(Enum):
    ASCENDING = 'asc'
    DESCENDING = 'desc'


class OrderByNode(StmtNode):
    def __init__(self, column: ExprNode):
        super().__init__()
        self.column = column

    @property
    def childs(self) -> ExprNode:
        return self.column

    def __str__(self) -> str:
        return 'order by'



class StmtListNode(AstNode):
    def __init__(self, *exprs: AstNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[AstNode]:
        return self.exprs

    def __str__(self) -> str:
        return '...'