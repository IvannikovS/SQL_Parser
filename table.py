class Table:
    def __init__(self, name, columns):
        self.name = name
        self._cols = [col for col in columns]
        self._rows = []

    @property
    def columns(self):
        return self._cols

    @property
    def rows(self):
        for row in self._rows:
            yield {self._cols[i]: row[i] for i in range(self.col_count)}

    @property
    def col_count(self):
        return len(self._cols)

    @property
    def row_count(self):
        return len(self._rows)

    def add_row(self, row):
        if len(row) != self.col_count:
            raise Exception("Row doesn't match table attributes")
        self._rows.append(row)

    def add_rows(self, rows):
        for row in rows:
            self.add_row(row)

    def drop(self):
        self._rows = []
        self._cols = []

    def has_column(self, column):
        return column in self.columns

    def get_column(self, column):
        if not self.has_column(column):
            raise Exception('Table has no column with name "{}"'.format(column))
        return [row[column] for row in self.rows]

    def single_value(self):
        if self.row_count == 1 and self.col_count == 1:
            return self.get_column(self._cols[0])
        else:
            raise Exception('Table is not single')
