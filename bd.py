import telebot
import mysql.connector
import time
from telebot.types import InputMediaPhoto
import datetime as dt_module  
from datetime import datetime, timedelta
from datetime import date
from telebot import types

bot = telebot.TeleBot("7088149058:AAGyUDs2AiBkPd3dhfvnqX0pzvlvmPW72xA")
def db_config():
    return {
        'host': 'junction.proxy.rlwy.net',
        'port': '14652',
        'database': 'garden',
        'user': 'root',
        'password': 'hepbYJAElHejqGrjlldoXkDbrLWFngfq',

    }
    
def conectar_banco_dados():
    while True:
        try:
            conn = mysql.connector.connect(**db_config())
            cursor = conn.cursor()
            return conn, cursor
        except mysql.connector.Error as e:
            print(f"Erro na conexão com o banco de dados: {e}")
            print("Tentando reconectar em 5 segundos...")
            time.sleep(5)

conn, cursor = conectar_banco_dados()

def fechar_conexao(cursor, conn):
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()   
