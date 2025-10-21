from fastapi import FastAPI
import os
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse


#IMPORTANTE: Lembre-se de criar o arquivo .env com a Secret_Key, Algorithm e Access_Token_Time

#Senhas criptografadas
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

#JWT tokens
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_TIME = int(os.getenv('ACCESS_TOKEN_TIME'))

#Ativar formulario de login na docs
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login_form')

#Roteadores de rota
from auth_routes import auth_router
from order_routes import order_router

#Cria o app
app = FastAPI(
    title='SkAPI',
    description='Uma base pra você já começar fazendo oque importa!',
    version='1.0.0'    
)

app.include_router(auth_router)
app.include_router(order_router)

#Vai redirecionar o usuário da API direto pras docs quando usar o comando: uvicorn main:app --reload
@app.get('/', include_in_schema=False)
def root():
    return RedirectResponse(url='/docs')
#end