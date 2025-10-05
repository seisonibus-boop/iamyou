from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bd import *
from gif import *
from pesquisas import *
import globals
from botoes import *
from halloween import *
import os
import random
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import *
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# Configurar autenticação do Spotify com credenciais diretas
sp = Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id="804047efa98c4d1d81da250b0770c05d",
    client_secret="6deb00cb4cea42f79abe41cc4da05f13"
))

def enviar_perfil(chat_id, legenda, imagem_fav, fav, id_usuario,message):
    gif_url = obter_gif_url(fav, id_usuario)
    if gif_url:

        if gif_url.lower().endswith(('.mp4', '.gif')):
            bot.send_animation(chat_id, gif_url, caption=legenda, parse_mode="HTML",reply_to_message_id=message.message_id)
        else:
            bot.send_photo(chat_id, gif_url, caption=legenda, parse_mode="HTML",reply_to_message_id=message.message_id)
    elif legenda:

        if imagem_fav.lower().endswith(('.jpg', '.jpeg', '.png')):
            bot.send_photo(chat_id, imagem_fav, caption=legenda, parse_mode="HTML",reply_to_message_id=message.message_id)
        elif imagem_fav.lower().endswith(('.mp4', '.gif')):
            bot.send_animation(chat_id, imagem_fav, caption=legenda, parse_mode="HTML",reply_to_message_id=message.message_id)
    else: 
        bot.send_message(chat_id, legenda, parse_mode="HTML")


def handle_set_musica(message):
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) == 2:
        link_spotify = command_parts[1].strip()
        id_usuario = message.from_user.id

        try:
            track_id = link_spotify.split("/")[-1].split("?")[0]
            track_info = sp.track(track_id)
            nome_musica = track_info['name']
            artista = track_info['artists'][0]['name']
            nova_musica = f"{nome_musica} - {artista}"

            atualizar_coluna_usuario(id_usuario, 'musica', nova_musica)
            bot.send_message(message.chat.id, f"Música atualizada para: {nova_musica}")
        except Exception as e:
            bot.send_message(message.chat.id, f"Erro ao processar o link do Spotify: {e}")
    else:
        bot.send_message(message.chat.id, "Formato incorreto. Use /setmusica seguido do link do Spotify, por exemplo: /setmusica https://open.spotify.com/track/xxxx.")
            
def handle_set_fav(message):
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) == 2 and command_parts[1].isdigit():
        id_personagem = int(command_parts[1])
        id_usuario = message.from_user.id
        nome_personagem = obter_nome(id_personagem)
        qtd_cartas = buscar_cartas_usuario(id_usuario, id_personagem)

        if qtd_cartas > 0:
            atualizar_coluna_usuario(id_usuario, 'fav', id_personagem)
            bot.send_message(message.chat.id, f"❤ {id_personagem} — {nome_personagem} definido como favorito.", reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, f"Você não possui {id_personagem} no seu inventário, que tal ir pescar?", reply_to_message_id=message.message_id)

def handle_obter_username(message):
    if len(message.text.split()) == 2 and message.text.split()[1].isdigit():
        user_id = int(message.text.split()[1])
        username = obter_username_por_id(user_id)
        bot.reply_to(message, username)
    else:
        bot.reply_to(message, "Formato incorreto. Use /usuario seguido do user desejado, por exemplo: /usuario manoela")

