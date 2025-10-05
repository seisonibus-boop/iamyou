#Bibliotecas para interagir com o Telegram e HTTP
import telebot
import requests
import flask
import http.server
import socketserver
from telebot.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import numpy as np
#Conexão com o Banco de Dados
import mysql.connector
from mysql.connector import Error
#Manipulação de Data e Tempo
import time
import datetime
from datetime import datetime, timedelta, date
from labirinto import *
import datetime as dt_module
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
#Manipulação de Imagens e Áudio
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, UnidentifiedImageError
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from io import BytesIO
import tempfile
from telebot.types import ReactionTypeEmoji
#Análise e Manipulação de Strings e Web
import re
import Levenshtein
from bs4 import BeautifulSoup
from urllib.parse import urlparse
#Gerenciamento de Tarefas e Threads
import threading
from queue import Queue
#Manipulação de Arquivos e Sistema Operacional
import os
import json
import io
#Operações Matemáticas e Funções Utilitárias
import math
import random
import functools
#Cache e Armazenamento Temporário
import diskcache as dc
from cachetools import TTLCache
#Integração com APIs Externas (Spotify)
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
#Logs e Monitoramento
import logging
import newrelic.agent
#Módulos Personalizados do Projeto
from aboboras import *
from halloween import *
from doaçao import *
from wish import *
from songs import *
from credentials import *
from cestas import *
from album import *
from pescar import *
from evento import *
from phrases import *
from callbacks2 import choose_subcategoria_callback
from trocas import *
from bd import *
from saves import *
from calculos import *
from fonte import *
from trintadas import *
from eu import *
from sub import *
from submenu import *
from especies import *
from config import *
from historico import *
from tag import *
from banco import *
from diary import *
from admin import *
from peixes import *
from halloween import *
from vips import *
from petalas import *
from compat import *
from armazem import *
from diamantes import *
from game import *
from gif import *
from verao import *
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import threading
import time
import importdir
grupodeerro = -1002209493474
scheduler = BackgroundScheduler()
scheduler.start()
# Configuração de Webhook
WEBHOOK_URL_PATH = '/' + API_TOKEN + '/'
WEBHOOK_LISTEN = "0.0.0.0"
WEBHOOK_PORT = int(os.getenv('PORT', 5000))
#Inicialização do Bot e Aplicações
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)
newrelic.agent.initialize('newrelic.ini')
#Cache e Filas de Tarefas
cache_musicas_editadas = dc.Cache('./cache_musicas_editadas')
song_cooldown_cache = TTLCache(maxsize=1000, ttl=15)
cache = dc.Cache('./cache')
task_queue = Queue()
conn, cursor = conectar_banco_dados()
GRUPO_SUGESTAO = -4546359573
from datetime import datetime, timedelta
import pytz
from cachetools import TTLCache, cached

# Configuração do cache: máximo de 100 itens, expira após 600 segundos (10 minutos)
cache_precos_cartas = TTLCache(maxsize=100, ttl=600)
# Defina o fuso horário local desejado (exemplo: 'America/Sao_Paulo')
FUSO_HORARIO_LOCAL = pytz.timezone('America/Sao_Paulo')


@app.route("/")
def set_webhook():

    bot.remove_webhook()
    success = bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    
    if success:
        return "Webhook configurado com sucesso!", 200
    else:
        return "Falha ao configurar o webhook.", 500

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'Server is running.'

@bot.message_handler(commands=['resettime'])
def reset_time_wrapper(message):
    handle_reset_time(message)

@bot.message_handler(commands=['futebol'])
def mandar_futebol(message):
    send_futebol_dice(message)
@bot.callback_query_handler(func=lambda call: call.data.startswith(('trocar_', 'manter_')))
def wrapper_troca_picole(call):
    handle_troca_picole(call)
@bot.callback_query_handler(func=lambda call: call.data == 'refresh_subcategorias')
def handle_refresh_subcategorias(call):
    try:
        # Recarregar as subcategorias
        message = call.message
        tratar_subcategorias_padroes(message.chat.id, None, 'geral', message)
        bot.answer_callback_query(call.id, "Espécies atualizadas!")
        
    except Exception as e:
        print(f"Erro no refresh: {str(e)}")
        bot.answer_callback_query(call.id, "❌ Erro ao atualizar")
@bot.message_handler(commands=['sorveteiro'])
def wrapper_handle_sorveteiro(message):
    handle_sorveteiro(message)
@bot.message_handler(commands=['tesouro'])
def send_treasure_hunt(message):
    try:
        user_id = message.from_user.id
        nome = message.from_user.first_name

        if not can_play(user_id, 'tesouro'):
            bot.send_message(message.from_user.id, "⏳ Calma, aventureiro! Só uma vez por hora.")
            return

        tesouro = random.randint(0, 8)
        escolhas = []
        tentativas = 3
        
        send_game_ui(message.from_user.id, tesouro, tentativas, escolhas, nome)
        
    except Exception as e:
        print(f"Erro em /tesouro: {e}")
@bot.message_handler(commands=['picolés'])
def lista_picoles(message):
    try:
        texto = """❄️ *Lista de Picolés Disponíveis* ❄️

🍓 *Picolé de Morango* 
▸ Cartas podem vir com 1-5 unidades extras

🥥 *Picolé de Coco* 
▸ Chance de receber carta extra da mesma subcategoria

🌽 *Picolé de Milho Verde* 
▸ Ganha 50 cenouras a cada hora

🍇 *Picolé de Uva* 
▸ +25% chance de eventos especiais

🍫 *Picolé de Chocolate* 
▸ Dobra ingredientes recebidos

🥜 *Picolé de Amendoim* 
▸ Favoritar subcategorias (/favserie)
▸ 10x mais chances de aparecerem

🍉 *Picolé de Melancia* 
▸ Favoritar personagens (/favperso)
▸ 3x mais chances nas pescas


✨ *Como obter?* 
Use /sorveteiro para tentar ganhar um!"""


        bot.reply_to(message, texto, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"❌ Erro: {str(e)}")
@bot.callback_query_handler(func=lambda call: call.data.startswith("jogada_"))
def handle_click(call):
    try:
        data = call.data.split('_')
        escolha = int(data[1])
        tesouro = int(data[2])
        tentativas = int(data[3])
        escolhas = list(map(int, data[4].split(','))) if data[4] else []
        nome = data[5]

        acertou = (escolha == tesouro)
        escolhas.append(escolha)
        tentativas -= 1

        # Prepara a grade ANTES de montar a mensagem
        linha = ['⛱️'] * 9
        for pos in escolhas:
            linha[pos] = '❌'
        
        if acertou or tentativas == 0:
            linha[tesouro] = '💰'  # Revela o tesouro

        grade = "\n".join([" ".join(linha[i:i+3]) for i in range(0, 9, 3)])

        if acertou:
            # Recompensas
            cenouras = random.randint(50, 100)
            sucesso_cen = aumentar_cenouras(call.from_user.id, cenouras)
            
            # Carta de evento (30% chance)
            carta_evento = None
            if random.random() < 1:  # 30% de chance
                carta_evento = obter_carta_evento_verao()

            # Chama send_game_ui com todos os dados necessários
            send_game_ui(
                call.message.chat.id,
                tesouro,
                0,
                escolhas,
                nome,
                call.message.message_id,
                cenouras=cenouras,
                carta_evento=carta_evento  # Novo parâmetro
            )
        elif tentativas == 0:
            send_game_ui(
                call.message.chat.id,
                tesouro,
                0,
                escolhas,
                nome,
                call.message.message_id
            )
           

        else:
            send_game_ui(
                call.message.chat.id,
                tesouro,
                tentativas,
                escolhas,
                nome,
                call.message.message_id,
            )

        update_interaction_time(call.from_user.id, 'tesouro')

    except Exception as e:
        print(f"Erro no clique: {str(e)}")
        traceback.print_exc()
        bot.answer_callback_query(call.id, "⚡ O tesouro fugiu!", show_alert=True)
@bot.callback_query_handler(func=lambda call: call.data.startswith('card_confirmar_') or call.data.startswith('card_cancelar_'))
def callback_query(call):
    try:
        dados = call.data.split('_')
        id_carta = dados[2]

        if call.data.startswith('card_confirmar_'):
            conn, cursor = conectar_banco_dados()

            cursor.execute("""
                SELECT canela, po_estrela, glitter, cola
                FROM precos_cartas
                WHERE id_personagem = %s
            """, (id_carta,))
            preco_existente = cursor.fetchone()

            if not preco_existente:
                bot.answer_callback_query(call.id, "Erro: preço do card não encontrado.")
                return

            canela, estrela, glitter, cola = preco_existente

            cursor.execute("""
                UPDATE materiais_usuario
                SET canela = canela - %s,
                    estrela = estrela - %s,
                    glitter = glitter - %s,
                    cola = cola - %s
                WHERE id_usuario = %s
            """, (canela, estrela, glitter, cola, call.from_user.id))

            add_to_inventory(call.from_user.id, id_carta)

            cursor.execute("""
                SELECT quantidade FROM inventario WHERE id_usuario = %s AND id_personagem = %s
            """, (call.from_user.id, id_carta))
            result = cursor.fetchone()
            quantidade_atual = result[0] if result else 0

            cursor.execute("""
                SELECT nome, subcategoria FROM personagens WHERE id_personagem = %s
            """, (id_carta,))
            personagem = cursor.fetchone()

            if not personagem:
                bot.answer_callback_query(call.id, "Personagem não encontrado.")
                return

            nome, subcategoria = personagem

            conn.commit()

            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                caption=(
                    f"✨ Seu trabalho árduo colhendo ingredientes deu frutos! Você criou esta carta com sucesso.\n\n"
                    f"🐟 <b>{nome} de {subcategoria}: {quantidade_atual + 1}x</b>\n\n"
                    "Obrigado por usar a oficina!"
                ),
                parse_mode="HTML"
            )
        elif call.data.startswith('card_cancelar_'):
            bot.answer_callback_query(call.id, "Operação cancelada.")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"Operação cancelada para o card ID {id_carta}.",
                parse_mode="HTML"
            )

    except Exception as e:
        erro = traceback.format_exc()
        bot.send_message(
            call.message.chat.id,
            f"❌ Ocorreu um erro no callback:\n{e}\n{erro}",
            parse_mode="HTML"
        )
    finally:
        fechar_conexao(cursor, conn)
@bot.callback_query_handler(func=lambda call: call.data.startswith("cenourarbotao_"))
def callback_cenourar(call):
    try:
        id_usuario = call.from_user.id
        id_personagem = call.data.split("_")[1]

        # Chamar a função para perguntar se deseja cenourar
        enviar_pergunta_cenoura(call.message, id_usuario, [id_personagem], bot)

        # Notificar o usuário que a ação foi iniciada
        bot.answer_callback_query(call.id, "🥕 Preparando para cenourar a carta...", show_alert=False)

    except Exception as e:
        erro = traceback.format_exc()
        bot.send_message(grupodeerro, f"Erro no callback /cenourar: {e}\n{erro}", parse_mode="HTML")
@bot.callback_query_handler(func=lambda call: call.data.startswith("oferecer_"))
def callback_oferecer(call):
    try:
        id_usuario = call.message.chat.id
        id_user = call.from_user.id
        username = call.from_user.username or call.from_user.first_name

        # Pegar o ID da carta do callback_data (exemplo: "oferecer_12345" → "12345")
        id_carta = call.data.split("_")[1]

        # Conectar ao banco de dados
        conn, cursor = conectar_banco_dados()

        # Verificar se o usuário possui a carta no inventário
        quantidade = verificar_inventario(id_usuario, id_carta, cursor)
        if quantidade == 0:
            bot.answer_callback_query(call.id, "❌ Você não possui essa carta para oferecer!", show_alert=True)
            cursor.close()
            conn.close()
            return

        # Buscar usuários interessados
        usuarios_interessados = buscar_usuarios_interessados(id_carta, cursor)

        # Notificar usuários interessados
        if usuarios_interessados:
            for usuario_id in usuarios_interessados:
                if usuario_id != id_usuario:  # Evita notificar o próprio usuário
                    try:
                        bot.send_message(
                            usuario_id,
                            f"🔔 Alerta! @{username} está oferecendo a carta {id_carta} que você busca!\n"
                            f"Entre em contato para negociar.",
                            parse_mode="HTML"
                        )
                    except Exception as e:
                        print(f"Erro ao notificar usuário {usuario_id}: {e}")

            bot.answer_callback_query(call.id, f"✅ Carta {id_carta} anunciada! {len(usuarios_interessados)} usuários foram notificados.", show_alert=True)
        else:
            bot.answer_callback_query(call.id, f"✅ Carta {id_carta} anunciada, mas ninguém está buscando essa carta no momento.", show_alert=True)

        cursor.close()
        conn.close()

    except Exception as e:
        erro = traceback.format_exc()
        bot.send_message(grupodeerro, f"Erro no callback /oferecer: {e}\n{erro}", parse_mode="HTML")
