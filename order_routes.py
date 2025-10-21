from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Usuario

#Aqui você pode definir a url e o nome da rota, o modo que ela vai aparecer nas docs
order_router = APIRouter(prefix='/order', tags=['Comando'])


#Essa é a aba onde você vai criar os seus comandos, as suas requisições ao banco de dados