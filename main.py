import websockets
import asyncio

import re

def get_answer(input):
    split_message = re.split('\s|[.:;_\-!?=\+*]\s', input.lower())
    response = check_all_answers(split_message)
    return response

def message_probability(user_message, recognized_words, single_answer=False, required_word=[]):
    message_accuracy = 0
    has_required_words = True

    for word in user_message:
        if word in recognized_words:
            message_accuracy += 1

    percentage_accuracy = float(message_accuracy) / float(len(recognized_words))

    for word in required_word:
        if word not in user_message:
            has_required_words = False
            break
    if has_required_words or single_answer:
        return int(percentage_accuracy * 100)
    else:
        return 0


def check_all_answers(message):
    highest_probability = {}

    def answer(bot_answer, list_of_words, single_answer=False, required_word=[]):
        nonlocal highest_probability
        highest_probability[bot_answer] = message_probability(message, list_of_words, single_answer, required_word)

    answer('Hola', ['hola', 'saludos', 'buenas'], single_answer=True)
    answer('Estoy bien y tu?', ['como', 'estas', 'va', 'vas', 'sientes'], required_word=['como'])
    answer('No hay de que estoy para servirte', ['gracias', 'te lo agradezco', 'thanks'], single_answer=True)
    answer('Hasta pronto y buena suerte', ['adios', 'hasta', 'luego', 'nos vemos'], single_answer=True)
    answer('Hola soy el asistente virtual si tienes algun problema estoy para servirte', ['start'], single_answer=True)
    answer('Para cerrar sesion da clic en tu mini perfil en la parte de arriba y seguido se abrira un menu en el que la opcion de cerrar sesion sera la ultima'
           , ['sesion', 'cerrar', 'salirme', 'puedo', 'como'], required_word=['cerrar sesion','salirme'])
    answer('Para editar tu perfil da clic en tu mini perfil en la parte de arriba y seguido se abrira un menu en el que la opcion de editar perfil sera la primera',
           ['perfil', 'mi', 'editar', 'edito', 'como', 'cambio'], required_word=['perfil'])
    answer('Para ver tus favoritos da clic en tu mini perfil en la parte de arriba a la derecha  y seguido se abrira un menu en el que la opcion de mis favoritos sera la segunda',
           ['favorito', 'mi', 'favoritos', 'mis', 'veo', 'como'], required_word=['favoritos'])
    answer('Para ver los programas disponibles dirigete a la pagina de inicio puedes dar clic en Programas CUCEI arriba a la izquierda', ['inicio', 'programas', 'becas', 'internados', 'trabajos'], required_word=['programas'])
    answer('Para ver las becas laborales disponibles en la pagina de inicio da clic en ver programas en el apartado de Becas', ['como', 'becas', 'laborales', 'becas laborales', 'ver'], required_word=['becas'])
    answer('Para ver los Internados disponibles en la pagina de inicio da clic en ver programas en el apartado de Interships', ['como', 'internado', 'intership', 'interships', 'ver'], required_word=['internados'])
    answer('Para ver los Trabajos disponibles en la pagina de inicio da clic en ver programas en el apartado de Trabajos', ['como', 'tabajo', 'trabajos', 'oferta laboral', 'ver','empleo'], required_word=['trabajos'])



    best_match = max(highest_probability, key=highest_probability.get)

    if highest_probability[best_match] < 1:
        return unknown()

    else:
        return best_match


def unknown():
    answer = ['No comprendi puedes repetirlo por favor']
    return answer



PORT = "Aqui va el puerto disponible del equipo"

print("server listening")

async def echo(websocket,path):
    print("new client connected")
    async for message in websocket:
        answer = get_answer(str(message))
        await websocket.send(answer)


start_server = websockets.serve(echo,"Aqui va la ip del equipo",PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

