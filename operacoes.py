from pesquisas import *
from peixes import *
from user import *
from bd import *
from loja import *
from gnome import *
from operacoes import *
import requests
from datetime import datetime

def diminuir_cenouras(id_usuario, valor):
    try:
        conn, cursor = conectar_banco_dados()
        cursor.execute("SELECT cenouras FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        resultado = cursor.fetchone()

        if resultado:
            cenouras_atuais = int(resultado[0]) 
            if cenouras_atuais >= valor:
                nova_quantidade = cenouras_atuais - valor
                cursor.execute("UPDATE usuarios SET cenouras = %s WHERE id_usuario = %s", (nova_quantidade, id_usuario))
                conn.commit()
            else:
                print("Erro: Não há cenouras suficientes para diminuir.")
        else:
            print("Erro: Usuário não encontrado.")

    except Exception as e:
        print(f"Erro ao diminuir cenouras: {e}")

    finally:
        fechar_conexao(cursor, conn)
        
def diminuir_giros(id_usuario, quantidade):
    try:
        conn, cursor = conectar_banco_dados()
        cursor.execute("SELECT id_usuario, nome, iscas FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        resultado_usuario = cursor.fetchone()

        if resultado_usuario:
            id_usuario = resultado_usuario[0]
            nome_usuario = resultado_usuario[1]
            iscas_atuais = int(resultado_usuario[2]) 

            if iscas_atuais >= quantidade:
                nova_quantidade = iscas_atuais - quantidade
                cursor.execute("UPDATE usuarios SET iscas = %s WHERE id_usuario = %s", (nova_quantidade, id_usuario))

                conn.commit()
            else:
                print("Erro: Não há iscas suficientes para diminuir.")
        else:
            print("Erro: Usuário não encontrado.")
    except Exception as e:
        print(f"Erro ao diminuir iscas: {e}")
    finally:
        fechar_conexao(cursor, conn)

def registrar_usuario(id_usuario, nome_usuario, username):
    try:
        conn, cursor = conectar_banco_dados()
        
        if verificar_valor_existente("id_usuario", id_usuario):
            return

        query = "INSERT INTO usuarios (id_usuario, nome_usuario, nome, qntcartas, fav, cenouras, iscas) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (id_usuario,username, nome_usuario,0,0,10,10))
        conn.commit()

        print(f"Registro para o usuário com ID {id_usuario} e nome {nome_usuario} inserido com sucesso.")

    except mysql.connector.Error as err:
        print(f"Erro ao registrar usuário: {err}")

    finally:
        fechar_conexao(cursor, conn)

def verifica_inventario_troca(id_usuario, id_personagem):
    conn, cursor = conectar_banco_dados()
    query = f"SELECT quantidade FROM inventario WHERE id_usuario = {id_usuario} AND id_personagem = {id_personagem}"
    cursor.execute(query)
    quantidade_total = cursor.fetchone()
    if quantidade_total is None:
        return 0  # Retorna 0 se a quantidade total for nula
    else:
        return quantidade_total[0]
def registrar_valor(coluna, valor, id_usuario):
    try:
        conn, cursor = conectar_banco_dados()
        if not verificar_valor_existente("id_usuario", id_usuario):
            query = f"INSERT INTO usuarios (id_usuario, {coluna}, qntcartas, cenouras, iscas) VALUES (%s, %s, 0, 0, 0, 0)"
            conn.commit()
            print(f"Novo registro adicionado para o ID do usuário {id_usuario}")

        else:
            query = f"UPDATE usuarios SET {coluna} = %s WHERE id_usuario = %s"
            cursor.execute(query, (valor, id_usuario))
            conn.commit()
            print(f"Valor {valor} registrado na coluna {coluna} para o ID do usuário {id_usuario}")

    except mysql.connector.Error as err:
        print(f"Erro ao registrar {coluna}: {err}")

    finally:
        fechar_conexao(cursor, conn)
        
def qnt_carta(id_usuario):
    try:
        conn, cursor = conectar_banco_dados()
        query_atualizar_qnt_cartas = """
            UPDATE usuarios u
            SET u.qntcartas = (
                SELECT COALESCE(SUM(i.quantidade), 0)
                FROM inventario i
                WHERE i.id_usuario = %s
            )
            WHERE u.id_usuario = %s
        """
        cursor.execute(query_atualizar_qnt_cartas, (id_usuario, id_usuario))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao atualizar quantidade total de cartas do usuário: {err}")
    finally:
        fechar_conexao(cursor, conn)        
def adicionar_iscas(id_usuario, quantidade):

    try:
        conn, cursor = conectar_banco_dados()
        query_atualizar_iscas = """
            UPDATE usuarios
            SET iscas = iscas + %s
            WHERE id_usuario = %s
        """
        cursor.execute(query_atualizar_iscas, (quantidade, id_usuario))
        conn.commit()

        print(f"Iscas adicionadas com sucesso para o usuário com ID {id_usuario}")

    except mysql.connector.Error as e:
        print(f"Erro ao adicionar iscas para o usuário: {e}")

    finally:
        fechar_conexao(cursor, conn)
        
def verificar_giros(id_pessoa):
    try:
        conn, cursor = conectar_banco_dados()

        try:
            query = f"SELECT iscas FROM usuarios WHERE id_usuario = {id_pessoa}"
            cursor.execute(query)
            resultado = cursor.fetchone()

            if resultado:
                qtd_iscas = int(resultado[0])
                return qtd_iscas
            else:
                return 0

        except Exception as e:
            print(f"Erro ao executar a consulta de verificação de giros: {e}")

    finally:
        fechar_conexao(cursor, conn)

def verificar_id_na_tabela(id_pessoa, tabela, coluna_iduser):
    try:
        conn, cursor = conectar_banco_dados()
        cursor.execute(f"SELECT COUNT(*) FROM {tabela} WHERE {coluna_iduser} = %s", (id_pessoa,))
        resultado_contagem = cursor.fetchone()[0]

        if resultado_contagem > 0:
            raise ValueError(f"ID {id_pessoa} já está na tabela '{tabela}' na coluna '{coluna_iduser}'")

    except mysql.connector.Error as err:
        print(f"Erro ao verificar ID {id_pessoa} na tabela '{tabela}': {err}")

    finally:
        fechar_conexao(cursor, conn)
                
def answer_callback_query(bot, callback_query_id, text):
    bot.answer_callback_query(callback_query_id, text)
    
def set_reaction(chat_id, message_id, emoji):
    url = f"https://api.telegram.org/bot{bot.token}/setMessageReaction"
    data = {
        'chat_id': chat_id,
        'message_id': message_id,
        'reaction': json.dumps([{'type': 'emoji', 'emoji': emoji}])
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Reação definida com sucesso.")
    else:
        print(f"Erro ao definir a reação: {response.status_code} - {response.text}")                
        
def send_notification(chat_id, message_text):
    try:
        bot.send_message(chat_id, message_text)
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")

def aumentar_cenouras(user, valor):
    try:
        conn, cursor = conectar_banco_dados()
        cursor.execute("SELECT cenouras FROM usuarios WHERE user = %s", (user,))
        resultado = cursor.fetchone()

        if resultado:
            cenouras_atuais = int(resultado[0]) 
            nova_quantidade = cenouras_atuais + int(valor)
            cursor.execute("UPDATE usuarios SET cenouras = %s WHERE user = %s", (nova_quantidade, user))
            conn.commit()
            print("cenouras aumentadas.", cenouras_atuais, nova_quantidade)
    except Exception as e:
        traceback.print_exc()

    except Exception as e:
        print(f"Erro ao diminuir cenouras: {e}")

    finally:
        fechar_conexao(cursor, conn)
        
def diminuir_cenouras(id_usuario, valor):
    try:
        conn, cursor = conectar_banco_dados()
        cursor.execute("SELECT cenouras FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        resultado = cursor.fetchone()

        if resultado:
            cenouras_atuais = int(resultado[0]) 
            if cenouras_atuais >= int(valor):
                nova_quantidade = cenouras_atuais - int(valor)
                cursor.execute("UPDATE usuarios SET cenouras = %s WHERE id_usuario = %s", (nova_quantidade, id_usuario))
                conn.commit()
            else:
                print("Erro: Não há cenouras suficientes para diminuir.")
        else:
            print("Erro: Usuário não encontrado.")

    except Exception as e:
        print(f"Erro ao diminuir cenouras: {e}")

    finally:
        fechar_conexao(cursor, conn)

def diminuir_peixes(id_usuario, valor):
    try:
        conn, cursor = conectar_banco_dados()
        cursor.execute("SELECT cenouras FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        resultado = cursor.fetchone()

        if resultado:
            cenouras_atuais = int(resultado[0]) 
            if cenouras_atuais >= valor:
                nova_quantidade = cenouras_atuais - valor
                cursor.execute("UPDATE usuarios SET cenouras = %s WHERE id_usuario = %s", (nova_quantidade, id_usuario))
                conn.commit()
            else:
                print("Erro: Não há cenouras suficientes para diminuir.")
        else:
            print("Erro: Usuário não encontrado.")

    except Exception as e:
        print(f"Erro ao diminuir cenouras: {e}")

    finally:
        fechar_conexao(cursor, conn)
        
def diminuir_giros(id_usuario, quantidade):
    try:
        conn, cursor = conectar_banco_dados()
        cursor.execute("SELECT id_usuario, nome, iscas FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        resultado_usuario = cursor.fetchone()

        if resultado_usuario:
            id_usuario = resultado_usuario[0]
            nome_usuario = resultado_usuario[1]
            iscas_atuais = int(resultado_usuario[2]) 

            if iscas_atuais >= quantidade:
                nova_quantidade = iscas_atuais - quantidade
                cursor.execute("UPDATE usuarios SET iscas = %s WHERE id_usuario = %s", (nova_quantidade, id_usuario))

                conn.commit()
            else:
                print("Erro: Não há iscas suficientes para diminuir.")
        else:
            print("Erro: Usuário não encontrado.")
    except Exception as e:
        print(f"Erro ao diminuir iscas: {e}")
    finally:
        fechar_conexao(cursor, conn)

def verificar_comando_peixes(message):
    try:
        # Separar os parâmetros do comando
        parametros = message.text.split(' ', 2)[1:]  

        if not parametros:
            bot.reply_to(message, "Por favor, forneça a subcategoria.")
            return
        
        # Combinar os parâmetros restantes para formar a subcategoria
        subcategoria = " ".join(parametros)  
        
        # Se o primeiro parâmetro for 'img', enviar a imagem do peixe
        if len(parametros) > 1 and parametros[0].lower() == 'img':
            subcategoria = " ".join(parametros[1:])
            enviar_imagem_peixe(message, subcategoria)
        else:
            # Caso contrário, mostrar a lista de peixes da subcategoria
            mostrar_lista_peixes(message, subcategoria)
        
    except Exception as e:
        print(f"Erro ao processar comando /peixes: {e}")
        bot.reply_to(message, "Ocorreu um erro ao processar sua solicitação.")


def formatar_titulo(titulo):
    """
    Formata um título para que cada palavra comece com letra maiúscula,
    exceto preposições e conjunções como 'de', 'do', 'da', 'e'.
    """
    # Lista de palavras que devem permanecer em minúsculo
    palavras_minusculas = {"de", "do", "da", "dos", "das", "e", "em", "por", "para", "com", "a", "o", "as", "os", "um", "uma"}
    
    # Quebra o título em palavras
    palavras = titulo.split()
    
    # Formata cada palavra
    palavras_formatadas = [
        palavra.capitalize() if i == 0 or palavra.lower() not in palavras_minusculas else palavra.lower()
        for i, palavra in enumerate(palavras)
    ]
    
    # Junta as palavras formatadas novamente em uma string
    return " ".join(palavras_formatadas)
def handle_completos(message):
    try:
        parts = message.text.split(' ', 1)
        if len(parts) < 2:
            bot.reply_to(message, "Por favor, forneça a categoria após o comando, por exemplo: /completos música")
            return

        categoria = parts[1].strip()
        id_usuario = message.from_user.id
        nome_usuario = message.from_user.first_name

        conn, cursor = conectar_banco_dados()

        # Corrigir a mistura de collations com COLLATE utf8mb4_unicode_ci nas colunas envolvidas na comparação
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

        if not completos:
            bot.reply_to(message, f"Você ainda não completou nenhuma subcategoria em '{categoria}'.")
            return

        total_paginas = (len(completos) + 14) // 15  # Calcula total de páginas
        # Envia a primeira página e guarda o ID da mensagem
        message_inicial = mostrar_pagina_completos(message.chat.id, 1, total_paginas, completos, categoria, nome_usuario, id_usuario, primeira_pagina=True)


    except Exception as e:
        print(f"Erro ao processar comando /completos: {e}")
        bot.reply_to(message, "Ocorreu um erro ao processar sua solicitação.")
    finally:
        fechar_conexao(cursor, conn)

def mostrar_pagina_completos(chat_id, pagina_atual, total_paginas, completos, categoria, nome_usuario, id_usuario, message_id=None, primeira_pagina=False):
    """
    Mostra os resultados da subcategoria completada em formato paginado.
    """
    try:
        # Definir o número de itens por página
        itens_por_pagina = 15
        inicio = (pagina_atual - 1) * itens_por_pagina
        fim = inicio + itens_por_pagina

        # Filtrar os itens da página atual
        pagina_atual_itens = completos[inicio:fim]

        # Formatar o nome da categoria
        categoria_formatada = formatar_titulo(categoria)

        # Montar o texto da mensagem
        texto = f"🎉 <b>{nome_usuario}</b>, você completou as seguintes subcategorias em {categoria_formatada}:\n\n"
        for subcategoria, total_possui, total_necessario, imagem in pagina_atual_itens:
            subcategoria_formatada = formatar_titulo(subcategoria)
            texto += f"🏆 <b>{subcategoria_formatada}</b> ({total_possui}/{total_necessario})\n"

        texto += f"\nPágina {pagina_atual} de {total_paginas}"

        # Criar os botões de navegação (se necessário)
        keyboard = telebot.types.InlineKeyboardMarkup()

        #Envia o ID da mensagem para os botões de navegação
        if primeira_pagina:
            # Envia a primeira mensagem
            message = bot.send_message(chat_id, texto, reply_markup=keyboard, parse_mode="HTML")
            message_id = message.message_id #Captura o ID da mensagem
            if pagina_atual > 1:
                keyboard.add(telebot.types.InlineKeyboardButton(
                    text="⬅️ Anterior", callback_data=f"completos_{pagina_atual - 1}_{categoria}_{id_usuario}_{message_id}"
                ))

            if pagina_atual < total_paginas:
                keyboard.add(telebot.types.InlineKeyboardButton(
                    text="➡️ Próximo", callback_data=f"completos_{pagina_atual + 1}_{categoria}_{id_usuario}_{message_id}"
                ))
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
            return message #Retorna a mensagem para capturar o ID
        else:
            if pagina_atual > 1:
                keyboard.add(telebot.types.InlineKeyboardButton(
                    text="⬅️ Anterior", callback_data=f"completos_{pagina_atual - 1}_{categoria}_{id_usuario}_{message_id}"
                ))

            if pagina_atual < total_paginas:
                keyboard.add(telebot.types.InlineKeyboardButton(
                    text="➡️ Próximo", callback_data=f"completos_{pagina_atual + 1}_{categoria}_{id_usuario}_{message_id}"
                ))
            # Edita a mensagem existente
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=texto, reply_markup=keyboard, parse_mode="HTML")
            except telebot.apihelper.ApiTelegramException as e:
                if "message is not modified" in str(e):
                    print("Mensagem não foi modificada pois o conteúdo é o mesmo.")
                else:
                    print(f"Erro ao editar mensagem: {e}")
            return None


    except Exception as e:
        print(f"Erro ao mostrar página de completos: {e}")
        bot.send_message(chat_id, "Ocorreu um erro ao mostrar os resultados.")
        return None

def processar_historico_command(message):
    id_usuario = message.chat.id  
    tipo_historico = message.text.split()[-1].lower()  

    if tipo_historico == 'troca':
        historico = obter_historico_trocas(id_usuario)
        if historico:
            historico_mensagem = "🤝 | Seu histórico de trocas:\n\n"
            for troca in historico:
                id_usuario1, id_usuario2, carta1, carta2, aceita = troca
                carta1 = obter_nome(carta1)
                carta2 = obter_nome(carta2)
                nome1 = obter_nome_usuario_por_id(id_usuario1)
                nome2 = obter_nome_usuario_por_id(id_usuario2)
                status = "✅" if aceita else "⛔️"
                mensagem = f"ꕤ Troca entre {nome1} e {nome2}:\n{carta1} e {carta2} - {status}\n\n"
                historico_mensagem += mensagem

            bot.send_message(id_usuario, historico_mensagem)
        else:
            bot.send_message(id_usuario, "Nenhuma troca encontrada para este usuário.")

    elif tipo_historico == 'pesca':
        historico = obter_historico_pescas(id_usuario)
        if historico:
            historico_mensagem = "🎣 | Seu histórico de pescas:\n\n"
            for pesca in historico:
                id_carta, data_hora = pesca
                carta1 = obter_nome(id_carta)
                data_formatada = datetime.strftime(data_hora, "%d/%m/%Y - %H:%M")
                mensagem = f"✦ Carta: {id_carta} → {carta1}\nPescada em: {data_formatada}\n\n"
                historico_mensagem += mensagem

            bot.send_message(id_usuario, historico_mensagem)
        else:
            bot.send_message(id_usuario, "Nenhuma pesca encontrada para este usuário.")
    else:
        bot.send_message(id_usuario, "Tipo de histórico inválido. Use 'troca' ou 'pesca'.")
