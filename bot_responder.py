import json
import time
import random
import threading
import os

from flask import Flask
from telethon import TelegramClient, events
from langdetect import detect
from deep_translator import GoogleTranslator

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient("session", api_id, api_hash)

# 🔥 SERVIDOR PARA RENDER
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot activo 🚀"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def iniciar_web():
    t = threading.Thread(target=run_web)
    t.start()

ADMIN_ID = -1003934691572

# =========================
# DETECTAR IDIOMA
# =========================
def detectar_idioma(texto):
    texto = texto.lower().strip()

    palabras_en = [
    "hello", "hi", "hey", "heyy", "hii",
    "good morning", "good afternoon", "good evening",
    "whats up", "what's up", "sup",
    "bro", "man", "friend",
    "thanks", "thank you", "thx", "ty",
    "price", "cost", "how much", "information", "details",
    "interested", "i'm interested", "interesed",
    "help", "support",
    "start", "get started",
    "buy", "purchase",
    "send info", "more info"
]
    palabras_pt = [
    "olá", "ola", "oi", "oie", "opa",
    "bom dia", "boa tarde", "boa noite",
    "tudo bem", "blz", "beleza",
    "obrigado", "obrigada", "vlw", "valeu",
    "preço", "preco", "valor", "quanto custa",
    "informação", "informacoes", "detalhes",
    "interessado", "tenho interesse", "quero",
    "ajuda", "suporte",
    "começar", "comecar", "iniciar",
    "comprar", "adquirir",
    "me envia", "manda info"
]

    for p in palabras_en:
        if p in texto:
            return "en"

    for p in palabras_pt:
        if p in texto:
            return "pt"

    try:
        lang = detect(texto)

        # Si detecta portugués pero el texto es corto, puede ser error
        if lang == "pt" and len(texto) <= 4:
            return "es"

        if lang in ["es","en","pt"]:
            return lang
        else:
            return "es"
    except:
        return "es"

# =========================
# TRADUCCIÓN (CORREGIDA)
# =========================
def traducir_idioma_usuario(texto, idioma):
    if idioma == "es":
        return texto
    try:
        return GoogleTranslator(source="auto", target=idioma).translate(texto)
    except:
        return texto

async def responder(event, texto, user_id):
    if int(user_id) == ADMIN_ID:
        await event.respond(texto)
        return

    idioma = usuarios[user_id].get("idioma","es")
    texto_final = traducir_idioma_usuario(texto, idioma)
    await event.respond(texto_final)

# =========================

respuestas_inicio = [
    "Perfecto 👌",
    "Genial 👍",
    "Listo ✅",
    "Excelente 🔥",
    "Bien 👌",

    "Claro 👌",
    "Correcto ✅",
    "Entendido 👍",

    "Buenísimo 🔥",
    "Excelente 💯",
    "Ideal 👌",

    "Ok 👌",
    "Vale 👍",
    "Dale 👌",

    "Super 🔥",
    "Top 🚀"
]

def respuesta_random():
    return random.choice(respuestas_inicio)

