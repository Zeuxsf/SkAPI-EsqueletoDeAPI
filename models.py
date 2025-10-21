from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base

#Cria o banco de dados
db = create_engine('sqlite:///banco.db')
base = declarative_base()

#Essa classe vai passar as informações necessárias para salvar os usuário no  Banco de dados
class Usuario(base):
    __tablename__ = 'usuarios'
    
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String)
    email = Column('email', String, nullable=False)
    senha = Column('senha', String)
    saldo = Column('saldo', Float, default=0)
    admin = Column('admin', Boolean, default=False)
    
    def __init__(self, nome, email, senha, saldo = 0, admin = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.saldo = saldo
        self.admin = admin


        