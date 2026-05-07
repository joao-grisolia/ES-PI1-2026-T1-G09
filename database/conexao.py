import mysql.connector
import os
from dotenv import load_dotenv

def conectar():
    load_dotenv() # carrega oq ta escrito no .env, ou seja, as credenciais do banco
    try: # tenta fazer a conexão com o banco
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            port=os.getenv("DB_PORT"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )

        return conexao # se der tudo certinho retorna a conexão

    except mysql.connector.Error as erro: # se a conexao der erro
        print("Erro ao conectar no banco:", erro) # printa o erro
        return None  # retorna nada pq deu erro 

"""
    Para fazer a conexão com o banco precisa inicialmente instalar a 
    biblioteca mysql.connector, so digitar no terminal
    
    pip install mysql-connector-python python-dotenv
    
    Depois cria na pasta raiz do projeto
    um arquivo .env com as seguintes informações
    
    DB_HOST=pi-projeto-pi.j.aivencloud.com
    DB_PORT=15817
    DB_USER=avnadmin
    DB_PASSWORD=coloca pwd aqui
    DB_NAME=projetoPI
    
    Só trocar os valores da USEr e PASSWORD para o certo
    Como é um repositorio publico e estamos usando um database remoto
    Por motivos de segurança usamos o .env para ocultar as informações
    De acesso ao banco, para somente a gente ter acesso.
    Se reparaem no arquivo .gitignore tem a linha .env
    isso é para o git ignorar o arquivo e não subir ele para o repositorio
"""