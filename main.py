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
    answer('Estoy bien y tu?', ['estas', 'va', 'vas', 'sientes'], required_word=['estas'])
    answer('No hay de que estoy para servirte', ['gracias', 'te lo agradezco', 'thanks'], single_answer=True)
    answer('Hasta pronto y buena suerte', ['adios', 'hasta', 'luego', 'nos vemos'], single_answer=True)
    answer('Hola soy el asistente virtual si tienes algun problema estoy para servirte', ['start'], single_answer=True)
    answer('Para cerrar sesion da clic en tu mini perfil en la parte de arriba a la derecha y seguido se abrira un menu en el que la opcion de cerrar sesion sera la ultima'
           , ['sesion', 'cerrar', 'salirme','terminar'], single_answer=True)
    answer('Para editar tu perfil da clic en tu mini perfil en la parte de arriba a la derecha y seguido se abrira un menu en el que la opcion de editar perfil sera la primera y seguido da clic en editar datos en la parte inferior de la pagina de perfil',
           ['perfil', 'mi', 'editar', 'edito', 'como', 'cambio'], required_word=['editar'])
    answer('Para ver tus favoritos da clic en tu mini perfil en la parte de arriba a la derecha y seguido se abrira un menu en el que la opcion de mis favoritos sera la segunda',
           ['favorito', 'mi', 'favoritos', 'mis', 'veo', 'como'], required_word=['favoritos'])
    answer('Para ver tus favoritos da clic en tu mini perfil en la parte de arriba a la derecha y seguido se abrira un menu en el que la opcion de mis favoritos es la segunda',
           ['publicaciones', 'mi', 'favoritas', 'mis', 'veo', 'como'], required_word=['favoritas'])
    answer('Para ver los programas disponibles dirigete a la pagina de inicio puedes dar clic en Programas CUCEI arriba a la izquierda', ['inicio', 'programas', 'becas', 'internados', 'trabajos'], required_word=['programas'])
    answer('Para ver las becas laborales disponibles en la pagina de inicio da clic en ver programas en el apartado de Becas', ['como', 'becas', 'laborales', 'becas laborales', 'ver'], required_word=['becas'])
    answer('Para ver los Internados disponibles en la pagina de inicio da clic en ver programas en el apartado de Interships', ['como', 'internado', 'veo   ', 'interships', 'ver'], required_word=['internados'])
    answer('Para ver los Trabajos disponibles en la pagina de inicio da clic en ver programas en el apartado de Trabajos', ['como', 'tabajo', 'trabajos', 'oferta laboral', 'ver','veo'], required_word=['trabajos'])
    answer('Para ver los detalles de una publicacion da clic en ver detalles y se mostraran los detalles de la publicacion', ['como', 'ver', 'detalle', 'detalles', 'publicacion','oferta'], required_word=['detalles'])
    answer('En caso de que mi asistencia no sea suficiente y necesites hablar con algun docente da clic en tu mini perfil arriba a la derecha y da clic en ayuda ahi podras ver los contactos de los docentes', ['como', 'contacto', 'atencion', 'ayuda','necesito'], required_word=['ayuda'])
    answer('Para buscar alguna publicacion tienes que escribir el nombre del programa', ['como','puedo', 'publicacion','buscar'], required_word=['buscar'])
    answer('Para buscar alguna publicacion solo tienes que escribir el nombre del programa', ['como', 'busco', 'programa', 'publicacion'], required_word=['busco'])
    answer('Para postularte es necesario que veas los detalles de la publicacion y seguido dar clic en postularme te tiene que llegar un correo, en caso de que no lo recibas despues de unos minutos dirigete al apartado de ayuda y contacta con algun docente', ['como', 'postulo', 'me', 'registro'], required_word=['postulo'])
    answer('Para registrarte es necesario que veas los detalles de la publicacion y seguido dar clic en postularme te tiene que llegar un correo, en caso de que no lo recibas despues de unos minutos dirigete al apartado de ayuda y contacta con algun docente', ['como', 'postulo', 'me', 'registro'], required_word=['registro'])








    best_match = max(highest_probability, key=highest_probability.get)

    if highest_probability[best_match] < 1:
        return unknown()

    else:
        return best_match


def unknown():
    answer = ['No comprendi puedes repetirlo por favor']
    return answer



PORT = ""

print("server listening")

async def echo(websocket,path):
    print("new client connected")
    async for message in websocket:
        answer = get_answer(str(message))
        await websocket.send(answer)


start_server = websockets.serve(echo,"",PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