@bot.message_handler(commands=['beneficios'])
def mostrar_beneficios(message):
    beneficios = """
<b>🌿 BENEFÍCIOS VIP - AGRICULTORES DO GARDEN 🌿</b>

⛲ <b>Fonte VIP</b>
• Recarrega a cada 3 horas (metade do tempo normal)

📔 <b>Diary Protegido</b>
• Não perde a sequência se esquecer um dia
• Exemplo: Faz na sexta → esquece no sábado → continua no domingo

🍃 <b>Identificação Exclusiva</b>
• Selo especial no perfil: 🌿 Agricultor do Garden

📥 <b>Pedidos Prioritários</b>
• Atendimento VIP em qualquer dia da semana
• Prioridade na fila de pedidos
• Até 4 submenus por mês
• Sugestões diretas para eventos

🌹 <b>Roseira</b>
• Funciona em qualquer subcategoria
• Escolha entre 3 cartas ao usar /roseira
• Pétalas regeneram a cada 2 horas

🎴 <b>Vantagens Exclusivas</b>
• Card especial de Agricultor
• Acesso a grupo privado VIP
• Novos recursos prioritários

💵 <b>Investimento</b>
• Valor: R$ 7,50 mensais
• Recursos destinados à manutenção do servidor premium

✉️ <b>Interessado?</b>
Envie mensagem privada para @bala_de_cafe e cultive sua experiência no Garden!

    """
    
    try:
        bot.send_message(
            message.chat.id,
            beneficios,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Erro ao enviar benefícios: {str(e)}")
@bot.message_handler(commands=['favperso', 'delfavperso'])
def handle_character_fav(message):
    try:
        user_id = message.from_user.id
        comando = message.text.split()[0]
        character_id = int(message.text.split()[1])

        conn, cursor = conectar_banco_dados()
        
        if 'favperso' in comando:
            cursor.execute("""
                INSERT INTO user_favorite_characters (user_id, character_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE character_id = VALUES(character_id)
            """, (user_id, character_id))
            msg = f"⭐ Personagem {character_id} favoritado!"
        else:
            cursor.execute("""
                DELETE FROM user_favorite_characters
                WHERE user_id = %s AND character_id = %s
            """, (user_id, character_id))
            msg = f"🗑️ Personagem {character_id} removido dos favoritos!"
        
        conn.commit()
        bot.reply_to(message, msg)

    except (IndexError, ValueError):
        bot.reply_to(message, f"ℹ️ Formato correto: {message.text.split()[0]} ID_DO_PERSONAGEM")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro: {str(e)}")
    finally:
        fechar_conexao(cursor, conn)

@bot.message_handler(commands=['favpersonagens'])
def list_fav_characters(message):
    try:
        user_id = message.from_user.id
        conn, cursor = conectar_banco_dados()
        
        cursor.execute("""
            SELECT p.emoji, p.id_personagem, p.nome, p.subcategoria 
            FROM user_favorite_characters ufc
            JOIN personagens p ON ufc.character_id = p.id_personagem
            WHERE ufc.user_id = %s
        """, (user_id,))
        
        favoritos = cursor.fetchall()
        
        if not favoritos:
            bot.reply_to(message, "📭 Você não tem personagens favoritos!")
            return
            
        lista = "\n".join([f"{emoji} <code>{char_id}</code> - {nome} ({sub})" 
                          for emoji, char_id, nome, sub in favoritos])
        
        bot.reply_to(message, f"🍉 Personagens Favoritos:\n\n{lista}", parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"❌ Erro: {str(e)}")
    finally:
        fechar_conexao(cursor, conn)
@bot.message_handler(commands=['favseries'])
def listar_favoritos(message):
    try:
        user_id = message.from_user.id
        conn, cursor = conectar_banco_dados()
        
        # Query corrigida
        cursor.execute("""
            SELECT uf.subcategoria, p.categoria 
            FROM user_favorites uf
            JOIN personagens p 
                ON uf.subcategoria COLLATE utf8mb4_unicode_ci = p.subcategoria
            WHERE uf.user_id = %s
            GROUP BY uf.subcategoria, p.categoria  # Corrigido aqui
        """, (user_id,))
        
        favoritos = cursor.fetchall()
        
        if not favoritos:
            bot.reply_to(message, "📭 Você ainda não tem séries favoritadas!\nUse /favserie NOME para adicionar")
            return
            
        # Mapeamento de emojis
        EMOJI_CATEGORIAS = {
            'Música': '☁️',
            'Animangá': '🌷',
            'Jogos': '🧶',
            'Filmes': '🍰',
            'Séries': '🍄',
            'Miscelânea': '🍂'
        }
        
        # Construir lista formatada
        lista = []
        for subcategoria, categoria in favoritos:
            emoji = EMOJI_CATEGORIAS.get(categoria, '🔹')
            lista.append(f"{emoji} {subcategoria}")

        # Ordenar por categoria
        lista_ordenada = sorted(lista, key=lambda x: x.split()[0], reverse=True)
        
        bot.reply_to(message, f"📚 Suas séries favoritas:\n\n" +
                     "\n".join(lista_ordenada) +
                     f"\n\nTotal: {len(favoritos)} séries favoritadas")

    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao listar favoritos: {str(e)}")
    finally:
        fechar_conexao(cursor, conn)
        
@bot.message_handler(commands=['favserie'])
def add_favorite(message):
    try:
        user_id = message.from_user.id
        subcategoria = message.text.split(' ', 1)[1].strip()
        
        conn, cursor = conectar_banco_dados()
        
        # Verificar se a subcategoria existe
        cursor.execute("SELECT 1 FROM personagens WHERE subcategoria = %s LIMIT 1", (subcategoria,))
        if not cursor.fetchone():
            bot.reply_to(message, f"❌ Subcategoria '{subcategoria}' não encontrada!")
            return
            
        # Adicionar aos favoritos
        cursor.execute("""
            INSERT INTO user_favorites (user_id, subcategoria)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE subcategoria = VALUES(subcategoria)
        """, (user_id, subcategoria))
        conn.commit()
        
        bot.reply_to(message, f"⭐ '{subcategoria}' adicionada aos favoritos!")
        
    except IndexError:
        bot.reply_to(message, "❌ Uso correto: /favserie NomeDaSubcategoria")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao adicionar favorito: {str(e)}")
    finally:
        fechar_conexao(cursor, conn)

@bot.message_handler(commands=['delfavserie'])
def remove_favorite(message):
    try:
        user_id = message.from_user.id
        subcategoria = message.text.split(' ', 1)[1].strip()
        
        conn, cursor = conectar_banco_dados()
        
        # Remover dos favoritos
        cursor.execute("DELETE FROM user_favorites WHERE user_id = %s AND subcategoria = %s", 
                      (user_id, subcategoria))
        conn.commit()
        
        if cursor.rowcount > 0:
            bot.reply_to(message, f"🗑️ '{subcategoria}' removida dos favoritos!")
        else:
            bot.reply_to(message, f"❌ '{subcategoria}' não estava nos favoritos!")
            
    except IndexError:
        bot.reply_to(message, "❌ Uso correto: /delfavserie NomeDaSubcategoria")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao remover favorito: {str(e)}")
    finally:
        fechar_conexao(cursor, conn)        
def possui_materiais(id_usuario, canela, estrela, glitter, cola):
    try:
        conn, cursor = conectar_banco_dados()
        cursor.execute("""
            SELECT
                canela, estrela, glitter, cola
            FROM materiais_usuario
            WHERE id_usuario = %s
        """, (id_usuario,))
        materiais = cursor.fetchone()

        if not materiais:
            return False  # Sem materiais registrados

        return (
            materiais[0] >= canela and
            materiais[1] >= estrela and
            materiais[2] >= glitter and
            materiais[3] >= cola
        )
    except Exception as e:
        print(f"Erro ao verificar materiais: {e}")
        return False
    finally:
        fechar_conexao(cursor, conn)
# Função para processar o comando /addvip
@bot.message_handler(commands=['addvip'])
def handle_addvip(message):
    adicionar_vip(message)

# Função para processar o comando /removevip
@bot.message_handler(commands=['removevip'])
def handle_removevip(message):
    remover_vip(message)
    
def obter_imagem_id(id_personagem, offset):
    conn, cursor = conectar_banco_dados()
    try:
        query = "SELECT imagem, emoji, nome, id_personagem FROM personagens WHERE id_personagem = %s LIMIT 1 OFFSET %s"
        cursor.execute(query, (id_personagem, offset))
        return cursor.fetchone()
    finally:
        fechar_conexao(cursor, conn)

@bot.message_handler(commands=['material'])
def doar_material(message):
    try:
        # Verificar se o comando foi usado em resposta a uma mensagem
        if not message.reply_to_message:
            bot.reply_to(message, "Você deve usar este comando em resposta a uma mensagem de outro usuário para doar materiais.")
            return

        # Extrair o ID do remetente (quem está doando) e do destinatário (quem vai receber)
        id_remetente = message.from_user.id
        id_destinatario = message.reply_to_message.from_user.id

        # Dividir o comando para obter o tipo de material e a quantidade
        comandos = message.text.split()
        if len(comandos) != 3:
            bot.reply_to(message, "Uso incorreto do comando. O formato correto é: /material (canela, estrela, cola, glitter) (quantidade)")
            return

        tipo_material = comandos[1].lower()  # Tipo de material (e.g., canela, estrela, etc.)
        try:
            quantidade = int(comandos[2])  # Quantidade a ser doada
        except ValueError:
            bot.reply_to(message, "A quantidade deve ser um número inteiro.")
            return

        # Verificar se a quantidade é válida
        if quantidade <= 0:
            bot.reply_to(message, "A quantidade deve ser maior que zero.")
            return

        # Mapeamento de nomes amigáveis para os nomes reais das colunas no banco de dados
        mapa_materiais = {
            "canela": "canela",
            "estrela": "estrela",  # Mapeia "estrela" para "po_estrela"
            "cola": "cola",
            "glitter": "glitter"
        }

        # Verificar se o tipo de material é válido
        if tipo_material not in mapa_materiais:
            bot.reply_to(message, f"O material '{tipo_material}' não é válido. Os materiais válidos são: canela, estrela, cola, glitter.")
            return

        # Obter o nome real da coluna do banco de dados
        coluna_material = mapa_materiais[tipo_material]

        # Conectar ao banco de dados
        conn, cursor = conectar_banco_dados()

        # Verificar se o remetente tem materiais suficientes
        cursor.execute(f"SELECT {coluna_material} FROM materiais_usuario WHERE id_usuario = %s", (id_remetente,))
        resultado_remetente = cursor.fetchone()
        if not resultado_remetente:
            bot.reply_to(message, "Você não possui este material para doar.")
            return

        quantidade_remetente = resultado_remetente[0] or 0
        if quantidade_remetente < quantidade:
            bot.reply_to(message, f"Você não tem {quantidade} de {tipo_material} para doar. Você possui apenas {quantidade_remetente}.")
            return

        # Remover a quantidade do remetente
        cursor.execute(f"UPDATE materiais_usuario SET {coluna_material} = {coluna_material} - %s WHERE id_usuario = %s", (quantidade, id_remetente))

        # Adicionar a quantidade ao destinatário
        cursor.execute(f"SELECT {coluna_material} FROM materiais_usuario WHERE id_usuario = %s", (id_destinatario,))
        resultado_destinatario = cursor.fetchone()
        if resultado_destinatario:
            # Atualizar a quantidade existente do destinatário
            cursor.execute(f"UPDATE materiais_usuario SET {coluna_material} = {coluna_material} + %s WHERE id_usuario = %s", (quantidade, id_destinatario))
        else:
            # Criar registro do destinatário caso ele ainda não tenha materiais
            cursor.execute(f"INSERT INTO materiais_usuario (id_usuario, {coluna_material}) VALUES (%s, %s) ON DUPLICATE KEY UPDATE {coluna_material} = {coluna_material} + %s", (id_destinatario, quantidade, quantidade))

        # Confirmar as alterações no banco de dados
        conn.commit()

        # Enviar mensagem de confirmação
        bot.reply_to(
            message,
            f"💝 Você doou {quantidade} unidade(s) de {tipo_material} para {message.reply_to_message.from_user.first_name}!"
        )

    except Exception as e:
        erro = traceback.format_exc()
        bot.send_message(
            message.chat.id,
            f"❌ Ocorreu um erro ao processar a doação:\n{e}\n{erro}",
            parse_mode="HTML"
        )
    finally:
        fechar_conexao(cursor, conn)
        
def cadastrar_busca(id_usuario, id_carta, cursor, conn):
    """
    Cadastra uma carta que o usuário está buscando.
    """
    try:
        print(f"📥 Cadastrando busca: Usuário {id_usuario}, Carta {id_carta}")  # Depuração
        
        cursor.execute(
            "INSERT INTO buscas_cartas (id_usuario, id_carta) VALUES (%s, %s) "
            "ON DUPLICATE KEY UPDATE data_cadastro = CURRENT_TIMESTAMP",
            (id_usuario, id_carta)
        )
        conn.commit()
        print("✅ Busca cadastrada com sucesso!")  # Depuração
        return True
    except Exception as e:
        print(f"❌ Erro ao cadastrar busca: {e}")
        return False
        
def verificar_inventario(id_usuario, id_carta, cursor):
    """
    Verifica se o usuário possui a carta no inventário e retorna a quantidade.
    Retorna 0 se a carta não estiver no inventário.
    """
    try:
        cursor.execute(
            "SELECT quantidade FROM inventario WHERE id_usuario = %s AND id_personagem = %s",
            (id_usuario, id_carta)
        )
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0
    except Exception as e:
        print(f"Erro ao verificar inventário: {e}")
        return 0
def remover_busca(id_usuario, id_carta, cursor, conn):
    """
    Remove uma carta da lista de buscas do usuário.
    """
    try:
        cursor.execute(
            "DELETE FROM buscas_cartas WHERE id_usuario = %s AND id_carta = %s",
            (id_usuario, id_carta)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao remover busca: {e}")
        return False

def buscar_usuarios_interessados(id_carta, cursor):
    """
    Retorna a lista de usuários que estão buscando uma carta específica.
    """
    try:
        cursor.execute(
            "SELECT id_usuario FROM buscas_cartas WHERE id_carta = %s",
            (id_carta,)
        )
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Erro ao buscar usuários interessados: {e}")
        return []

@bot.message_handler(commands=['oferecer'])
def comando_oferecer(message):
    try:
        id_usuario = message.chat.id
        id_user = message.from_user.id
        username = message.from_user.username or message.from_user.first_name
        args = message.text.split()

        if len(args) != 2:
            bot.reply_to(message, "Uso correto: /oferecer <id_carta>")
            return

        id_carta = args[1]

        # Conectar ao banco de dados
        conn, cursor = conectar_banco_dados()

        # Verificar se o usuário possui a carta no inventário
        quantidade = verificar_inventario(id_usuario, id_carta, cursor)
        if quantidade == 0:
            bot.reply_to(message, f"❌ Você não possui a carta {id_carta} no seu inventário.")
            cursor.close()
            conn.close()
            return

        # Buscar usuários interessados
        usuarios_interessados = buscar_usuarios_interessados(id_carta, cursor)

        # Notificar usuários interessados
        if usuarios_interessados:
            for usuario_id in usuarios_interessados:
                if usuario_id != id_usuario:  # Não notificar o próprio usuário
                    try:
                        bot.send_message(
                            usuario_id,
                            f"🔔 Alerta! @{username} está oferecendo a carta {id_carta} que você busca!\n"
                            f"Entre em contato para negociar.",
                            parse_mode="HTML"
                        )
                    except Exception as e:
                        print(f"Erro ao notificar usuário {usuario_id}: {e}")
            bot.reply_to(message, f"✅ Carta {id_carta} anunciada! {len(usuarios_interessados)} "
                                f"usuários foram notificados. (Você possui {quantidade} unidade(s) desta carta.)")
        else:
            bot.reply_to(message, f"✅ Carta {id_carta} anunciada, mas ninguém está buscando "
                                f"essa carta no momento. (Você possui {quantidade} unidade(s) desta carta.)")

        cursor.close()
        conn.close()

    except Exception as e:
        erro = traceback.format_exc()
        bot.send_message(grupodeerro, f"Erro no comando /oferecer: {e}\n{erro}", parse_mode="HTML")
@bot.message_handler(commands=['busco'])
def comando_busco(message):
    try:
        print(f"📩 Mensagem recebida: {message.text}")  # Depuração

        id_usuario = message.chat.id
        args = message.text.split()

        if len(args) != 2:
            bot.reply_to(message, "Uso correto: /busco <id_carta>")
            return

        id_carta = args[1]
        print(f"🔍 Usuário {id_usuario} busca a carta {id_carta}")  # Depuração

        # Conectar ao banco de dados
        conn, cursor = conectar_banco_dados()

        # Cadastrar a busca
        if cadastrar_busca(id_usuario, id_carta, cursor, conn):
            bot.reply_to(message, f"✅ Você está buscando a carta {id_carta}. "
                                  "Você será notificado quando alguém a oferecer.")
        else:
            bot.reply_to(message, "❌ Erro ao cadastrar a busca. Tente novamente.")

        cursor.close()
        conn.close()

    except Exception as e:
        erro = traceback.format_exc()
        bot.send_message(grupodeerro, f"Erro no comando /busco: {e}\n{erro}", parse_mode="HTML")
@bot.message_handler(commands=['oficina'])       
def oficina(message):
    try:
        # Extrair o ID do card da mensagem
        comandos = message.text.split()
        if len(comandos) < 2:
            bot.reply_to(message, "Por favor, forneça o ID do card.")
            return

        id_carta = comandos[1]
        id_usuario = message.from_user.id

        # Conectar ao banco de dados
        conn, cursor = conectar_banco_dados()

        # Obter nome e subcategoria do personagem
        cursor.execute("""
            SELECT nome, subcategoria FROM personagens WHERE id_personagem = %s
        """, (id_carta,))
        personagem = cursor.fetchone()

        if not personagem:
            bot.reply_to(message, "Personagem não encontrado.")
            return

        nome, subcategoria = personagem

        # Verificar se o preço já foi definido
        cursor.execute("""
            SELECT canela, po_estrela, glitter, cola
            FROM precos_cartas
            WHERE id_personagem = %s
        """, (id_carta,))
        preco_existente = cursor.fetchone()

        if preco_existente:
            canela, estrela, glitter, cola = preco_existente
        else:
            # Gerar preços aleatórios
            canela = random.randint(1, 10)
            estrela = random.randint(1, 10)
            glitter = random.randint(1, 10)
            cola = random.randint(1, 10)

            # Inserir os preços no banco de dados
            cursor.execute("""
                INSERT INTO precos_cartas (id_personagem, canela, po_estrela, glitter, cola)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_carta, canela, estrela, glitter, cola))
            conn.commit()

        # Verificar se o usuário possui os materiais necessários
        possui_materiais_suficientes = possui_materiais(id_usuario, canela, estrela, glitter, cola)

        if possui_materiais_suficientes:
            # Criar mensagem com botões (caso o usuário tenha os materiais)
            mensagem = (
                f"🐟 <b>{id_carta} - {nome} de {subcategoria}</b>\n\n"
                "Este peixe custa:\n"
                f"🍯 <b>{canela} Canelas</b>\n"
                f"🌟 <b>{estrela} Pó de Estrela</b>\n"
                f"✨ <b>{glitter} Glitter</b>\n"
                f"✂️ <b>{cola} Cola</b>\n\n"
                "<b>Deseja fazê-lo na oficina?</b>"
            )

            # Criar botões de "Sim" e "Cancelar" com callbacks específicos
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(
                InlineKeyboardButton("Sim", callback_data=f"card_confirmar_{id_carta}"),
                InlineKeyboardButton("Cancelar", callback_data=f"card_cancelar_{id_carta}")
            )
        else:
            # Criar mensagem SEM botões (caso o usuário não tenha os materiais)
            mensagem = (
                f"Você não possui materiais suficientes para criar este peixe.\n\n"
                f"🐟 <b>{id_carta} - {nome} de {subcategoria}</b>\n\n"
                "Este peixe custa:\n"
                f"🍯 <b>{canela} Canelas</b>\n"
                f"🌟 <b>{estrela} Pó de Estrela</b>\n"
                f"✨ <b>{glitter} Glitter</b>\n"
                f"✂️ <b>{cola} Cola</b>"
            )
            markup = None  # Não incluir botões

        # Obter imagem do card
        imagem_info = obter_imagem_id(id_carta, 0)
        if imagem_info:
            imagem, emoji, nome, id_personagem = imagem_info

            # Enviar a foto com a mensagem (com ou sem botões, dependendo da lógica acima)
            bot.send_photo(
                chat_id=message.chat.id,
                photo=imagem,
                caption=mensagem,
                reply_markup=markup,
                parse_mode="HTML"
            )
        else:
            bot.reply_to(message, "Imagem do card não encontrada.")

    except Exception as e:
        erro = traceback.format_exc()
        bot.send_message(
            message.chat.id,
            f"❌ Ocorreu um erro ao processar o card:\n{e}\n{erro}",
            parse_mode="HTML"
        )
    finally:
        fechar_conexao(cursor, conn)
        
@cached(cache_precos_cartas)
def listar_precos_cartas():
    """
    Retorna todos os preços das cartas armazenados no banco.
    """
    try:
        conn, cursor = conectar_banco_dados()
        query = """
            SELECT id_personagem, nome, canela, po_estrela, glitter, cola
            FROM precos_cartas
        """
        cursor.execute(query)
        precos = cursor.fetchall()
        return precos
    except Exception as e:
        print(f"Erro ao listar preços: {e}")
        return []
    finally:
        fechar_conexao(cursor, conn)
@bot.message_handler(commands=['pesca', 'pescar'])
def handle_pescar(message):
    pescar(message)

# Cache de resultados para melhorar a performance
def listar_precos_paginado(pagina=1, itens_por_pagina=15):
    """
    Retorna uma página dos preços das cartas da lista fixa.
    """
    try:
        total_cartas = len(PRECOS_CARTAS_FIXOS)
        total_paginas = (total_cartas // itens_por_pagina) + (1 if total_cartas % itens_por_pagina > 0 else 0)

        # Calcular o intervalo da página
        start_index = (pagina - 1) * itens_por_pagina
        end_index = start_index + itens_por_pagina

        # Extrair a página atual
        precos_pagina = PRECOS_CARTAS_FIXOS[start_index:end_index]

        return precos_pagina, total_paginas
    except Exception as e:
        print(f"Erro ao listar preços paginados: {e}")
        return [], 0

        
@bot.message_handler(commands=['preco'])
def exibir_preco_carta(message):
    try:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "❌ Por favor, use o comando no formato: /preco <ID da carta>")
            return

        id_carta = args[1]

        conn, cursor = conectar_banco_dados()

        # Verifica se o preço já foi definido
        cursor.execute("""
            SELECT canela, po_estrela, glitter, cola
            FROM precos_cartas
            WHERE id_personagem = %s
        """, (id_carta,))
        preco_existente = cursor.fetchone()

        if preco_existente:
            canela, estrela, glitter, cola = preco_existente
            bot.reply_to(message, f"💰 Preço da carta ID {id_carta}:\n🍯 Canela: {canela}\n🌟 Pó de Estrela: {estrela}\n✨ Glitter: {glitter}\n✂️ Cola: {cola}")
        else:
            # Gera um preço aleatório e salva
            preco_canela = random.randint(1, 5)  # Ajuste os intervalos conforme necessário
            preco_estrela = random.randint(1, 5)
            glitter = random.randint(1, 5)
            cola = random.randint(1, 5)
            cursor.execute("""
                INSERT INTO precos_cartas (id_personagem, canela, po_estrela, glitter, cola)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                canela = VALUES(canela),
                po_estrela = VALUES(po_estrela),
                glitter = VALUES(glitter),
                cola = VALUES(cola)
            """, (id_carta, preco_canela, preco_estrela, glitter, cola))
            conn.commit()
            bot.reply_to(message, f"✨ Preço gerado para a carta ID {id_carta}:\n🍯 Canela: {preco_canela}\n🌟 Pó de Estrela: {preco_estrela}\n✨ Glitter: {glitter}\n✂️ Cola: {cola}")

    except Exception as e:
        print(f"Erro ao exibir/gerar preço da carta: {e}")
        bot.reply_to(message, "❌ Ocorreu um erro ao tentar exibir o preço da carta.")
    finally:
        fechar_conexao(cursor, conn)
@bot.callback_query_handler(func=lambda call: call.data.startswith("comando_pescar"))
def callback_pescar(call):
    try:
        # Criar um objeto de mensagem fictício para reutilizar a função `pescar`
        message = call.message
        message.from_user = call.from_user  # Substituir o from_user pelo usuário que clicou no botão
        
        # Chamar a função de pesca
        pescar(message)
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Erro no callback do botão de pesca: {error_details}")
        bot.send_message(call.message.chat.id, "Ocorreu um erro ao tentar realizar a pesca novamente.")
    
def callback_subcategory(call):
    try:
        subcategory_data = call.data.split("_")
        subcategory = subcategory_data[1]
        card = get_random_card_valentine(subcategory)
        if card:
            evento_aleatorio = card
            send_card_message(call.message, evento_aleatorio)
        else:
            bot.answer_callback_query(call.id, "Ocorreu um erro ao processar sua solicitação. Tente novamente mais tarde.")
    except Exception as e:
        newrelic.agent.record_exception()    
        print(f"Erro ao processar callback de subcategoria: {e}")
        traceback.print_exc()
        
def verificar_cenouras(user_id):
    # Consulta para verificar quantas cenouras o usuário possui
    conn, cursor = conectar_banco_dados()
    cursor.execute("SELECT cenouras FROM usuarios WHERE id_usuario = %s", (user_id,))
    resultado = cursor.fetchone()
    fechar_conexao(cursor, conn)
    return resultado[0] if resultado else 0

@bot.callback_query_handler(func=lambda call: call.data.startswith("evento_"))
def callback_evento_navegacao(call):
    try:
        # Extraindo informações do callback_data
        _, tipo, pagina, evento, id_usuario = call.data.split("_")
        pagina = int(pagina)
        id_usuario = int(id_usuario)

        # Buscar subcategoria, total de personagens e exibir página atual
        nome_usuario = call.from_user.first_name

        if tipo == 's':
            # Personagens possuídos no evento
            ids_personagens = obter_ids_personagens_evento_inventario(id_usuario, evento)
            total_personagens = obter_total_personagens_evento(evento)
            total_paginas = (len(ids_personagens) // 15) + (1 if len(ids_personagens) % 15 > 0 else 0)
            mostrar_pagina_evento_s(message, evento, id_usuario, pagina)
        elif tipo == 'f':
            # Personagens faltantes no evento
            ids_personagens_faltantes = obter_ids_personagens_evento_faltantes(id_usuario, evento)
            total_personagens = obter_total_personagens_evento(evento)
            total_paginas = (len(ids_personagens_faltantes) // 15) + (1 if len(ids_personagens_faltantes) % 15 > 0 else 0)
            mostrar_pagina_evento_f(call.message, evento, id_usuario, pagina, total_paginas, ids_personagens_faltantes, total_personagens, nome_usuario, call)

    except Exception as e:
        print(f"Erro no callback de navegação do evento: {e}")

def comprar_carta(user_id, carta_id):
    # Desconta as cenouras e adiciona a carta ao inventário do usuário
    conn, cursor = conectar_banco_dados()
    cursor.execute("UPDATE usuarios SET cenouras = cenouras - 10 WHERE id_usuario = %s", (user_id,))
    cursor.execute("INSERT INTO colecao_usuario (id_usuario, id_personagem) VALUES (%s, %s)", (user_id, carta_id))
    conn.commit()
    fechar_conexao(cursor, conn)

def obter_cartas_por_categoria(categoria):
    # Consulta para obter as cartas disponíveis de uma categoria específica
    conn, cursor = conectar_banco_dados()
    cursor.execute(
        "SELECT id_personagem, nome, imagem, emoji FROM personagens WHERE categoria = %s AND imagem IS NOT NULL ORDER BY RAND() LIMIT 6",
        (categoria,)
    )
    cartas = [{"id": row[0], "nome": row[1], "imagem": row[2], "emoji": row[3]} for row in cursor.fetchall()]
    fechar_conexao(cursor, conn)
    return cartas

processing_lock = threading.Lock()
# Função de callback para processar navegação
@bot.callback_query_handler(func=lambda call: call.data.startswith('vendinha_'))
def processar_callback_cartas_compradas(call):
    # Extraímos a página e ID do callback data
    _, pagina_str, id_usuario_str = call.data.split('_')
    pagina_atual = int(pagina_str)
    id_usuario = int(id_usuario_str)

    # Verificar se o usuário tem cartas salvas no cache para navegação
    if id_usuario in globals.cartas_compradas_dict:
        cartas = globals.cartas_compradas_dict[id_usuario]
        mostrar_cartas_compradas(call.message.chat.id, cartas, id_usuario, pagina_atual, call.message.message_id)
    else:
        bot.send_message(call.message.chat.id, "Erro ao exibir cartas compradas. Tente novamente.")
@bot.callback_query_handler(func=lambda call: call.data.startswith("cesta_"))
def callback_query_cesta(call):
    global processing_lock

    # Log para confirmar que o callback foi chamado
    print(f"Callback acionado com dados: {call.data}")

    if not processing_lock.acquire(blocking=False):
        print("Processando outra requisição, bloqueio ativo.")
        return

    try:
        # Dividir o callback data em partes
        parts = call.data.split('_')
        print(f"Dados divididos em partes: {parts}")

        # Verificar se todas as partes necessárias estão presentes
        if len(parts) < 5:
            print("Erro: Dados insuficientes em parts.")
            bot.answer_callback_query(call.id, "Erro ao processar a navegação.")
            return

        # Extrair informações da mensagem
        tipo = parts[1]
        pagina = int(parts[2])
        categoria = parts[3]
        id_usuario_original = int(parts[4])
        nome_usuario = bot.get_chat(id_usuario_original).first_name
        print(f"Tipo: {tipo}, Página: {pagina}, Categoria: {categoria}, ID Usuário: {id_usuario_original}")

        # Lógica de navegação baseada no tipo de consulta
        if tipo == 's':
            ids_personagens = obter_ids_personagens_inventario_sem_evento(id_usuario_original, categoria)
            total_personagens_subcategoria = obter_total_personagens_subcategoria(categoria)
            total_registros = len(ids_personagens)

            if total_registros > 0:
                total_paginas = (total_registros // 15) + (1 if total_registros % 15 > 0 else 0)
                mostrar_pagina_cesta_s(call.message, categoria, id_usuario_original, pagina, total_paginas, ids_personagens, total_personagens_subcategoria, nome_usuario, call=call)
            else:
                bot.answer_callback_query(call.id, f"Nenhum personagem encontrado na cesta '{categoria}'.")

        elif tipo == 'f':
            ids_personagens_faltantes = obter_ids_personagens_faltantes_sem_evento(id_usuario_original, categoria)
            total_personagens_subcategoria = obter_total_personagens_subcategoria(categoria)
            total_registros = len(ids_personagens_faltantes)

            if total_registros > 0:
                total_paginas = (total_registros // 15) + (1 if total_registros % 15 > 0 else 0)
                mostrar_pagina_cesta_f(call.message, categoria, id_usuario_original, pagina, total_paginas, ids_personagens_faltantes, total_personagens_subcategoria, nome_usuario, call=call)
            else:
                bot.answer_callback_query(call.id, f"Todos os personagens na subcategoria '{categoria}' estão no seu inventário.")

        # Outros tipos de tratamento de navegação
        elif tipo == 'se':
            ids_personagens = obter_ids_personagens_inventario_com_evento(id_usuario_original, categoria)
            total_personagens_com_evento = obter_total_personagens_subcategoria(categoria)
            total_registros = len(ids_personagens)

            if total_registros > 0:
                total_paginas = (total_registros // 15) + (1 if total_registros % 15 > 0 else 0)
                mostrar_pagina_cesta_s(call.message, categoria, id_usuario_original, pagina, total_paginas, ids_personagens, total_personagens_com_evento, nome_usuario, call=call)
            else:
                bot.answer_callback_query(call.id, f"Nenhum personagem encontrado na cesta '{categoria}'.")

        elif tipo == 'fe':
            ids_personagens_faltantes = obter_ids_personagens_faltantes_com_evento(id_usuario_original, categoria)
            total_personagens_subcategoria = obter_total_personagens_subcategoria(categoria)
            total_registros = len(ids_personagens_faltantes)

            if total_registros > 0:
                total_paginas = (total_registros // 15) + (1 if total_registros % 15 > 0 else 0)
                mostrar_pagina_cesta_f(call.message, categoria, id_usuario_original, pagina, total_paginas, ids_personagens_faltantes, total_personagens_subcategoria, nome_usuario, call=call)
            else:
                bot.answer_callback_query(call.id, f"Todos os personagens na subcategoria '{categoria}' estão no seu inventário.")

        elif tipo == 'c':
            ids_personagens = obter_ids_personagens_categoria(id_usuario_original, categoria)
            total_personagens_categoria = obter_total_personagens_categoria(categoria)
            total_registros = len(ids_personagens)

            if total_registros > 0:
                total_paginas = (total_registros // 15) + (1 if total_registros % 15 > 0 else 0)
                mostrar_pagina_cesta_c(call.message, categoria, id_usuario_original, pagina, total_paginas, ids_personagens, total_personagens_categoria, nome_usuario, call=call)
            else:
                bot.answer_callback_query(call.id, f"Nenhum personagem encontrado na categoria '{categoria}'.")

        elif tipo == 'cf':
            ids_personagens_faltantes = obter_ids_personagens_faltantes_categoria(id_usuario_original, categoria)
            total_personagens_categoria = obter_total_personagens_categoria(categoria)
            total_registros = len(ids_personagens_faltantes)

            if total_registros > 0:
                total_paginas = (total_registros // 15) + (1 if total_registros % 15 > 0 else 0)
                mostrar_pagina_cesta_cf(call.message, categoria, id_usuario_original, pagina, total_paginas, ids_personagens_faltantes, total_personagens_categoria, nome_usuario, call=call)
            else:
                bot.answer_callback_query(call.id, f"Você possui todos os personagens na categoria '{categoria}'.")

    except Exception as e:
        print(f"Erro ao processar callback da cesta: {e}")
        bot.answer_callback_query(call.id, "Erro ao processar o callback.")
    finally:
        processing_lock.release()
def handle_callback_query_evento(call):
    data_parts = call.data.split('_')
    action = data_parts[1]
    id_usuario_inicial = int(data_parts[2])
    evento = data_parts[3]
    page = int(data_parts[4])
    
    try:
        conn, cursor = conectar_banco_dados()

        # Verificar a ação de navegação: anterior ou próxima página
        if action == "prev":
            page -= 1
        elif action == "next":
            page += 1

        # Selecionar a função correta para o tipo de evento (s para "tem" e f para "falta")
        if call.message.text.startswith('🌾'):
            resposta_completa = comando_evento_s(id_usuario_inicial, evento, cursor, call.from_user.first_name, page)
        else:
            resposta_completa = comando_evento_f(id_usuario_inicial, evento, cursor, call.from_user.first_name, page)

        if isinstance(resposta_completa, tuple):
            subcategoria_pesquisada, lista, total_pages = resposta_completa
            # Corrigir a página e exibir apenas se estiver dentro do total
            if page > total_pages:
                bot.answer_callback_query(call.id, "Não há mais páginas.")
                return

            resposta = f"{lista}\n\nPágina {page} de {total_pages}"

            # Definir botões de navegação
            markup = InlineKeyboardMarkup()
            if page > 1:
                markup.add(InlineKeyboardButton("Anterior", callback_data=f"evt_prev_{id_usuario_inicial}_{evento}_{page - 1}"))
            if page < total_pages:
                markup.add(InlineKeyboardButton("Próxima", callback_data=f"evt_next_{id_usuario_inicial}_{evento}_{page + 1}"))

            bot.edit_message_text(resposta, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
        
        else:
            # Caso não tenha resultados, exibir mensagem apropriada e desativar a navegação
            bot.edit_message_text(resposta_completa, chat_id=call.message.chat.id, message_id=call.message.message_id)

    except Exception as e:
        traceback.print_exc()
    finally:
        fechar_conexao(cursor, conn)

def diminuir_cenouras(user_id, quantidade):
    conn, cursor = conectar_banco_dados()
    try:
        cursor.execute("SELECT cenouras FROM usuarios WHERE id_usuario = %s", (user_id,))
        cenouras = cursor.fetchone()
        
        if cenouras and cenouras[0] >= quantidade:
            cursor.execute("UPDATE usuarios SET cenouras = cenouras - %s WHERE id_usuario = %s", (quantidade, user_id))
            conn.commit()
            cursor.execute("SELECT cenouras FROM usuarios WHERE id_usuario = %s", (user_id,))
            cenouras_restantes = cursor.fetchone()[0]
            
            return True, cenouras_restantes
        else:
            return False, cenouras[0] if cenouras else 0  
    except Exception as e:
        print(f"Erro ao diminuir cenouras: {e}")
        return False, 0
    finally:
        fechar_conexao(cursor, conn)

@bot.callback_query_handler(func=lambda call: call.data.startswith("aprovar_tag_") or call.data.startswith("reprovar_tag_"))
def callback_personalizacao_tag(call):
    try:
        # Dividir o callback_data para obter os detalhes
        data_parts = call.data.split('_')
        print(f"DEBUG: Callback recebido - {call.data}")  # Log do callback recebido
        print(f"DEBUG: Partes do callback - {data_parts}")  # Log das partes separadas

        # Verificar se o callback contém o número esperado de partes
        if len(data_parts) != 4:
            bot.answer_callback_query(call.id, "Formato de callback incorreto. Tente novamente.")
            print(f"DEBUG: Formato incorreto detectado. Tamanho de data_parts: {len(data_parts)}")
            return

        # Extrair os dados do callback
        acao = data_parts[0]  # "aprovar" ou "reprovar"
        id_usuario = int(data_parts[2])  # ID do usuário
        nometag = data_parts[3]  # Nome da tag

        print(f"DEBUG: Ação - {acao}, ID Usuário - {id_usuario}, Nome Tag - {nometag}")  # Log para verificação

        conn, cursor = conectar_banco_dados()

        if acao == "aprovar":
            # Aprovar personalização
            cursor.execute("""
                UPDATE personalizacoes_tags 
                SET aprovado = 1 
                WHERE id_usuario = %s AND nometag = %s
            """, (id_usuario, nometag))
            conn.commit()
            bot.answer_callback_query(call.id, f"Personalização para a tag {nometag} aprovada.")
            bot.send_message(call.message.chat.id, f"✔️ A personalização para a tag <b>{nometag}</b> foi aprovada!", parse_mode="HTML")

        elif acao == "reprovar":
            # Reprovar personalização
            cursor.execute("""
                DELETE FROM personalizacoes_tags 
                WHERE id_usuario = %s AND nometag = %s
            """, (id_usuario, nometag))
            conn.commit()
            bot.answer_callback_query(call.id, f"Personalização para a tag {nometag} reprovada.")
            bot.send_message(call.message.chat.id, f"❌ A personalização para a tag <b>{nometag}</b> foi reprovada!", parse_mode="HTML")

        # Apagar os botões de aprovação/reprovação
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    except Exception as e:
        bot.answer_callback_query(call.id, "Erro ao processar callback.")
        print(f"Erro no callback de personalização da tag: {e}")
        traceback.print_exc()
    finally:
        fechar_conexao(cursor, conn)



@bot.message_handler(commands=['deltagimg'])
def handle_deltagimg(message):
    try:
        partes_comando = message.text.split(maxsplit=1)
        if len(partes_comando) < 2:
            bot.send_message(message.chat.id, "Use o formato: /deltagimg <nometag>")
            return

        nometag = partes_comando[1].strip()
        id_usuario = message.from_user.id

        conn, cursor = conectar_banco_dados()

        cursor.execute(
            "DELETE FROM personalizacoes_tags WHERE id_usuario = %s AND nometag = %s",
            (id_usuario, nometag),
        )
        if cursor.rowcount > 0:
            bot.send_message(message.chat.id, f"A personalização da tag '{nometag}' foi removida.")
        else:
            bot.send_message(message.chat.id, "Você não possui nenhuma personalização para essa tag.")

        conn.commit()

    except Exception as e:
        print(f"Erro no comando /deltagimg: {e}")
        bot.send_message(message.chat.id, f"Erro ao remover a personalização: {e}")
    finally:
        fechar_conexao(cursor, conn)

@bot.message_handler(commands=['settag'])
def handle_settag(message):
    try:
        if '|' not in message.text:
            bot.send_message(
                message.chat.id,
                "Formato inválido. Use o comando no formato:\n<b>/settag tag_name | link</b>",
                parse_mode="HTML"
            )
            return

        # Extrair tag e link
        command_parts = message.text.split('|', 1)
        nometag = command_parts[0].replace('/settag', '').strip()
        link = command_parts[1].strip()

        if not nometag or not link:
            bot.send_message(
                message.chat.id,
                "Formato inválido. Certifique-se de fornecer a tag e o link separados por '|'.",
                parse_mode="HTML"
            )
            return

        id_usuario = message.from_user.id
        username = message.from_user.username

        # Verificar se o link é válido
        if not re.match(r'^https?://\S+$', link):
            bot.send_message(
                message.chat.id,
                "Por favor, forneça um link válido para a personalização.",
                parse_mode="HTML"
            )
            return

        conn, cursor = conectar_banco_dados()

        # Verificar se a tag existe
        cursor.execute("SELECT COUNT(*) FROM tags WHERE nometag = %s AND id_usuario = %s", (nometag, id_usuario))
        tag_existe = cursor.fetchone()[0]

        if not tag_existe:
            bot.send_message(
                message.chat.id,
                f"A tag <b>{nometag}</b> não existe. Verifique se o nome está correto.",
                parse_mode="HTML"
            )
            fechar_conexao(cursor, conn)
            return

        # Registrar a personalização no banco de dados
        cursor.execute("""
            INSERT INTO personalizacoes_tags (id_usuario, nometag, link, aprovado)
            VALUES (%s, %s, %s, 0)
            ON DUPLICATE KEY UPDATE link = VALUES(link), aprovado = 0
        """, (id_usuario, nometag, link))
        conn.commit()

        # Confirmar ao usuário que o pedido foi registrado
        bot.send_message(
            message.chat.id,
            f"Sua personalização para a tag <b>{nometag}</b> foi registrada e está aguardando aprovação!",
            parse_mode="HTML"
        )

        # Enviar para o grupo de aprovação
        grupo_id = -1002144134360  # Substitua pelo ID do grupo de aprovação
        enviar_mensagem_aprovacao_tag(grupo_id, id_usuario, username, nometag, link)

    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao processar o comando /settag: {e}")
        traceback.print_exc()
    finally:
        fechar_conexao(cursor, conn)

def enviar_mensagem_aprovacao_tag(grupo_id, id_usuario, username, nometag, link):
    try:
        # Mensagem formatada para o grupo de aprovação
        mensagem = (
            f"📝 Nova solicitação de personalização para a tag!\n\n"
            f"👤 Usuário: @{username} (ID: {id_usuario})\n"
            f"🔖 Tag: {nometag}\n"
            f"🔗 Link: {link}\n\n"
            f"🛠️ Ações de Aprovação/Rejeição:"
        )

        # Criar botões para aprovação/reprovação
        markup = telebot.types.InlineKeyboardMarkup()
        callback_aprovar = f"aprovar_tag_{id_usuario}_{nometag}"
        callback_reprovar = f"reprovar_tag_{id_usuario}_{nometag}"
        btn_aprovar = telebot.types.InlineKeyboardButton("✔️ Aprovar", callback_data=callback_aprovar)
        btn_reprovar = telebot.types.InlineKeyboardButton("❌ Reprovar", callback_data=callback_reprovar)
        markup.add(btn_aprovar, btn_reprovar)

        # Enviar mensagem para o grupo
        bot.send_message(grupo_id, mensagem, reply_markup=markup, parse_mode="HTML")
        print(f"Mensagem enviada para o grupo de aprovação. Grupo ID: {grupo_id}")

    except Exception as e:
        print(f"Erro ao enviar mensagem para o grupo: {e}")
        traceback.print_exc()

@bot.message_handler(commands=['setcesta'])
def handle_setcesta(message):
    try:
        # Verificar formato do comando
        if '|' not in message.text:
            bot.send_message(
                message.chat.id,
                "Formato inválido. Use o comando no formato:\n<b>/setcesta subcategoria | link</b>",
                parse_mode="HTML"
            )
            return

        # Extrair subcategoria e link
        command_parts = message.text.split('|', 1)
        subcategoria = command_parts[0].replace('/setcesta', '').strip()
        link = command_parts[1].strip()

        if not subcategoria or not link:
            bot.send_message(
                message.chat.id,
                "Formato inválido. Certifique-se de fornecer a subcategoria e o link separados por '|'.",
                parse_mode="HTML"
            )
            return

        id_usuario = message.from_user.id
        username = message.from_user.username
        message_id = message.message_id

        conn, cursor = conectar_banco_dados()

        # Verificar se a subcategoria existe
        cursor.execute("SELECT COUNT(*) FROM subcategorias WHERE subcategoria = %s", (subcategoria,))
        subcategoria_existe = cursor.fetchone()[0]

        if not subcategoria_existe:
            bot.send_message(
                message.chat.id,
                f"A subcategoria <b>{subcategoria}</b> não existe. Verifique se o nome está correto.",
                parse_mode="HTML"
            )
            fechar_conexao(cursor, conn)
            return

        # Verificar se o usuário tem a coleção completa
        cursor.execute("""
            SELECT COUNT(*) 
            FROM personagens p
            WHERE p.subcategoria = %s
              AND p.id_personagem NOT IN (
                  SELECT id_personagem
                  FROM inventario
                  WHERE id_usuario = %s
              )
        """, (subcategoria, id_usuario))
        falta_count = cursor.fetchone()[0]

        if falta_count > 0:
            bot.send_message(
                message.chat.id,
                f"Você ainda não completou a coleção da subcategoria <b>{subcategoria}</b>. Complete a coleção antes de personalizar sua cesta.",
                parse_mode="HTML"
            )
            fechar_conexao(cursor, conn)
            return

        # Verificar se o link é válido
        if not re.match(r'^https?://\S+$', link):
            bot.send_message(
                message.chat.id,
                "Por favor, forneça um link válido para a personalização.",
                parse_mode="HTML"
            )
            fechar_conexao(cursor, conn)
            return

        # Registrar a personalização no banco de dados
        cursor.execute("""
            INSERT INTO personalizacoes_cesta (id_usuario, subcategoria, link, aprovado)
            VALUES (%s, %s, %s, 0)
            ON DUPLICATE KEY UPDATE link = VALUES(link), aprovado = 0
        """, (id_usuario, subcategoria, link))
        conn.commit()

        # Confirmar ao usuário que o pedido foi registrado
        bot.send_message(
            message.chat.id,
            f"Sua personalização para a subcategoria <b>{subcategoria}</b> foi registrada e está aguardando aprovação!",
            parse_mode="HTML"
        )

        # Enviar para aprovação
        grupo_id = -1002144134360  # Substitua pelo ID do grupo de aprovação
        enviar_mensagem_aprovacao_cesta(grupo_id, id_usuario, subcategoria, link, username, message_id)

    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao processar o comando /setcesta: {e}")
        traceback.print_exc()
    finally:
        fechar_conexao(cursor, conn)

@bot.message_handler(commands=['delcesta'])
def handle_delcesta(message):
    try:
        partes_comando = message.text.split(maxsplit=1)
        if len(partes_comando) < 2:
            bot.send_message(message.chat.id, "Use o formato: /delcesta <subcategoria>")
            return

        subcategoria = partes_comando[1].strip()
        id_usuario = message.from_user.id

        conn, cursor = conectar_banco_dados()

        # Excluir a personalização da subcategoria
        cursor.execute(
            "DELETE FROM personalizacoes_cesta WHERE id_usuario = %s AND subcategoria = %s",
            (id_usuario, subcategoria),
        )
        if cursor.rowcount > 0:
            bot.send_message(message.chat.id, f"A personalização da cesta de {subcategoria} foi removida.")
        else:
            bot.send_message(message.chat.id, "Você não possui nenhuma personalização para essa subcategoria.")

        conn.commit()

    except Exception as e:
        print(f"Erro no comando /delcesta: {e}")
        bot.send_message(message.chat.id, f"Erro ao remover a personalização: {e}")
    finally:
        fechar_conexao(cursor, conn)
@bot.callback_query_handler(func=lambda call: call.data.startswith("aprovar_cesta_") or call.data.startswith("reprovar_cesta_"))
def callback_personalizacao_cesta(call):
    try:
        # Validar o formato do callback data
        data_parts = call.data.split("_", 3)
        if len(data_parts) < 4:
            bot.send_message(call.message.chat.id, "Formato de callback incorreto. Tente novamente.")
            print(f"Formato de callback incorreto: {call.data}")
            return

        acao = data_parts[0]
        id_usuario = int(data_parts[2])
        subcategoria = data_parts[3].rsplit("_", 1)[0]  # Extraí o subcategoria corretamente
        message_id = data_parts[3].rsplit("_", 1)[-1]

        conn, cursor = conectar_banco_dados()

        # Processar a ação
        if acao == "aprovar":
            # Aprovar personalização
            cursor.execute("""
                UPDATE personalizacoes_cesta 
                SET aprovado = 1 
                WHERE id_usuario = %s AND subcategoria = %s
            """, (id_usuario, subcategoria))
            conn.commit()

            # Avisar o usuário que sua personalização foi aprovada
            bot.send_message(id_usuario, f"🎉 Sua personalização para a subcategoria <b>{subcategoria}</b> foi aprovada!", parse_mode="HTML")

            # Criar mensagem no grupo para confirmar a aprovação
            mensagem_aprovada = (
                f"✅ <b>Personalização Aprovada!</b>\n\n"
                f"👤 Usuário: {id_usuario}\n"
                f"📂 Subcategoria: {subcategoria}\n"
                f"🔗 Link: Aprovado."
            )
            bot.send_message(call.message.chat.id, mensagem_aprovada, parse_mode="HTML")

        elif acao == "reprovar":
            # Reprovar personalização
            cursor.execute("""
                DELETE FROM personalizacoes_cesta 
                WHERE id_usuario = %s AND subcategoria = %s
            """, (id_usuario, subcategoria))
            conn.commit()

            # Criar mensagem no grupo para confirmar a rejeição
            mensagem_reprovada = (
                f"❌ <b>Personalização Rejeitada!</b>\n\n"
                f"👤 Usuário: {id_usuario}\n"
                f"📂 Subcategoria: {subcategoria}\n"
                f"🔗 Link: Removido."
            )
            bot.send_message(call.message.chat.id, mensagem_reprovada, parse_mode="HTML")

        # Apagar a mensagem original com os botões
        bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as e:
        bot.send_message(call.message.chat.id, f"Erro ao processar callback: {e}")
        print(f"Erro no callback de personalização da cesta: {e}")
        traceback.print_exc()
    finally:
        fechar_conexao(cursor, conn)

def enviar_mensagem_aprovacao_cesta(grupo_id, id_usuario, subcategoria, link, username, message_id):
    try:
        # Mensagem para o grupo com formatação específica
        mensagem = (
            f"📝 Nova solicitação de personalização para cesta!\n\n"
            f"👤 Usuário: {username} (ID: {id_usuario})\n"
            f"📂 Subcategoria: {subcategoria}\n"
            f"🔗 Link: {link}\n\n"
            f"🛠️ Ações de Aprovação/Rejeição:"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        callback_aprovar = f"aprovar_cesta_{id_usuario}_{subcategoria}_{message_id}"
        callback_reprovar = f"reprovar_cesta_{id_usuario}_{subcategoria}_{message_id}"
        btn_aprovar = telebot.types.InlineKeyboardButton("✔️ Aprovar", callback_data=callback_aprovar)
        btn_reprovar = telebot.types.InlineKeyboardButton("❌ Reprovar", callback_data=callback_reprovar)
        markup.add(btn_aprovar, btn_reprovar)

        bot.send_message(grupo_id, mensagem, reply_markup=markup, parse_mode="HTML")
    except Exception as e:
        print(f"Erro ao enviar mensagem para aprovação: {e}")
        traceback.print_exc()


@bot.message_handler(commands=['setgif'])
def handle_setgif(message):
    enviar_gif(message)

def enviar_gif(message):
    try:
        comando = message.text.split('/setgif', 1)[1].strip().lower()
        partes_comando = comando.split(' ')
        id_personagem = partes_comando[0]
        id_usuario = message.from_user.id

        conn, cursor = conectar_banco_dados()

        # Verificar se o usuário possui 30 unidades da carta
        cursor.execute("SELECT quantidade FROM inventario WHERE id_usuario = %s AND id_personagem = %s", (id_usuario, id_personagem))
        resultado = cursor.fetchone()
        if not resultado or resultado[0] < 30:
            bot.send_message(message.chat.id, "Você precisa ter pelo menos 30 unidades dessa carta para enviar um gif.")
            fechar_conexao(cursor, conn)
            return

        if 'eusoqueriasernormal' not in partes_comando:
            tempo_restante = verifica_tempo_ultimo_gif(id_usuario)
            if tempo_restante:
                bot.send_message(message.chat.id, f"Você já enviou um gif recentemente. Aguarde {tempo_restante} antes de enviar outro.")
                fechar_conexao(cursor, conn)
                return

        bot.send_message(message.chat.id, "Eba! Você pode escolher um gif!\nEnvie o link do gif gerado pelo @LinksdamabiBot:")

        # Armazena o estado global para o próximo handler
        globals.links_gif[id_usuario] = id_personagem

        # Registra o próximo step para capturar o link do GIF
        bot.register_next_step_handler(message, receber_link_gif, id_personagem)

        fechar_conexao(cursor, conn)

    except IndexError:
        bot.send_message(message.chat.id, "Por favor, forneça o ID do personagem.")
    except Exception as e:
        print(f"Erro ao processar o comando /setgif: {e}")
        fechar_conexao(cursor, conn)
def receber_link_gif(message, id_personagem):
    id_usuario = message.from_user.id

    if id_usuario:
        link_gif = message.text

        if not re.match(r'^https?://\S+$', link_gif):
            bot.send_message(message.chat.id, "Por favor, envie <b>apenas</b> o <b>link</b> do GIF.", parse_mode="HTML")
            return

        if id_usuario in globals.links_gif:
            id_personagem = globals.links_gif[id_usuario]

            if id_personagem:
                numero_personagem = id_personagem.split('_')[0]
                conn, cursor = conectar_banco_dados()

                sql_usuario = "SELECT nome_usuario, nome FROM usuarios WHERE id_usuario = %s"
                cursor.execute(sql_usuario, (id_usuario,))
                resultado_usuario = cursor.fetchone()

                sql_personagem = "SELECT nome, subcategoria FROM personagens WHERE id_personagem = %s"
                cursor.execute(sql_personagem, (numero_personagem,))
                resultado_personagem = cursor.fetchone()

                if resultado_usuario and resultado_personagem:
                    nome_usuario = resultado_usuario[0]
                    nome_personagem = resultado_personagem[0]
                    subcategoria_personagem = resultado_personagem[1]

                    sql_temp_insert = """
                        INSERT INTO temp_data (id_usuario, id_personagem, chave, valor)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE valor = VALUES(valor), chave = VALUES(chave)
                    """
                    chave = f"{id_usuario}_{numero_personagem}"
                    cursor.execute(sql_temp_insert, (id_usuario, numero_personagem, chave, link_gif))
                    conn.commit()
                    fechar_conexao(cursor, conn)

                    keyboard = telebot.types.InlineKeyboardMarkup()
                    btn_aprovar = telebot.types.InlineKeyboardButton(text="✔️ Aprovar", callback_data=f"aprovar_{id_usuario}_{numero_personagem}_{message.message_id}")
                    btn_reprovar = telebot.types.InlineKeyboardButton(text="❌ Reprovar", callback_data=f"reprovar_{id_usuario}_{numero_personagem}_{message.message_id}")

                    keyboard.row(btn_aprovar, btn_reprovar)
                    bot.forward_message(chat_id=-1002144134360, from_chat_id=message.chat.id, message_id=message.message_id)
                    chat_id = -1002144134360
                    mensagem = f"Pedido de aprovação de GIF:\n\n"
                    mensagem += f"ID Personagem: {numero_personagem}\n"
                    mensagem += f"{nome_personagem} de {subcategoria_personagem}\n\n"
                    mensagem += f"Usuário: @{message.from_user.username}\n"
                    mensagem += f"Nome: {nome_usuario}\n"

                    sent_message = bot.send_message(chat_id, mensagem, reply_markup=keyboard)
                    bot.send_message(message.chat.id, "Link do GIF registrado com sucesso. Aguardando aprovação.")
                    return sent_message.message_id
                else:
                    fechar_conexao(cursor, conn)
                    bot.send_message(message.chat.id, "Erro ao obter informações do usuário ou do personagem.")
            else:
                bot.send_message(message.chat.id, "Erro ao processar o link do GIF. Por favor, use o comando /setgif novamente.")
        else:
            bot.send_message(message.chat.id, "Erro ao processar o link do GIF. ID de usuário inválido.")
    else:
        bot.send_message(message.chat.id, "Erro ao processar o link do GIF. ID de usuário inválido.")

def adicionar_bonus_sorte(user_id, multiplicador_sorte, duracao_horas, chat_id):
    try:
        conn, cursor = conectar_banco_dados()
        fim_bonus = datetime.now() + timedelta(hours=duracao_horas)

        # Inserir ou atualizar o bônus de sorte na tabela 'boosts'
        cursor.execute("""
            INSERT INTO boosts (id_usuario, tipo_boost, multiplicador, fim_boost)
            VALUES (%s, 'sorte', %s, %s)
            ON DUPLICATE KEY UPDATE multiplicador = %s, fim_boost = %s
        """, (user_id, multiplicador_sorte, fim_bonus, multiplicador_sorte, fim_bonus))
        
        conn.commit()

    except Exception as e:
        print(f"Erro ao adicionar Bônus de Sorte: {e}")

    finally:
        fechar_conexao(cursor, conn)
        
# Armazenamento de jogadores no labirinto
jogadores_labirinto = {}

def gerar_labirinto_com_caminho_e_validacao(tamanho=10):
    labirinto = [['🪨' for _ in range(tamanho)] for _ in range(tamanho)]
    
    # Ponto inicial e final
    x, y = 1, 1  # Início
    saida_x, saida_y = tamanho - 2, random.randint(1, tamanho - 2)  # Saída aleatória na borda inferior
    
    # Caminho garantido até a saída usando backtracking
    caminho = [(x, y)]
    labirinto[x][y] = '⬜'
    
    while (x, y) != (saida_x, saida_y):
        direcoes = []
        if x > 1 and labirinto[x-1][y] == '🪨':
            direcoes.append((-1, 0))
        if x < tamanho - 2 and labirinto[x+1][y] == '🪨':
            direcoes.append((1, 0))
        if y > 1 and labirinto[x][y-1] == '🪨':
            direcoes.append((0, -1))
        if y < tamanho - 2 and labirinto[x][y+1] == '🪨':
            direcoes.append((0, 1))

        if not direcoes:
            x, y = caminho.pop()
        else:
            dx, dy = random.choice(direcoes)
            x += dx
            y += dy
            labirinto[x][y] = '⬜'
            caminho.append((x, y))

    # Define a saída
    labirinto[saida_x][saida_y] = '🚪'
    
    # Função para criar ramos extras em algumas áreas do labirinto
    def criar_caminho_ramificado(start_x, start_y, max_ramos=2):
        for _ in range(max_ramos):
            comprimento_ramo = random.randint(2, 3)  # Comprimento do ramo
            ramo_x, ramo_y = start_x, start_y
            for _ in range(comprimento_ramo):
                direcoes = [
                    (dx, dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if 1 <= ramo_x + dx < tamanho - 1 and 1 <= ramo_y + dy < tamanho - 1
                    and labirinto[ramo_x + dx][ramo_y + dy] == '🪨'
                ]
                if not direcoes:
                    break
                dx, dy = random.choice(direcoes)
                ramo_x, ramo_y = ramo_x + dx, ramo_y + dy
                labirinto[ramo_x][ramo_y] = '⬜'
    
    # Adicionar ramificações para complexidade
    for i in range(0, len(caminho), max(1, len(caminho) // 4)):
        criar_caminho_ramificado(*caminho[i])

    # Adicionar monstros e recompensas somente nos espaços abertos ('⬜')
    for _ in range(5):
        while True:
            mx, my = random.randint(1, tamanho - 2), random.randint(1, tamanho - 2)
            if labirinto[mx][my] == '⬜' and (mx, my) != (saida_x, saida_y):  # Não coloca sobre a saída
                labirinto[mx][my] = '👻'
                break
    
    for _ in range(3):
        while True:
            rx, ry = random.randint(1, tamanho - 2), random.randint(1, tamanho - 2)
            if labirinto[rx][ry] == '⬜' and (rx, ry) != (saida_x, saida_y):  # Não coloca sobre a saída
                labirinto[rx][ry] = '🎃'
                break

    return labirinto

# Função para mostrar o labirinto parcialmente, baseado na posição do jogador
def mostrar_labirinto(labirinto, posicao):
    mapa = ""
    x, y = posicao
    for i in range(len(labirinto)):
        for j in range(len(labirinto[i])):
            if (i, j) == posicao:
                mapa += "🔦"
            elif abs(x - i) <= 1 and abs(y - j) <= 1:
                mapa += labirinto[i][j]
            else:
                mapa += "⬛"
        mapa += "\n"
    return mapa

# Função para mover o jogador no labirinto
def mover_posicao(posicao_atual, direcao, labirinto):
    x, y = posicao_atual
    if direcao == 'norte' and x > 0 and labirinto[x - 1][y] != '🪨':
        return (x - 1, y)
    elif direcao == 'sul' and x < len(labirinto) - 1 and labirinto[x + 1][y] != '🪨':
        return (x + 1, y)
    elif direcao == 'leste' and y < len(labirinto[0]) - 1 and labirinto[x][y + 1] != '🪨':
        return (x, y + 1)
    elif direcao == 'oeste' and y > 0 and labirinto[x][y - 1] != '🪨':
        return (x, y - 1)
    return posicao_atual  # Movimento inválido, retorna posição atual



# Exemplo de como iniciar o labirinto com labirinto importado
def iniciar_labirinto(user_id, chat_id):
    try:
        labirinto = escolher_labirinto()
        posicao_inicial = (1, 1)
        movimentos_restantes = 35  # Limite de movimentos

        jogadores_labirinto[user_id] = {
            "labirinto": labirinto,
            "posicao": posicao_inicial,
            "movimentos": movimentos_restantes
        }

        mapa = mostrar_labirinto(labirinto, posicao_inicial)
        markup = criar_botoes_navegacao()
        
        bot.send_message(chat_id, f"🏰 Bem-vindo ao Labirinto! Você tem {movimentos_restantes} movimentos para escapar.\n\n{mapa}", reply_markup=markup)
    except Exception as e:
        print(f"Erro ao iniciar o labirinto: {e}")
        
# Função para criar botões de navegação
def criar_botoes_navegacao():
    markup = types.InlineKeyboardMarkup(row_width=4)
    markup.add(
        types.InlineKeyboardButton("⬆️", callback_data="norte"),
        types.InlineKeyboardButton("⬅️", callback_data="oeste"),
        types.InlineKeyboardButton("➡️", callback_data="leste"),
        types.InlineKeyboardButton("⬇️", callback_data="sul")
    )
    return markup

# Função para mover dentro do labirinto
@bot.callback_query_handler(func=lambda call: call.data in ['norte', 'sul', 'leste', 'oeste'])
def mover_labirinto(call):
    id_usuario = call.from_user.id
    if id_usuario not in jogadores_labirinto:
        bot.send_message(call.message.chat.id, "👻 Inicie o labirinto com /labirinto.")
        return
    
    direcao = call.data
    jogador = jogadores_labirinto[id_usuario]
    labirinto = jogador["labirinto"]
    posicao_atual = jogador["posicao"]
    movimentos_restantes = jogador["movimentos"]
    
    nova_posicao = mover_posicao(posicao_atual, direcao, labirinto)
    
    if nova_posicao != posicao_atual:  # Movimento válido
        jogadores_labirinto[id_usuario]["posicao"] = nova_posicao
        jogadores_labirinto[id_usuario]["movimentos"] -= 1
        movimentos_restantes -= 1
        conteudo = labirinto[nova_posicao[0]][nova_posicao[1]]
        
        # Verifica vitória, derrota ou continuidade
        if conteudo == '🚪':
            recompensa = random.randint(50, 100)
            aplicar_recompensa_cenouras(id_usuario, recompensa)  # Função de recompensa
            bot.edit_message_text(
                f"🏆 Parabéns! Você encontrou a saída e ganhou {recompensa} cenouras extras!\n\n{revelar_labirinto(labirinto)}", 
                call.message.chat.id, call.message.message_id
            )
            del jogadores_labirinto[id_usuario]  # Remove jogador
        elif movimentos_restantes == 0:
            penalidade = random.randint(50, 100)
            aplicar_penalidade_cenouras(id_usuario, -penalidade)  # Função de penalidade
            bot.edit_message_text(
                f"😢 Seus movimentos acabaram. Fim de jogo! Você perdeu {penalidade} cenouras.\n\n{revelar_labirinto(labirinto)}", 
                call.message.chat.id, call.message.message_id
            )
            del jogadores_labirinto[id_usuario]
        else:
            atualizar_labirinto(call, labirinto, nova_posicao, movimentos_restantes, conteudo)
    else:
        bot.answer_callback_query(call.id, "👻 Direção bloqueada por uma parede!")


# Função para aplicar penalidade de cenouras ao encontrar um monstro
def aplicar_penalidade_cenouras(user_id, quantidade):
    conn, cursor = conectar_banco_dados()
    try:
        # Reduz cenouras do usuário
        cursor.execute("UPDATE usuarios SET cenouras = GREATEST(0, cenouras + %s) WHERE id_usuario = %s", (quantidade, user_id))
        conn.commit()
        
        # Obter saldo atualizado de cenouras
        cursor.execute("SELECT cenouras FROM usuarios WHERE id_usuario = %s", (user_id,))
        saldo_atual = cursor.fetchone()[0]

        return saldo_atual  # Retorna o saldo para mostrar na mensagem
    except Exception as e:
        print(f"Erro ao aplicar penalidade de cenouras: {e}")
        return None
    finally:
        fechar_conexao(cursor, conn)

# Função para aplicar recompensa de cenouras ao encontrar uma abóbora
def aplicar_recompensa_cenouras(user_id, quantidade):
    conn, cursor = conectar_banco_dados()
    try:
        # Aumenta cenouras do usuário
        cursor.execute("UPDATE usuarios SET cenouras = cenouras + %s WHERE id_usuario = %s", (quantidade, user_id))
        conn.commit()
        
        # Obter saldo atualizado de cenouras
        cursor.execute("SELECT cenouras FROM usuarios WHERE id_usuario = %s", (user_id,))
        saldo_atual = cursor.fetchone()[0]

        return saldo_atual  # Retorna o saldo para mostrar na mensagem
    except Exception as e:
        print(f"Erro ao aplicar recompensa de cenouras: {e}")
        return None
    finally:
        fechar_conexao(cursor, conn)

# Função para atualizar o labirinto e aplicar consequências (monstro ou recompensa)
def atualizar_labirinto(call, labirinto, posicao, movimentos_restantes, conteudo):
    mapa = mostrar_labirinto(labirinto, posicao)
    markup = criar_botoes_navegacao()

    if conteudo == '👻':
        labirinto[posicao[0]][posicao[1]] = '⬜'
        saldo_atual = aplicar_penalidade_cenouras(call.from_user.id, -20)
        if saldo_atual is not None:
            bot.edit_message_text(
                f"👻 Você encontrou um monstro! Perdeu 20 cenouras. Saldo atual: {saldo_atual} cenouras.\n\n{mapa}",
                call.message.chat.id, call.message.message_id, reply_markup=criar_botoes_opcoes()
            )
    elif conteudo == '🎃':
        labirinto[posicao[0]][posicao[1]] = '⬜'
        saldo_atual = aplicar_recompensa_cenouras(call.from_user.id, 50)
        if saldo_atual is not None:
            bot.edit_message_text(
                f"🎃 Você encontrou uma abóbora! Ganhou 50 cenouras. Saldo atual: {saldo_atual} cenouras.\n\n{mapa}",
                call.message.chat.id, call.message.message_id, reply_markup=criar_botoes_opcoes()
            )
    else:
        bot.edit_message_text(
            f"Movimentos restantes: {movimentos_restantes}\n\n{mapa}", 
            call.message.chat.id, call.message.message_id, reply_markup=markup
        )

# Função para criar botões de opções (encerrar ou continuar)
def criar_botoes_opcoes():
    markup_opcoes = types.InlineKeyboardMarkup()
    markup_opcoes.add(
        types.InlineKeyboardButton("Encerrar", callback_data="encerrar"),
        types.InlineKeyboardButton("Continuar", callback_data="continuar")
    )
    return markup_opcoes

# Handlers para encerrar ou continuar no labirinto
@bot.callback_query_handler(func=lambda call: call.data in ['encerrar', 'continuar'])
def encerrar_ou_continuar(call):
    id_usuario = call.from_user.id
    if call.data == 'encerrar':
        bot.edit_message_text("💀 Você encerrou o jogo. Fim de jornada!", call.message.chat.id, call.message.message_id)
        del jogadores_labirinto[id_usuario]
    elif call.data == 'continuar':
        jogador = jogadores_labirinto[id_usuario]
        mapa = mostrar_labirinto(jogador["labirinto"], jogador["posicao"])
        markup = criar_botoes_navegacao()
        bot.edit_message_text(f"Movimentos restantes: {jogador['movimentos']}\n\n{mapa}", call.message.chat.id, call.message.message_id, reply_markup=markup)
def verificar_desconto_loja(user_id):
    """
    Verifica se o usuário tem um desconto ativo na loja.
    """
    conn, cursor = conectar_banco_dados()
    try:
        cursor.execute("""
            SELECT fim_desconto FROM descontos_loja 
            WHERE id_usuario = %s AND fim_desconto > NOW()
        """, (user_id,))
        resultado = cursor.fetchone()
        return resultado is not None
    except Exception as e:
        print(f"Erro ao verificar desconto na loja: {e}")
        return False
    finally:
        fechar_conexao(cursor, conn)

def handle_callback_compra(call):
    try:
        chat_id = call.message.chat.id
        parts = call.data.split('_')
        categoria = parts[1]
        id_usuario = parts[2]
        original_message_id = parts[3]
        conn, cursor = conectar_banco_dados()
        
        # Verifica se o usuário possui desconto ativo
        desconto_ativo = verificar_desconto_loja(id_usuario)
        preco = 3 if desconto_ativo else 5  # Aplica desconto se ativo

        cursor.execute("SELECT cenouras FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        result = cursor.fetchone()
        qnt_cenouras = int(result[0]) if result else 0

        if qnt_cenouras >= preco:
            # Seleciona uma carta aleatória da categoria do dia
            cursor.execute(
                "SELECT loja.id_personagem, personagens.nome, personagens.subcategoria, personagens.emoji "
                "FROM loja "
                "JOIN personagens ON loja.id_personagem = personagens.id_personagem "
                "WHERE loja.categoria = %s AND loja.data = %s ORDER BY RAND() LIMIT 1",
                (categoria, datetime.today().strftime("%Y-%m-%d"))
            )
            carta_comprada = cursor.fetchone()

            if carta_comprada:
                id_personagem, nome, subcategoria, emoji = carta_comprada
                mensagem = f"Você tem {qnt_cenouras} cenouras.\nDeseja usar {preco} para comprar o peixe:\n\n{emoji} {id_personagem} - {nome} de {subcategoria}?"
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.row(
                    telebot.types.InlineKeyboardButton(text="Sim", callback_data=f'confirmar_compra_{categoria}_{id_usuario}'),
                    telebot.types.InlineKeyboardButton(text="Não", callback_data='cancelar_compra')
                )
                imagem_url = "https://telegra.ph/file/d4d5d0af60ec66f35e29c.jpg"
                bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=original_message_id,
                    reply_markup=keyboard,
                    media=telebot.types.InputMediaPhoto(media=imagem_url, caption=mensagem)
                )
            else:
                print(f"Nenhuma carta disponível para compra na categoria {categoria} hoje.")
        else:
            bot.send_message(chat_id, "Desculpe, você não tem cenouras suficientes para realizar esta compra.")
    except Exception as e:
        print(f"Erro ao processar a compra: {e}")
    finally:
        fechar_conexao(cursor, conn)

@bot.callback_query_handler(func=lambda call: call.data.startswith("pronomes_"))
def pronomes(call):
    atualizar_pronomes(call)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith("bpronomes_"))
def bpronomes(call):
    mostrar_opcoes_pronome(call)

# Função principal de troca
@bot.message_handler(commands=['picnic', 'trocar', 'troca'])
def trade(message):
    try:
        chat_id = message.chat.id
        eu = message.from_user.id
        voce = message.reply_to_message.from_user.id
        seunome = message.reply_to_message.from_user.first_name
        meunome = message.from_user.first_name
        bot_id = 7088149058
        categoria = message.text.replace('/troca', '')
        minhacarta = message.text.split()[1]
        suacarta = message.text.split()[2]
        
        # Verificação de bloqueios entre os usuários
        if verificar_bloqueio(eu, voce):
            bot.send_message(chat_id, "A troca não pode ser realizada porque um dos usuários bloqueou o outro.")
            return

        # Verificação se o destinatário é o bot
        if voce == bot_id:
            bot.send_message(chat_id, "Você não pode fazer trocas com a Mabi :(", reply_to_message_id=message.message_id)
            return

        # Verificação de inventário para o usuário que iniciou a troca
        if verifica_inventario_troca(eu, minhacarta) == 0:
            bot.send_message(chat_id, f"🌦️ ་  {meunome}, você não possui o peixe {minhacarta} para trocar.", reply_to_message_id=message.message_id)
            return

        # Verificação de inventário para o destinatário da troca
        if verifica_inventario_troca(voce, suacarta) == 0:
            bot.send_message(chat_id, f"🌦️ ་  Parece que {seunome} não possui o peixe {suacarta} para trocar.", reply_to_message_id=message.message_id)
            return

        # Obter informações das cartas
        info_minhacarta = obter_informacoes_carta(minhacarta)
        info_suacarta = obter_informacoes_carta(suacarta)
        emojiminhacarta, idminhacarta, nomeminhacarta, subcategoriaminhacarta = info_minhacarta
        emojisuacarta, idsuacarta, nomesuacarta, subcategoriasuacarta = info_suacarta

        meu_username = bot.get_chat_member(chat_id, eu).user.username
        seu_username = bot.get_chat_member(chat_id, voce).user.username

        seu_nome_formatado = f"@{seu_username}" if seu_username else seunome

        # Texto de descrição da troca
        texto = (
            f"🥪 | Hora do picnic!\n\n"
            f"{meunome} oferece de lanche:\n"
            f" {idminhacarta} {emojiminhacarta}  —  {nomeminhacarta} de {subcategoriaminhacarta}\n\n"
            f"E {seunome} oferece de lanche:\n"
            f" {idsuacarta} {emojisuacarta}  —  {nomesuacarta} de {subcategoriasuacarta}\n\n"
            f"Podemos começar a comer, {seu_nome_formatado}?"
        )

        # Criação dos botões de confirmação e rejeição
        keyboard = types.InlineKeyboardMarkup()
        primeiro = [
            types.InlineKeyboardButton(text="✅", callback_data=f'troca_sim_{eu}_{voce}_{minhacarta}_{suacarta}_{chat_id}'),
            types.InlineKeyboardButton(text="❌", callback_data=f'troca_nao_{eu}_{voce}_{minhacarta}_{suacarta}_{chat_id}'),
        ]
        keyboard.add(*primeiro)

        # Envio da imagem do picnic com a descrição da troca
        image_url = "https://pub-6f23ef52e8614212a14d24b0cf55ae4a.r2.dev/BQACAgEAAxkBAAI7p2ecQmMl1uRZUpR0jshow5UkA2R4AAIzBgACWOrpRL-yjDTLcwUKNgQ.jpg"
        bot.send_photo(chat_id, image_url, caption=texto, reply_markup=keyboard, reply_to_message_id=message.reply_to_message.message_id)

    except Exception as e:
        traceback.print_exc()
        erro = traceback.format_exc()
        mensagem = f"Erro durante a troca. dados: {voce},{eu},{minhacarta},{suacarta}\n{erro}"
        bot.send_message(grupodeerro, mensagem, parse_mode="HTML")


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

# Registra o comando para iniciar o jogo Termo
@bot.message_handler(commands=['termo'])
def handle_termo(message):
    iniciar_termo(message)  # Chama a função iniciar_termo do arquivo halloween.py

@bot.message_handler(commands=['verificar'])
def verificar_ids(message):
    try:
        if not message.reply_to_message:
            bot.reply_to(message, "Por favor, responda a uma mensagem que contenha os IDs que você deseja verificar.")
            return
        texto_original = message.reply_to_message.text
        soup = BeautifulSoup(texto_original, 'html.parser')
        ids_code = [tag.text for tag in soup.find_all('code')]

        ids_text = re.findall(r'\b\d{1,5}\b', texto_original)

        ids = list(set(ids_code + ids_text))

        if not ids:
            bot.reply_to(message, "Nenhum ID válido encontrado na mensagem.")
            return

        ids = list(map(int, ids))
        id_usuario = message.from_user.id

        conn, cursor = conectar_banco_dados()
        
        inventario = []

        for id_personagem in ids:
            cursor.execute("SELECT nome FROM personagens WHERE id_personagem = %s", (id_personagem,))
            resultado = cursor.fetchone()
            if resultado:
                nome_personagem = resultado[0]
                cursor.execute("SELECT quantidade FROM inventario WHERE id_usuario = %s AND id_personagem = %s", (id_usuario, id_personagem))
                quantidade = cursor.fetchone()
                if quantidade and quantidade[0] > 0:
                    inventario.append((id_personagem, nome_personagem, quantidade[0]))
            else:
                cursor.execute("SELECT nome FROM evento WHERE id_personagem = %s", (id_personagem,))
                resultado = cursor.fetchone()
                if resultado:
                    nome_personagem = resultado[0]
                    cursor.execute("SELECT quantidade FROM inventario WHERE id_usuario = %s AND id_personagem = %s", (id_usuario, id_personagem))
                    quantidade = cursor.fetchone()
                    if quantidade and quantidade[0] > 0:
                        inventario.append((id_personagem, nome_personagem, quantidade[0]))

        if not inventario:
            bot.send_message(message.chat.id, "Você não possui nenhuma das cartas mencionadas.", reply_to_message_id=message.message_id)
            return

        inventario.sort(key=lambda x: x[0])

        resposta = "🧺 Seu armazém:\n\n"
        for id_personagem, nome, quantidade in inventario:
            resposta += f"<code>{id_personagem}</code> — {nome}: {quantidade}x\n"

        max_chars = 4096  
        partes = [resposta[i:i + max_chars] for i in range(0, len(resposta), max_chars)]
        for parte in partes:
            bot.send_message(message.chat.id, parte, reply_to_message_id=message.message_id,parse_mode="HTML")

    except Exception as e:
        print(f"Erro ao verificar IDs: {e}")
        bot.reply_to(message, "Não foi possivel verificar essa mensagem, tente copiar e colar para verificar novamente.")
        
def process_wish(message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        command_parts = message.text.split()
        id_cartas = list(map(int, command_parts[:-1]))[:5]  
        quantidade_cenouras = int(command_parts[-1])

        if quantidade_cenouras < 10 or quantidade_cenouras > 20:
            bot.send_message(chat_id, "A quantidade de cenouras deve ser entre 10 e 20.")
            return
        if user_id != 1011473517:
            can_make_wish, time_remaining = check_wish_time(user_id)
            if not can_make_wish:
                hours, remainder = divmod(time_remaining.total_seconds(), 3600)
                minutes, _ = divmod(remainder, 60)
                image_url = "https://telegra.ph/file/94c9c66af4ca4d6f0a3e5.jpg"
                caption = (f"<b>Você já fez um pedido recentemente.</b> Por favor, aguarde {int(hours)} horas e {int(minutes)} minutos "
                           "para fazer um novo pedido.")
                media = InputMediaPhoto(image_url, caption=caption, parse_mode="HTML")
                bot.send_message(chat_id=message.chat.id, text=caption, parse_mode="HTML")
                return

            results = []
            debug_info = []
            diminuir_cenouras(user_id, quantidade_cenouras)
            adicionar_cenouras_banco(quantidade_cenouras)  # Adiciona as cenouras ao banco da cidade
    
            for id_carta in id_cartas:
                chance = random.randint(1, 100)
                if chance <= 15:  # 10% de chance
                    results.append(id_carta)
                    update_inventory(user_id, id_carta)
                debug_info.append(f"ID da carta: {id_carta}, Chance: {chance}, Resultado: {'Ganhou' if chance <= 10 else 'Não ganhou'}")
    
            if results:
                bot.send_message(chat_id, f"<i>As águas da fonte começam a circular em uma velocidade assutadora, mas antes que você possa reagir, aparece na sua cesta os seguintes peixes:<b> {', '.join(map(str, results))}.</b>\n\nA fonte então desaparece. Quem sabe onde ele estará daqui 6 horas?</i>", parse_mode="HTML")
            else:
                bot.send_message(chat_id, "<i>A fonte nem se move ao receber suas cenouras, elas apenas desaparecem no meio da água calma. Talvez você deva tentar novamente mais tarde... </i>", parse_mode="HTML")
    
            log_wish_attempt(user_id, id_cartas, quantidade_cenouras, results)
        else:
            results = []
            debug_info = []
            diminuir_cenouras(user_id, quantidade_cenouras)
            adicionar_cenouras_banco(quantidade_cenouras)  # Adiciona as cenouras ao banco da cidade
    
            for id_carta in id_cartas:
                chance = random.randint(1, 100)
                if chance <= 50:  # 10% de chance
                    results.append(id_carta)
                    update_inventory(user_id, id_carta)
                debug_info.append(f"ID da carta: {id_carta}, Chance: {chance}, Resultado: {'Ganhou' if chance <= 10 else 'Não ganhou'}")
    
            if results:
                bot.send_message(chat_id, f"<i>As águas da fonte começam a circular em uma velocidade assutadora, mas antes que você possa reagir, aparece na sua cesta os seguintes peixes:<b> {', '.join(map(str, results))}.</b>\n\nA fonte então desaparece. Quem sabe onde ele estará daqui 6 horas?</i>", parse_mode="HTML")
            else:
                bot.send_message(chat_id, "<i>A fonte nem se move ao receber suas cenouras, elas apenas desaparecem no meio da água calma. Talvez você deva tentar novamente mais tarde... </i>", parse_mode="HTML")
    
    except Exception as e:
        bot.send_message(message.chat.id, f"Ocorreu um erro. Você escreveu da maneira correta?")

def handle_fazer_pedido(call):
    user_id = call.from_user.id  # Adicionando a identificação do usuário

    can_make_wish, time_remaining = check_wish_time(user_id)
    if not can_make_wish:
        hours, remainder = divmod(time_remaining.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)
        image_url = "https://telegra.ph/file/94c9c66af4ca4d6f0a3e5.jpg"
        caption = (f"<b>Você já fez um pedido recentemente.</b> Por favor, aguarde {int(hours)} horas e {int(minutes)} minutos "
                   "para fazer um novo pedido.")
        media = InputMediaPhoto(image_url, caption=caption, parse_mode="HTML")
        bot.send_photo(chat_id=call.message.chat.id, photo=image_url, caption=caption, parse_mode="HTML")
        return
    else:
        image_url = "https://telegra.ph/file/94c9c66af4ca4d6f0a3e5.jpg"
        caption = ("<b>⛲: Para pedir os seus peixes é simples!</b> \n\nMe envie até <b>5 IDs</b> dos peixes e a quantidade de cenouras que você quer doar "
                   "\n(eu aceito qualquer quantidade entre 10 e 20 cenouras...) \n\n<i>exemplo: ID1 ID2 ID3 ID4 ID5 cenouras</i>")
        media = InputMediaPhoto(image_url, caption=caption, parse_mode="HTML")
        bot.edit_message_media(media, chat_id=call.message.chat.id, message_id=call.message.message_id)
        
        bot.register_next_step_handler(call.message, process_wish)

def processar_pedido_peixes(call):
    try:
        image_url = "https://telegra.ph/file/94c9c66af4ca4d6f0a3e5.jpg"
        caption = ("<b>⛲: Para pedir os seus peixes é simples!</b> \n\nMe envie até <b>5 IDs</b> dos peixes e a quantidade de cenouras que você quer doar "
                   "\n(eu aceito qualquer quantidade entre 10 e 20 cenouras...) \n\n<i>exemplo: ID1 ID2 ID3 ID4 ID5 cenouras</i>")
        media = InputMediaPhoto(image_url, caption=caption, parse_mode="HTML")
        bot.edit_message_media(media, chat_id=call.message.chat.id, message_id=call.message.message_id)

        bot.register_next_step_handler(call.message, process_wish)

    except Exception as e:
        print(f"Erro ao processar o pedido de peixes: {e}")
@bot.message_handler(commands=['sugestao'])
def sugestao_command(message):
    try:
        argumentos = message.text.split(maxsplit=1)
        if len(argumentos) < 2:
            bot.reply_to(message, "Por favor, envie sua sugestão no formato:\n"
                                  "/sugestao nome, subcategoria, categoria, imagem")
            return
        
        dados = argumentos[1].split(",")
        if len(dados) < 4:
            bot.reply_to(message, "Erro no formato. Envie como:\n"
                                  "/sugestao nome, subcategoria, categoria, imagem")
            return

        nome = dados[0].strip()
        subcategoria = dados[1].strip()
        categoria = dados[2].strip()
        imagem = dados[3].strip()

        nome_usuario = message.from_user.first_name
        user_usuario = message.from_user.username

        sugestao_texto = (f"Sugestão recebida:\n"
                          f"Nome: {nome}\nSubcategoria: {subcategoria}\nCategoria: {categoria}\n"
                          f"Imagem: {imagem}\n"
                          f"Usuário: {nome_usuario} (@{user_usuario})")

        bot.send_message(GRUPO_SUGESTOES, sugestao_texto)

    except Exception as e:
        print(f"Erro ao processar o comando /sugestao: {e}")
        bot.reply_to(message, "Ocorreu um erro ao processar sua sugestão. Tente novamente.")

@bot.message_handler(commands=['adicionar_vip'])
def handle_adicionar_vip(message):
    adicionar_vip_logic(message)

@bot.message_handler(commands=['remover_vip'])
def handle_remover_vip(message):
    remover_vip_logic(message)

@bot.message_handler(commands=['vips'])
def handle_listar_vips(message):
    listar_vips_logic(message)

@bot.message_handler(commands=['pedidos'])
def handle_listar_pedidos_vips(message):
    listar_pedidos_vips_logic(message)

@bot.message_handler(commands=['ficha'])
def handle_ver_ficha_vip(message):
    ver_ficha_vip_logic(message)

@bot.message_handler(commands=['doar'])
def handle_doar(message):
    doar(message)

@bot.message_handler(commands=['roseira'])
def handle_roseira_command(message):
    roseira_command(message)

@bot.message_handler(commands=['pedidosubmenu'])
def handle_pedido_submenu_command(message):
    pedido_submenu_command(message)

@bot.message_handler(commands=['pedidovip'])
def handle_pedidovip_command(message):
    pedidovip_command(message)

@bot.message_handler(commands=['gift'])
def handle_gift_cards(message):
    conn, cursor = conectar_banco_dados()
    if message.from_user.id != 5532809878 and message.from_user.id != 1805086442:
        bot.reply_to(message, "Você não é a Hashi ou a Skar para usar esse comando.")
        return
    try:
        _, quantity, card_id, user_id = message.text.split()
        quantity = int(quantity)
        card_id = int(card_id)
        user_id = int(user_id)
    except (ValueError, IndexError):
        bot.reply_to(message, "Por favor, use o formato correto: /gift quantidade card_id user_id")
        return
    gift_cards(quantity, card_id, user_id)
    bot.reply_to(message, f"{quantity} cartas adicionadas com sucesso!")
allowed_user_ids = [5532809878, 1805086442, 5869653045]
@bot.message_handler(commands=['criarvendinha'])
def criar_colagem(message):
    if message.from_user.id not in allowed_user_ids:
        bot.send_message(message.chat.id, "Você não tem permissão para usar este comando.")
        return

    try:
        cartas_aleatorias = obter_cartas_aleatorias()
        data_atual_str = dt_module.date.today().strftime("%Y-%m-%d") 
        if not cartas_aleatorias:
            bot.send_message(message.chat.id, "Não foi possível obter cartas aleatórias.")
            return

        registrar_cartas_loja(cartas_aleatorias, data_atual_str)
        imagens = []
        for carta in cartas_aleatorias:
            img_url = carta.get('imagem', '')
            try:
                if img_url:
                    response = requests.get(img_url)
                    if response.status_code == 200:
                        img = Image.open(io.BytesIO(response.content))
                        img = img.resize((300, 400), Image.LANCZOS)
                    else:
                        img = Image.new('RGB', (300, 400), color='black')
                else:
                    img = Image.new('RGB', (300, 400), color='black')
            except Exception as e:
                print(f"Erro ao abrir a imagem da carta {carta['id']}: {e}")
                img = Image.new('RGB', (300, 400), color='black')
            imagens.append(img)

        altura_total = (len(imagens) // 3) * 400

        colagem = Image.new('RGB', (900, altura_total))  
        coluna_atual = 0
        linha_atual = 0

        for img in imagens:
            colagem.paste(img, (coluna_atual, linha_atual))
            coluna_atual += 300

            if coluna_atual >= 900:
                coluna_atual = 0
                linha_atual += 400

        colagem.save('colagem_cartas.png')
        
        mensagem_loja = "🐟 Peixes na vendinha hoje:\n\n"
        for carta in cartas_aleatorias:
            mensagem_loja += f"{carta['emoji']}| {carta['id']} • {carta['nome']} - {carta['subcategoria']}\n"
        mensagem_loja += "\n🥕 Acesse usando o comando /vendinha"

        with open('colagem_cartas.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=mensagem_loja, reply_to_message_id=message.message_id)
    except Exception as e:
        print(f"Erro ao criar colagem: {e}")
        bot.send_message(message.chat.id, "Erro ao criar colagem.")


@bot.message_handler(commands=['vendinha'])
def handle_vendinha_command(message):
    loja(message)

@bot.message_handler(commands=['peixes'])
def handle_peixes_command(message):
    verificar_comando_peixes(message)

@bot.message_handler(commands=['delgif'])
def handle_delgif(message):
    processar_comando_delgif(message)
            
@bot.message_handler(commands=['raspadinha'])
def handle_sorte(message):
    comando_sorte(message)

@bot.message_handler(commands=['casar'])
def handle_casar_command(message):
    casar_command(message)

@bot.message_handler(commands=['divorciar'])
def handle_divorciar_command(message):
    divorciar_command(message)

@bot.message_handler(commands=['tag','tags'])
def handle_tag_command(message):
    verificar_comando_tag(message)

@bot.message_handler(commands=['addtag'])
def handle_addtag_command(message):
    adicionar_tag(message)
@bot.callback_query_handler(func=lambda call: call.data.startswith("completos_"))
def navegar_completos(call):
    try:
        # Extrair informações do callback_data
        data = call.data.split("_")
        if len(data) != 5:
            print(f"Callback data inesperado: {call.data}")
            bot.answer_callback_query(call.id, "Ocorreu um erro ao processar sua solicitação.", show_alert=True)
            return

        _, pagina, categoria, id_usuario, message_id = data
        pagina = int(pagina)
        id_usuario = int(id_usuario)
        message_id = int(message_id)  # Converte para inteiro

        # Verificar se o ID do usuário no callback corresponde ao ID do usuário que clicou
        if id_usuario != call.from_user.id:
            bot.answer_callback_query(call.id, "Você não pode acessar essa página.", show_alert=True)
            return

        # Reconectar ao banco de dados para buscar novamente os resultados
        conn, cursor = conectar_banco_dados()

        query = """
        SELECT s.subcategoria COLLATE utf8mb4_unicode_ci AS subcategoria, 
               SUM(CASE WHEN inv.id_personagem IS NOT NULL THEN 1 ELSE 0 END) AS total_possui, 
               COUNT(p.id_personagem) AS total_necessario,
               MAX(s.Imagem) AS Imagem
        FROM subcategorias s
        JOIN personagens p ON s.subcategoria COLLATE utf8mb4_unicode_ci = p.subcategoria COLLATE utf8mb4_unicode_ci
        LEFT JOIN inventario inv ON p.id_personagem = inv.id_personagem AND inv.id_usuario = %s
        WHERE p.categoria = %s COLLATE utf8mb4_unicode_ci
        GROUP BY s.subcategoria
        HAVING total_possui = total_necessario
        ORDER BY s.subcategoria ASC
        """
        cursor.execute(query, (id_usuario, categoria))
        completos = cursor.fetchall()

        total_paginas = (len(completos) + 14) // 15  # Calcula total de páginas
        mostrar_pagina_completos(call.message.chat.id, pagina, total_paginas, completos, categoria, call.from_user.first_name, id_usuario, message_id=message_id)

        # Confirma ao usuário que o botão foi clicado
        bot.answer_callback_query(call.id)

    except Exception as e:
        print(f"Erro ao navegar nos completos: {e}")
        bot.answer_callback_query(call.id, "Ocorreu um erro ao processar sua solicitação.", show_alert=True)
    finally:
        fechar_conexao(cursor, conn)


@bot.message_handler(commands=['completos'])
def handle_completos_command(message):
    handle_completos(message)

@bot.message_handler(commands=['spicnic'])
def handle_spicnic(message):
    spicnic_command(message)
@bot.message_handler(commands=['delcards'])
def delcards_handler(message):
    delcards_command(message)
    
@bot.message_handler(commands=['versubs'])
def versubs_handler(message):
    versubs_command(message)

@bot.message_handler(commands=['rep'])
def ver_repetidos_evento(message):
    try:
        id_usuario = message.from_user.id
        nome_usuario = message.from_user.first_name

        # Captura o nome completo do evento a partir do segundo elemento em diante
        comando_parts = message.text.split(maxsplit=1)
        if len(comando_parts) < 2:
            bot.send_message(message.chat.id, "Por favor, use o formato: /rep <nome do evento>")
            return

        evento = comando_parts[1].strip().lower()  # Todo o texto após o comando é o nome do evento
        print(f"DEBUG: Evento capturado - '{evento}'")  # Depuração para o nome do evento

        conn, cursor = conectar_banco_dados()

        # Consulta para eventos válidos sem diferenciação de acentos
        cursor.execute("SELECT DISTINCT evento FROM evento WHERE evento COLLATE utf8mb4_unicode_ci = %s", (evento,))
        evento_existe = cursor.fetchone()
        if not evento_existe:
            cursor.execute("SELECT DISTINCT evento FROM evento")
            eventos_validos = [row[0] for row in cursor.fetchall()]
            print(f"DEBUG: Eventos válidos - {eventos_validos}")  # Depuração para eventos válidos
            bot.send_message(message.chat.id, f"O evento '{evento}' não existe. Eventos válidos: {', '.join(eventos_validos)}")
            return

        # Consulta para cartas repetidas do evento
        cursor.execute("""
            SELECT inv.id_personagem, ev.nome, ev.subcategoria, inv.quantidade 
            FROM inventario inv
            JOIN evento ev ON inv.id_personagem = ev.id_personagem
            WHERE inv.id_usuario = %s AND ev.evento COLLATE utf8mb4_unicode_ci = %s AND inv.quantidade > 1
        """, (id_usuario, evento))
        
        cartas_repetidas = cursor.fetchall()
        print(f"DEBUG: Cartas repetidas - {cartas_repetidas}")  # Depuração para cartas repetidas

        if not cartas_repetidas:
            bot.send_message(message.chat.id, f"Você não possui cartas repetidas do evento '{evento}'.")
            return

        # Armazena dados de repetidos no cache global
        globals.user_event_data[message.message_id] = {
            'id_usuario': id_usuario,
            'nome_usuario': nome_usuario,
            'evento': evento,
            'cartas_repetidas': cartas_repetidas
        }

        total_paginas = (len(cartas_repetidas) // 20) + (1 if len(cartas_repetidas) % 20 > 0 else 0)
        mensagem = bot.send_message(message.chat.id, "Gerando relatório de cartas repetidas, por favor aguarde...")
        mostrar_repetidas_evento(mensagem.chat.id, nome_usuario, evento, cartas_repetidas, 1, total_paginas, mensagem.message_id, message.message_id)

    except mysql.connector.Error as err:
        bot.send_message(message.chat.id, f"Erro ao buscar cartas repetidas do evento: {err}")
        print(f"Erro ao buscar cartas repetidas do evento: {err}")  # Depuração para erro SQL
    finally:
        fechar_conexao(cursor, conn)


@bot.message_handler(commands=['progresso'])
def progresso_evento(message):
    try:
        id_usuario = message.from_user.id
        nome_usuario = message.from_user.first_name

        # Captura o nome completo do evento após o comando
        comando_parts = message.text.split(maxsplit=1)
        if len(comando_parts) < 2:
            bot.send_message(message.chat.id, "Por favor, use o formato: /progresso <nome do evento>")
            return

        evento = comando_parts[1].strip().lower()  # Todo o texto após o comando é o nome do evento
        print(f"DEBUG: Evento capturado para progresso - '{evento}'")  # Depuração para o nome do evento

        conn, cursor = conectar_banco_dados()

        # Consulta de eventos válidos sem diferenciação de acentos
        cursor.execute("SELECT DISTINCT evento FROM evento WHERE evento COLLATE utf8mb4_unicode_ci = %s", (evento,))
        evento_existe = cursor.fetchone()
        if not evento_existe:
            cursor.execute("SELECT DISTINCT evento FROM evento")
            eventos_validos = [row[0] for row in cursor.fetchall()]
            print(f"DEBUG: Eventos válidos - {eventos_validos}")  # Depuração para eventos válidos
            bot.send_message(message.chat.id, f"O evento '{evento}' não existe. Eventos válidos: {', '.join(eventos_validos)}")
            return

        progresso_mensagem = calcular_progresso_evento(cursor, id_usuario, evento)
        print(f"DEBUG: Progresso mensagem - {progresso_mensagem}")  # Depuração para a mensagem de progresso

        resposta = f"Progresso de {nome_usuario} no evento {evento.capitalize()}:\n\n" + progresso_mensagem
        bot.send_message(message.chat.id, resposta)

    except mysql.connector.Error as err:
        bot.send_message(message.chat.id, f"Erro ao buscar progresso do evento: {err}")
        print(f"Erro ao buscar progresso do evento: {err}")  # Depuração para erro SQL
    finally:
        fechar_conexao(cursor, conn)

    
@bot.message_handler(commands=['saldo'])
def saldo_command(message):
    processar_saldo_usuario(message)

@bot.message_handler(commands=['trintadas', 'abelhadas', 'abelhas'])
def handle_trintadas(message): 
    enviar_mensagem_trintadas(message, pagina_atual=1)
    
@bot.message_handler(commands=['setmusica', 'setmusic'])
def set_musica_command(message):
    handle_set_musica(message)

@bot.message_handler(commands=['evento'])
def processar_evento(message):
    try:
        # Dividir o comando para extrair o tipo e o nome do evento
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            bot.reply_to(message, "Use o formato: /evento <s ou f> <nome do evento>")
            return
        
        tipo = parts[1].strip().lower()
        evento = parts[2].strip().lower()
        
        id_usuario = message.from_user.id
        nome_usuario = message.from_user.first_name

        # Validar o tipo (apenas 's' e 'f' são permitidos)
        if tipo not in ['s', 'f']:
            bot.reply_to(message, "Tipo inválido. Use 's' para possuídos e 'f' para faltantes.")
            return

        # Definir parâmetros da função de exibição com base no tipo
        if tipo == 's':
            ids_personagens = obter_ids_personagens_evento_inventario(id_usuario, evento)
            total_personagens = obter_total_personagens_evento(evento)
            total_paginas = (len(ids_personagens) // 15) + (1 if len(ids_personagens) % 15 > 0 else 0)
            mostrar_pagina_evento_s(message, evento, id_usuario, 1, total_paginas, ids_personagens, total_personagens, nome_usuario)
        
        elif tipo == 'f':
            ids_personagens_faltantes = obter_ids_personagens_evento_faltantes(id_usuario, evento)
            total_personagens = obter_total_personagens_evento(evento)
            total_paginas = (len(ids_personagens_faltantes) // 15) + (1 if len(ids_personagens_faltantes) % 15 > 0 else 0)
            mostrar_pagina_evento_f(message, evento, id_usuario, 1, total_paginas, ids_personagens_faltantes, total_personagens, nome_usuario)

    except Exception as e:
        print(f"Erro ao processar comando /evento: {e}")


@bot.message_handler(commands=['setfav'])
def set_fav_command(message):  
    handle_set_fav(message)

@bot.message_handler(commands=['usuario'])
def obter_username_por_comando(message):
    from eu import handle_obter_username
    handle_obter_username(message)

@bot.message_handler(commands=['eu'])
def me_command(message):
    handle_me_command(message)
    
@bot.message_handler(commands=['gperfil'])
def gperfil_command(message):
    handle_gperfil_command(message)

@bot.message_handler(commands=['config'])
def config_command(message):
    handle_config(message)
    
@bot.message_handler(commands=['delpage'])
def del_page(message):
    try:
        user_id = message.from_user.id
        params = message.text.split(' ', 1)[1:]
        if len(params) < 1:
            bot.send_message(message.chat.id, "Uso: /delpage <número_da_página>")
            return

        page_number = int(params[0])

        conn, cursor = conectar_banco_dados()

        cursor.execute("SELECT data, anotacao FROM anotacoes WHERE id_usuario = %s ORDER BY data DESC", (user_id,))
        anotacoes = cursor.fetchall()

        if not anotacoes or page_number < 1 or page_number > len(anotacoes):
            bot.send_message(message.chat.id, "Número de página inválido.")
            return

        data, anotacao = anotacoes[page_number - 1]

        response = f"Mabigarden, dia {data.strftime('%d/%m/%Y')}\n\n<i>\"{anotacao}\"</i>\n\nDeseja deletar esta página?"

        markup = types.InlineKeyboardMarkup()
        confirm_button = types.InlineKeyboardButton("✔️ Confirmar", callback_data=f"confirmar_delete_{page_number}")
        cancel_button = types.InlineKeyboardButton("❌ Cancelar", callback_data=f"cancelar_delete_{page_number}")
        markup.add(confirm_button, cancel_button)

        bot.send_message(message.chat.id, response, reply_markup=markup)

    except Exception as e:
        bot.send_message(message.chat.id, "Erro ao processar o comando de deletar página.")
        print(f"Erro ao deletar página: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirmar_delete_'))
def confirmar_delete(call):
    try:
        user_id = call.from_user.id
        page_number = int(call.data.split('_')[-1])

        conn, cursor = conectar_banco_dados()

        cursor.execute("SELECT id FROM anotacoes WHERE id_usuario = %s ORDER BY data DESC LIMIT 1 OFFSET %s", (user_id, page_number - 1))
        anotacao_id = cursor.fetchone()

        if anotacao_id:
            cursor.execute("DELETE FROM anotacoes WHERE id = %s", (anotacao_id[0],))
            conn.commit()
            bot.edit_message_text("Página deletada com sucesso.", call.message.chat.id, call.message.message_id)
        else:
            bot.edit_message_text("Erro ao deletar a página. Página não encontrada.", call.message.chat.id, call.message.message_id)

    except Exception as e:
        bot.send_message(call.message.chat.id, "Erro ao deletar a página.")
        print(f"Erro ao deletar página: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('cancelar_delete_'))
def cancelar_delete(call):
    bot.edit_message_text("Ação cancelada.", call.message.chat.id, call.message.message_id)

@bot.message_handler(commands=['editdiary'])
def handle_edit_diary(message):
    edit_diary(message, bot)

@bot.callback_query_handler(func=lambda call: call.data == 'edit_note')
def handle_edit_note_callback(call):
    bot.send_message(call.message.chat.id, "Envie a nova anotação para editar.")
    bot.register_next_step_handler(call.message, salvar_ou_editar_anotacao, call.from_user.id, date.today(), bot)

@bot.callback_query_handler(func=lambda call: call.data == 'cancel_edit')
def handle_cancel_edit_callback(call):
    cancelar_edicao(call, bot)

# Função para truncar aleatoriamente nomes de subcategorias
def truncar_texto(texto, truncar_percent=0.5):
    # Separar tags HTML do texto visível
    partes = re.split(r'(<[^>]+>)', texto)  # Divide o texto preservando as tags
    texto_embaralhado = ""

    for parte in partes:
        if parte.startswith("<") and parte.endswith(">"):
            # Se é uma tag HTML, preserve sem alterar
            texto_embaralhado += parte
        else:
            # Trunca exatamente a metade da parte do texto visível
            metade = len(parte) // 2
            texto_embaralhado += parte[:metade]  # Pega somente a primeira metade


    return texto_embaralhado

# Inicializar dicionário global para armazenar os resultados de pesquisa
resultados_gnome = {}

# Função para lidar com o comando gnome
@bot.message_handler(commands=['gnome'])
def handle_gnome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    try:
        partes = message.text.split()
        conn, cursor = conectar_banco_dados()

        # Verificar qual SQL usar com base na presença de 'e' no comando
        if 'e' in partes:
            nome = ' '.join(partes[2:])
            sql_personagens = """
                SELECT
                    e.id_personagem,
                    e.nome,
                    e.subcategoria,
                    e.categoria,
                    COALESCE(i.quantidade, 0) AS quantidade_usuario,
                    e.imagem
                FROM evento e
                LEFT JOIN inventario i ON e.id_personagem = i.id_personagem AND i.id_usuario = %s
                WHERE e.nome LIKE %s
            """
        else:
            nome = ' '.join(partes[1:])
            sql_personagens = """
                SELECT
                    p.id_personagem,
                    p.nome,
                    p.subcategoria,
                    p.categoria,
                    COALESCE(i.quantidade, 0) AS quantidade_usuario,
                    p.imagem
                FROM personagens p
                LEFT JOIN inventario i ON p.id_personagem = i.id_personagem AND i.id_usuario = %s
                WHERE p.nome LIKE %s
            """

        values_personagens = (user_id, f"%{nome}%")
        cursor.execute(sql_personagens, values_personagens)
        resultados_personagens = cursor.fetchall()

        if not resultados_personagens:
            bot.send_message(chat_id, f"Nenhum personagem encontrado com o nome '{nome}'.")
            return

        # Salvar os resultados no dicionário global
        resultados_gnome[user_id] = resultados_personagens

        # Enviar a primeira carta
        enviar_primeira_carta(chat_id, user_id, resultados_personagens, 0)

    except Exception as e:
        print(f"Erro: {e}")
        traceback.print_exc()
        bot.send_message(chat_id, "Ocorreu um erro ao processar seu comando.")
    finally:
        fechar_conexao(cursor, conn)

# Função para enviar a primeira carta
def enviar_primeira_carta(chat_id, user_id, resultados_personagens, index):
    try:
        id_personagem, nome, subcategoria, categoria, quantidade_usuario, imagem_url = resultados_personagens[index]
        # Tentar obter um GIF específico para o personagem
        gif_url = obter_gif_url(id_personagem, user_id)
        if gif_url:
            imagem_url = gif_url
        mensagem = f"💌 | Personagem:\n\n<code>{id_personagem}</code> • {nome}\nde {subcategoria}\n"
        if quantidade_usuario > 0:
            mensagem += f"☀ | {quantidade_usuario}⤫"
        else:
            mensagem += f"🌧 | Tempo fechado..."

        # Criar os botões de navegação
        keyboard = criar_botoes_navegacao(index, len(resultados_personagens), user_id)

        # Verificar se existe uma imagem URL e se é um GIF, vídeo ou imagem
        if imagem_url:
            if imagem_url.lower().endswith(".gif"):
                bot.send_animation(chat_id, imagem_url, caption=mensagem, reply_markup=keyboard, parse_mode="HTML")
            elif imagem_url.lower().endswith(".mp4"):
                bot.send_video(chat_id, imagem_url, caption=mensagem, reply_markup=keyboard, parse_mode="HTML")
            elif imagem_url.lower().endswith((".jpeg", ".jpg", ".png")):
                bot.send_photo(chat_id, imagem_url, caption=mensagem, reply_markup=keyboard, parse_mode="HTML")
            else:
                bot.send_message(chat_id, mensagem, reply_markup=keyboard, parse_mode="HTML")
    except Exception as e:
        print(f"Erro ao enviar a primeira carta: {e}")

# Função para criar os botões de navegação
def criar_botoes_navegacao(index, total, user_id):
    keyboard = types.InlineKeyboardMarkup()
    if index > 0:
        keyboard.add(types.InlineKeyboardButton("⬅️ Anterior", callback_data=f"gnome_prev_{index-1}_{user_id}"))
    if index < total - 1:
        keyboard.add(types.InlineKeyboardButton("Próxima ➡️", callback_data=f"gnome_next_{index+1}_{user_id}"))
    return keyboard

# Função de callback para a navegação
@bot.callback_query_handler(func=lambda call: call.data.startswith('gnome_'))
def callback_gnome_navigation(call):
    try:
        data = call.data.split('_')
        action = data[1]  # 'prev' ou 'next'
        index = int(data[2])
        user_id = int(data[3])

        # Recuperar os resultados da pesquisa
        resultados_personagens = resultados_gnome.get(user_id, [])

        if resultados_personagens:
            editar_carta(call.message.chat.id, user_id, resultados_personagens, index, call.message.message_id)
        else:
            bot.answer_callback_query(call.id, "Não foi possível encontrar os resultados. Tente novamente.")
    except Exception as e:
        bot.answer_callback_query(call.id, "Erro ao processar a navegação.")
        print(f"Erro ao processar callback de navegação: {e}")

# Função para editar a carta com navegação
def editar_carta(chat_id, user_id, resultados_personagens, index, message_id):
    try:
        id_personagem, nome, subcategoria, categoria, quantidade_usuario, imagem_url = resultados_personagens[index]

        # Montar a mensagem com as informações do personagem
        mensagem = f"💌 | Personagem:\n\n<code>{id_personagem}</code> • {nome}\nde {subcategoria}\n"
        if quantidade_usuario > 0:
            mensagem += f"☀ | {quantidade_usuario}⤫"
        else:
            mensagem += f"🌧 | Tempo fechado..."
        # Tentar obter um GIF específico para o personagem
        gif_url = obter_gif_url(id_personagem, user_id)
        if gif_url:
            imagem_url = gif_url
        # Criar os botões de navegação
        keyboard = criar_botoes_navegacao(index, len(resultados_personagens), user_id)

        # Verificar se existe uma imagem URL
        if imagem_url and imagem_url.lower().endswith((".jpeg", ".jpg", ".png", ".gif", ".mp4")):
            # Tipo de mídia
            if imagem_url.lower().endswith(".gif"):
                media = types.InputMediaAnimation(media=imagem_url, caption=mensagem, parse_mode="HTML")
            elif imagem_url.lower().endswith(".mp4"):
                media = types.InputMediaVideo(media=imagem_url, caption=mensagem, parse_mode="HTML")
            else:
                media = types.InputMediaPhoto(media=imagem_url, caption=mensagem, parse_mode="HTML")

            # Editar mensagem com mídia
            bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
        else:
            # Editar mensagem de texto
            bot.edit_message_text(mensagem, chat_id=chat_id, message_id=message_id, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        print(f"Erro ao editar a carta: {e}")
        bot.send_message(chat_id, "Erro ao editar a carta. Tente novamente.")




# Função para manusear o comando /gnomes
def gnomes(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    conn, cursor = conectar_banco_dados()

    try:
        nome = message.text.split('/gnomes', 1)[1].strip()
        if len(nome) <= 2:
            bot.send_message(chat_id, "Por favor, forneça um nome com mais de 3 letras.", reply_to_message_id=message.message_id)
            return

        sql_personagens = """
            SELECT
                p.emoji,
                p.id_personagem,
                p.nome,
                p.subcategoria
            FROM personagens p
            WHERE p.nome LIKE %s
        """
        values_personagens = (f"%{nome}%",)
        cursor.execute(sql_personagens, values_personagens)
        resultados_personagens = cursor.fetchall()

        if resultados_personagens:
            total_resultados = len(resultados_personagens)
            resultados_por_pagina = 15
            total_paginas = -(-total_resultados // resultados_por_pagina)
            pagina_solicitada = 1

            if total_resultados > resultados_por_pagina:
                resultados_pagina_atual = resultados_personagens[(pagina_solicitada - 1) * resultados_por_pagina:pagina_solicitada * resultados_por_pagina]
                lista_resultados = [f"{emoji} <code>{id_personagem}</code> • {nome}\nde {subcategoria}" for emoji, id_personagem, nome, subcategoria in resultados_pagina_atual]

                mensagem_final = f"🐠 Peixes de nome <b>{nome}</b>:\n\n" + "\n".join(lista_resultados) + f"\n\nPágina {pagina_solicitada}/{total_paginas}:"
                markup = create_navigation_markup(pagina_solicitada, total_paginas)
                msg = bot.send_message(chat_id, mensagem_final, reply_markup=markup, reply_to_message_id=message.message_id, parse_mode="HTML")

                save_state(user_id, nome, resultados_personagens, chat_id, msg.message_id)
            else:
                lista_resultados = [f"{emoji} <code>{id_personagem}</code> • {nome}\nde {subcategoria}" for emoji, id_personagem, nome, subcategoria in resultados_personagens]
                mensagem_final = f"🐠 Peixes de nome <b>{nome}</b>:\n\n" + "\n".join(lista_resultados)
                bot.send_message(chat_id, mensagem_final, reply_to_message_id=message.message_id, parse_mode='HTML')

        else:
            bot.send_message(chat_id, f"Nenhum resultado encontrado para o nome '{nome}'.", reply_to_message_id=message.message_id)
    finally:
        fechar_conexao(cursor, conn)

# Função de callback para manusear os botões de navegação da lista de /gnomes
@bot.callback_query_handler(func=lambda call: call.data.startswith('gnomes_'))
def callback_gnomes_navigation(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # Recuperar o estado do usuário
    if user_id in globals.resultados_gnome:
        dados = globals.resultados_gnome[user_id]
        resultados_personagens = dados['resultados']
        pesquisa = dados['pesquisa']
        total_resultados = len(resultados_personagens)
        resultados_por_pagina = 10  # Mesmo número que foi usado na função /gnomes
        total_paginas = -(-total_resultados // resultados_por_pagina)

        # Determinar qual página foi solicitada
        data = call.data.split('_')
        acao = data[1]  # 'prev' ou 'next'
        pagina_solicitada = int(data[2])

        # Calcular os resultados da página solicitada
        resultados_pagina_atual = resultados_personagens[(pagina_solicitada - 1) * resultados_por_pagina:pagina_solicitada * resultados_por_pagina]
        lista_resultados = [f"{emoji} <code>{id_personagem}</code> • {nome}\nde {subcategoria}" for emoji, id_personagem, nome, subcategoria in resultados_pagina_atual]

        # Criar a mensagem com os resultados
        mensagem_final = f"🐠 Peixes de nome <b>{pesquisa}</b>:\n\n" + "\n".join(lista_resultados) + f"\n\nPágina {pagina_solicitada}/{total_paginas}:"
        markup = create_navigation_markup(pagina_solicitada, total_paginas)

        # Editar a mensagem existente para exibir os resultados da nova página
        bot.edit_message_text(mensagem_final, chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="HTML")

    else:
        bot.answer_callback_query(call.id, "Erro ao recuperar os resultados. Tente novamente.")

@bot.message_handler(commands=['gnomes'])
def gnomes_command(message):
    gnomes(message)

# Função de callback para manusear os botões de navegação
@bot.callback_query_handler(func=lambda call: call.data.startswith('gnome_'))
def callback_gnome_navigation(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # Recuperar o estado do usuário
    if user_id in globals.resultados_gnome:
        dados = globals.resultados_gnome[user_id]
        resultados_personagens = dados['resultados']
        pesquisa = dados['pesquisa']
        total_resultados = len(resultados_personagens)
        resultados_por_pagina = 15
        total_paginas = -(-total_resultados // resultados_por_pagina)

        # Determinar qual página foi solicitada
        data = call.data.split('_')
        acao = data[1]  # 'prev' ou 'next'
        pagina_solicitada = int(data[2])

        # Calcular os resultados da página solicitada
        resultados_pagina_atual = resultados_personagens[(pagina_solicitada - 1) * resultados_por_pagina:pagina_solicitada * resultados_por_pagina]
        lista_resultados = [f"{emoji} <code>{id_personagem}</code> • {nome}\nde {subcategoria}" for emoji, id_personagem, nome, subcategoria in resultados_pagina_atual]

        # Criar a mensagem com os resultados
        mensagem_final = f"🐠 Peixes de nome <b>{pesquisa}</b>:\n\n" + "\n".join(lista_resultados) + f"\n\nPágina {pagina_solicitada}/{total_paginas}:"
        markup = create_navigation_markup(pagina_solicitada, total_paginas)

        # Editar a mensagem existente
        bot.edit_message_text(mensagem_final, chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="HTML")

    else:
        bot.answer_callback_query(call.id, "Erro ao recuperar os resultados. Tente novamente.")


@bot.message_handler(commands=['gid'])
def obter_id_e_enviar_info_com_imagem(message):
    try:      
        conn, cursor = conectar_banco_dados()
        user_id = message.from_user.id
        chat_id = message.chat.id

        command_parts = message.text.split()
        if len(command_parts) == 2 and command_parts[1].isdigit():
            id_pesquisa = command_parts[1]

            # Verificar se o ID pertence a um evento
            is_evento = verificar_evento(cursor, id_pesquisa)

            # Se for evento, usa a query de evento
            if is_evento:
                sql_evento = """
                    SELECT
                        e.id_personagem,
                        e.nome,
                        e.subcategoria,
                        COALESCE(i.quantidade, 0) AS quantidade_usuario,
                        e.imagem
                    FROM evento e
                    LEFT JOIN inventario i ON e.id_personagem = i.id_personagem AND i.id_usuario = %s
                    WHERE e.id_personagem = %s
                """
                values_evento = (user_id, id_pesquisa)

                cursor.execute(sql_evento, values_evento)
                resultado_evento = cursor.fetchone()

                if resultado_evento:
                    enviar_mensagem_personagem(chat_id, resultado_evento, message.message_id, user_id)
                else:
                    bot.send_message(chat_id, f"Nenhum resultado encontrado para o ID '{id_pesquisa}'.", reply_to_message_id=message.message_id)

            # Se não for evento, trata como personagem regular
            else:
                sql_normal = """
                    SELECT
                        p.id_personagem,
                        p.nome,
                        p.subcategoria,
                        COALESCE(i.quantidade, 0) AS quantidade_usuario,
                        p.imagem,
                        p.cr
                    FROM personagens p
                    LEFT JOIN inventario i ON p.id_personagem = i.id_personagem AND i.id_usuario = %s
                    WHERE p.id_personagem = %s
                """
                values_normal = (user_id, id_pesquisa)

                cursor.execute(sql_normal, values_normal)
                resultado_normal = cursor.fetchone()

                if resultado_normal:
                    enviar_mensagem_personagem(chat_id, resultado_normal, message.message_id, user_id)
                else:
                    bot.send_message(chat_id, f"Nenhum resultado encontrado para o ID '{id_pesquisa}'.", reply_to_message_id=message.message_id)
        else:
            bot.send_message(chat_id, "Formato incorreto. Use /gid seguido do ID desejado, por exemplo: /gid 123", reply_to_message_id=message.message_id)
    except Exception as e:
        import traceback
        traceback.print_exc()
        erro = traceback.print_exc()
        mensagem = f"Erro ao processar o ID: {id_pesquisa}. Erro: {e}"
        bot.send_message(grupodeerro, mensagem, parse_mode="HTML")
    finally:
        fechar_conexao(cursor, conn)

def enviar_mensagem_personagem(chat_id, resultado_personagem, message_id, user_id):
    id_personagem, nome, subcategoria, quantidade_usuario, imagem_url = resultado_personagem[:5]
    cr = resultado_personagem[5] if len(resultado_personagem) > 5 else None
    categoria = subcategoria  # Usar a categoria correta se a travessura não estiver ativa

    # Montar a mensagem
    mensagem = f"💌 | Personagem:\n\n<code>{id_personagem}</code> • {nome}\nde {categoria}"
    if quantidade_usuario > 0:
        mensagem += f"\n\n☀ | {quantidade_usuario}⤫"
    else:
        mensagem += f"\n\n🌧 | Tempo fechado..."

    if cr:
        link_cr = obter_link_formatado(cr)
        mensagem += f"\n\n{link_cr}"

    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("💟", callback_data=f"total_{id_personagem}"))

    gif_url = obter_gif_url(id_personagem, user_id)
    print(gif_url)
    if gif_url:
        imagem_url = gif_url

    # Enviar mídia
    try:
        if imagem_url.lower().endswith(".gif"):
            # Tenta enviar como animação
            bot.send_animation(chat_id, imagem_url, caption=mensagem, reply_markup=markup, reply_to_message_id=message_id, parse_mode="HTML")
        elif imagem_url.lower().endswith(".mp4"):
            # Tenta enviar como vídeo
            bot.send_video(chat_id, imagem_url, caption=mensagem, reply_markup=markup, reply_to_message_id=message_id, parse_mode="HTML")
        elif imagem_url.lower().endswith((".jpeg", ".jpg", ".png")):
            # Envia como foto
            bot.send_photo(chat_id, imagem_url, caption=mensagem, reply_markup=markup, reply_to_message_id=message_id, parse_mode="HTML")
        else:
            # Se o arquivo não for suportado, envia a mensagem sem mídia
            bot.send_message(chat_id, mensagem, reply_markup=markup, parse_mode="HTML")
    except Exception as e:
        print(f"Erro ao enviar a mídia: {e}")
        try:
            # Se houver erro, tenta enviar como documento
            bot.send_document(chat_id, imagem_url, caption=mensagem, reply_markup=markup, reply_to_message_id=message_id, parse_mode="HTML")
        except Exception as e2:
            print(f"Erro ao enviar como documento: {e2}")
            bot.send_message(chat_id, mensagem, reply_markup=markup, parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: call.data.startswith('toggle_'))
def handle_toggle_config(call):
    toggle_config(call)

@bot.callback_query_handler(func=lambda call: call.data == 'toggle_casamento')
def handle_toggle_casamento(call):
    toggle_casamento(call)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith("escolher_"))
def handle_callback_escolher_carta(call):
    callback_escolher_carta(call)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('pescar_'))
def categoria_callback(call):
    try:
        categoria = call.data.replace('pescar_', '')
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        id_usuario = call.from_user.id  # Captura o ID do usuário que acionou o callback

        if chat_id and message_id:
            # Passamos o ID do usuário para verificar travessura ou embaralhamento
            ultimo_clique[chat_id] = {'categoria': categoria}
            categoria_handler(call.message, categoria, id_usuario)
        else:
            print("Invalid message or chat data in the callback query.")
    except Exception as e:
        print(f"Erro em categoria_callback: {e}")


@bot.callback_query_handler(func=lambda call: call.data.startswith('peixes_'))
def callback_peixes(call):
    try:
        parts = call.data.split('_')
        pagina = int(parts[1])
        subcategoria = parts[2]
        
        pagina_peixes_callback(call, pagina, subcategoria)
    except Exception as e:
        print(f"Erro ao processar callback de peixes: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('choose_subcategoria_'))
def callback_subcategoria_handler(call):
    try:
        # Extrair dados do callback
        data = call.data.split('_')
        subcategoria = data[2]
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        conn, cursor = conectar_banco_dados()
        
        # Tentar obter um evento fixo para a subcategoria
        evento_fixo = obter_carta_evento_fixo(subcategoria=subcategoria)
        chance = random.randint(1, 100)

        # Se o evento fixo existe e a chance de 5% se aplica, enviar o evento fixo
        if evento_fixo and chance <= 5:
            emoji, id_personagem_carta, nome, subcategoria, imagem = evento_fixo
            send_card_message(call.message, emoji, id_personagem_carta, nome, subcategoria, imagem)
        else:
            # Caso contrário, envia uma carta aleatória normal da subcategoria
            subcategoria_handler(call.message, subcategoria, cursor, conn, None, chat_id, message_id)
    
    except Exception as e:
        traceback.print_exc()
        erro = traceback.format_exc()
        bot.send_message(grupodeerro, f"Erro em categoria_callback: {e}\n{erro}")
    
    finally:
        fechar_conexao(cursor, conn)



@bot.callback_query_handler(func=lambda call: call.data.startswith("confirmar_casamento_"))
def handle_confirmar_casamento(call):
    confirmar_casamento(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('cdoacao_'))
def handle_confirmar_doacao(call):
    confirmar_doacao(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('ccancelar_'))
def handle_cancelar_doacao(call):
    cancelar_doacao(call)

@bot.callback_query_handler(func=lambda call: call.data == 'acoes_vendinha')
def handle_acoes_vendinha(call):
    exibir_acoes_vendinha(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('comprar_acao_vendinha_'))
def handle_confirmar_compra_vendinha(call):
    confirmar_compra_vendinha(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirmar_categoria_'))
def handle_processar_compra_vendinha_categoria(call):
    processar_compra_vendinha_categoria(call)

@bot.callback_query_handler(func=lambda call: call.data == 'cancelar_compra_vendinha')
def cancelar_compra_vendinha(call):
    bot.edit_message_caption(caption="Poxa, Até logo!", chat_id=call.message.chat.id, message_id=call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirmar_compra_vendinha_'))
def handle_processar_compra_vendinha(call):
    processar_compra_vendinha(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("change_page_"))
def handle_page_change(call):
    page_index = int(call.data.split("_")[2])
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    data = globals.state_data.get(chat_id)
    if not data:
        return

    if isinstance(data, list):
        mensagens = data
    else:
        return

    total_count = len(mensagens)
    if 0 <= page_index < total_count:
        media_url, mensagem = mensagens[page_index]
        markup = create_navigation_markup(page_index, total_count)

        try:
            update_message_media(media_url, mensagem, chat_id, message_id, markup)
            bot.answer_callback_query(call.id)
        except Exception as e:
            bot.answer_callback_query(call.id, "Falha ao atualizar a mensagem.")
            newrelic.agent.record_exception()    
    else:
        bot.answer_callback_query(call.id, "Índice de página inválido.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('submenu_'))
def handle_submenu(call):
    callback_submenu(call)

@bot.callback_query_handler(func=lambda call: call.data == "add_note")
def handle_add_note_callback(call):
    bot.send_message(call.message.chat.id, "Digite sua anotação para o diário:")
    bot.register_next_step_handler(call.message, receive_note)

@bot.callback_query_handler(func=lambda call: call.data == "cancel_note")
def handle_cancel_note_callback(call):
    bot.send_message(call.message.chat.id, "Anotação cancelada.")
  
@bot.callback_query_handler(func=lambda call: call.data.startswith('versubs_'))
def handle_versubs_callback(call):
    callback_pagina_versubs(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('rep_'))
def callback_repetidas_evento_handler(call):
    callback_repetidas_evento(call)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('cdoacao_'))
def handle_confirmar_doacao(call):
    confirmar_doacao(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('ccancelar_'))
def handle_cancelar_doacao(call):
    cancelar_doacao(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("submenus_"))
def callback_submenus_handler(call):
    callback_submenus(call)
        
@bot.callback_query_handler(func=lambda call: call.data.startswith('especies_'))
def callback_especies(call):
    try:
        # Extrair a página e a categoria do callback_data
        _, pagina_str, categoria = call.data.split('_')
        pagina_atual = int(pagina_str)

        # Obter o número total de páginas
        conn, cursor = conectar_banco_dados()
        query_total = "SELECT COUNT(DISTINCT subcategoria) FROM personagens WHERE categoria = %s"
        cursor.execute(query_total, (categoria,))
        total_registros = cursor.fetchone()[0]
        total_paginas = (total_registros // 20) + (1 if total_registros % 15 > 0 else 0)

        # Editar a mensagem com os novos dados da página
        editar_mensagem_especies(call, categoria, pagina_atual, total_paginas)

    except Exception as e:
        print(f"Erro ao processar o callback de espécies: {e}")
        bot.reply_to(call.message, "Ocorreu um erro ao processar sua solicitação.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('poço_dos_desejos'))
def handle_poco_dos_desejos_handler(call):
    handle_poco_dos_desejos(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('fazer_pedido'))
def handle_fazer_pedido_handler(call):
    handle_fazer_pedido(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('trintadas_'))
def callback_trintadas(call):
    data = call.data.split('_')
    user_id_inicial = int(data[1])
    pagina_atual = int(data[2])
    nome_usuario_inicial = data[3]
    editar_mensagem_trintadas(call, user_id_inicial, pagina_atual, nome_usuario_inicial)

@bot.callback_query_handler(func=lambda call: call.data.startswith('fazer_pedido'))
def handle_fazer_pedido(call):
    processar_pedido_peixes(call)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('notificar_'))
def callback_handler(call):
    processar_notificacao_personagem(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('next_button', 'prev_button')))
def navigate_messages(call):
    handle_navigate_messages(call)
        
@bot.callback_query_handler(func=lambda call: call.data.startswith('total_'))
def callback_total_personagem(call):
    handle_callback_total_personagem(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('armazem_anterior_', 'armazem_proxima_','armazem_ultima_','armazem_primeira_')))
def callback_paginacao_armazem(call):
    handle_callback_paginacao_armazem(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('subcategory_'))
def handle_callback_subcategory(call):
    callback_subcategory(call)

@bot.message_handler(commands=['cenourar'])
def handle_cenourar(message):
    processar_verificar_e_cenourar(message, bot)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('cenourar_'))
def callback_cenourar(call):
    try:
        # Dividindo os dados do callback para extrair ação, usuário e cartas
        data_parts = call.data.split("_")
        acao = data_parts[1]  # Ação (sim ou nao)
        if acao == "sim":
            id_usuario = int(data_parts[2])  # ID do usuário
            ids_personagens = data_parts[3].split(",")  # IDs das cartas
            cenourar_carta(call, id_usuario, ids_personagens)
        elif acao == "nao":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🍂 Ufa! As cartas escaparam de serem cenouradas por pouco!")
    except Exception as e:
        print(f"Erro ao processar callback de cenoura: {e}")
        traceback.print_exc()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Erro ao processar a cenoura.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('loja_geral'))
def callback_loja_geral(call):
    try:
        loja_geral_callback(call)
    except Exception as e:
        print(f"Erro ao processar callback de loja geral: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('img_'))
def callback_img_peixes_handler(call):
    try:
        dados = call.data.split('_')
        pagina = int(dados[-2])
        subcategoria = dados[-1]
        callback_img_peixes(call, pagina, subcategoria)
    except Exception as e:
        newrelic.agent.record_exception()    
        print(f"Erro ao processar callback 'img' de peixes: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('peixes_'))
def callback_peixes(call):
    try:
        dados = call.data.split('_')
        pagina = int(dados[-2])
        subcategoria = dados[-1]
        pagina_peixes_callback(call, pagina, subcategoria)
    except Exception as e:
        print(f"Erro ao processar callback de peixes: {e}")
        newrelic.agent.record_exception()
@bot.callback_query_handler(func=lambda call: call.data.startswith("tag_"))
def callback_tag(call):
    try:
        parts = call.data.split('_')
        pagina = int(parts[1])
        nometag = parts[2]
        total_paginas = int(parts[3])
        id_usuario = call.from_user.id
        nome_usuario = call.from_user.first_name  # Obtém o nome do usuário

        # Chamar a função correta com todos os argumentos necessários
        editar_mensagem_tag(call.message, nometag, pagina, id_usuario, total_paginas, nome_usuario)

    except Exception as e:
        print(f"Erro ao processar callback de página para a tag: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('aprovar_'))
def callback_aprovar(call):
    try:
                # Apaga a mensagem original após o botão ser pressionado
        bot.delete_message(call.message.chat.id, call.message.message_id)
        aprovar_callback(call)
    except Exception as e:
        print(f"Erro ao processar callback de aprovação: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('reprovar_'))
def callback_reprovar(call):
    try:
                # Apaga a mensagem original após o botão ser pressionado
        bot.delete_message(call.message.chat.id, call.message.message_id)
        reprovar_callback(call)
    except Exception as e:
        print(f"Erro ao processar callback de reprovação: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('repor_'))
def callback_repor(call):
    try:
        quantidade = 1
        message_data = call.data
        parts = message_data.split('_')
        id_usuario = parts[1]
        adicionar_iscas(id_usuario, quantidade, call.message)
    except Exception as e:
        print(f"Erro ao processar callback de reposição: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('loja_loja'))
def callback_loja_loja(call):
    from loja import handle_callback_loja_loja
    handle_callback_loja_loja(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('compra_'))
def callback_compra(call):
    from loja import handle_callback_compra
    handle_callback_compra(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirmar_compra_'))
def callback_confirmar_compra(call):
    from loja import handle_callback_confirmar_compra
    handle_callback_confirmar_compra(call)
        
@bot.callback_query_handler(func=lambda call: call.data.startswith("evt_"))
def callback_query_evento(call):
    handle_callback_query_evento(call)
@bot.message_handler(commands=['editartag'])
def handle_edit_tag_command(message):
    handle_edit_tag(message)

@bot.message_handler(commands=['start'])
def start_comando(message):
    user_id = message.from_user.id
    nome_usuario = message.from_user.first_name  
    username = message.chat.username
    grupo_id = -4209628464  # ID do grupo para enviar a notificação do /start
    print(f"Comando /start recebido. ID do usuário: {user_id} - {nome_usuario}")
    # Enviar notificação do start para o grupo
    bot.send_message(grupo_id, f"Novo usuário iniciou o bot: {nome_usuario} (@{username}) - ID: {user_id}")
    try:
        verificar_id_na_tabela(user_id, "ban", "iduser")
        print("Novo /start ", {user_id}, "-", {nome_usuario}, "-", {username})

        if verificar_id_na_tabelabeta(user_id):
            registrar_usuario(user_id, nome_usuario, username)
            registrar_valor("nome_usuario", nome_usuario, user_id)
            
            keyboard = telebot.types.InlineKeyboardMarkup()
            image_url = "https://pub-6f23ef52e8614212a14d24b0cf55ae4a.r2.dev/AgACAgEAAxkBAAIZf2cSyI4kuw-GHGMBuPUdp-Gefo_ZAAKprTEbhPYRRedTrmeod49GAQADAgADeAADNgQ.jpg"
            bot.send_photo(message.chat.id, image_url,
                           caption='Seja muito bem-vindo ao MabiGarden! Entre, busque uma sombra e aproveite a estadia.',
                           reply_markup=keyboard, reply_to_message_id=message.message_id)
        else:
            video_url = "https://pub-6f23ef52e8614212a14d24b0cf55ae4a.r2.dev/BAACAgEAAxkBAAIZfGcSx9DRGzg211Ym_G47xld4U-sdAAJHBQACuXZhRGUFAAGmQXGCtTYE.mp4"
            caption = "🧐 QUEM É VO-CÊ? Estranho detectado! Lembrando que você precisa se identificar antes de usar. Chame a gente no suporte se houver dúvidas!"
            bot.send_video(message.chat.id, video=video_url, caption=caption, reply_to_message_id=message.message_id)

    except ValueError as e:
        print(f"Erro: {e}")
        mensagem_banido = "Você foi banido permanentemente do garden. Entre em contato com o suporte caso haja dúvidas."
        bot.send_message(message.chat.id, mensagem_banido, reply_to_message_id=message.message_id)

@bot.message_handler(commands=['especies'])
def verificar_comando_especies(message):
    try:
        parametros = message.text.split(' ', 1)[1:]  
        if not parametros:
            bot.reply_to(message, "Por favor, forneça a categoria.")
            return

        categoria = parametros[0]
        mostrar_primeira_pagina_especies(message, categoria)

    except Exception as e:
        print(f"Erro ao processar comando /especies: {e}")

@bot.message_handler(commands=['cesta'])
def verificar_cesta(message):
    processar_cesta(message)


@bot.message_handler(commands=['submenus'])
def submenus_command(message):
    processar_submenus_command(message)

@bot.message_handler(commands=['submenu'])
def submenu_command(message):
    processar_submenu_command(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('navigate_submenus_'))
def callback_navegacao_submenus(call):
    callback_navegacao_submenus(call)

def command_historico(message):
    processar_historico_command(message)
    
@bot.message_handler(commands=['sub'])
def sub_command(message):
    processar_sub_command(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('s_pagina_', 'f_pagina_', 'all_pagina_')))
def callback_pagina(call):
    callback_pagina_sub(call)
    
@bot.message_handler(commands=['deltag'])
def deletar_tag(message):
    processar_deletar_tag(message)
    
@bot.message_handler(commands=['apoiar'])
def doacao(message):
    markup = telebot.types.InlineKeyboardMarkup()
    chave_pix = "80388add-294e-4075-8cd5-8765cc9f9be0"
    mensagem = f"👨🏻‍🌾 Oi, jardineiro! Se está vendo esta mensagem, significa que está interessado em nos ajudar, certo? A equipe MabiGarden fica muito feliz em saber que nosso trabalho o agradou e o motivou a nos ajudar! \n\nCaso deseje contribuir com PIX, a chave é: <code>{chave_pix}</code> (clique na chave para copiar automaticamente) \n\n"
    bot.send_message(message.chat.id, mensagem, parse_mode="HTML", reply_to_message_id=message.message_id)

@bot.message_handler(commands=['banco'])
def banco_command(message):
    processar_banco_command(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('banco_pagina_'))
def callback_banco_pagina(call):
    processar_callback_banco_pagina(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('cartas_compradas_pagina_'))
def callback_cartas_compradas(call):
    processar_callback_cartas_compradas(call)

@bot.message_handler(commands=['armazém', 'armazem', 'amz'])
def armazem_command(message):
    try:
        id_usuario = message.from_user.id
        usuario = message.from_user.first_name
        verificar_id_na_tabela(id_usuario, "ban", "iduser")

        conn, cursor = conectar_banco_dados()
        qnt_carta(id_usuario)
        globals.armazem_info[id_usuario] = {'id_usuario': id_usuario, 'usuario': usuario}
        pagina = 1
        resultados_por_pagina = 15
        
        id_fav_usuario, emoji_fav, nome_fav, subcategoria_fav, imagem_fav = obter_favorito(id_usuario)

            

        if id_fav_usuario is not None:
            resposta = f"💌 | Cartas no armazém de {usuario}:\n\n🩷 ∙ {id_fav_usuario} — {nome_fav} de {subcategoria_fav}\n\n"

            sql = f"""
                SELECT id_personagem, emoji, nome_personagem, subcategoria, quantidade, categoria, evento
                FROM (
                    SELECT i.id_personagem, 
                           p.emoji COLLATE utf8mb4_general_ci AS emoji, 
                           p.nome COLLATE utf8mb4_general_ci AS nome_personagem, 
                           p.subcategoria COLLATE utf8mb4_general_ci AS subcategoria, 
                           i.quantidade, 
                           p.categoria COLLATE utf8mb4_general_ci AS categoria, 
                           '' COLLATE utf8mb4_general_ci AS evento
                    FROM inventario i
                    JOIN personagens p ON i.id_personagem = p.id_personagem
                    WHERE i.id_usuario = {id_usuario} AND i.quantidade > 0

                    UNION

                    SELECT e.id_personagem, 
                           e.emoji COLLATE utf8mb4_general_ci AS emoji, 
                           e.nome COLLATE utf8mb4_general_ci AS nome_personagem, 
                           e.subcategoria COLLATE utf8mb4_general_ci AS subcategoria, 
                           0 AS quantidade, 
                           e.categoria COLLATE utf8mb4_general_ci AS categoria, 
                           e.evento COLLATE utf8mb4_general_ci AS evento
                    FROM evento e
                    WHERE e.id_personagem IN (
                        SELECT id_personagem
                        FROM inventario
                        WHERE id_usuario = {id_usuario} AND quantidade > 0
                    )
                ) AS combined
                ORDER BY 
                    CASE WHEN categoria = 'evento' THEN 0 ELSE 1 END, 
                    categoria, 
                    CAST(id_personagem AS UNSIGNED) ASC
                LIMIT {15}
            """
            cursor.execute(sql)
            resultados = cursor.fetchall()

            if resultados:
                markup = telebot.types.InlineKeyboardMarkup()
                buttons_row = [
                    telebot.types.InlineKeyboardButton("⏪️", callback_data=f"armazem_primeira_{pagina}_{id_usuario}"),
                    telebot.types.InlineKeyboardButton("◀️", callback_data=f"armazem_anterior_{pagina}_{id_usuario}"),
                    telebot.types.InlineKeyboardButton("▶️", callback_data=f"armazem_proxima_{pagina}_{id_usuario}"),
                    telebot.types.InlineKeyboardButton("⏩️", callback_data=f"armazem_ultima_{pagina}_{id_usuario}")
                ]
                markup.row(*buttons_row)

                for carta in resultados:
                    id_carta, emoji_carta, nome_carta, subcategoria_carta, quantidade_carta, categoria_carta, evento_carta = carta
                    quantidade_carta = int(quantidade_carta) if quantidade_carta is not None else 0

                    if categoria_carta == 'evento':
                        emoji_carta = obter_emoji_evento(evento_carta)

                    if quantidade_carta == 1:
                        letra_quantidade = ""
                    elif 2 <= quantidade_carta <= 4:
                        letra_quantidade = "🌾"
                    elif 5 <= quantidade_carta <= 9:
                        letra_quantidade = "🌼"
                    elif 10 <= quantidade_carta <= 19:
                        letra_quantidade = "☀️"
                    elif 20 <= quantidade_carta <= 29:
                        letra_quantidade = "🍯️"
                    elif 30 <= quantidade_carta <= 39:
                        letra_quantidade = "🐝"
                    elif 40 <= quantidade_carta <= 49:
                        letra_quantidade = "🌻"
                    elif 50 <= quantidade_carta <= 99:
                        letra_quantidade = "👑"
                    elif 100 <= quantidade_carta:
                        letra_quantidade = "⭐️"    
                    else:
                        letra_quantidade = ""

                    repetida = " [+]" if quantidade_carta > 1 and categoria_carta != 'evento' else ""

                    resposta += f" {emoji_carta} <code>{id_carta}</code> • {nome_carta} - {subcategoria_carta} {letra_quantidade}{repetida}\n"

                quantidade_total_cartas = obter_quantidade_total_cartas(id_usuario)
                total_paginas = (quantidade_total_cartas + resultados_por_pagina - 1) // resultados_por_pagina
                resposta += f"\n{pagina}/{total_paginas}"
                gif_url = obter_gif_url(id_fav_usuario, id_usuario)
                if (gif_url):
                    bot.send_animation(
                        chat_id=message.chat.id,
                        animation=gif_url,
                        caption=resposta,
                        reply_to_message_id=message.message_id,
                        reply_markup=markup,
                        parse_mode="HTML"
                    )
                else:
                    bot.send_photo(
                        chat_id=message.chat.id,
                        photo=imagem_fav,
                        caption=resposta,
                        reply_to_message_id=message.message_id,
                        reply_markup=markup,
                        parse_mode="HTML"
                    )
            return

        resposta = f"💌 | Cartas no armazém de {usuario}:\n\n"

        sql = f"""
            SELECT id_personagem, emoji, nome_personagem, subcategoria, quantidade, categoria, evento
            FROM (
                -- Consulta para cartas no inventário do usuário
                SELECT i.id_personagem, 
                       p.emoji COLLATE utf8mb4_general_ci AS emoji, 
                       p.nome COLLATE utf8mb4_general_ci AS nome_personagem, 
                       p.subcategoria COLLATE utf8mb4_general_ci AS subcategoria, 
                       i.quantidade, 
                       p.categoria COLLATE utf8mb4_general_ci AS categoria, 
                       '' COLLATE utf8mb4_general_ci AS evento
                FROM inventario i
                JOIN personagens p ON i.id_personagem = p.id_personagem
                WHERE i.id_usuario = {id_usuario} AND i.quantidade > 0

                UNION ALL

                -- Consulta para cartas de evento que o usuário possui
                SELECT e.id_personagem, 
                       e.emoji COLLATE utf8mb4_general_ci AS emoji, 
                       e.nome COLLATE utf8mb4_general_ci AS nome_personagem, 
                       e.subcategoria COLLATE utf8mb4_general_ci AS subcategoria, 
                       0 AS quantidade, 
                       e.categoria COLLATE utf8mb4_general_ci AS categoria, 
                       e.evento COLLATE utf8mb4_general_ci AS evento
                FROM evento e
                WHERE e.id_personagem IN (
                    SELECT id_personagem
                    FROM inventario
                    WHERE id_usuario = {id_usuario} AND quantidade > 0
                )
            ) AS combined
            ORDER BY 
                CASE WHEN categoria = 'evento' THEN 0 ELSE 1 END, 
                categoria, 
                CAST(id_personagem AS UNSIGNED) ASC
            LIMIT {resultados_por_pagina} OFFSET {(pagina - 1) * resultados_por_pagina}
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()

        if resultados:
            markup = telebot.types.InlineKeyboardMarkup()
            buttons_row = [
                telebot.types.InlineKeyboardButton("⏪️", callback_data=f"armazem_primeira_{pagina}_{id_usuario}"),
                telebot.types.InlineKeyboardButton("◀️", callback_data=f"armazem_anterior_{pagina}_{id_usuario}"),
                telebot.types.InlineKeyboardButton("▶️", callback_data=f"armazem_proxima_{pagina}_{id_usuario}"),
                telebot.types.InlineKeyboardButton("⏩️", callback_data=f"armazem_ultima_{pagina}_{id_usuario}")
            ]
            markup.row(*buttons_row)

            for carta in resultados:
                id_carta, emoji_carta, nome_carta, subcategoria_carta, quantidade_carta, categoria_carta, evento_carta = carta
                quantidade_carta = int(quantidade_carta) if quantidade_carta is not None else 0

                if categoria_carta == 'evento':
                    emoji_carta = obter_emoji_evento(evento_carta)

                if quantidade_carta == 1:
                    letra_quantidade = ""
                elif 2 <= quantidade_carta <= 4:
                    letra_quantidade = "🌾"
                elif 5 <= quantidade_carta <= 9:
                    letra_quantidade = "🌼"
                elif 10 <= quantidade_carta <= 19:
                    letra_quantidade = "☀️"
                elif 20 <= quantidade_carta <= 29:
                    letra_quantidade = "🍯️"
                elif 30 <= quantidade_carta <= 39:
                    letra_quantidade = "🐝"
                elif 40 <= quantidade_carta <= 49:
                    letra_quantidade = "🌻"
                elif 50 <= quantidade_carta <= 99:
                    letra_quantidade = "👑"
                elif 100 <= quantidade_carta:
                    letra_quantidade = "⭐️"    
                else:
                    letra_quantidade = ""

                repetida = " [+]" if quantidade_carta > 1 and evento_carta else ""

                resposta += f" {emoji_carta} <code>{id_carta}</code> • {nome_carta} - {subcategoria_carta} {letra_quantidade}{repetida}\n"

            quantidade_total_cartas = obter_quantidade_total_cartas(id_usuario)
            total_paginas = (quantidade_total_cartas + resultados_por_pagina - 1) // resultados_por_pagina
            resposta += f"\n{pagina}/{total_paginas}"
            
            carta_aleatoria = random.choice(resultados)
            id_carta_aleatoria, emoji_carta_aleatoria, _, _, _, _ = carta_aleatoria
            foto_carta_aleatoria = obter_url_imagem_por_id(id_carta_aleatoria)
            if foto_carta_aleatoria:
                bot.send_photo(chat_id=message.chat.id, photo=foto_carta_aleatoria, caption=resposta, reply_to_message_id=message.message_id, reply_markup=markup, parse_mode="HTML")
            else:       
                bot.send_message(
                    chat_id=message.chat.id,
                    text=resposta,
                    reply_to_message_id=message.message_id,
                    reply_markup=markup,
                    parse_mode="HTML"
                )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text="Você não possui cartas no armazém.",
                reply_to_message_id=message.message_id
            )

    except mysql.connector.Error as err:
        print(f"Erro de SQL: {err}")
        newrelic.agent.record_exception()
        bot.send_message(message.chat.id, "Ocorreu um erro ao processar a consulta no banco de dados.")
    except ValueError as e:
        print(f"Erro: {e}")
        mensagem_banido = "Um erro ocorreu ao abrir seu armazém... Tente trocar seu fav usando o coamndo <code>/setfav</code>. Caso não resolva, entre em contato com o suporte."
        bot.send_message(message.chat.id, mensagem_banido,parse_mode="HTML")
    except telebot.apihelper.ApiHTTPException as e:
        print(f"Erro na API do Telegram: {e}")
    finally:
        fechar_conexao(cursor, conn)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    process_callback(call)

@bot.message_handler(commands=['youcompatev'])
def youcompatev_command_handler(message):
    youcompatev_command(message)
    
@bot.message_handler(commands=['mecompatev'])
def youcompatev_command_handler(message):
    mecompatev_command(message)    
    
def youcompatev_command(message):
    try:
        if not message.reply_to_message:
            bot.reply_to(message, "Você precisa usar este comando em resposta a uma mensagem de outro usuário.")
            return

        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "Uso: /youcompatev <nome do evento>")
            return
        
        evento = ' '.join(args[1:]).lower().strip()
        
        id_usuario_1 = message.from_user.id
        nome_usuario_1 = message.from_user.first_name
        id_usuario_2 = message.reply_to_message.from_user.id
        nome_usuario_2 = message.reply_to_message.from_user.first_name

        conn, cursor = conectar_banco_dados()

        query = """
        SELECT inv.id_personagem, e.nome
        FROM inventario inv
        JOIN evento e ON inv.id_personagem = e.id_personagem
        WHERE inv.id_usuario = %s AND e.evento = %s
        """
        cursor.execute(query, (id_usuario_1, evento))
        personagens_usuario_1 = {row[0]: row[1] for row in cursor.fetchall()}

        cursor.execute(query, (id_usuario_2, evento))
        personagens_usuario_2 = {row[0]: row[1] for row in cursor.fetchall()}

        diferenca = set(personagens_usuario_1.keys()) - set(personagens_usuario_2.keys())
        mensagem = f"<b>🎀 COMPATIBILIDADE DE EVENTO 🎀 \n\n</b>🍎 | <b><i>{evento.title()}</i></b>\n🧺 |<b> Cesta de:</b> {nome_usuario_1} \n⛈️ | <b>Faltantes de:</b> {nome_usuario_2} \n\n"
        if diferenca:
            for id_personagem in diferenca:
                mensagem += f"<code>{id_personagem}</code> - {personagens_usuario_1.get(id_personagem)}\n"
        else:
            mensagem += "Parece que não temos um match para este evento. Tente outro evento!"
        bot.send_message(message.chat.id, mensagem, parse_mode="HTML", reply_to_message_id=message.id)

    except Exception as e:
        bot.reply_to(message, f"Ocorreu um erro ao processar o comando: {e}")
    finally:
        fechar_conexao(cursor, conn)

def mecompatev_command(message):
    try:
        if not message.reply_to_message:
            bot.reply_to(message, "Você precisa usar este comando em resposta a uma mensagem de outro usuário.")
            return

        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "Uso: /mecompatev <nome do evento>")
            return
        
        evento = ' '.join(args[1:]).lower().strip()
        
        id_usuario_1 = message.from_user.id
        nome_usuario_1 = message.from_user.first_name
        id_usuario_2 = message.reply_to_message.from_user.id
        nome_usuario_2 = message.reply_to_message.from_user.first_name

        conn, cursor = conectar_banco_dados()

        query = """
        SELECT inv.id_personagem, e.nome
        FROM inventario inv
        JOIN evento e ON inv.id_personagem = e.id_personagem
        WHERE inv.id_usuario = %s AND e.evento = %s
        """
        cursor.execute(query, (id_usuario_1, evento))
        personagens_usuario_1 = {row[0]: row[1] for row in cursor.fetchall()}

        cursor.execute(query, (id_usuario_2, evento))
        personagens_usuario_2 = {row[0]: row[1] for row in cursor.fetchall()}

        diferenca = set(personagens_usuario_2.keys()) - set(personagens_usuario_1.keys())
        mensagem = f"<b>🎀 COMPATIBILIDADE DE EVENTO 🎀 \n\n</b>🍎 | <b><i>{evento.title()}</i></b>\n🧺 |<b> Cesta de:</b> {nome_usuario_2} \n⛈️ | <b>Faltantes de:</b> {nome_usuario_1} \n\n"
        if diferenca:
            for id_personagem in diferenca:
                mensagem += f"<code>{id_personagem}</code> - {personagens_usuario_2.get(id_personagem)}\n"
        else:
            mensagem += "Parece que não temos um match para este evento. Tente outro evento!"
        bot.send_message(message.chat.id, mensagem, parse_mode="HTML", reply_to_message_id=message.id)

    except Exception as e:
        bot.reply_to(message, f"Ocorreu um erro ao processar o comando: {e}")
    finally:
        fechar_conexao(cursor, conn)
    
