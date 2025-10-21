from fastapi import APIRouter, Depends, HTTPException
from dependencies import pegar_sessao, verificar_token
from models import Usuario
from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_TIME
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

#Aqui você pode definir a url e o nome da rota, o modo que ela vai aparecer nas docs
auth_router = APIRouter(prefix='/auth', tags=['Autenticação'])

#Vai criar um token jwt para o usuário
def criar_token(id_usuario, duracao = timedelta(minutes=ACCESS_TOKEN_TIME)):
    data_expiracao = datetime.now(timezone.utc) + duracao
    dict_info = {'sub': str(id_usuario), 'exp': data_expiracao}
    token = jwt.encode(dict_info,SECRET_KEY,ALGORITHM)
    return token

#Vai autenticar o login do usuário
def autenticar_usuario(email,senha,session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

#Rota para registrar novos usuários. Não é aceito email repetido
@auth_router.post('/registrar')
async def registrar(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        return {'mensagem': 'Já existe um usuário com esse E-mail.'}
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return {'mensagem': 'Usuário cadastrado com sucesso!'}

#Rota de login padrão
@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail='Usuario ou senha incorretos.')
    else:
        token_de_acesso = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao=timedelta(days=7))
        return {
            'access_token': token_de_acesso,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
        }

#Formulario de login das docs
@auth_router.post('/login_form')
async def login_form(dados_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_form.username, dados_form.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail='Usuario ou senha incorretos.')
    else:
        token_de_acesso = criar_token(usuario.id)
        return {
            'access_token': token_de_acesso,
            'token_type': 'Bearer'
        }

#Vai criar um novo token para o usuário, sem ele precisar logar novamente
@auth_router.get('/refresh')
async def refresh_token(usuario: Usuario = Depends(verificar_token)):
    token_de_acesso = criar_token(usuario.id)
    return {
        'access_token': token_de_acesso,
        'token_type': 'Bearer'
    }
        