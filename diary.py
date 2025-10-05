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
from sub import *
phrases = [
    "Você abre seu diário e escreve sobre como acordou com o som suave dos pássaros, e a brisa fresca da manhã trouxe consigo o perfume das flores do campo.",
    "Você abre seu diário e escreve sobre a tarde que passou colhendo flores silvestres e sentindo a grama macia sob seus pés descalços. Há algo de mágico na simplicidade da natureza.",
    "Você abre seu diário e escreve sobre o momento em que preparava o chá com ervas frescas do seu jardim, percebendo a beleza dos pequenos detalhes que tornam a vida tão especial.",
    "Você abre seu diário e escreve sobre a luz do sol filtrada pelas árvores, criando sombras dançantes no chão da floresta, lembrando-lhe que a beleza pode ser encontrada nas coisas mais simples.",
    "Você abre seu diário e escreve sobre a serenidade de bordar à beira da lareira, sentindo uma profunda conexão com as tradições antigas e o estilo de vida rural.",
    "Você abre seu diário e escreve sobre como cuidar do jardim é terapêutico. Cada planta que floresce é um lembrete da paciência e do cuidado que cultivamos em nossas vidas.",
    "Você abre seu diário e escreve sobre como os dias são mais doces quando preenchidos com atividades simples, como fazer pão caseiro e ouvir o canto dos pássaros.",
    "Você abre seu diário e escreve sobre as noites na cabana, acolhedoras e tranquilas. O crepitar do fogo na lareira é a melodia perfeita para um coração em paz.",
    "Você abre seu diário e escreve sobre o momento em que se sentou à sombra de um carvalho antigo, lendo um livro enquanto a natureza sussurrava seus segredos ao seu redor.",
    "Você abre seu diário e escreve sobre como a vida no campo ensina a valorizar a calma e a beleza que existem no presente. Cada momento é um presente a ser apreciado.",
    "Você abre seu diário e escreve sobre como passou a manhã fazendo geleia de frutas frescas, sentindo o doce aroma se espalhar pela cozinha.",
    "Você abre seu diário e escreve sobre a caminhada pelo bosque, onde encontrou um riacho cristalino que parecia sussurrar segredos antigos.",
    "Você abre seu diário e escreve sobre a tarde que passou tricotando uma manta macia, cada ponto representando uma memória querida.",
    "Você abre seu diário e escreve sobre a visita ao mercado local, onde encontrou produtos frescos e artesanatos únicos.",
    "Você abre seu diário e escreve sobre o momento em que se sentou no alpendre, observando o pôr do sol tingir o céu de tons dourados e rosados.",
    "Você abre seu diário e escreve sobre o prazer de ler um livro clássico à sombra de uma árvore frondosa, ouvindo o som suave das folhas ao vento.",
    "Você abre seu diário e escreve sobre o aroma da lavanda que plantou no jardim, trazendo um senso de calma e serenidade.",
    "Você abre seu diário e escreve sobre o prazer de fazer uma torta caseira, desde amassar a massa até saborear o resultado final.",
    "Você abre seu diário e escreve sobre como decorou a casa com flores silvestres, enchendo os cômodos de cores vibrantes e vida.",
    "Você abre seu diário e escreve sobre a alegria de alimentar os animais da fazenda, sentindo a conexão com cada ser vivo.",
    "Você abre seu diário e escreve sobre a manhã passada ajudando os vizinhos a colher maçãs no pomar comunitário, compartilhando risadas e histórias antigas.",
    "Você abre seu diário e escreve sobre o piquenique à beira do lago com outros camponeses, onde cada um trouxe um prato caseiro para compartilhar.",
    "Você abre seu diário e escreve sobre a feira de trocas na aldeia, onde artesãos e agricultores se reuniram para trocar seus produtos e habilidades.",
    "Você abre seu diário e escreve sobre a tarde em que ajudou um vizinho a construir uma cerca, aprendendo novas habilidades e fortalecendo amizades.",
    "Você abre seu diário e escreve sobre a festa da colheita, onde dançou ao som de músicas tradicionais e celebrou a abundância com os outros moradores.",
    "Você abre seu diário e escreve sobre a reunião ao redor da fogueira, onde ouviu histórias de tempos passados e compartilhou risadas com amigos.",
    "Você abre seu diário e escreve sobre a visita à feira de artesanato local, onde conheceu artesãos talentosos e aprendeu sobre suas técnicas.",
    "Você abre seu diário e escreve sobre o mutirão para plantar árvores na praça da aldeia, sentindo a alegria de contribuir para o futuro da comunidade.",
    "Você abre seu diário e escreve sobre a tarde em que preparou um chá para os vizinhos, desfrutando de uma conversa agradável e fortalecendo laços.",
    "Você abre seu diário e escreve sobre a caminhada com outros camponeses pelas trilhas da floresta, apreciando a natureza e a companhia um do outro."
]