# (SERVICIOS EXACTO - NO MODIFICADO)
servicios = {
    "1": {"key":"arbitraje","tipo":"herramienta","nombre":"Arbitraje Triangular","info":"""🔀 Herramienta de Arbitraje Triangular

📊 Diseñada en Excel con macros avanzadas, esta herramienta:

Importa precios de criptomonedas en tiempo real desde múltiples exchanges.
Analiza automáticamente los pares en milisegundos.
Detecta oportunidades de arbitraje triangular para generar ganancias.

⚙️ Compatibilidad y uso:

Funciona con Binance y más de 10 exchanges adicionales.
Se instala fácilmente en PC (Windows 7 o superior).
También puede utilizarse desde el celular.
Compatible con Mac.

🚀 Ventaja clave:
Automatiza el análisis del mercado y encuentra oportunidades que serían imposibles de detectar manualmente.

💵 Si ya operas con criptomonedas, esta herramienta te ayudará a potenciar y automatizar tus ganancias.""","precio":"""💰 Precio Especial Promocional

💳 Precio regular: 69 USDT
🔥 Hoy: 49 USDT — Pago único

🔹 Sin cobros adicionales
🔹 Incluye actualizaciones
🔹 Soporte disponible 24/7

📦 Entrega del producto:
🔹 Recibirás el archivo de descarga en tu correo electrónico ✉️
🔹 Acceso a videos de instalación paso a paso
🔹 Incluye manual completo de funcionamiento

🚀 Instalación rápida y lista para usar desde el primer día."""},
    "2": {"key":"conector","tipo":"herramienta","nombre":"Conector de Señales","info":"""🤖 Conector de Señales con Inteligencia Artificial

Este software está diseñado para automatizar tus operaciones copiando señales directamente desde grupos de Telegram 📲

⚡ ¿Qué puede hacer?
🔹 Funciona con cualquier grupo de señales (público o privado, en cualquier idioma)
🔹 Compatible con Binarias, Forex y Criptomonedas
🔹 Puede copiar hasta 10 grupos simultáneamente
🔹 Permite conectar hasta 3 brokers al mismo tiempo
🔹 Opera en mercados Normal y OTC

💻📱 Acceso y compatibilidad:
🔹 Disponible en PC, Android y iOS
🔹 Funciona 24/7 sin interrupciones
🔹 Opera tanto en cuenta Demo como Real

📊 Funciones avanzadas:
🔹 Envía reportes automáticos cada 24 horas a tu correo
🔹 Sistema desarrollado con Inteligencia Artificial
🔹 100% configurable según tu estrategia

🚀 Ventaja clave:
Actúa como un Trader personal automático, ejecutando operaciones incluso cuando estás desconectado, viajando o descansando

💡 Una herramienta potente para automatizar tus resultados.""","precio":"""💰 Costo de la Herramienta

💳 29 USDT — Pago único
🔹 Incluye actualizaciones
🔹 Soporte disponible 24/7

📦 Entrega del producto:
🔹 Recibirás el archivo de descarga en tu correo electrónico ✉️
🔹 Acceso a videos de instalación paso a paso
🔹 Incluye manual completo de funcionamiento

🚀 Empieza a usarla de inmediato, sin pagos mensuales."""},
    "3": {"key":"indicadores","tipo":"herramienta","nombre":"Automatización de Indicadores","info":"""⚙️ Automatizamos tu Estrategia de Trading

Convertimos tu indicador o estrategia en un sistema automático que opere directamente en tu broker 📊

🔧 ¿Cómo trabajamos?

1️⃣ Si ya tienes un indicador:
🔹 Envíanos el archivo
🔹 Lo convertimos en un sistema 100% automatizado para tu broker

2️⃣ Si no tienes indicador:
🔹 Cuéntanos tu estrategia (entradas, filtros, gestión, etc.)
🔹 Lo desarrollamos desde cero, totalmente a medida

💳 Proceso:
🔹 Definimos todos los detalles contigo
🔹 Confirmas y realizas el pago
🔹 Iniciamos el desarrollo

⏰ Entrega rápida:
En aproximadamente 24 horas recibirás tu sistema automatizado en tu correo ✉️ listo para usar en tu broker

🚀 Opera de forma automática y lleva tu trading al siguiente nivel.""","precio":"""💰 Planes de Automatización

📦 Automatizar tu indicador:
💳 39 USDT — Pago único
🔹 Convertimos tu indicador en un sistema automático listo para operar

📦 Desarrollar desde cero + automatizar:
💳 49 USDT — Pago único
🔹 Creamos tu estrategia y la dejamos funcionando en automático

📌 Plan Opcional – Ajustes Ilimitados

💳 15 USDT adicional (único pago)

🔹 Cambios de broker
🔹 Modificación de reglas
🔹 Ajustes visuales (flechas, colores, etc.)
🔹 Optimización de parámetros

✔️ Con este plan, puedes solicitar cualquier modificación futura sin volver a pagar

⚠️ Importante:
Si eliges solo automatizar tu indicador, cada ajuste futuro se considera una nueva programación."""},
    "4": {"key":"copytrade","tipo":"sistema","nombre":"Copy Trade","info":"""📥 Activación de Copy Trade

Para recibir las operaciones en tu cuenta, sigue estos pasos:

🔹 Debes crear una cuenta con nuestro link 🔗
🔹 Si ya tienes cuenta en Pocket Option, debes cerrarla y crear una nueva con otro correo

📌 Una vez creada:
🔹 Envíanos tu ID de cuenta 🆔
🔹 Verificamos tu registro y activamos el Copy Trade

📊 Resultados estimados:
💰 Ganancias diarias entre 5 y 17 USD, dependiendo de tu capital

🆓 Costo:
🔹 Activación GRATUITA
🔹 Copy Trade activo por tiempo ILIMITADO

⚠️ Importante:
Si deseas conservar tu cuenta actual, el acceso tiene un costo de:
💳 35 USDT — Pago único

🚀 Tenemos algunos espacios todavía.""","enlace":"Link de Registro 👇🏼\n\n🔗 https://u3.shortink.io/register?utm_campaign=68917&utm_source=affiliate&utm_medium=sr&a=A4rIXrS1IW9PCf&ac=nuevoenlace2025&code=BQI667\n\n8️⃣ Hablar con Nano 👨‍💻\n9️⃣ Volver al menú principal 👈🏼"},
    "5": {"key":"senales","tipo":"sistema","nombre":"Grupo de Señales","info":"""📥 Acceso al Grupo VIP de Señales

Para ingresar, sigue estos pasos:

🔹 Crea una cuenta con nuestro link 🔗
🔹 Si ya tienes cuenta en Pocket Option, puedes cerrarla y crear una nueva con otro correo

📌 Luego:
🔹 Envíanos tu ID de cuenta 🆔
🔹 Verificamos tu registro y activamos tu acceso al grupo VIP

🆓 Costo de ingreso:
🔹 GRATUITO registrándote con nuestro link

⚠️ Importante:
Si deseas conservar tu cuenta actual, el acceso tiene un costo de:
💳 35 USDT — Pago único y acceso al Grupo VIP por siempre

🚀 Tenemos algunos espacios todavía.""","enlace":"Link de Registro 👇🏼\n\n🔗 https://u3.shortink.io/register?utm_campaign=68917&utm_source=affiliate&utm_medium=sr&a=A4rIXrS1IW9PCf&ac=nuevoenlace2025&code=BQI667\n\n8️⃣ Hablar con Nano 👨‍💻\n9️⃣ Volver al menú principal 👈🏼"},
    "6": {"key":"fdi","tipo":"sistema","nombre":"Fondo de Inversión FDI","info":"""📊 Fondo de Inversión FDI

💼 Tenemos un sistema exclusivo donde operamos una cuenta propia en Pocket Option con un robot avanzado 🤖 diseñado para manejar capitales altos y generar rendimientos consistentes.

💰 ¿Cómo funciona?
🔹 Inversión mínima: 100 USD  
🔹 Sin límite máximo de inversión  
🔹 Operamos tu capital durante 5 días  

📈 Resultado:
Recibes el 50% de ganancia + el 100% de tu capital inicial al finalizar el ciclo.

🚀 Ejemplo:
Si inviertes 100 USD → recibes 150 USD en total  
(100 de capital + 50 de ganancia)

🔁 Puedes ingresar las veces que desees al fondo, sin restricciones.

⏳ Importante:
El período de operación comienza el mismo día en que realizas tu depósito.

📊 Puedes ver pagos reales y testimonios aquí:
👉🏼 https://t.me/inversioneess

🔥 Es una opción ideal si buscas generar ingresos sin necesidad de operar por tu cuenta.""","enlace":"""📋 Requisitos para ingresar al Fondo de Inversión FDI

Para comenzar es muy sencillo 👇

1️⃣ Realizas tu depósito en nuestra cuenta de Pocket Option  
2️⃣ Completas un breve registro con tus datos  
3️⃣ Indicas la billetera donde deseas recibir tu pago  

💰 Una vez finalizado el ciclo:
Recibes el 50% de ganancia + tu capital inicial directamente en tu billetera.

📊 Puedes ver pagos reales y testimonios aquí:
👉🏼 https://t.me/inversioneess

🚨 Deseas continuar o tienes alguna consulta?

7️⃣ Quiero hacer el depósito 💰  
8️⃣ Hablar con Nano 👨‍💻  
9️⃣ Volver al menú principal 👈🏼"""}
}

