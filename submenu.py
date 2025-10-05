from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bd import *
from gif import *
import globals
from botoes import *
import random
def mostrar_primeira_pagina_submenus(message, subcategoria):
    try:
        conn, cursor = conectar_banco_dados()
        query_total = "SELECT COUNT(DISTINCT submenu) FROM personagens WHERE subcategoria = %s"
        cursor.execute(query_total, (subcategoria,))
        total_registros = cursor.fetchone()[0]
        total_paginas = (total_registros // 15) + (1 if total_registros % 15 > 0 else 0)

        if total_registros == 0:
            bot.reply_to(message, f"Nenhum submenu encontrado para a subcategoria '{subcategoria}'.")
            return

        query = "SELECT DISTINCT submenu FROM personagens WHERE subcategoria = %s LIMIT 15"
        cursor.execute(query, (subcategoria,))
        resultados = cursor.fetchall()

        if resultados:
            resposta = f"🔖| Submenus na subcategoria {subcategoria}:\n\n"
            for resultado in resultados:
                submenu = resultado[0]
                resposta += f"• {submenu}\n"

            markup = None
            if total_paginas > 1:
                markup = criar_markup_submenus(1, total_paginas, subcategoria)
            bot.send_message(message.chat.id, resposta, reply_markup=markup, parse_mode="HTML")
        else:
            bot.reply_to(message, f"Nenhum submenu encontrado para a subcategoria '{subcategoria}'.")

    except Exception as e:
        print(f"Erro ao processar comando /submenus: {e}")
        bot.reply_to(message, "Ocorreu um erro ao processar sua solicitação.")

def editar_mensagem_submenus(call, subcategoria, pagina_atual, total_paginas):
    try:
        conn, cursor = conectar_banco_dados()

        offset = (pagina_atual - 1) * 15
        query = "SELECT DISTINCT submenu FROM personagens WHERE subcategoria = %s LIMIT 15 OFFSET %s"
        cursor.execute(query, (subcategoria, offset))
        resultados = cursor.fetchall()

        if resultados:
            resposta = f"🔖| Submenus na subcategoria {subcategoria}, página {pagina_atual}/{total_paginas}:\n\n"
            for resultado in resultados:
                submenu = resultado[0]
                resposta += f"• {submenu}\n"

            markup = criar_markup_submenus(pagina_atual, total_paginas, subcategoria)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=resposta, reply_markup=markup, parse_mode="HTML")
        else:
            bot.reply_to(call.message, f"Nenhum submenu encontrado para a subcategoria '{subcategoria}'.")

    except Exception as e:
        print(f"Erro ao editar mensagem de submenus: {e}")
        bot.reply_to(call.message, "Ocorreu um erro ao processar sua solicitação.")

def criar_markup_submenus(pagina_atual, total_paginas, subcategoria):
    markup = telebot.types.InlineKeyboardMarkup()

    if pagina_atual > 1:
        btn_anterior = telebot.types.InlineKeyboardButton("⬅️", callback_data=f"submenus_{pagina_atual-1}_{subcategoria}")
        markup.add(btn_anterior)
    
    if pagina_atual < total_paginas:
        btn_proxima = telebot.types.InlineKeyboardButton("➡️", callback_data=f"submenus_{pagina_atual+1}_{subcategoria}")
        markup.add(btn_proxima)

    return markup

def callback_submenu(call):
    _, subcategoria, submenu_selecionado = call.data.split('_')
    conn, cursor = conectar_banco_dados()
    try:
        cartas_disponiveis = obter_cartas_por_subcategoria_e_submenu(subcategoria, submenu_selecionado, cursor)
        
        if not cartas_disponiveis:
            bot.send_message(call.message.chat.id, "Nenhuma carta disponível para esta combinação.")
            return

        # Enviar carta principal
        carta_principal = random.choice(cartas_disponiveis)
        id_principal, emoji_principal, nome_principal, imagem_principal = carta_principal
        send_card_message(call.message, emoji_principal, id_principal, nome_principal, subcategoria, imagem_principal)

        # Verificar picolé de coco (30% chance)
        cursor.execute("SELECT sabor FROM sorvetes WHERE user_id = %s AND sabor = 'coco'", (call.from_user.id,))
        tem_coco = cursor.fetchone()
        
        if tem_coco and random.random() < 1:
            carta_extra = random.choice(cartas_disponiveis)
            id_extra, emoji_extra, nome_extra, imagem_extra = carta_extra

            # Usar a função existente para adicionar ao inventário
            add_to_inventory(call.from_user.id, id_extra)  # Alteração crucial aqui

            # Montar e enviar mensagem com foto e bônus
            caption = (
                f"🥥 Bônus Picolé de Coco!\n"
                f"Você pescou junto:\n"
                f"<code>{id_extra}</code> - {nome_extra}\n"
                f"▸ {subcategoria.replace('_', ' ').title()} → {submenu_selecionado.title()}"
            )
            
            bot.send_photo(
                call.message.chat.id,
                imagem_extra,
                caption=caption,
                parse_mode="HTML"
            )

    except Exception as e:
        print(f"Erro no submenu: {str(e)}")
        bot.send_message(call.message.chat.id, "❌ Ocorreu um erro ao processar o submenu.")
    finally:
        cursor.close()
        conn.close()