fortunes = [
    "Sorte do dia: Hoje você encontrará paz nos sons da natureza.",
    "Sorte do dia: Pequenos momentos trarão grandes alegrias hoje.",
    "Sorte do dia: A simplicidade será sua maior aliada.",
    "Sorte do dia: Beleza inesperada surgirá em seu caminho.",
    "Sorte do dia: Conexões profundas enriquecerão seu dia.",
    "Sorte do dia: Sua paciência será recompensada hoje.",
    "Sorte do dia: Encontre doçura nas tarefas simples.",
    "Sorte do dia: A tranquilidade estará ao seu alcance.",
    "Sorte do dia: A sabedoria chegará até você em momentos de quietude.",
    "Sorte do dia: Aprecie cada momento, pois eles são únicos.",
    "Sorte do dia: Hoje, você saboreará os frutos do seu trabalho.",
    "Sorte do dia: Novas descobertas trarão alegria ao seu dia.",
    "Sorte do dia: Seus esforços de hoje criarão conforto para o futuro.",
    "Sorte do dia: Conexões locais enriquecerão sua vida hoje.",
    "Sorte do dia: A beleza do entardecer trará paz ao seu coração.",
    "Sorte do dia: Encontre inspiração nas palavras dos sábios de antigamente.",
    "Sorte do dia: Aromas calmantes irão transformar seu ambiente.",
    "Sorte do dia: A satisfação estará nos detalhes das suas criações.",
    "Sorte do dia: A natureza trará alegria e cor ao seu espaço.",
    "Sorte do dia: A interação com os animais trará momentos de pura felicidade.",
    "Sorte do dia: A colaboração trará alegria e união ao seu dia.",
    "Sorte do dia: O compartilhamento de alimentos fortalecerá os laços de amizade.",
    "Sorte do dia: Novas conexões trarão oportunidades valiosas.",
    "Sorte do dia: Ajudar os outros trará uma sensação de realização e comunidade.",
    "Sorte do dia: Celebrações comunitárias encherão seu coração de alegria.",
    "Sorte do dia: As histórias compartilhadas fortalecerão os vínculos de amizade.",
    "Sorte do dia: Aprender com os outros enriquecerá sua perspectiva.",
    "Sorte do dia: Seus esforços comunitários trarão benefícios duradouros.",
    "Sorte do dia: Pequenos gestos de hospitalidade criarão grandes memórias.",
    "Sorte do dia: A camaradagem ao ar livre renovará seu espírito."
]

