import random
from pesquisas import *
from user import *
from bd import *
from loja import * 
from gnome import *
from operacoes import *
from inventario import *
from gif import *
from cachetools import cached, TTLCache
from evento import *
from gif import *
from verao import *
import traceback
import time

# Cache para controlar os refreshes (1 hora de duração)
refresh_cache = TTLCache(maxsize=1000, ttl=3600)

ultimo_clique = {}

grupodeerro = -4209628464
GRUPO_PESCAS_ID = -4209628464  

cache = TTLCache(maxsize=1000, ttl=600)  
cache_cartas = TTLCache(maxsize=1000, ttl=3600)
cache_submenus = TTLCache(maxsize=1000, ttl=3600)
cache_eventos = TTLCache(maxsize=1000, ttl=3600)

@cached(cache_cartas)
def obter_cartas_subcateg(subcategoria, conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_personagem, emoji, nome, imagem FROM personagens WHERE subcategoria = %s", (subcategoria,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erro ao obter cartas da subcategoria: {err}")
        return []
    finally:
        cursor.close()
        
@cached(cache_cartas)
def buscar_subcategorias(categoria):
    try:
        if categoria=="geral":
            conn, cursor = conectar_banco_dados()
            cursor.execute("SELECT DISTINCT subcategoria FROM personagens")
            subcategorias = cursor.fetchall()
            # Utilizando um conjunto para garantir unicidade
            subcategorias_unicas = {subcategoria[0] for subcategoria in subcategorias}
            return list(subcategorias_unicas)
        else:
            conn, cursor = conectar_banco_dados()
            cursor.execute("SELECT DISTINCT subcategoria FROM personagens WHERE categoria = %s", (categoria,))
            subcategorias = cursor.fetchall()
            # Utilizando um conjunto para garantir unicidade
            subcategorias_unicas = {subcategoria[0] for subcategoria in subcategorias}
            return list(subcategorias_unicas)
    except mysql.connector.Error as err:
        print(f"Erro ao buscar subcategorias: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close() 
            
def categoria_handler(message, categoria, id_usuario):
    try:
        conn, cursor = conectar_banco_dados()
        chat_id = message.chat.id
        
        # Verificar picolé de uva
        cursor.execute("SELECT sabor FROM sorvetes WHERE user_id = %s AND sabor = 'uva'", (id_usuario,))
        tem_uva = cursor.fetchone()
        
        # Ajustar chances conforme o picolé
        evento_chance = 0.75 if tem_uva else 0.5  # 75% de chance se tiver uva, 50% padrão
        
        # Inicializar variáveis de evento
        evento_ativo = True
        chance_evento = random.random()

        if categoria.lower() == 'geral':
            # Verifica a chance de ativação do evento
            if evento_ativo and chance_evento <= evento_chance:
                subcategories_valentine = get_random_subcategories_all_valentine(conn)
                
                # Sorteia entre a opção de múltiplas subcategorias ou apenas uma
                if random.random() <= 0.5:
                    # Seleciona duas subcategorias e configura o markup com botões para cada uma
                    subcategories_aleatorias = random.sample(subcategories_valentine, k=2)
                    image_link = "https://pub-6f23ef52e8614212a14d24b0cf55ae4a.r2.dev/BQACAgEAAxkBAAI7n2ecQXBdesOt-fWK6swkFPn_ik2YAAIwBgACWOrpRNt9zhyQtwgINgQ.jpg"
                    caption = "Um sopro do tempo revela memórias esquecidas, trazendo à tona momentos especiais do passado. Escolha uma categoria e reviva essa jornada de retrospectiva mágica:\n\n"
                    
                    # Configurar botões inline para seleção de subcategoria
                    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
                    emoji_numbers = ['⏰', '📅']
                    row_buttons = []
                    for i, subcategory in enumerate(subcategories_aleatorias):
                        caption += f"{emoji_numbers[i]} - {subcategory} \n"
                        button_text = emoji_numbers[i]
                        row_buttons.append(telebot.types.InlineKeyboardButton(button_text, callback_data=f"subcategory_{subcategory}_valentine"))
                    markup.row(*row_buttons)

                    # Enviar a mensagem com imagem e botões para escolher subcategoria
                    bot.edit_message_media(
                        chat_id=message.chat.id,
                        message_id=message.message_id,
                        reply_markup=markup,
                        media=telebot.types.InputMediaPhoto(media=image_link, caption=caption)
                    )
                else:
                    # Se apenas uma subcategoria, exibe um botão único
                    subcategoria_aleatoria = random.choice(subcategories_valentine)
                    emoji_numbers = ['⏰', '📅']
                    button_text = emoji_numbers[subcategories_valentine.index(subcategoria_aleatoria)]

                    # Configura botão único para subcategoria
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    button = telebot.types.InlineKeyboardButton(button_text, callback_data=f"subcategory_{subcategoria_aleatoria}_valentine")
                    keyboard.add(button)

                    # Configuração de imagem e texto para a seleção de uma subcategoria
                    caption = "Um vento suave carrega memórias do passado, trazendo uma sensação mágica de redescoberta e escolhas inesquecíveis:"
                    bot.edit_message_media(
                        chat_id=message.chat.id,
                        message_id=message.message_id,
                        reply_markup=keyboard,
                        media=telebot.types.InputMediaPhoto(media="https://pub-6f23ef52e8614212a14d24b0cf55ae4a.r2.dev/BQACAgEAAxkBAAI7omecQdq_6Cuk5ddXtMgY26C1kpp1AAIxBgACWOrpRH6R6RmYDQQhNgQ.jpg", caption=caption)
                    )
            else:
                # Caso não ative o evento, segue com a lógica padrão de 'geral' com subcategorias
                tratar_subcategorias_padroes(chat_id, cursor, categoria, message)

        else:
            # Lógica padrão para categorias diferentes de "geral"
            tratar_subcategorias_padroes(chat_id, cursor, categoria, message)

    except mysql.connector.Error as err:
        bot.send_message(chat_id, f"Erro ao buscar subcategorias: {err}")
    finally:
        fechar_conexao(cursor, conn)

def tratar_subcategorias_padroes(chat_id, cursor, categoria, message):
    user_id = message.chat.id
    subcategorias = buscar_subcategorias(categoria)
    subcategorias = [sub for sub in subcategorias if sub]

    # Verificar picolé de amendoim
    cursor.execute("SELECT sabor FROM sorvetes WHERE user_id = %s AND sabor = 'amendoim'", (user_id,))
    tem_amendoim = cursor.fetchone()
    efeito_ativado = False
    sub_favs = []
    status_picole = ""

    if tem_amendoim:
        # Obter favoritos em lowercase para comparação
        cursor.execute("SELECT LOWER(subcategoria) FROM user_favorites WHERE user_id = %s", (user_id,))
        favoritos = [row[0] for row in cursor.fetchall()]
        
        if favoritos:
            efeito_ativado = True
            # Aumentar peso das favoritas
            subcategorias_weighted = []
            for sub in subcategorias:
                if sub.lower() in favoritos:
                    subcategorias_weighted.extend([sub] * 13)  # 3x mais chances
                    sub_favs.append(sub)
                else:
                    subcategorias_weighted.append(sub)
            subcategorias = subcategorias_weighted
            
            status_picole = "🥜 EFEITO ATIVADO - Favoritas têm 10x mais chance!\n\n"
        else:
            status_picole = "🥜 AVISO: Picolé ativo mas nenhum favorito!\nUse /favserie NOME\n\n"

    # Seleção aleatória
    try:
        subcategorias_aleatorias = random.sample(subcategorias, min(6, len(subcategorias)))
    except ValueError:
        subcategorias_aleatorias = subcategorias

    # Montar mensagem
    resposta_texto = "Sua isca atraiu 6 espécies, qual peixe você vai levar?\n"
    
    # Adicionar status só se tiver picolé
    resposta_texto += status_picole

    # Listar subcategorias com indicação
    for i, sub in enumerate(subcategorias_aleatorias, start=1):
        if sub in sub_favs:
            resposta_texto += f"{i}\uFE0F\u20E3 - {sub} 🥜\n"
        else:
            resposta_texto += f"{i}\uFE0F\u20E3 - {sub}\n"

    # Debug no console se tiver picolé
    if tem_amendoim:
        print(f"\n[DEBUG] Usuário {user_id}")
        print(f"Favoritos detectados: {sub_favs}")
        print(f"Efeito aplicado: {efeito_ativado}")

    # Configurar botões
    markup = telebot.types.InlineKeyboardMarkup(row_width=6)
    row_buttons = []
    for i, subcategoria in enumerate(subcategorias_aleatorias, start=1):
        button_text = f"{i}\uFE0F\u20E3"
        callback_data = f"choose_subcategoria_{subcategoria}"
        row_buttons.append(telebot.types.InlineKeyboardButton(button_text, callback_data=callback_data))

    markup.row(*row_buttons)
    imagem_url = "https://pub-6f23ef52e8614212a14d24b0cf55ae4a.r2.dev/BQACAgEAAxkBAAI7jGecPx4vlb0XgVOnn7aCzAEbJZkoAAIrBgACWOrpREtWJu24hUlONgQ.jpg"
    
    # Editar mensagem
    bot.edit_message_media(
        chat_id=chat_id,
        message_id=message.message_id,
        reply_markup=markup,
        media=telebot.types.InputMediaPhoto(media=imagem_url, caption=resposta_texto)
    )
def criar_markup(subcategorias, tipo):
    markup = telebot.types.InlineKeyboardMarkup()
    row_buttons = []
    emoji_numbers = ['⛄', '🦌'] if tipo == "valentine" else [f"{i}\uFE0F\u20E3" for i in range(1, 7)]
    for i, subcategoria in enumerate(subcategorias):
        button_text = emoji_numbers[i] if tipo == "valentine" else f"{i+1}\uFE0F\u20E3"
        callback_data = f"subcategory_{subcategoria}_{tipo}"
        row_buttons.append(telebot.types.InlineKeyboardButton(button_text, callback_data=callback_data))
    markup.add(*row_buttons)
    return markup
def subcategoria_handler(message, subcategoria, cursor, conn, categoria, chat_id, message_id):
    id_usuario = message.chat.id
    try:
        conn, cursor = conectar_banco_dados()

        if subcategoria.lower() == 'geral':
            if random.randint(1, 100) <= 10:
                evento_aleatorio = obter_carta_evento_fixo(conn, subcategoria)
                if evento_aleatorio:
                    send_card_message(message, evento_aleatorio, cursor=cursor, conn=conn)
                    return

        if verificar_se_subcategoria_tem_submenu(cursor, subcategoria):
            submenus = obter_submenus_para_subcategoria(cursor, subcategoria)
            if isinstance(submenus, list) and submenus:
                submenu_opcoes = random.sample(submenus, min(3, len(submenus)))
                enviar_opcoes_submenu(message, submenu_opcoes, subcategoria, chat_id, message_id)
                return

        cartas_disponiveis = obter_cartas_subcateg(subcategoria, conn)
        if cartas_disponiveis:
            # Verificar picolés especiais
            cursor.execute("SELECT sabor FROM sorvetes WHERE user_id = %s", (id_usuario,))
            picole = cursor.fetchone()
            tem_melancia = picole and picole[0] == 'melancia'
            tem_coco = picole and picole[0] == 'coco'

            # Aplicar peso para Melancia
            if tem_melancia:
                cursor.execute("SELECT character_id FROM user_favorite_characters WHERE user_id = %s", (id_usuario,))
                favoritos_melancia = [row[0] for row in cursor.fetchall()]
                
                # Criar lista ponderada
                cartas_ponderadas = []
                for carta in cartas_disponiveis:
                    if carta[0] in favoritos_melancia:
                        cartas_ponderadas.extend([carta] * 3)  # 3x mais chances
                        print(f"[MELANCIA] Personagem {carta[0]} recebeu peso extra")
                    else:
                        cartas_ponderadas.append(carta)
                cartas_disponiveis = cartas_ponderadas

            # Seleção da carta principal
            carta_principal = random.choice(cartas_disponiveis)
            id_principal, emoji_principal, nome_principal, imagem_principal = carta_principal
            send_card_message(message, emoji_principal, id_principal, nome_principal, subcategoria, imagem_principal)

            # Verificar bônus Coco
            if tem_coco and random.random() < 0.3:
                carta_extra = random.choice(cartas_disponiveis)
                id_extra, emoji_extra, nome_extra, imagem_extra = carta_extra
                add_to_inventory(id_usuario, id_extra)
                
                bot.send_photo(
                    chat_id,
                    imagem_extra,
                    caption=f"🥥 Bônus Picolé de Coco!\n<code>{id_extra}</code> - {nome_extra}\n▸ {subcategoria.replace('_', ' ').title()}",
                    parse_mode="HTML",
                    reply_to_message_id=message_id
                )

        else:
            print(f"Nenhuma carta disponível para: {subcategoria}")

    except Exception as e:
        traceback.print_exc()
    finally:
        fechar_conexao(cursor, conn)

def verificar_se_subcategoria_tem_submenu(cursor, subcategoria):
    """
    Verifica se a subcategoria possui submenus associados.
    """
    try:
        cursor.execute("SELECT COUNT(*) FROM subcategoria_submenu WHERE subcategoria = %s", (subcategoria,))
        return cursor.fetchone()[0] > 0
    except mysql.connector.Error as err:
        print(f"Erro ao verificar submenu da subcategoria: {err}")
        return False


def obter_submenus_para_subcategoria(cursor, subcategoria):
    """
    Obtém submenus associados a uma subcategoria.
    """
    try:
        cursor.execute("SELECT submenu FROM subcategoria_submenu WHERE subcategoria = %s", (subcategoria,))
        resultados = cursor.fetchall()
        if resultados:
            return [submenu[0] for submenu in resultados]  # Extrai os nomes dos submenus
        else:
            return []  # Retorna uma lista vazia se nenhum submenu for encontrado
    except mysql.connector.Error as err:
        print(f"Erro ao obter submenus da subcategoria: {err}")
        return []


def enviar_opcoes_submenu(message, submenu_opcoes, subcategoria, chat_id, message_id):
    try:
        # Definir a quantidade de botões com base na quantidade de opções
        row_width = 3 if len(submenu_opcoes) >= 3 else 2
        opcoes = [telebot.types.InlineKeyboardButton(text=opcao, callback_data=f"submenu_{subcategoria}_{opcao}") for opcao in submenu_opcoes]
        markup = telebot.types.InlineKeyboardMarkup(row_width=row_width)
        markup.add(*opcoes)
        
        # Editar a mensagem original para apresentar as opções de submenu
        bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption=f"A espécie <b>{subcategoria}</b> possuí variedades, qual dessas você deseja levar?", 
            parse_mode="HTML",
            reply_markup=markup
        )
    except Exception as e:
        print(f"Erro ao enviar opções de submenu: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('submenu_'))
def callback_submenu_handler(call):
    try:
        print(f"[DEBUG] Iniciando processamento de submenu para {call.from_user.id}")
        data = call.data.split('_')
        subcategoria = data[1]
        submenu = data[2]

        conn = conectar_banco_dados()
        cursor = conn.cursor()
        
        # Obter carta principal
        print(f"[DEBUG] Buscando carta principal para {subcategoria}/{submenu}")
        carta = obter_carta_por_submenu(cursor, subcategoria, submenu)
        
        if carta:
            id_personagem, emoji, nome, imagem = carta
            print(f"[DEBUG] Enviando carta principal: {id_personagem} {nome}")
            send_card_message(call.message, emoji, id_personagem, nome, f"{subcategoria}_{submenu}", imagem)
            
            # Verificar picolé de coco
            print(f"[DEBUG] Verificando picolé de coco para {call.from_user.id}")
            cursor.execute("SELECT sabor FROM sorvetes WHERE user_id = %s AND sabor = 'coco'", (call.from_user.id,))
            tem_coco = cursor.fetchone()
            print(f"[DEBUG] Resultado da verificação de coco: {tem_coco}")
            
            if tem_coco and random.random() < 1:  # Forçado para testes
                print("[DEBUG] Efeito coco ativado! Buscando carta extra")
                carta_extra = obter_carta_por_submenu(cursor, subcategoria, submenu)
                
                if carta_extra:
                    id_extra, emoji_extra, nome_extra, imagem_extra = carta_extra
                    print(f"[DEBUG] Enviando carta extra: {id_extra} {nome_extra}")
                    send_card_message(call.message, emoji_extra, id_extra, nome_extra, f"{subcategoria}_{submenu}", imagem_extra)
                    
                    # Enviar mensagem de bônus como nova mensagem
                    print("[DEBUG] Enviando mensagem de bônus")
                    bot.send_message(
                        call.message.chat.id,
                        f"🥥✨ <b>Bônus Picolé de Coco!</b>\n"
                        f"Você pescou junto:\n"
                        f"<code>{id_extra}</code> - {nome_extra}\n"
                        f"▸ {subcategoria.replace('_', ' ').title()} → {submenu.title()}",
                        parse_mode="HTML"
                    )
                else:
                    print("[ERRO] Nenhuma carta extra encontrada!")
        else:
            print(f"[ERRO] Nenhuma carta encontrada para {subcategoria}/{submenu}")

    except Exception as e:
        print(f"[ERRO CRÍTICO] No handler de submenu: {str(e)}")
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("[DEBUG] Conexões fechadas")
@cached(cache_cartas)
def obter_carta_por_submenu(cursor, subcategoria, submenu):
    try:
        cursor.execute("SELECT id_personagem, emoji, nome, imagem FROM personagens WHERE subcategoria = %s AND submenu = %s ORDER BY RAND() LIMIT 1", (subcategoria, submenu))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Erro ao obter carta por submenu: {err}")
        return None
        
grupodefofoca = [7174619329, 1176725749, 6657417699, 624599461, 1805086442, 5532809878]
def get_current_picole(user_id):
    """Retorna o sabor ativo do usuário na tabela sorvetes"""
    try:
        conn, cursor = conectar_banco_dados()
        cursor.execute(
            "SELECT sabor FROM sorvetes WHERE user_id = %s ORDER BY data_obtencao DESC LIMIT 1",
            (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"[ERRO] Falha ao obter picolé: {str(e)}")
        return None
    finally:
        fechar_conexao(cursor, conn)

def apply_picole_effect(user_id, current_picole, subcategoria=None):
    """Retorna (quantidade, mensagem) mesmo sem picolé"""
    try:
        print(f"[DEBUG] apply_picole_effect - Picolé atual: {current_picole}")  # Log do picolé recebido

        if not current_picole:  # Se não tem picolé
            return (1, "") 
        # --- Efeito Morango (Verificação Prioritária) ---
        if current_picole.lower() == "morango":  # Case-insensitive
            rand_val = random.random()
            print(f"[DEBUG] Morango: rand_val = {rand_val}")  # Debug do valor aleatório
            if rand_val < 0.3:
                print(f"[SUCESSO] Morango ativado para {user_id}")
                bonus_qty = random.randint(2, 5)
                return (bonus_qty, "\n\n🍓 Bônus Morango: Unidades extras!")
            else:
                print(f"[DEBUG] Morango não ativado (random >= 0.3)")

        # Efeito Milho Verde (Movido para depois do morango)
        elif current_picole == "milho":
            print(f"[DEBUG] Ativando bônus do milho para {user_id}")
            try:
                conn, cursor = conectar_banco_dados()
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
                print(f"[DEBUG] Milho ativado/atualizado para {user_id}")
            except Exception as e:
                print(f"[ERRO] Falha ao ativar milho: {str(e)}")
            finally:
                fechar_conexao(cursor, conn)
            
            return (1, "\n\n🌽 Bônus Milho Verde: Ganhando 50 cenouras/hora!")
        # Efeito Coco
        elif current_picole == "coco" and random.random() < 0.3:
            sub = subcategoria.replace('_', ' ') if subcategoria else "esta categoria"
            return (2, f"\n\n🥥 Bônus Coco: Item extra de {sub}!")
            
        # Efeito Amendoim
        elif current_picole == "amendoim":
            return (1, "\n\n🥜 Bônus Amendoim: Favoritos têm prioridade!"
                      "\nUse /favserie Nome para adicionar"
                      "\n/delfavserie Nome para remover")
            
        # Efeito Melancia
        elif current_picole == "melancia":
            return (1, "\n\n🍉 Bônus Melancia: Personagens favoritos têm prioridade!"
                      "\n▸ /favperso ID - Adicionar"
                      "\n▸ /delfavperso ID - Remover")

        # Padrão para outros picolés
        else:
            return (1, "") 

    except Exception as e:
        print(f"Erro nos efeitos: {str(e)}")
        return (1, "")
        
def send_card_message(message, *args, cursor=None, conn=None):
    try:
        id_usuario = message.chat.id
        id_user = message.from_user.id
        # Verificar picolé fora da lógica principal
        current_picole = get_current_picole(id_user)
        quantidade, bonus_msg = apply_picole_effect(id_user, current_picole)

        # Adicionar cartas (mantendo a função original)
        for _ in range(quantidade):
            if len(args) == 1 and isinstance(args[0], dict):
                add_to_inventory(id_usuario, args[0]['id_personagem'])
            elif len(args) == 5:
                add_to_inventory(id_usuario, args[1])  # args[1] = id_personagem
                
        # Ingredientes e chances
        ingredientes = ["Canela", "Pó de Estrela", "Glitter", "Cola"]
        emojis_ingredientes = {"Canela": "🍯", "Pó de Estrela": "🌟", "Glitter": "✨", "Cola": "✂️"}
        ingredientes_recebidos = {}

        # Aumentar chance de ingredientes para chocolate
        tem_chocolate = current_picole == 'chocolate'
        chance_ingrediente = 0.8 if tem_chocolate else 0.1  # 20% com chocolate, 10% padrão

        for ingrediente in ingredientes:
            if random.random() < chance_ingrediente:
                ingredientes_recebidos[ingrediente] = ingredientes_recebidos.get(ingrediente, 0) + 1
        # Adicionar os ingredientes ao banco de dados de uma só vez
        adicionar_ingredientes_em_massa(id_usuario, ingredientes_recebidos)

        # Adicionar mensagem do chocolate
        if tem_chocolate:
            bonus_msg += "\n\n🍫 Bônus Chocolate: Chance de ingredientes aumentada!"
        # Criar teclado de botões
        keyboard = telebot.types.InlineKeyboardMarkup()
        botao_pescar = telebot.types.InlineKeyboardButton(text="🎣 Pescar novamente", callback_data="comando_pescar")
        keyboard.add(botao_pescar)
        # Verifica se é um evento fixo (dicionário passado)
        if len(args) == 1 and isinstance(args[0], dict):
            evento_aleatorio = args[0]
            subcategoria_display = evento_aleatorio['subcategoria'].split('_')[-1]
            id_personagem = evento_aleatorio['id_personagem']
            nome = evento_aleatorio['nome']
            subcategoria = evento_aleatorio['subcategoria']

            # Adicionar carta ao inventário
            add_to_inventory(id_usuario, id_personagem)
            quantidade = verifica_inventario_troca(id_usuario, id_personagem)
            quantidade_display = "☀" if quantidade == 1 else f"☀ {quantidade}⤫"
            imagem = evento_aleatorio.get('imagem', "https://telegra.ph/file/8a50bf408515b52a36734.jpg")
            texto = (
                f"🎣 Parabéns! Sua isca era boa e você recebeu:\n\n"
                f"🍒 <code>{id_personagem}</code> - {nome}\n"
                f"de {subcategoria_display}\n\n"
                f"{quantidade_display}"
                f"{bonus_msg}" 
            )

            # Adicionar mensagem de ingredientes recebidos
            if ingredientes_recebidos:
                texto += "\n\n🎁 Ingredientes bônus recebidos:\n"
                texto += "\n".join([f"{emojis_ingredientes[ing]} {ing} x{qt}" for ing, qt in ingredientes_recebidos.items()])

            # Enviar mensagem com o resultado e os botões
            enviar_mensagem_com_imagem(message, imagem, texto, reply_markup=keyboard)
            register_card_history(message, id_usuario, id_personagem)

        # Verifica se é uma carta aleatória (5 argumentos)
        elif len(args) == 5:
            emoji_categoria, id_personagem, nome, subcategoria, imagem = args
            subcategoria_display = subcategoria.split('_')[-1]

            # Adicionar carta ao inventário
            add_to_inventory(id_usuario, id_personagem)
            quantidade = verifica_inventario_troca(id_usuario, id_personagem)

            imagem_url = imagem if imagem else "https://telegra.ph/file/8a50bf408515b52a36734.jpg"
            texto = (
                f"🎣 Parabéns! Sua isca era boa e você recebeu:\n\n"
                f"{emoji_categoria}<code> {id_personagem}</code> - {nome}\n"
                f"de {subcategoria_display}\n\n"
                f"☀ | {quantidade}⤫"
                f"{bonus_msg}" 
            )

            # Adicionar mensagem de ingredientes recebidos
            if ingredientes_recebidos:
                texto += "\n\n🎁 Ingredientes bônus recebidos:\n"
                texto += "\n".join([f"{emojis_ingredientes[ing]} {ing} x{qt}" for ing, qt in ingredientes_recebidos.items()])

            # Se o usuário estiver no grupodefofoca, adiciona o botão de oferecer carta
            if id_usuario in grupodefofoca:
                botao_oferecer = telebot.types.InlineKeyboardButton(
                    text="🔔",
                    callback_data=f"oferecer_{id_personagem}"
                )
                botao_cenourar = telebot.types.InlineKeyboardButton(
                    text="🥕",
                    callback_data=f"cenourarbotao_{id_personagem}"
                )
                keyboard.row(botao_oferecer, botao_cenourar)
                
            # Enviar mensagem com o resultado e os botões
            enviar_mensagem_com_imagem(message, imagem_url, texto, reply_markup=keyboard)
            register_card_history(message.from_user, id_usuario, id_personagem)

        else:
            print("[DEBUG] Número incorreto de argumentos.")

    except Exception as e:
        erro = traceback.format_exc()
        mensagem = f"Erro ao enviar carta: {e}\n{erro}"
        bot.send_message(grupodeerro, mensagem, parse_mode="HTML")


def adicionar_ingredientes_em_massa(id_usuario, ingredientes_recebidos):
    """
    Adiciona múltiplos ingredientes ao mesmo tempo no banco de dados.
    """
    conn = None
    cursor = None
    try:
        if not ingredientes_recebidos:
            return  # Nada a adicionar

        conn, cursor = conectar_banco_dados()

        # Verificar se o usuário já está na tabela
        cursor.execute("SELECT 1 FROM materiais_usuario WHERE id_usuario = %s", (id_usuario,))
        existe = cursor.fetchone()

        if not existe:
            # Se o usuário não existir, criar uma linha inicial
            cursor.execute("""
                INSERT INTO materiais_usuario (id_usuario, canela, estrela, glitter, cola)
                VALUES (%s, 0, 0, 0, 0)
            """, (id_usuario,))
            conn.commit()

        # Atualizar os ingredientes recebidos
        updates = []
        for ingrediente, quantidade in ingredientes_recebidos.items():
            coluna = {
                "Canela": "canela",
                "Pó de Estrela": "estrela",
                "Glitter": "glitter",
                "Cola": "cola"
            }.get(ingrediente)
            if coluna:
                updates.append(f"{coluna} = {coluna} + {quantidade}")

        if updates:
            query = f"UPDATE materiais_usuario SET {', '.join(updates)} WHERE id_usuario = %s"
            cursor.execute(query, (id_usuario,))
            conn.commit()

        print(f"[DEBUG] Ingredientes adicionados para o usuário {id_usuario}: {ingredientes_recebidos}")
    except Exception as e:
        erro = traceback.format_exc()
        print(f"[DEBUG] Erro ao adicionar ingredientes em massa: {e}\n{erro}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def enviar_mensagem_com_imagem(message, imagem_url, text, reply_markup=None):
    """
    Função para enviar mensagem com imagem ou vídeo, tratando o tipo de mídia
    e adicionando suporte para teclados inline.
    """
    try:
        # Caso seja uma imagem
        if imagem_url.lower().endswith(('.jpg', '.jpeg', '.png')):
            bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.message_id,
                media=telebot.types.InputMediaPhoto(media=imagem_url, caption=text, parse_mode="HTML"),
                reply_markup=reply_markup  # Adiciona o teclado inline
            )
        # Caso seja um vídeo
        elif imagem_url.lower().endswith(('.mp4', '.gif')):
            bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.message_id,
                media=telebot.types.InputMediaVideo(media=imagem_url, caption=text, parse_mode="HTML"),
                reply_markup=reply_markup  # Adiciona o teclado inline
            )
    except Exception as ex:
        print(f"Erro ao editar mensagem: {ex}")
        try:
            # Caso não consiga editar, envia uma nova mensagem com imagem
            if imagem_url.lower().endswith(('.jpg', '.jpeg', '.png')):
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=imagem_url,
                    caption=text,
                    parse_mode="HTML",
                    reply_markup=reply_markup  # Adiciona o teclado inline
                )
            # Caso não consiga editar, envia uma nova mensagem com vídeo
            elif imagem_url.lower().endswith(('.mp4', '.gif')):
                bot.send_video(
                    chat_id=message.chat.id,
                    video=imagem_url,
                    caption=text,
                    parse_mode="HTML",
                    reply_markup=reply_markup  # Adiciona o teclado inline
                )
        except Exception as send_ex:
            print(f"Erro ao enviar mensagem com mídia: {send_ex}")
