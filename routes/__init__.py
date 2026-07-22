from flask import Blueprint

main = Blueprint(
    "main",
    __name__
)

from . import dashboard
from . import produtos
from . import movimentacoes
from . import compras
from . import entrada
from . import saida
from . import validade