def receive_note(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    note = message.text
    today = date.today()

    conn, cursor = conectar_banco_dados()

    try:
        # Registrar a anotação no banco de dados
        cursor.execute("INSERT INTO anotacoes (id_usuario, data, nome_usuario, anotacao) VALUES (%s, %s, %s, %s)",
                       (user_id, today, user_name, note))
        conn.commit()
        bot.send_message(message.chat.id, "Sua anotação foi registrada com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro ao registrar anotação: {err}")
        bot.send_message(message.chat.id, "Ocorreu um erro ao tentar registrar sua anotação. Tente novamente mais tarde.")
    finally:
        fechar_conexao(cursor, conn)
        
def diary_command(message):
    user_id = message.from_user.id
    today = date.today()

    conn, cursor = conectar_banco_dados()

    try:
        # Verifica se o usuário é VIP
        cursor.execute("SELECT COUNT(*) FROM vips WHERE id_usuario = %s", (user_id,))
        is_vip = cursor.fetchone()[0] > 0

        # Recupera o registro do diário do usuário
        cursor.execute("SELECT ultimo_diario, dias_consecutivos FROM diario WHERE id_usuario = %s", (user_id,))
        result = cursor.fetchone()

        if result:
            ultimo_diario, dias_consecutivos = result

            # Verifica se o usuário já fez o diário hoje
            if ultimo_diario == today:
                bot.send_message(message.chat.id, "Você já recebeu suas cenouras hoje. Volte amanhã!")
                return

            # Se fez ontem, aumenta o streak
            if ultimo_diario == today - timedelta(days=1):
                dias_consecutivos += 1
            elif is_vip and ultimo_diario == today - timedelta(days=2):
                # Se VIP, permite recuperar um dia perdido
                dias_consecutivos += 1
            else:
                # Caso contrário, reseta o streak
                dias_consecutivos = 1

            # Calcula as cenouras baseadas no streak
            cenouras = min(dias_consecutivos * 10, 100)

            # Atualiza o diário e o saldo de cenouras do usuário
            cursor.execute("UPDATE diario SET ultimo_diario = %s, dias_consecutivos = %s WHERE id_usuario = %s", 
                           (today, dias_consecutivos, user_id))
            cursor.execute("UPDATE usuarios SET cenouras = cenouras + %s WHERE id_usuario = %s", 
                           (cenouras, user_id))
            conn.commit()

        else:
            # Se for a primeira vez que o usuário registra no diário
            cenouras = 10
            dias_consecutivos = 1
            cursor.execute("INSERT INTO diario (id_usuario, ultimo_diario, dias_consecutivos) VALUES (%s, %s, %s)", 
                           (user_id, today, dias_consecutivos))
            cursor.execute("UPDATE usuarios SET cenouras = cenouras + %s WHERE id_usuario = %s", 
                           (cenouras, user_id))
            conn.commit()

        # Envia a mensagem de confirmação ao usuário
        phrase = random.choice(phrases)
        fortune = random.choice(fortunes)
        bot.send_message(message.chat.id, f"<i>{phrase}</i>\n\n<b>{fortune}</b>\n\nVocê recebeu <i>{cenouras} cenouras</i>!\n\n<b>Dias consecutivos:</b> <i>{dias_consecutivos}</i>\n\n", parse_mode="HTML")

        # Pergunta se o usuário deseja adicionar uma anotação ao diário
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text="Sim", callback_data="add_note"))
        markup.add(telebot.types.InlineKeyboardButton(text="Não", callback_data="cancel_note"))
        bot.send_message(message.chat.id, "Deseja anotar algo nesse dia especial?", reply_markup=markup)

    except mysql.connector.Error as err:
        print(f"Erro ao processar o comando /diary: {err}")
        bot.send_message(message.chat.id, "Ocorreu um erro ao tentar registrar seu diário. Tente novamente mais tarde.")
    finally:
        fechar_conexao(cursor, conn)

def pages_command(message):
    user_id = message.from_user.id
    conn, cursor = conectar_banco_dados()

    try:
        cursor.execute("SELECT data, anotacao FROM anotacoes WHERE id_usuario = %s ORDER BY data DESC", (user_id,))
        anotacoes = cursor.fetchall()

        if not anotacoes:
            bot.send_message(message.chat.id, "Você ainda não tem anotações no diário.")
            return

        response = ""
        total_anotacoes = len(anotacoes)
        for i, (data, anotacao) in enumerate(anotacoes, 1):
            page_number = total_anotacoes - i + 1
            response += f"Dia {page_number} - {data.strftime('%d/%m/%Y')}\n"
            # Verificar se a travessura está ativa e embaralhar, se necessário
        bot.send_message(message.chat.id, response)

    except mysql.connector.Error as err:
        print(f"Erro ao obter anotações: {err}")
        bot.send_message(message.chat.id, "Ocorreu um erro ao tentar obter suas anotações. Tente novamente mais tarde.")
    finally:
        fechar_conexao(cursor, conn)