def verificar_se_subcategoria_tem_submenu(cursor, subcategoria):
    try:
        cursor.execute("SELECT COUNT(*) FROM subcategoria_submenu WHERE subcategoria = %s", (subcategoria,))
        return cursor.fetchone()[0] > 0
    except mysql.connector.Error as err:
        print(f"Erro ao verificar submenu da subcategoria: {err}")
        return False

def obter_submenus_para_subcategoria(cursor, subcategoria):
    try:
        cursor.execute("SELECT submenu FROM subcategoria_submenu WHERE subcategoria = %s", (subcategoria,))
        resultados = cursor.fetchall()
        return [submenu[0] for submenu in resultados]
    except mysql.connector.Error as err:
        print(f"Erro ao obter submenus da subcategoria: {err}")
        return []

def add_to_inventory(id_usuario, id_personagem, max_retries=5):
    attempt = 0
    id_usuario = int(id_usuario)
    id_personagem = int(id_personagem)
    
    while attempt < max_retries:
        try:
            conn, cursor = conectar_banco_dados()

            # Iniciar uma transação
            conn.start_transaction()

            # Ordenar as operações em ordem específica para evitar deadlocks
            if id_usuario < id_personagem:
                cursor.execute("SELECT quantidade FROM inventario WHERE id_usuario = %s AND id_personagem = %s FOR UPDATE",
                               (id_usuario, id_personagem))
            else:
                cursor.execute("SELECT quantidade FROM inventario WHERE id_personagem = %s AND id_usuario = %s FOR UPDATE",
                               (id_personagem, id_usuario))

            existing_carta = cursor.fetchone()

            if existing_carta:
                nova_quantidade = existing_carta[0] + 1
                cursor.execute("UPDATE inventario SET quantidade = %s WHERE id_usuario = %s AND id_personagem = %s",
                               (nova_quantidade, id_usuario, id_personagem))
            else:
                cursor.execute("INSERT INTO inventario (id_personagem, id_usuario, quantidade) VALUES (%s, %s, 1)",
                               (id_personagem, id_usuario))

            cursor.execute("UPDATE personagens SET total = IFNULL(total, 0) + 1 WHERE id_personagem = %s", (id_personagem,))

            # Confirmar a transação
            conn.commit()
            break  # Saia do loop se a transação for bem-sucedida

        except mysql.connector.errors.DatabaseError as db_err:
            if db_err.errno == 1205:  # Código de erro para lock wait timeout exceeded
                attempt += 1
                time.sleep(1)  # Esperar um pouco antes de tentar novamente
                if attempt >= max_retries:
                    mensagem = "Erro: Excedido o número máximo de tentativas para resolver o deadlock."
                    bot.send_message(grupodeerro, mensagem, parse_mode="HTML")
            else:
                mensagem = f"Erro ao adicionar carta ao inventário: {db_err}"
                bot.send_message(grupodeerro, mensagem, parse_mode="HTML")
                break
        except Exception as e:
            traceback.print_exc()
            erro = traceback.format_exc()
            mensagem = f"Adição de personagem com erro: {id_personagem} - usuário {id_usuario}. erro: {e}\n{erro}"
            bot.send_message(grupodeerro, mensagem, parse_mode="HTML")
            break
        finally:
            fechar_conexao(cursor, conn)
