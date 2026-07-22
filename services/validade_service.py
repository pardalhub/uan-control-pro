from datetime import date, timedelta
from models import Lote


def listar_validade():

    hoje = date.today()

    sete_dias = hoje + timedelta(days=7)

    vencidos = (
        Lote.query
        .filter(Lote.validade < hoje)
        .order_by(Lote.validade)
        .all()
    )

    proximos = (
        Lote.query
        .filter(
            Lote.validade >= hoje,
            Lote.validade <= sete_dias
        )
        .order_by(Lote.validade)
        .all()
    )

    return vencidos, proximos