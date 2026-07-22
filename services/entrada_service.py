from models import db, Produto, Lote, Movimentacao


def registrar_entrada(
    produto_id,
    quantidade,
    lote,
    validade,
    fornecedor,
    nota_fiscal,
    valor_unitario,
    responsavel,
    observacao
):

    produto = Produto.query.get(produto_id)

    if produto is None:
        raise Exception("Produto não encontrado.")

    novo_lote = Lote(
        produto_id=produto.id,
        lote=lote,
        quantidade=quantidade,
        validade=validade,
        fornecedor=fornecedor,
        nota_fiscal=nota_fiscal,
        valor_unitario=valor_unitario
    )

    db.session.add(novo_lote)

    produto.estoque_atual += quantidade

    movimentacao = Movimentacao(
        produto_id=produto.id,
        tipo="ENTRADA",
        quantidade=quantidade,
        responsavel=responsavel,
        observacao=observacao,
        lote=lote,
        validade=validade,
        nota_fiscal=nota_fiscal,
        valor_unitario=valor_unitario
    )

    db.session.add(movimentacao)

    db.session.commit()

    return True