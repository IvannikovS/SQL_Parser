from table import Table
from join_table import JoinTable


class Context:
    def __init__(self):
        self._tables = {}

    def clear(self):
        self._tables.clear()

    def add_table(self, table: Table, alias=None):
        table_id = alias if alias else table.name
        if not table_id:
            table_id = 't' + str(len(self._tables) + 1)
        self._tables[table_id] = table
        return table_id

    def get_table_name(self, alias: str):
        if alias in self._tables.keys():
            return self._tables[alias]
        else:
            raise Exception(f'Not found table with {alias}')

    def join(self, name: str):
        columns_join = []
        for table in self._tables.values():
            for col in table.columns:
                columns_join.append(table.name + '.' + col)

        return JoinTable(list(self._tables.values()), name, columns_join)

    def remove(self, alias: str):
        if alias in self._tables.keys():
            del self._tables[alias]

    def get_count(self):
        return len(self._tables)