usuarios = {}

def cargar_usuarios():
    global usuarios

    # 🔥 CREAR ARCHIVO SI NO EXISTE
    if not os.path.exists("usuarios.json"):
        with open("usuarios.json", "w") as f:
            json.dump({}, f)

    try:
        with open("usuarios.json","r") as f:
            usuarios = json.load(f)
    except:
        usuarios = {}

def guardar_usuarios():
    with open("usuarios.json","w") as f:
        json.dump(usuarios,f,indent=4)

def registrar_usuario(user_id,nombre):
    user_id=str(user_id)
    if user_id not in usuarios:
        usuarios[user_id]={
            "nombre":nombre,
            "interes":None,
            "tipo":None,
            "ultimo_mensaje":time.time(),
            "bloqueado":False,
            "estado":"bot",
            "expira":0,
            "recordatorio_enviado": False,
            "idioma":"es"
        }
        return True
    else:
        usuarios[user_id]["ultimo_mensaje"]=time.time()
        usuarios[user_id]["recordatorio_enviado"]=False
        return False

def verificar_recordatorios():
    while True:
        ahora = time.time()
        for user_id, user in usuarios.items():
            if not user.get("recordatorio_enviado") and ahora - user["ultimo_mensaje"] >= 108000:
                try:
                    idioma = user.get("idioma","es")
                    texto = traducir_idioma_usuario("Esperamos sus consultas, saludos 👍🏻", idioma)
                    client.loop.create_task(
                        client.send_message(int(user_id), texto)
                    )
                    user["recordatorio_enviado"] = True
                    guardar_usuarios()
                except:
                    pass
        time.sleep(300)