@bot.message_handler(commands=['youcompat'])
def youcompat_command_handler(message):
    youcompat_command(message)
    
@bot.message_handler(commands=['diamante'])
def mostrar_diamante_handler(message):
    mostrar_diamante_por_nome(message)

@bot.message_handler(commands=['diamantes'])
def mostrar_diamantes_handler(message):
    mostrar_diamantes(message)
    
@bot.message_handler(commands=['incrementar_banco'])
def incrementar_banco_command(message):
    try:
        mensagens = incrementar_quantidades_banco()
        if isinstance(mensagens, list):
            for msg in mensagens:
                bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(message.chat.id, mensagens)
    except Exception as e:
        print(f"Erro ao incrementar quantidades no banco: {e}")
        bot.send_message(message.chat.id, "Erro ao incrementar quantidades no banco.")

@bot.message_handler(commands=['mecompat'])
def mecompat_handler(message):
    mecompat_command(message)

@bot.message_handler(commands=['diary'])
def handle_diary(message):
    diary_command(message)

@bot.message_handler(commands=['pages'])
def handle_pages(message):
    pages_command(message)

@bot.message_handler(commands=['page'])
def handle_page(message):
    page_command(message)                      

@bot.message_handler(commands=['wishlist'])
def verificar_cartas(message):
    try:
        conn, cursor = conectar_banco_dados()
        id_usuario = message.from_user.id

        # Definir a consulta SQL para a wishlist com collation uniforme
        sql_wishlist = f"""
            SELECT p.id_personagem, 
                   p.nome COLLATE utf8mb4_general_ci AS nome_personagem, 
                   p.subcategoria COLLATE utf8mb4_general_ci AS subcategoria, 
                   p.emoji COLLATE utf8mb4_general_ci AS emoji
            FROM wishlist w
            JOIN personagens p ON w.id_personagem = p.id_personagem
            WHERE w.id_usuario = {id_usuario}
            
            UNION
            
            SELECT e.id_personagem, 
                   e.nome COLLATE utf8mb4_general_ci AS nome_personagem, 
                   e.subcategoria COLLATE utf8mb4_general_ci AS subcategoria, 
                   e.emoji COLLATE utf8mb4_general_ci AS emoji
            FROM wishlist w
            JOIN evento e ON w.id_personagem = e.id_personagem
            WHERE w.id_usuario = {id_usuario}
        """

        cursor.execute(sql_wishlist)
        cartas_wishlist = cursor.fetchall()

        if cartas_wishlist:
            cartas_removidas = []

            for carta_wishlist in cartas_wishlist:
                id_personagem_wishlist = carta_wishlist[0]
                nome_carta_wishlist = carta_wishlist[1]
                subcategoria_carta_wishlist = carta_wishlist[2]
                emoji_carta_wishlist = carta_wishlist[3]

                cursor.execute("SELECT COUNT(*) FROM inventario WHERE id_usuario = %s AND id_personagem = %s",
                               (id_usuario, id_personagem_wishlist))
                existing_inventory_count = cursor.fetchone()[0]
                inventory_exists = existing_inventory_count > 0

                if inventory_exists:
                    cursor.execute("DELETE FROM wishlist WHERE id_usuario = %s AND id_personagem = %s",
                                   (id_usuario, id_personagem_wishlist))
                    cartas_removidas.append(f"{emoji_carta_wishlist} - {nome_carta_wishlist} de {subcategoria_carta_wishlist}")

            if cartas_removidas:
                resposta = f"Algumas cartas foram removidas da wishlist porque já estão no seu inventário:\n{', '.join(map(str, cartas_removidas))}"
                bot.send_message(message.chat.id, resposta, reply_to_message_id=message.message_id)

            lista_wishlist_atualizada = f"🤞 | Cartas na wishlist de {message.from_user.first_name}:\n\n"
            for carta_atualizada in cartas_wishlist:
                id_carta = carta_atualizada[0]
                emoji_carta = carta_atualizada[3]
                nome_carta = carta_atualizada[1]
                subcategoria_carta = carta_atualizada[2]
                lista_wishlist_atualizada += f"{emoji_carta} ∙ <code>{id_carta}</code> - {nome_carta} de {subcategoria_carta}\n"

            # Enviar mensagem com a foto
            imagem_url = "https://pub-6f23ef52e8614212a14d24b0cf55ae4a.r2.dev/BQACAgEAAxkBAAIe5mclnBkjVDX23Cd6UPDZqVLhCveaAAI0BQACsqkwRUye8-fjLlt-NgQ.jpg"
            bot.send_photo(
                message.chat.id,
                photo=imagem_url,
                caption=lista_wishlist_atualizada,
                reply_to_message_id=message.message_id,
                parse_mode="HTML"
            )
        else:
            bot.send_message(message.chat.id, "Sua wishlist está vazia! Devo te desejar parabéns?", reply_to_message_id=message.message_id)

    except mysql.connector.Error as err:
        print(f"Erro de SQL: {err}")
        traceback.print_exc()
        erro = traceback.format_exc()
        mensagem = f"wish com erro: {id_personagem}. erro: {err}\n{erro}"
        bot.send_message(grupodeerro, mensagem, parse_mode="HTML")
        bot.send_message(message.chat.id, "Ocorreu um erro ao processar a consulta no banco de dados.", reply_to_message_id=message.message_id)
    except ValueError as e:
        print(f"Erro: {e}")
        mensagem_banido = "Um erro ocorreu ao abrir seu armazém... Tente trocar seu fav usando o </code>comando /setfav</code>. Caso não resolva, entre em contato com o suporte."
        bot.send_message(message.chat.id, mensagem_banido)
    except telebot.apihelper.ApiHTTPException as e:
        print(f"Erro na API do Telegram: {e}")
    finally:
        conn.commit() 
        fechar_conexao(cursor, conn)