def handle_me_command(message):
    id_usuario = message.from_user.id
    query_verificar_usuario = "SELECT COUNT(*) FROM usuarios WHERE id_usuario = %s"

    try:
        conn, cursor = conectar_banco_dados()

        # Verificar se o usuário existe
        cursor.execute(query_verificar_usuario, (id_usuario,))
        usuario_existe = cursor.fetchone()[0]

        if usuario_existe > 0:
            # Obter perfil do usuário
            query_obter_perfil = """
                SELECT 
                    u.nome, u.nome_usuario, u.fav, u.adm, u.qntcartas, u.cenouras, u.iscas, u.bio, u.musica, u.pronome, u.privado, u.user, u.beta,
                    COALESCE(p.nome, e.nome) AS nome_fav, 
                    COALESCE(p.imagem, e.imagem) AS imagem_fav
                FROM usuarios u
                LEFT JOIN personagens p ON u.fav = p.id_personagem
                LEFT JOIN evento e ON u.fav = e.id_personagem
                WHERE u.id_usuario = %s
            """
            cursor.execute(query_obter_perfil, (id_usuario,))
            perfil = cursor.fetchone()

            # Verificar se o usuário é VIP
            query_verificar_vip = "SELECT COUNT(*) FROM vips WHERE id_usuario = %s"
            cursor.execute(query_verificar_vip, (id_usuario,))
            is_vip = cursor.fetchone()[0] > 0

            # Verificar estado de casamento
            query_controle_casamento = """
                SELECT c.conjuge, COALESCE(p.nome, e.nome) AS nome_conjuge
                FROM controle_de_casamento c
                LEFT JOIN personagens p ON c.conjuge = p.id_personagem
                LEFT JOIN evento e ON c.conjuge = e.id_personagem
                WHERE c.usuario = %s AND c.casado = 'sim'
            """
            cursor.execute(query_controle_casamento, (id_usuario,))
            casamento_controle = cursor.fetchone()

            if not casamento_controle:
                query_casamentos = """
                    SELECT c.id_personagem, COALESCE(p.nome, e.nome) AS nome_parceiro
                    FROM casamentos c
                    LEFT JOIN personagens p ON c.id_personagem = p.id_personagem
                    LEFT JOIN evento e ON c.id_personagem = e.id_personagem
                    WHERE c.user_id = %s AND c.estado = 'casado'
                """
                cursor.execute(query_casamentos, (id_usuario,))
                casamento = cursor.fetchone()
            else:
                casamento = casamento_controle

            if perfil:
                nome, nome_usuario, fav, adm, qntcartas, cenouras, iscas, bio, musica, pronome, privado, user, beta, nome_fav, imagem_fav = perfil
                legenda = f"<b>Perfil de {nome}</b>\n\n" \
                          f"❤️ Fav: {fav} — {nome_fav}\n\n"

                if is_vip:
                    legenda += "<i>🌿 Agricultor do Garden</i>\n\n"

                if casamento:
                    parceiro_id, parceiro_nome = casamento
                    legenda += f"💍 Casado(a) com {parceiro_nome}\n\n"

                if adm:
                    legenda += f"🌈 Adm: {adm.capitalize()}\n\n"
                if beta:
                    legenda += f"🍀 Usuario Beta\n\n"

                legenda += f"👩🏻‍🌾 Camponês: {user}\n" \
                           f"🎣 Peixes: {qntcartas}\n" \
                           f"🥕 Cenouras: {cenouras}\n" \
                           f"🪝 Iscas: {iscas}\n"

                if pronome:
                    legenda += f"🪷 Pronomes: {pronome}\n\n"

                legenda += f"💬: {bio}\n\n" \
                           f"🎧: {musica}"

                # Criar botões de votação
                doces, fantasmas = contar_votos(id_usuario)
                markup = InlineKeyboardMarkup()
                botao_doce = InlineKeyboardButton(text=f"💗 {doces}", callback_data=f"votar_doce_{id_usuario}")
                botao_fantasma = InlineKeyboardButton(text=f"🕊️ {fantasmas}", callback_data=f"votar_fantasma_{id_usuario}")
                markup.add(botao_doce, botao_fantasma)

                enviar_perfil(message.chat.id, legenda, imagem_fav, fav, id_usuario, message)

        else:
            bot.send_message(message.chat.id, "Você ainda não iniciou o bot. Use /start para começar.", reply_to_message_id=message.message_id)

    except Exception as e:
        traceback.print_exc() 
        print(f"Erro ao verificar perfil: {e}")
        bot.send_message(message.chat.id, f"Erro ao verificar perfil: {e}", reply_to_message_id=message.message_id)

    finally:
        fechar_conexao(cursor, conn)
        
def handle_gperfil_command(message):
    if len(message.text.split()) != 2:
        bot.send_message(message.chat.id, "Formato incorreto. Use /gperfil seguido do nome de usuário desejado.")
        return

    username = message.text.split()[1].strip()

    try:
        conn, cursor = conectar_banco_dados()

        query_verificar_usuario = "SELECT 1 FROM usuarios WHERE user = %s"
        cursor.execute(query_verificar_usuario, (username,))
        usuario_existe = cursor.fetchone()

        if usuario_existe:

            query_obter_perfil = """
                SELECT 
                    u.nome, u.nome_usuario, u.fav, u.adm, u.qntcartas, u.cenouras, u.iscas, u.bio, u.musica, u.pronome, u.privado, u.beta,
                    COALESCE(p.nome, e.nome) AS nome_fav, 
                    COALESCE(p.imagem, e.imagem) AS imagem_fav
                FROM usuarios u
                LEFT JOIN personagens p ON u.fav = p.id_personagem
                LEFT JOIN evento e ON u.fav = e.id_personagem
                WHERE u.user = %s
            """
            cursor.execute(query_obter_perfil, (username,))
            perfil = cursor.fetchone()

            if perfil:
                nome, nome_usuario, fav, adm, qntcartas, cenouras, iscas, bio, musica, pronome, privado, beta, nome_fav, imagem_fav = perfil

                if beta == 1:
                    usuario_beta = True
                else:
                    usuario_beta = False
                if privado == 1:
                    resposta = f"<b>Perfil de {username}</b>\n\n" \
                               f"✨ Fav: {fav} — {nome_fav}\n\n"
                    if usuario_beta:
                        resposta += f"🍀 Usuario Beta\n\n"         
                    if adm:
                        resposta += f"🌈 Adm: {adm.capitalize()}\n\n"
                    if pronome:
                        resposta += f"🌺 Pronomes: {pronome.capitalize()}\n\n" 
                          
                    resposta += f"🔒 Perfil Privado"
                else:
                    resposta = f"<b>Perfil de {nome_usuario}</b>\n\n" \
                               f"✨ Fav: {fav} — {nome_fav}\n\n" \
                      
                    if usuario_beta:
                        resposta += f"🍀 <b>Usuario Beta</b>\n\n" 
                    if adm:
                        resposta += f"🌈 Adm: {adm.capitalize()}\n\n"
                    if pronome:
                        resposta += f"🌺 Pronomes: {pronome.capitalize()}\n\n" \
 
                    
                    resposta += f"‍🧑‍🌾 Camponês: {nome}\n" \
                                f"🐟 Peixes: {qntcartas}\n" \
                                f"🥕 Cenouras: {cenouras}\n" \
                                f"🪝 Iscas: {iscas}\n" \
                                f"✍ {bio}\n\n" \
                                f"🎧: {musica}"

                enviar_perfil(message.chat.id, resposta, imagem_fav, fav, message.from_user.id, message)
            else:
                bot.send_message(message.chat.id, "Perfil não encontrado.")
        else:
            bot.send_message(message.chat.id, "O nome de usuário especificado não está registrado.")

        
    except mysql.connector.Error as err:
        bot.send_message(message.chat.id, f"Erro ao verificar o perfil: {err}")
    finally:
        fechar_conexao(cursor, conn)