@cached(cache_submenus)            
def obter_cartas_por_subcategoria_e_submenu(subcategoria, submenu, cursor):
    try:
        cursor.execute("SELECT id_personagem, emoji, nome, imagem FROM personagens WHERE subcategoria = %s AND submenu = %s", (subcategoria, submenu))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erro ao obter cartas por subcategoria e submenu: {err}")
        return []

@cached(cache_submenus)
def verificar_subcategoria_evento(subcategoria, cursor):
    try:
        cursor.execute(
            "SELECT id_personagem, nome, subcategoria, imagem FROM evento WHERE subcategoria = %s AND evento = 'fixo' ORDER BY RAND() LIMIT 1",
            (subcategoria,))
        evento_aleatorio = cursor.fetchone()
        if evento_aleatorio:
            chance = random.randint(1, 100)

            if chance <= 20:
                id_personagem, nome, subcategoria, imagem = evento_aleatorio
                evento_formatado = {
                    'id_personagem': id_personagem,
                    'nome': nome,
                    'subcategoria': subcategoria,
                    'imagem': imagem
                }
                return evento_formatado
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Erro ao verificar subcategoria na tabela de eventos: {e}")
        return None

def obter_carta_evento_fixo(subcategoria=None):
    try:
        conn, cursor = conectar_banco_dados()
        if subcategoria:
            cursor.execute("SELECT emoji, id_personagem, nome, subcategoria, imagem FROM evento WHERE subcategoria = %s AND evento = 'fixo' ORDER BY RAND() LIMIT 1", (subcategoria,))
        else:
            cursor.execute("SELECT emoji, id_personagem, nome, subcategoria, imagem FROM evento WHERE evento = 'fixo' ORDER BY RAND() LIMIT 1")
        evento_aleatorio = cursor.fetchone()
        return evento_aleatorio
    except mysql.connector.Error as err:
        print(f"Erro ao obter carta de evento fixo: {err}")
        return None
    finally:
        fechar_conexao(cursor, conn)

