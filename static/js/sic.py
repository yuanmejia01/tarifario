import random

# El jugador solo puede fallar 3 preguntas
vidas = 3
# El jugador tendra un puntaje, cuando llegue a 10 puntos gana.
puntaje = 0
# Lista preguntas para no repetirlas
lista_preguntas = []
# Diccionario con las preguntas del Quizz
preguntas = {"""\n¿Cuantos Objetivos de Desarrollo Sostenible hay?
a)	 5
b)	 17
c)	 20""": "b",
             """\n¿Que son los objetivos de desarrollo sostenible?
             a)	 Objetivos que se tienen que cumplir para que el mundo sea un lugar mejor
             b)	 Es una empresa
             c)	 Es juego 
             d)	 No existen 
             """: "a",
             """\n¿Que significan las 3R?
             a)	 Recambiar, reducir y reusar
             b)	 Reutilizar, reducir y reciclar 
             c)	 Recoger, recambiar y reciclar
             """: "b",
             """\nEl ODS 1 define pobreza extrema como un ingreso 
             a)	 Inferior a 1 dolar al dia
             b)	 Inferior a 2 dolares al dia
             c)	 Inferior a 1,25 dolares al dia
             d)	 Ninguna de las anteriores
             """: "c",
             """\nMejorar el uso de la tecnologia para promover el empoderamiento de las mujeres es meta del ODS:
             a)	 8- Trabajo decente y crecimiento economico 
             b)	 5- Igualdad de genero 
             c)	 4- Educacion de calidad 
             d)	 10- Reduccion de las desigualdades 
             """: "b",
             """\nLos 3 pilares de desarrollo sostenible de la Agenda 2030 son el ambiental, el económico y el _______
             a)	 Juridico
             b)	 Social
             c)	 Familiar
             d)	 Cultural
             """: "b",
             """\n La cantidad de personas que no tienen miedo de caminar solas cerca de donde viven es un indicador del ODS
             a)	 10- Reduccion de las igualdades 
             b)	 16- Paz, justicia e instituciones solida
             c)	 5- Igualdad de genero
             d)	 11- Ciudades y comunidades sostenibles 
             """: "b",
             """\n¿Que contamina mas?
             a)	 Un carro 
             b)	 Una bicicleta 
             c)	 Una moto
             d)	 Unos patines
             """: "a",
             """\n¿Por qué el cambio climatico es malo para nosotros?
             a)	 Porque nos hace daño a los pulmones
             b)	 No es malo para nosotros 
             c)	 Porque afecta nuestro planeta
             """: "c",
             """\n¿Hay que tratar a los niños y niñas igual?
             a)	 No, porque los niños son mejores 
             b)	 Todos somos diferentes 
             c)	 No, porque las niñas son mejores 
             d)	 Si, todos somos iguales
             """: "d",
             """\nExiste ________ cuando todas las personas tienen en todo momento acceso físico y económico a suficientes alimentos nutritivos para satisfacer sus necesidades alimenticias a fin de llevar una vida activa y sana.
             a)	 subalimentacion
             b)	 sostenibilidad de los sistemas de producción
             c)	 seguridad alimentaria
             """: "c",
             """\nMejorar la coherencia de las politicas para el desarrollo sostenible es una meta del ODS
             a)	 16- Paz, justicia, e instituciones solidas 
             b)	 10- Reduccion de las desigualdades 
             c)	 8- Trabajo decente y crecimiento economico
             d)	 17- Alianzas para lograr objetivos
             """: "d",
             """\nEl transporte publico efectivo y de bajo costo es fundamental para la reducción de la pobreza y la desigualdad urbana porque...
             a)	 Facilita el acceso a empleos, atención medica, servicios educativos y otros bienes públicos.
             b)	 Es mas seguro y reduce el riesgo de asaltos.
             c)	 Es menos seguro y aumenta el riesgo de asaltos.
             """: "a",
             """\n ¿Que se aprobo antes: la agenda 2030 (ODS) o la Estrategia Nacional de Desarrollo (END) 2030?
             a)	 Las dos fueron aprobadas el mismo año (2015)
             b)	 La END 2030
             c)	 La END fue aprobada, la agenda todavía no
             d)	 La agenda 2030
             """: "b",
             """\n¿Es importante el agua limpia?
             a)	 Si, porque esta mas rica
             b)	 No, porque es mejor el agua sucia 
             c)	 Si, es bueno para la salud 
             """: "c",
             """\n¿La educacion es necesaria?
             a)	 Falso 
             b)	 Verdadero
             """: "b"}

preguntas_solas = list(preguntas.keys())
respuestas_solas = list(preguntas.values())
def bienvenida():
    print("Bienvenido a QuizzODS.")
    print("Responde las preguntas correctamente y ayudanos a llegar a la meta")


def has_ganado():
    return ("¡Felicidades, has ganado!")


def has_perdido():
    return ("¡Lo sentimos, has perdido! Intentalo de nuevo")


def pregunta():
    global puntaje
    global lista_preguntas
    global vidas
    global preguntas_solas
    global respuestas_solas
    n = 0
    lista_preguntas = []
    valido = True
    while valido:
        n = random.randint(0, 15)
        for i in lista_preguntas:
            if i == n:
                valido = True
            else:
                valido = False
                lista_preguntas.append(n)
                print(lista_preguntas)
    print(preguntas_solas[n])
    respuesta = input("Ingrese la respuesta: ")
    if respuesta == respuestas_solas[n]:
        print("Respuesta correcta.")
        puntaje += 1
    else:
        print("Respuesta incorrecta.")
        vidas -= 1
        print("La respuesta correcta es " + preguntas.values()[n] + ".")
    """while n not in lista_preguntas:
        n = random.randint(0, 15)
        lista_preguntas.append(n)
        print(lista_preguntas)
    print(preguntas_solas[n])
    respuesta = input("Ingrese la respuesta: ")
    if respuesta == respuestas_solas[n]:
        print("Respuesta correcta.")
        puntaje += 1
    else:
        print("Respuesta incorrecta.")
        vidas -= 1
        print("La respuesta correcta es " + preguntas.values()[n] + ".")"""


def main():
    bienvenida()
    global puntaje
    global lista_preguntas
    global preguntas_solas
    global vidas
    valido = True
    while valido:
        if puntaje == 10:
            valido = False
            print(has_ganado())
        elif vidas == 0:
            valido = False
            print(has_perdido())
        else:
            pregunta()


main()