from printer import Printer
from table import Table
from context import Context
from csv_table import CsvTable

table = Table("users", ['id', 'name'])
table.add_row(['1', 'Sergey'])
table.add_row(['2', 'Misha'])

table2 = Table("users2", ['id', 'name'])
table2.add_row(['1', 'Sergey'])
table2.add_row(['2', 'Misha'])

table3 = Table("test", ['id'])
table3.add_row('1')

Printer.print_table(table)
Printer.print_new_line()

Printer.print_table(table2)
Printer.print_new_line()

Printer.print_table(table3)
Printer.print_new_line()

Printer.print_message(table3.single_value())
Printer.print_new_line()

context = Context()

context.add_table(table)
context.add_table(table2)

join_table = context.join('merge')

Printer.print_table(join_table)
Printer.print_new_line()

Printer.print_message(context.get_count())
Printer.print_new_line()

context.remove('users')

Printer.print_message(context.get_count())
Printer.print_new_line()

csv_table = CsvTable('csv', 'resources/data1.csv')

Printer.print_table(csv_table)
Printer.print_new_line()

context.add_table(csv_table)
Printer.print_table(context.join('merge2'))
