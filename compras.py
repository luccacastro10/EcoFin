class compras:
    def __init__(self, valor, loja, data):
        self._valor = valor
        self._loja = loja
        self._data = data

    def treeView(self, tv):
        values = [self._valor, self._loja, self._data]
        tv.insert("", "end", values=values)
    