def set_bio_command(message):
    id_usuario = message.from_user.id
    nome_usuario = message.from_user.first_name  # Obtém o nome do usuário
    command_parts = message.text.split(maxsplit=1)
    
    if len(command_parts) == 2:
        nova_bio = command_parts[1].strip()
        atualizar_coluna_usuario(id_usuario, 'bio', nova_bio)
        bot.send_message(message.chat.id, f"Bio do {nome_usuario} atualizada para: {nova_bio}")
    else:
        bot.send_message(message.chat.id, "Formato incorreto. Use /setbio seguido da nova bio desejada, por exemplo: /setbio Hhmm, bolo de morango.")

def set_nome_command(message):
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) == 2:
        novo_nome = command_parts[1].strip()
        id_usuario = message.from_user.id
        atualizar_coluna_usuario(id_usuario, 'nome', novo_nome)
        bot.send_message(message.chat.id, f"Nome atualizado para: {novo_nome}", reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id,
                         "Formato incorreto. Use /setnome seguido do novo nome, por exemplo: /setnome Manoela Gavassi", reply_to_message_id=message.message_id)
def setuser_comando(message):
    command_parts = message.text.split()
    if len(command_parts) != 2:
        bot.send_message(message.chat.id, "Formato incorreto. Use /setuser seguido do user desejado, por exemplo: /setuser novouser.", reply_to_message_id=message.message_id)
        return

    nome_usuario = command_parts[1].strip()

    if not re.match("^[a-zA-Z0-9_]{1,20}$", nome_usuario):
        bot.send_message(message.chat.id, "Nome de usuário inválido. Use apenas letras, números e '_' e não ultrapasse 20 caracteres.", reply_to_message_id=message.message_id)
        return

    try:
        conn, cursor = conectar_banco_dados()
        cursor.execute("SELECT 1 FROM usuarios WHERE user = %s", (nome_usuario,))
        if cursor.fetchone():
            bot.send_message(message.chat.id, "O nome de usuário já está em uso. Escolha outro nome de usuário.", reply_to_message_id=message.message_id)
            return

        cursor.execute("SELECT 1 FROM usuarios_banidos WHERE id_usuario = %s", (nome_usuario,))
        if cursor.fetchone():
            bot.send_message(message.chat.id, "O nome de usuário já está em uso. Escolha outro nome de usuário.", reply_to_message_id=message.message_id)
            return

        cursor.execute("UPDATE usuarios SET user = %s WHERE id_usuario = %s", (nome_usuario, message.from_user.id))
        conn.commit()

        bot.send_message(message.chat.id, f"O nome de usuário foi alterado para '{nome_usuario}'.", reply_to_message_id=message.message_id)

    except mysql.connector.Error as err:
        bot.send_message(message.chat.id, f"Erro ao processar comando /setuser: {err}", reply_to_message_id=message.message_id)

    finally:
        fechar_conexao(cursor, conn)

def handle_config(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Pronomes', callback_data='bpronomes_')
    btn2 = types.InlineKeyboardButton('Privacidade', callback_data='privacy')
    btn3 = types.InlineKeyboardButton('Lembretes', callback_data='lembretes')
    btn_cancelar = types.InlineKeyboardButton('❌ Cancelar', callback_data='pcancelar')
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn_cancelar)
    
    bot.send_message(message.chat.id, "Escolha uma opção:", reply_markup=markup)

def remove_fav_command(message):
    id_usuario = message.from_user.id

    conn, cursor = conectar_banco_dados()
    cursor.execute("UPDATE usuarios SET fav = NULL WHERE id_usuario = %s", (id_usuario,))
    conn.commit()

    bot.send_message(message.chat.id, "Favorito removido com sucesso.", reply_to_message_id=message.message_id)


