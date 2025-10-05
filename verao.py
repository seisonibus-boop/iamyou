from bd import bot, conectar_banco_dados,fechar_conexao
from pescar import add_to_inventory
from telebot.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
import time
import random
# Adicione no início do arquivo
from datetime import datetime, timedelta
import traceback
# Listas de respostas temáticas de verão
respostas_acerto = [
    "Golaço na areia! 🏖️🌞",
    "Você balançou a rede! Vai um suco de coco para comemorar? 🥥🥳",
    "Gol de placa! A galera da praia vai à loucura! 🎉⚽",
    "Que chute certeiro! Toma um mergulho para refrescar! 🏊‍♂️",
    "Marcou bonito! Pega o sorvete e comemora! 🍦⚽"
]

respostas_erro = [
    "Quase! Mas a areia atrapalhou um pouco... 🏖️😅",
    "Ops, passou perto! Que tal tentar de novo depois de um banho de mar? 🌊😉",
    "Foi por pouco! A bola ficou na sombra do guarda-sol! 🌞⚽",
    "Não foi dessa vez, mas a praia é longa! Tente outra vez! 🏝️",
    "A bola foi parar na água! Vamos resgatar e tentar de novo! 🌊⚽"
]

def send_futebol_dice(message):
    try:
        user_id = message.from_user.id
        nome = message.from_user.first_name

        if not can_play(user_id, 'futebol'):
            bot.send_message(message.chat.id, "⏳ Calma, craque! Só um jogo por hora.")
            return

        # Envia o dado e processa
        sent_message = bot.send_dice(message.chat.id, emoji='⚽')
        result_value = sent_message.dice.value

        # Determina resultado
        acertou = result_value in [4, 5]
        
        # Monta resposta
        if acertou:
            # Frase temática + recompensas
            frase = random.choice(respostas_acerto)
            cenouras = random.randint(30, 60)
            sucesso = aumentar_cenouras_tesouro(user_id, cenouras)
            
            # 20% chance de carta de evento esportivo
            carta = None
            if random.random() < 0.8:
                carta = obter_carta_evento_verao()
            
            resposta = (
                f"⚽ {frase}\n\n"
                f"🧺 <b>Recompensas da Torcida:</b>\n"
                f"- +{cenouras} Cenouras Douradas 🥕\n"
            )
            
            if carta:
                emoji_carta, id_carta, nome_carta, subcat, img = carta
                add_to_inventory(user_id, id_carta)
                resposta += (
                    f"- {emoji_carta} {id_carta} - <i>{nome_carta}</i>\n"
                    f"  de {subcat.replace('_', ' ').title()}\n"
                )
            
            resposta += "\n🌴 Jogue novamente após 1 hora!"

        else:
            frase = random.choice(respostas_erro)
            resposta = f"🌊 {frase}\n\n🏖️ Tente novamente mais tarde!"

        bot.send_message(
            message.chat.id,
            resposta,
            parse_mode="HTML"
        )
        update_interaction_time(user_id, 'futebol')

    except Exception as e:
        print(f"Erro no futebol: {str(e)}")
        bot.send_message(message.chat.id, "⚽ A bola furou! Erro no jogo...")
    
def handle_reset_time(message):
    try:
        db, cursor = conectar_banco_dados()
        # Verifica se o comando foi enviado pelo administrador
        if message.from_user.id != 5532809878 and message.from_user.id != 1805086442:
            bot.reply_to(message, "🚫 Comando restrito ao desenvolvedor!")
            return

        # Verifica se é resposta a uma mensagem
        if not message.reply_to_message:
            bot.reply_to(message, "⚠️ Responda a uma mensagem do usuário que deseja resetar!")
            return

        # Pega o ID do usuário alvo
        target_user = message.reply_to_message.from_user.id

        # Executa a exclusão
        cursor.execute(
            "DELETE FROM user_interactions WHERE user_id = %s",
            (target_user,)
        )
        db.commit()

        # Confirmação
        bot.reply_to(
            message,
            f"✅ Tempo resetado para [User {target_user}](tg://user?id={target_user})",
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"Erro no /resettime: {str(e)}")
        bot.reply_to(message, f"💥 Falha ao resetar: {str(e)}")
def can_play(user_id, tipo):
    try:
        db, cursor = conectar_banco_dados()
        cursor.execute('SELECT last_interaction FROM user_interactions WHERE user_id = %s AND tipo = %s', (user_id, tipo))
        result = cursor.fetchone()
        if result:
            last_interaction = result[0]
            if time.time() - last_interaction < 3600:
                print(f"Debug: Usuário {user_id} tentou jogar {tipo} mas ainda está no tempo de espera.")
                return False
        print(f"Debug: Usuário {user_id} pode jogar {tipo}.")
        return True
    except Exception as e:
        print(f"Erro ao verificar se o usuário pode jogar: {e}")
        return False