def register_card_history(message,id_usuario, id_carta):
    try:
        conn, cursor = conectar_banco_dados()
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO historico_cartas_giradas (id_usuario, id_carta, data_hora) VALUES (%s, %s, %s)",
                       (id_usuario, id_carta, data_hora))
        conn.commit()
        user_info = bot.get_chat(id_usuario)
        # Obter detalhes da carta
        cursor.execute("SELECT nome, subcategoria FROM evento WHERE id_personagem = %s", (id_carta,))
        detalhes_carta = cursor.fetchone()
        if not detalhes_carta:
            return
        
        if detalhes_carta:
            nome_carta, subcategoria_carta = detalhes_carta  
            
            mensagem = f"🎣 Pesca realizada por: <code>{id_usuario}</code>-@{user_info.username}\n"
            mensagem += f"📅 Data e Hora: {data_hora}\n"
            mensagem += f"🃏 Carta: {id_carta} {nome_carta}\n"
            mensagem += f"🗂 Subcategoria: {subcategoria_carta}\n\n\n\n"
            mensagem += f"<code>/enviar_mensagem {id_usuario}</code>\n"
            # Enviar mensagem para o grupo
            bot.send_message(GRUPO_PESCAS_ID, mensagem,parse_mode="HTML")
        else:
            print(f"Detalhes da carta com id {id_carta} não encontrados.")
            
    except mysql.connector.Error as err:
        print(f"Erro ao registrar o histórico da carta: {err}")
    finally:
        fechar_conexao(cursor, conn)

