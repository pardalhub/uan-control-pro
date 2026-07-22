from models import db, Produto, Lote, Movimentacao


def registrar_saida(
    produto_id,
    quantidade,
    responsavel,
    observacao
):

    produto = Produto.query.get(produto_id)

    if produto is None:
        raise Exception("Produto não encontrado.")

    if produto.estoque_atual < quantidade:
        raise Exception("Estoque insuficiente.")

    restante = quantidade

    lotes = (
        Lote.query
        .filter(
            Lote.produto_id == produto_id,
            Lote.quantidade > 0
        )
        .order_by(Lote.validade)
        .all()
    )

    for lote in lotes:

        if restante <= 0:
            break

        retirar = min(lote.quantidade, restante)

        lote.quantidade -= retirar

        restante -= retirar

        movimentacao = Movimentacao(

            produto_id=produto.id,

            tipo="SAIDA",

            quantidade=retirar,

            responsavel=responsavel,

            observacao=observacao,

            lote=lote.lote,

            validade=lote.validade

        )

        db.session.add(movimentacao)

    produto.estoque_atual -= quantidade

    db.session.commit()

    return True