def update_interaction_time(user_id, tipo):
    try:
        db, cursor = conectar_banco_dados()
        current_time = time.time()
        cursor.execute('INSERT INTO user_interactions (user_id, tipo, last_interaction) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE last_interaction = %s', (user_id, tipo, current_time, current_time))
        db.commit()
        print(f"Debug: Tempo de interação atualizado para o usuário {user_id} no jogo {tipo}.")
    except Exception as e:
        print(f"Erro ao atualizar o tempo de interação: {e}")
def aumentar_cenouras_tesouro(user, valor):
    conn = None
    cursor = None
    try:
        conn, cursor = conectar_banco_dados()
        
        # 1. Verificar/Criar tabela se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario BIGINT PRIMARY KEY,
                cenouras INT NOT NULL DEFAULT 0
            )
        """)
        
        # 2. Verificar usuário
        cursor.execute("SELECT cenouras FROM usuarios WHERE id_usuario = %s", (user,))
        resultado = cursor.fetchone()

        if not resultado:
            # 3. Criar novo usuário se não existir
            cursor.execute(
                "INSERT INTO usuarios (id_usuario, cenouras) VALUES (%s, %s)",
                (user, valor)
            )
        else:
            # 4. Atualizar cenouras usando SQL mais seguro
            cursor.execute(
                "UPDATE usuarios SET cenouras = cenouras + %s WHERE id_usuario = %s",
                (valor, user)
            )
        
        conn.commit()
        return True

    except Exception as e:
        print(f"[ERRO] Falha ao atualizar cenouras:")
        traceback.print_exc()
        if conn:
            conn.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def send_game_ui(chat_id, tesouro, tentativas, escolhas, nome, message_id=None, cenouras=None, carta_evento=None):
    try:
        linha = ['⛱️'] * 9
        # Debug 6: Estado do jogo
        print(f"[DEBUG] send_game_ui - Tesouro: {tesouro}, Tentativas: {tentativas}, Escolhas: {escolhas}")
        # Preenche com X nas escolhas erradas
        for pos in escolhas:
            if pos != tesouro:  # Não sobrescreve o tesouro
                linha[pos] = '❌'

        # Revela o tesouro se o jogo acabou
        if tentativas == 0 or any(pos == tesouro for pos in escolhas):
            linha[tesouro] = '💰'

        grade = "\n".join([" ".join(linha[i:i+3]) for i in range(0, 9, 3)])
        
        # Monta a mensagem principal
        if any(pos == tesouro for pos in escolhas):
            texto = (
                f"🏆 <b>Parabéns, {nome}!</b>\n\n"
                f"<b>Tesouros encontrados:</b>\n"
                f"🧺 Cesta de vime com <b>{cenouras}</b> cenouras douradas 🥕\n"
            )
            
            if carta_evento:
                emoji, id_pers, nome_carta, subcat, img = carta_evento
                add_to_inventory(chat_id, id_pers)  # Assume-se que chat_id é o user_id
                texto += (
                    f"📜 <i>Tesouro Especial:</i> \n{emoji} {id_pers} - <b>{nome_carta}</b>\n"
                    f"de {subcat.replace('_', ' ').title()}\n\n"
                )
            
            texto += (
                f"🌊 No diário da vovó: receitas secretas de geleias marinhas!\n\n"
                f"{grade}"
            )
        elif tentativas == 0:
            texto = f"🌊<b> O vento trouxe o cheiro de maresia e o tesouro dança com as ondas do mar...</b> \n\n{grade}"
        else:
            texto = (
                f"🧺🌊<b><i>Na trilha do tesouro na areia...</i></b>\n\n"
                f"<b>Canteiro de Buscas:</b>\n\n{grade}\n\n"
                f"Sinais na areia: Você tem {tentativas} usos de pá\n"
            )
        # Remove botões se o jogo terminou
        markup = None
        if tentativas > 0 and not any(pos == tesouro for pos in escolhas):
            markup = InlineKeyboardMarkup()
            buttons = []
            for i in range(9):
                if i in escolhas:
                    buttons.append(InlineKeyboardButton('🚫', callback_data="invalid"))
                else:
                    data = f"jogada_{i}_{tesouro}_{tentativas}_{','.join(map(str, escolhas))}_{nome}"
                    buttons.append(InlineKeyboardButton(str(i+1), callback_data=data))
            
            markup.row(buttons[0], buttons[1], buttons[2])
            markup.row(buttons[3], buttons[4], buttons[5])
            markup.row(buttons[6], buttons[7], buttons[8])

        # Envia/atualiza a mensagem
        if message_id:
            bot.edit_message_text(
                texto,
                chat_id,
                message_id,
                reply_markup=markup,
                parse_mode="HTML"
            )
        else:
            bot.send_message(
                chat_id,
                texto,
                reply_markup=markup,
                parse_mode="HTML"
            )
            
    except Exception as e:
        print(f"Erro na UI: {e}")
def obter_carta_evento_verao():
    try:
        conn, cursor = conectar_banco_dados()
        
        query = """
            SELECT emoji, id_personagem, nome, subcategoria, imagem 
            FROM evento 
            WHERE evento = 'fixo'
            ORDER BY RAND() 
            LIMIT 1
        """
        cursor.execute(query)
        evento_aleatorio = cursor.fetchone()
        
        return evento_aleatorio
        
    except mysql.connector.Error as err:
        print(f"Erro ao obter carta de evento: {err}")
        return None
    finally:
        fechar_conexao(cursor, conn)
# Lista de picolés disponíveis
PICOLES = {
    "melancia": "🍉 Picolé de Melancia",
    "amendoim": "🥜 Picolé de Amendoim",
    "chocolate": "🍫 Picolé de Chocolate",
    "uva": "🍇 Picolé de Uva",
    "milho": "🌽 Picolé de Milho Verde",
    "coco": "🥥 Picolé de Coco",
    "morango": "🍓 Picolé de Morango"
}

FRASES_FALHA = [
    "O sorveteiro te viu e achou sua cara engraçada! Nada de picolé hoje... 😜",
    "O carrinho quebrou justo na sua vez! Melhor sorte na próxima! 🚚💨",
    "Um pássaro roubou seu picolé! 🐦❄️",
    "Você escorregou na calçada enquanto pegava... Tente novamente! 🧊💢",
    "O último picolé derreteu nas suas mãos! ☀️💦"
]

def handle_sorveteiro(message):
    try:
        db, cursor = conectar_banco_dados()
        user_id = message.from_user.id
        cursor.execute("SELECT sabor FROM sorvetes WHERE user_id = %s", (user_id,))
        resultado = cursor.fetchone()

        if random.random() < 0.5:
            sabor_novo = random.choice(list(PICOLES.keys()))
            texto = f"🎉 {PICOLES[sabor_novo]}!\nO sorveteiro te entregou um picolé refrescante!"

            if resultado:
                texto += f"\n\nVocê já tem um {PICOLES[resultado[0]]}! Deseja substituir?"
                markup = InlineKeyboardMarkup()
                markup.row(
                    InlineKeyboardButton("✅ Sim", callback_data=f"trocar_{user_id}_{sabor_novo}"),
                    InlineKeyboardButton("❌ Não", callback_data=f"manter_{user_id}")
                )
            else:
                cursor.execute("INSERT INTO sorvetes (user_id, sabor) VALUES (%s, %s)", 
                              (user_id, sabor_novo))
                db.commit()
                if sabor_novo == "milho":  # Novo: Ativar bônus se for milho
                    ativar_bonus_picole(user_id)
                    print(f"[DEBUG] Picolé de milho ativado para {user_id}")
                texto += "\n\n🍧 Aproveite seu picolé!"
                markup = None

        else:
            texto = f"❄️ {random.choice(FRASES_FALHA)}"
            markup = None

        bot.send_message(message.chat.id, texto, reply_markup=markup, parse_mode="HTML")

    except Exception as e:
        print(f"Erro no sorveteiro: {str(e)}")
        bot.send_message(message.chat.id, "🍦 O freezer quebrou! Tente novamente mais tarde.")
        
def handle_troca_picole(call):
    db, cursor = None, None
    try:
        db, cursor = conectar_banco_dados()
        data = call.data.split('_')
        user_id = int(data[1])
        sabor_completo = '_'.join(data[2:])

        # 1. Verificar operação de troca
        if call.data.startswith('trocar'):
            # 2. Buscar sabor antigo
            cursor.execute("SELECT sabor FROM sorvetes WHERE user_id = %s", (user_id,))
            resultado = cursor.fetchone()
            sabor_antigo = resultado[0] if resultado else None

            # 3. Atualizar sabor
            cursor.execute(
                """INSERT INTO sorvetes (user_id, sabor) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE sabor = VALUES(sabor)""",
                (user_id, sabor_completo)
            )
            db.commit()

            # 4. Gerenciar bônus do milho
            if sabor_completo == "milho":
                ativar_bonus_picole(user_id)
            elif sabor_antigo == "milho":
                desativar_bonus_picole(user_id)

            texto = f"🍦🔄 {PICOLES[sabor_completo]}\nSeu picolé foi atualizado!"
        else:
            # 5. Manter sabor atual
            cursor.execute("SELECT sabor FROM sorvetes WHERE user_id = %s", (user_id,))
            resultado = cursor.fetchone()
            if resultado:  # Verificação crítica
                texto = f"🍧 {PICOLES[resultado[0]]}\nSeu picolé original foi mantido!"
            else:
                texto = "❌ Nenhum picolé encontrado para manter!"

        # 6. Atualizar mensagem
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=texto
        )

    except mysql.connector.Error as err:
        print(f"Erro MySQL ({err.errno}): {err.msg}")
        bot.answer_callback_query(call.id, "❌ Erro no banco de dados!")
    except Exception as e:
        print(f"Erro geral na troca: {traceback.format_exc()}")
        bot.answer_callback_query(call.id, "❌ Ops! O picolé derreteu na troca...")
    finally:
        # 7. Fechar recursos de forma segura
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()
# --- FUNÇÕES ATUALIZADAS COM A ESTRUTURA CORRETA ---

def ativar_bonus_picole(user_id):
    """Registra o picolé de milho como ativo"""
    conn, cursor = conectar_banco_dados()
    try:
        cursor.execute(
            """INSERT INTO picole_milho_ativo 
            (id_usuario, data_ativacao, ultimo_processamento, total_minutos)
            VALUES (%s, NOW(), NOW(), 0)
            ON DUPLICATE KEY UPDATE 
                data_ativacao = NOW(),
                ultimo_processamento = NOW(),
                total_minutos = 0""",
            (user_id,)
        )
        conn.commit()
    except Exception as e:
        print(f"Erro ao ativar picolé: {str(e)}")
    finally:
        fechar_conexao(cursor, conn)

def calcular_cenouras_picole(user_id):
    print(f"[DEBUG] Iniciando cálculo para {user_id}")
    conn, cursor = None, None
    try:
        conn, cursor = conectar_banco_dados()
        
        # 1. Verificar se tem sorvete de milho
        cursor.execute(
            "SELECT sabor FROM sorvetes WHERE user_id = %s AND sabor = 'milho'",
            (user_id,)
        )
        tem_milho = cursor.fetchone()
        print(f"[DEBUG] Tem milho? {'Sim' if tem_milho else 'Não'}")
        
        if not tem_milho:
            print(f"[DEBUG] Removendo registro de milho (se existir)")
            cursor.execute(
                "DELETE FROM picole_milho_ativo WHERE id_usuario = %s",
                (user_id,)
            )
            conn.commit()
            return 0
        
        # 2. Buscar dados de tempo
        cursor.execute(
            """SELECT ultimo_processamento, total_minutos 
            FROM picole_milho_ativo 
            WHERE id_usuario = %s""",
            (user_id,)
        )
        resultado = cursor.fetchone()
        print(f"[DEBUG] Dados do cálculo: {resultado}")
        
        if not resultado:
            print(f"[ERRO] Registro de milho não encontrado para {user_id}")
            return 0
        
        ultimo_ts, minutos_acumulados = resultado
        agora = datetime.now()
        
        # 3. Calcular diferença de tempo
        diferenca_segundos = (agora - ultimo_ts).total_seconds()
        diferenca_minutos = diferenca_segundos // 60
        total_minutos = minutos_acumulados + diferenca_minutos
        print(f"[DEBUG] Diferença: {diferenca_minutos} min | Total: {total_minutos} min")
        
        # 4. Calcular cenouras
        horas, minutos_residuais = divmod(total_minutos, 60)
        cenouras = int(horas) * 50
        print(f"[DEBUG] Cenouras calculadas: {cenouras} ({horas}h)")
        
        if cenouras > 0:
            # 5. Atualizar usuário
            cursor.execute(
                "UPDATE usuarios SET cenouras = cenouras + %s WHERE id_usuario = %s",
                (cenouras, user_id)
            )
            
            # 6. Atualizar registro
            novo_ultimo_ts = agora - timedelta(minutes=minutos_residuais)
            print(f"[DEBUG] Novo último processamento: {novo_ultimo_ts}")
            
            cursor.execute(
                """UPDATE picole_milho_ativo SET 
                    ultimo_processamento = %s, 
                    total_minutos = %s 
                    WHERE id_usuario = %s""",
                (novo_ultimo_ts, minutos_residuais, user_id)
            )
            
            conn.commit()
            print(f"[DEBUG] {cenouras} cenouras adicionadas")
            return cenouras
            
        return 0
        
    except Exception as e:
        print(f"[ERRO] cálculo cenouras: {traceback.format_exc()}")
        return 0
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected():
            conn.close()