ultima_interacao = {}

def pescar(message):
    try:
        nome = message.from_user.first_name
        user_id = message.from_user.id
        
        if message.chat.type in ['group', 'supergroup']:
            username = message.from_user.username or "Sem username"
            mensagem_erro = f"⚠️ Usuário @{username} - {user_id} tentou pescar em grupo"
            bot.send_message(grupodeerro, mensagem_erro)
            bot.reply_to(message, "🚫 Comandos de pesca só funcionam em conversas privadas!")
            return

        qtd_iscas = verificar_giros(user_id)
        if qtd_iscas == 0:
            bot.send_message(message.chat.id, "Você está sem iscas.", reply_to_message_id=message.message_id)
            return

        if not verificar_tempo_passado(message.chat.id):
            return
        else:
            ultima_interacao[message.chat.id] = datetime.now()

        if verificar_id_na_tabelabeta(user_id):
            diminuir_giros(user_id, 1)

            # --- NOVO: Verificação do picolé de milho ---
            try:
                conn, cursor = conectar_banco_dados()
                # Verificar se tem o picolé e calcular bônus
                # Verificação 1: Tem sorvete de milho?
                cursor.execute(
                    "SELECT sabor FROM sorvetes WHERE user_id = %s AND sabor = 'milho'",
                    (user_id,)
                )
                tem_milho = cursor.fetchone()
                print(f"[DEBUG] Tem sorvete milho? {bool(tem_milho)}")
        
                if tem_milho:
                    print(f"[DEBUG] Chamando cálculo de cenouras")
                    cenouras_bonus = calcular_cenouras_picole(user_id)
                    print(f"[DEBUG] Cenouras calculadas: {cenouras_bonus}")
                    
                    if cenouras_bonus > 0:
                        bot.send_message(
                            message.chat.id,
                            f"🌽 Bônus Ativo: +{cenouras_bonus} cenouras!"
                        )
                else:
                    print(f"[DEBUG] Removendo registro de milho")
                    cursor.execute(
                        "DELETE FROM picole_milho_ativo WHERE id_usuario = %s",
                        (user_id,)
                    )
                    conn.commit()
                    
            except Exception as e:
                print(f"[ERRO] Milho: {traceback.format_exc()}")
            finally:
                fechar_conexao(cursor, conn)
            # --- FIM DA NOVA SEÇÃO ---

            keyboard = telebot.types.InlineKeyboardMarkup()
            primeira_coluna = [
                telebot.types.InlineKeyboardButton(text="☁  Música", callback_data='pescar_musica'),
                telebot.types.InlineKeyboardButton(text="🌷 Anime", callback_data='pescar_animanga'),
                telebot.types.InlineKeyboardButton(text="🧶  Jogos", callback_data='pescar_jogos')
            ]
            segunda_coluna = [
                telebot.types.InlineKeyboardButton(text="🍰  Filmes", callback_data='pescar_filmes'),
                telebot.types.InlineKeyboardButton(text="🍄  Séries", callback_data='pescar_series'),
                telebot.types.InlineKeyboardButton(text="🍂  Misc", callback_data='pescar_miscelanea')
            ]

            keyboard.add(*primeira_coluna)
            keyboard.add(*segunda_coluna)
            keyboard.row(telebot.types.InlineKeyboardButton(text="🍒 Retrospectiva", callback_data='pescar_geral'))

            photo = "https://pub-6f23ef52e8614212a14d24b0cf55ae4a.r2.dev/BQACAgEAAxkBAAI7hWecPpVWspiKQzfOQcKwt_XDbfkPAAIqBgACWOrpRKRKBMvnlAvZNgQ.jpg"
            texto = f'<i>Olá! {nome}, \nVocê tem disponível: {qtd_iscas} iscas. \nBoa pesca!\n\nSelecione uma categoria:</i>'
            bot.send_photo(message.chat.id, photo=photo, caption=texto, reply_markup=keyboard, reply_to_message_id=message.message_id, parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, "Ei visitante, você não foi convidado! 😡", reply_to_message_id=message.message_id)

    except ValueError as e:
        print(f"Erro: {e}") 
        bot.send_message(message.chat.id, "Você foi banido permanentemente do garden. Entre em contato com o suporte caso haja dúvidas.", reply_to_message_id=message.message_id)
    except Exception as e:
        error_details = traceback.format_exc() 
        print(f"Erro inesperado: {error_details}")  
        bot.send_message(message.chat.id, "Ocorreu um erro inesperado ao tentar pescar.", reply_to_message_id=message.message_id)