def page_command(message):
    user_id = message.from_user.id
    params = message.text.split(' ', 1)[1:]
    if len(params) < 1:
        bot.send_message(message.chat.id, "Uso: /page <número_da_página>")
        return
    page_number = int(params[0])

    conn, cursor = conectar_banco_dados()

    try:
        cursor.execute("SELECT data, anotacao FROM anotacoes WHERE id_usuario = %s ORDER BY data DESC", (user_id,))
        anotacoes = cursor.fetchall()

        if not anotacoes:
            bot.send_message(message.chat.id, "Você ainda não tem anotações no diário.")
            return

        if page_number < 1 or page_number > len(anotacoes):
            bot.send_message(message.chat.id, "Número de página inválido.")
            return

        data, anotacao = anotacoes[page_number - 1]
        response = f"Mabigarden, dia {data.strftime('%d/%m/%Y')}\n\nQuerido diário... {anotacao}"
        
        bot.send_message(message.chat.id, response)

    except mysql.connector.Error as err:
        print(f"Erro ao obter anotação: {err}")
        bot.send_message(message.chat.id, "Ocorreu um erro ao tentar obter sua anotação. Tente novamente mais tarde.")
    finally:
        fechar_conexao(cursor, conn)


def edit_diary(message, bot):
    user_id = message.from_user.id
    today = date.today()

    conn, cursor = conectar_banco_dados()

    try:
        # Verifica se existe anotação para o dia de hoje
        cursor.execute("SELECT anotacao FROM anotacoes WHERE id_usuario = %s AND data = %s", (user_id, today))
        result = cursor.fetchone()

        if result:
            anotacao = result[0]
            resposta = f"Sua anotação para hoje é:\n\n<i>\"{anotacao}\"</i>\n\nEscolha uma ação:"
        else:
            resposta = "Você ainda não tem uma anotação para hoje. Deseja fazer uma anotação?"

        # Criar os botões de edição e cancelamento
        markup = types.InlineKeyboardMarkup()
        edit_button = types.InlineKeyboardButton("✍️ Editar", callback_data="edit_note")
        cancel_button = types.InlineKeyboardButton("❌ Cancelar", callback_data="cancel_edit")
        markup.add(edit_button, cancel_button)

        # Enviar a mensagem com os botões
        bot.send_message(message.chat.id, resposta, reply_markup=markup, parse_mode="HTML")

    except Exception as e:
        bot.send_message(message.chat.id, "Erro ao processar o comando de edição do diário.")
        print(f"Erro ao editar anotação: {e}")
    finally:
        fechar_conexao(cursor, conn)

def salvar_ou_editar_anotacao(message, user_id, today, bot):
    anotacao = message.text

    conn, cursor = conectar_banco_dados()

    try:
        # Verifica se já existe anotação para o dia
        cursor.execute("SELECT COUNT(*) FROM anotacoes WHERE id_usuario = %s AND data = %s", (user_id, today))
        existe_anotacao = cursor.fetchone()[0]

        if existe_anotacao:
            cursor.execute("UPDATE anotacoes SET anotacao = %s WHERE id_usuario = %s AND data = %s", (anotacao, user_id, today))
            bot.send_message(message.chat.id, "Sua anotação foi editada com sucesso!")
        else:
            cursor.execute("INSERT INTO anotacoes (id_usuario, data, nome_usuario, anotacao) VALUES (%s, %s, %s, %s)", 
                           (user_id, today, message.from_user.first_name, anotacao))
            bot.send_message(message.chat.id, "Sua anotação foi registrada com sucesso!")
        
        conn.commit()

    except Exception as e:
        bot.send_message(message.chat.id, "Erro ao salvar ou editar sua anotação.")
        print(f"Erro ao salvar ou editar anotação: {e}")
    finally:
        fechar_conexao(cursor, conn)

def cancelar_edicao(call, bot):
    bot.delete_message(call.message.chat.id, call.message.message_id)