@bot.message_handler(commands=['addw'])
def add_to_wish(message):
    try:
        chat_id = message.chat.id
        id_usuario = message.from_user.id
        command_parts = message.text.split()
        if len(command_parts) == 2:
            id_personagem = command_parts[1]

            conn, cursor = conectar_banco_dados()
            cursor.execute("SELECT COUNT(*) FROM wishlist WHERE id_usuario = %s AND id_personagem = %s",
                           (id_usuario, id_personagem))
            existing_wishlist_count = cursor.fetchone()[0]
            wishlist_exists = existing_wishlist_count > 0

            if wishlist_exists:
                bot.send_message(chat_id, "Você já possui essa carta na wishlist!", reply_to_message_id=message.message_id)
            else:
                cursor.execute("SELECT COUNT(*) FROM inventario WHERE id_usuario = %s AND id_personagem = %s",
                               (id_usuario, id_personagem))
                existing_inventory_count = cursor.fetchone()[0]
                inventory_exists = existing_inventory_count > 0

                if inventory_exists:
                    bot.send_message(chat_id, "Você já possui essa carta no inventário!", reply_to_message_id=message.message_id)
                else:
                    cursor.execute("INSERT INTO wishlist (id_personagem, id_usuario) VALUES (%s, %s)",
                                   (id_personagem, id_usuario))
                    bot.send_message(chat_id, "Carta adicionada à sua wishlist!\nBoa sorte!", reply_to_message_id=message.message_id)
            conn.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao adicionar carta à wishlist: {err}")
    finally:
        fechar_conexao(cursor, conn)

