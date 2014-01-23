


class Cell:
    def __init__(self, text, row, **kwargs):
        self.text = text
        self.row = row

class Row:
    def __init__(self, table, **kwargs):
        self.cells = []
        self.table = table

    def cell(self, data, **kwargs):
        self.cells.append(Cell(data, self, **kwargs))
        return self

class Table:
    def __init__(self):
        self.rows = []

    def row(self, **kwargs):
        r = Row(self, **kwargs)
        self.rows.append(r)
        return r


t = Table()
t.row().cell('cell1').cell('cell2')
t.row().cell('cell3').cell('cell4')


#-----------------------
def dicts2tex(dicts, filepath):
    def totexrow(dlist):
        return ' & '.join((str(item) for item in dlist))

    with open(filepath, 'w') as f:
        f.write('%s\\\\\n' % totexrow(dicts[0].keys()))
        for d in dicts:
            f.write('%s\\\\\n' % totexrow(d.values()))

