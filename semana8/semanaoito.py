import os
import json
import subprocess
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base
import mlflow
from prefect import flow, task


# Carregando os dados
df = pd.read_csv('tudo.csv')  # Atualize o caminho se necessário

# Verificando o DataFrame
print(df.head())
print(df.columns)
print(df.dtypes)

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///Vendas.db"
engine = create_engine(DATABASE_URL)

# Criando a base do SQLAlchemy
Base = declarative_base()

# Definindo a tabela "Vendas"
class Vendas(Base):
    __tablename__ = 'Vendas'

    sale_id = Column(Integer, primary_key=True, index=True)
    price_y = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)

# Criando a tabela no banco de dados
Base.metadata.create_all(engine)

# Criando a sessão
Session = sessionmaker(bind=engine)
session = Session()

# Função para preencher a tabela com dados do CSV
def preencher_vendas():
    for index, row in df.iterrows():
        venda = Vendas(
            sale_id=int(row['sale_id']) if row['sale_id'].isdigit() else None,
            price_y=row['price_y'],
            quantity=row['quantity']
        )
        session.add(venda)
    session.commit()

# Registrando dados com MLflow e utilizando Prefect para orquestrar
@task
def preencher_vendas_com_mlflow():
    with mlflow.start_run():
        for index, row in df.iterrows():
            venda = Vendas(
                sale_id=int(row['sale_id']) if row['sale_id'].isdigit() else None,
                price_y=row['price_y'],
                quantity=row['quantity']
            )
            session.add(venda)

            # Registrando parâmetros e métricas no MLflow
            mlflow.log_param("sale_id", row['sale_id'])
            mlflow.log_metric("price_y", row['price_y'])
            mlflow.log_metric("quantity", row['quantity'])

        session.commit()

@flow
def fluxo_vendas():
    preencher_vendas_com_mlflow()

# Executando o fluxo
if __name__ == "__main__":
    fluxo_vendas()

    # Verificando se os dados foram inseridos
    vendas = session.query(Vendas).all()
    for venda in vendas:
        print(f"ID: {venda.sale_id}, Preço: {venda.price_y}, Quantidade: {venda.quantity}")