@bot.message_handler(commands=['iduser'])
def handle_iduser_command(message):
    if message.reply_to_message:
        idusuario = message.reply_to_message.from_user.id
        bot.send_message(chat_id=message.chat.id, text=f"O ID do usuário é <code>{idusuario}</code>", reply_to_message_id=message.message_id,parse_mode="HTML")

@bot.message_handler(commands=['ping'])
def ping_command(message):
    start_time = time.time()
    chat_id = message.chat.id

    # Enviar uma mensagem de ping para calcular o tempo de resposta
    sent_message = bot.send_message(chat_id, "Calculando o ping...")

    ping = time.time() - start_time
    queue_size = task_queue.qsize()

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=sent_message.message_id,
        text=f"🏓 Pong!\nPing: {ping:.2f} segundos\nTarefas na fila: {queue_size}"
    )

@bot.message_handler(commands=['addw'])
def handle_add_to_wishlist(message):
    add_to_wish(message)

@bot.message_handler(commands=['removew', 'delw'])
def handle_removew(message):
    remover_da_wishlist(message)

@bot.message_handler(commands=['setbio'])
def handle_setbio(message):
    set_bio_command(message)

@bot.message_handler(commands=['admin'])
def handle_admin(message):
    admin(message)

@bot.message_handler(commands=['enviar_mensagem'])
def handle_enviar_mensagem_privada(message):
    enviar_mensagem_privada(message)

