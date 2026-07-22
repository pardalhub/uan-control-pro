from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import date

db = SQLAlchemy()


# =====================================================
# PRODUTOS
# =====================================================

class Produto(db.Model):

    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(120), nullable=False)

    categoria = db.Column(db.String(80), nullable=False)

    unidade = db.Column(db.String(30), nullable=False)

    codigo_barras = db.Column(db.String(80))

    fornecedor = db.Column(db.String(120))

    localizacao = db.Column(db.String(120))

    estoque_atual = db.Column(db.Float, default=0)

    estoque_minimo = db.Column(db.Float, default=0)

    estoque_maximo = db.Column(db.Float, default=0)

    essencial = db.Column(db.Boolean, default=False)

    observacao = db.Column(db.Text)

    ativo = db.Column(db.Boolean, default=True)

    criado_em = db.Column(
        db.DateTime,
        default=datetime.now
    )

    atualizado_em = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )

    def __repr__(self):
        return self.nome


# ==========================================================
# LOTES
# ==========================================================

class Lote(db.Model):

    __tablename__ = "lotes"

    id = db.Column(db.Integer, primary_key=True)

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id"),
        nullable=False
    )

    produto = db.relationship("Produto")

    lote = db.Column(db.String(80), nullable=False)

    quantidade = db.Column(db.Float, default=0)

    validade = db.Column(db.Date)

    fornecedor = db.Column(db.String(120))

    nota_fiscal = db.Column(db.String(80))

    valor_unitario = db.Column(db.Float, default=0)

    criado_em = db.Column(
        db.DateTime,
        default=datetime.now
    )

    def __repr__(self):
        return f"<Lote {self.lote}>"

# =====================================================
# MOVIMENTAÇÕES
# =====================================================

class Movimentacao(db.Model):

    __tablename__ = "movimentacoes"

    id = db.Column(db.Integer, primary_key=True)

    data = db.Column(
        db.DateTime,
        default=datetime.now
    )

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id")
    )

    produto = db.relationship("Produto")

    tipo = db.Column(db.String(20))

    quantidade = db.Column(db.Float)

    responsavel = db.Column(db.String(100))

    observacao = db.Column(db.Text)

    lote = db.Column(db.String(60))

    validade = db.Column(db.Date)

    nota_fiscal = db.Column(db.String(80))

    valor_unitario = db.Column(db.Float)

    def __repr__(self):
        return str(self.id)