def obtener_saludo():
    hora=time.localtime().tm_hour
    if 5<=hora<12: return "Buenos días"
    elif 12<=hora<19: return "Buenas tardes"
    else: return "Buenas noches"

def obtener_link_usuario(sender):
    if sender.username:
        return f"@{sender.username}"
    else:
        return f"tg://user?id={sender.id}"

def obtener_nombre_interes(key):
    for s in servicios.values():
        if s["key"] == key:
            return s["nombre"]
    return "Sin especificar"

def menu_texto(nombre):
    saludo=obtener_saludo()
    return f"""Hola {nombre} 👋 {saludo}!

Gracias por escribir

¿Cual Herramienta o Sistema te interesa?

1️⃣ Arbitraje Triangular en Excel 🔀 
2️⃣ Conector de Señales 📡  
3️⃣ Automatización de Indicadores ⚙️  
4️⃣ Copy Trade 📊  
5️⃣ Grupo de Señales 📈  
6️⃣ Fondo de Inversión FDI 💼  

7️⃣ Quiero hacer un pedido 💰  
8️⃣ Hablar con Nano 👨‍💻 

Respóndeme con el número 👇"""

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private:
        return

    sender=await event.get_sender()
    
    if sender.id == 8756142735:
        return
    
    user_id=str(sender.id)
    nombre=sender.first_name or "Amigo"
    texto=event.raw_text.lower().strip()
    link_usuario = obtener_link_usuario(sender)

    es_nuevo=registrar_usuario(user_id,nombre)
    user = usuarios[user_id]

    # DETECTAR IDIOMA SOLO SI EL USUARIO ES NUEVO
    if es_nuevo:
        if any(c.isalpha() for c in texto):

            palabras_es_clave = ["hola", "buenas", "gracias"]
 
            idioma_detectado = detectar_idioma(texto)

            # 🔥 FORZAR ESPAÑOL SI CONTIENE PALABRAS CLAVE
            if any(p in texto for p in palabras_es_clave):
                idioma_detectado = "es"

            elif idioma_detectado not in ["es", "en", "pt"]:
                idioma_detectado = "es"

            user["idioma"] = idioma_detectado

    # NORMALIZAR INPUT
    if user.get("idioma") == "en":
        if any(p in texto for p in ["price", "prices", "cost", "how much"]):
            texto = "precio"
        if any(p in texto for p in ["access", "get access", "enter", "join"]):
            texto = "acceso"

    if user.get("idioma") == "pt":
        if any(p in texto for p in ["preço", "preco"]):
            texto = "precio"
        if any(p in texto for p in ["acesso", "acesse", "acessar"]):
            texto = "acceso"

    if es_nuevo:
        await responder(event, menu_texto(nombre), user_id)
        guardar_usuarios()
        return

    if user.get("bloqueado"):
        if time.time() > user.get("expira",0):
            user["bloqueado"] = False
            user["estado"] = "bot"
            guardar_usuarios()

            interes = obtener_nombre_interes(user["interes"])

            await client.send_message(ADMIN_ID,
f"""🔓 CLIENTE DESBLOQUEADO AUTOMÁTICAMENTE

👤 Nombre: {nombre}
🔗 Usuario: {link_usuario}
📦 Interés: {interes}

El bot ha retomado la conversación automáticamente.
""")
        else:
            return

    if texto in ["7","pedido"]:
        interes = obtener_nombre_interes(user["interes"])

        await client.send_message(ADMIN_ID,
f"""🟢 CLIENTE QUIERE COMPRAR

👤 Nombre: {nombre}
🔗 Usuario: {link_usuario}
📦 Interés: {interes}
""")

        user["bloqueado"]=True
        user["estado"]="humano"
        user["expira"]=time.time()+86400
        guardar_usuarios()

        if 0 <= time.localtime().tm_hour < 7:
            await responder(event, "🌙 En este horario Nano no está disponible, pero te atenderá lo más pronto posible. 🤝 Gracias por contactarnos.", user_id)
        else:
            await responder(event, """Perfecto 👌\n\nRecibimos USDT, USDC, BTC o cualquier criptomoneda 🌍🚀

Puedes enviar tu pago desde cualquier exchange o wallet de forma rápida y segura ⚡💼

📬 Escríbenos cuando estés listo y te facilitamos la dirección para completar tu envío sin complicaciones 🔐""", user_id)
        return

    if texto in ["8","soporte","nano"]:
        interes = obtener_nombre_interes(user["interes"])

        await client.send_message(ADMIN_ID,
f"""🟡 CLIENTE SOLICITA SOPORTE

👤 Nombre: {nombre}
🔗 Usuario: {link_usuario}
📦 Interés: {interes}
""")

        user["bloqueado"]=True
        user["estado"]="humano"
        user["expira"]=time.time()+86400
        guardar_usuarios()

        if 0 <= time.localtime().tm_hour < 7:
            await responder(event, "🌙 En este horario Nano no está disponible, pero te atenderá lo más pronto posible. 🤝 Gracias por contactarnos.", user_id)
        else:
            await responder(event, "Genial 👍\n\nEnseguida lo atenderá 👨‍💻", user_id)
        return

    if texto in servicios:
        servicio=servicios[texto]

        user["interes"]=servicio["key"]
        user["tipo"]=servicio["tipo"]
        guardar_usuarios()

        msg=f"""{respuesta_random()}

{servicio['info']}
"""

        if servicio["tipo"]=="herramienta":
            msg+="\n🚨Qué te pareció?, Si estás interesado escríbeme: 💰 precio 💰\n\n9️⃣ Volver al menú principal 👈🏼"
        else:
            msg+="\n🚨 Escríbeme 🔗 acceso 🔗 si deseas recibir toda la información para comenzar\n\n9️⃣ Volver al menú principal 👈🏼"

        await responder(event, msg, user_id)
        return

    if "precio" in texto:
        interes=user["interes"]

        if not interes:
            await responder(event, menu_texto(nombre), user_id)
            return

        for s in servicios.values():
            if s["key"]==interes and s["tipo"]=="herramienta":
                await responder(event, f"""{respuesta_random()}

{s['precio']}

¿Que te pareció, deseas continuar?

7️⃣ Quiero hacer el pedido 💰  
8️⃣ Hablar con Nano 👨‍💻
9️⃣ Volver al menú principal 👈🏼""", user_id)
                return

    if "acceso" in texto:
        interes=user["interes"]

        if not interes:
            await responder(event, menu_texto(nombre), user_id)
            return

        for s in servicios.values():
            if s["key"]==interes and s["tipo"]=="sistema":
                await responder(event, f"{respuesta_random()}\n\n{s['enlace']}", user_id)
                return

    await responder(event, menu_texto(nombre), user_id)

def main():
    cargar_usuarios()

    # 🔥 INICIAR SERVIDOR WEB (RENDER)
    iniciar_web()

    threading.Thread(target=verificar_recordatorios, daemon=True).start()

    print("BOT RESPONDER ACTIVO EN RENDER 🚀")

    client.start()
    client.run_until_disconnected()

if __name__=="__main__":
    main()