@bot.message_handler(commands=['enviar_grupo'])
def handle_enviar_mensagem_grupo(message):
    enviar_mensagem_grupo(message)


@bot.message_handler(commands=['supergroupid'])
def supergroup_id_command(message):
    chat_id = message.chat.id
    chat_type = message.chat.type

    if chat_type == 'supergroup':
        chat_info = bot.get_chat(chat_id)
        bot.send_message(chat_id, f"O ID deste supergrupo é: <code>{chat_info.id}</code>", reply_to_message_id=message.message_id,parse_mode="HTML")
    else:
        bot.send_message(chat_id, "Este chat não é um supergrupo.")

@bot.message_handler(commands=['idchat'])
def handle_idchat_command(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"O ID deste chat é<code>{chat_id}</code>", reply_to_message_id=message.message_id,parse_mode="HTML")

@bot.message_handler(commands=['setnome'])
def handle_set_nome(message):
    set_nome_command(message)

@bot.message_handler(commands=['setuser'])
def handle_setuser(message):
    setuser_comando(message)

@bot.message_handler(commands=['removefav'])
def handle_remove_fav(message):
    remove_fav_command(message)
    
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.chat.type == 'private':
        registrar_mensagens_privadas(message)
        
def apagar_cartas_quantidade_zero_ou_negativa():
    conn, cursor = conectar_banco_dados()
    try:
        query = "DELETE FROM inventario WHERE quantidade <= 0"
        cursor.execute(query)
        conn.commit()
        print(f"{cursor.rowcount} cartas deletadas.")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    finally:
        cursor.close()
        conn.close()

def registrar_mensagens_privadas(message):
    try:
        conn, cursor = conectar_banco_dados()
        user_id = message.from_user.id
        message_text = message.text
        cursor.execute("INSERT INTO mensagens_privadas (user_id, message_text) VALUES (%s, %s)", (user_id, message_text))
        conn.commit()
    except Exception as e:
        print(f"Erro ao registrar mensagem privada: {e}")
    finally:
        fechar_conexao(cursor, conn)   

def manter_proporcoes(imagem, largura_maxima, altura_maxima):
    largura_original, altura_original = imagem.size
    proporcao_original = largura_original / altura_original

    if proporcao_original > 1:
        nova_largura = largura_maxima
        nova_altura = int(largura_maxima / proporcao_original)
    else:
        nova_altura = altura_maxima
        nova_largura = int(altura_maxima * proporcao_original)

    return imagem.resize((nova_largura, nova_altura))        

# Função para criar a colagem
def criar_colagem(message):
    if message.from_user.id not in allowed_user_ids:
        bot.send_message(message.chat.id, "Você não tem permissão para usar este comando.")
        return

    try:
        cartas_aleatorias = obter_cartas_aleatorias()
        data_atual_str = dt_module.date.today().strftime("%Y-%m-%d") 
        if not cartas_aleatorias:
            bot.send_message(message.chat.id, "Não foi possível obter cartas aleatórias.")
            return

        registrar_cartas_loja(cartas_aleatorias, data_atual_str)

        imagens = []
        for carta in cartas_aleatorias:
            img_url = carta.get('imagem', '')
            try:
                if img_url:
                    response = requests.get(img_url)
                    if response.status_code == 200:
                        img = Image.open(io.BytesIO(response.content))
                        img = img.resize((300, 400), Image.LANCZOS)
                    else:
                        img = Image.new('RGB', (300, 400), color='black')
                else:
                    img = Image.new('RGB', (300, 400), color='black')
            except Exception as e:
                print(f"Erro ao abrir a imagem da carta {carta['id']}: {e}")
                img = Image.new('RGB', (300, 400), color='black')
            imagens.append(img)

        altura_total = (len(imagens) // 3) * 400

        colagem = Image.new('RGB', (900, altura_total))  
        coluna_atual = 0
        linha_atual = 0

        for img in imagens:
            colagem.paste(img, (coluna_atual, linha_atual))
            coluna_atual += 300

            if coluna_atual >= 900:
                coluna_atual = 0
                linha_atual += 400

        colagem.save('colagem_cartas.png')
        
        mensagem_loja = "🐟 Peixes na vendinha hoje:\n\n"
        for carta in cartas_aleatorias:
            mensagem_loja += f"{carta['emoji']}| {carta['id']} • {carta['nome']} - {carta['subcategoria']}\n"
        mensagem_loja += "\n🥕 Acesse usando o comando /vendinha"

        with open('colagem_cartas.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=mensagem_loja, reply_to_message_id=message.message_id)

    except Exception as e:
        print(f"Erro ao criar colagem: {e}")
        bot.send_message(message.chat.id, "Erro ao criar colagem.")


if __name__ == "__main__":
    app.run(host=WEBHOOK_LISTEN, port=int(WEBHOOK_PORT), debug=False)
