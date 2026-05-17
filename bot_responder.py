import json
import time
import random
import threading
import os
import feedparser
import asyncio

from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask
from telethon import TelegramClient, events
from langdetect import detect
from deep_translator import GoogleTranslator
from telethon.sessions import StringSession
from pymongo import MongoClient

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
SESSION = os.getenv("SESSION_STRING")
MONGO_URI = os.getenv("MONGO_URI")

if not SESSION:
    raise ValueError("❌ SESSION_STRING no está configurada en Render")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI no está configurado en Render")

print("SESSION cargada:", bool(SESSION))

client = TelegramClient(StringSession(SESSION), api_id, api_hash)

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["telegram_bot"]
usuarios_collection = db["usuarios"]

try:
    mongo_client.admin.command("ping")
    print("✅ MongoDB conectado correctamente")
except Exception as e:
    print("❌ Error conectando MongoDB:", e)

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

USUARIOS_BLOQUEADOS = [
    8444913830,
    1552962337,
    93372553,
    7978907188,
    52504489
]

# =========================
# 📡 CONFIG VIDEOS / RSS
# =========================
RSS_CHANNELS = {
    "arbitraje": "https://www.youtube.com/feeds/videos.xml?channel_id=UCbjZiBl3iyOPl1gy_nNxD5g",
    "indicadores": "https://www.youtube.com/feeds/videos.xml?channel_id=UCQa_4rQlE2FtJlX7IA0Zmug",
    "copytrade": "https://www.youtube.com/feeds/videos.xml?channel_id=UCfzQjeCdi4cK_WREJJvwzoQ"
}

VIDEO_FIJO = {
    "conector": "https://youtu.be/qBBcSHgEMlM"
}

LINK_SENALES = "https://t.me/senalessbinariass"

rss_cache = {}
rss_last_update = {}

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

def obtener_video_random(key):
    ahora = time.time()

    # Si tiene RSS
    if key in RSS_CHANNELS:
        url = RSS_CHANNELS[key]

        # Cache cada 30 minutos
        if key not in rss_cache or ahora - rss_last_update.get(key, 0) > 1800:
            try:
                feed = feedparser.parse(url)
                videos = []

                for entry in feed.entries[:10]:
                    videos.append({
                        "titulo": entry.title,
                        "link": entry.link
                    })

                if videos:
                    rss_cache[key] = videos
                    rss_last_update[key] = ahora
            except:
                return None

        videos = rss_cache.get(key, [])
        if videos:
            return random.choice(videos)

    # Video fijo
    if key in VIDEO_FIJO:
        return {
            "titulo": "Mira este video 👇",
            "link": VIDEO_FIJO[key]
        }

    return None

# (SERVICIOS EXACTO - NO MODIFICADO)
servicios = {
    "1": {"key":"arbitraje","tipo":"herramienta","nombre":"Arbitraje Triangular","info":"""🔀 Herramienta de Arbitraje Triangular

📊 Esta herramienta en Excel con macros avanzadas detecta oportunidades de arbitraje automáticamente entre múltiples exchanges de criptomonedas.

⚡ ¿Qué hace?

🔹 Importa precios en tiempo real  
🔹 Analiza pares en milisegundos  
🔹 Detecta oportunidades de arbitraje triangular  
🔹 Compatible con Binance y más de 10 exchanges

💻 Funciona en Celular, Windows y Mac

🚀 Ideal para automatizar análisis y encontrar oportunidades que manualmente serían Imposibles de detectar.

🎥 🔥 Mira cómo funciona aquí 👇
https://youtube.com/@arbitrajedecriptomonedas""","precio":"""💰 Precio Especial Promocional

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

📲 Este software automatiza tus operaciones copiando señales directamente desde grupos de Telegram.

⚡ ¿Qué puede hacer?

🔹 Funciona con grupos públicos o privados, en cualquier idioma  
🔹 Compatible con Binarias, Forex y Criptomonedas  
🔹 Copia hasta 10 grupos simultáneamente  
🔹 Permite conectar hasta 3 brokers al mismo tiempo  
🔹 Opera en mercado Normal y OTC

💻📱 Compatible con Android, iOS, Windows y Mac 
🔹 Funciona 24/7 sin interrupciones  
🔹 Opera en cuenta Demo y Real

🚀 Incluye reportes automáticos cada 24 horas y configuración 100% personalizable según tu estrategia.

🤖 Actúa como un Trader automático, operando incluso cuando estás desconectado, viajando o descansando.

🎥 🔥 Mira cómo funciona aquí 👇
https://youtube.com/@tradingautomaticoo""","precio":"""💰 Costo de la Herramienta

💳 29 USDT — Pago único
🔹 Incluye actualizaciones
🔹 Soporte disponible 24/7

📦 Entrega del producto:
🔹 Recibirás el archivo de descarga en tu correo electrónico ✉️
🔹 Acceso a videos de instalación paso a paso
🔹 Incluye manual completo de funcionamiento

🚀 Empieza a usarla de inmediato, sin pagos mensuales."""},
    "3": {"key":"indicadores","tipo":"herramienta","nombre":"Automatización de Indicadores","info":"""⚙️Convertimos tu indicador o estrategia en un sistema automático que opere directamente en tu broker.

🔧 ¿Cómo trabajamos?

1️⃣ Si ya tienes un indicador  
🔹 Nos envías el archivo  
🔹 Lo convertimos en un sistema que abre operaciones Automáticamente

2️⃣ Si no tienes indicador  
🔹 Nos explicas tu estrategia (entradas, filtros, gestión, etc.)  
🔹 Lo desarrollamos desde cero y te entregamos totalmente Automatico

💳 Proceso simple  
🔹 Definimos todos los detalles contigo  
🔹 Confirmas y realizas el pago  
🔹 Iniciamos la construcción

⏰ En 24 horas recibirás tu sistema listo para usar en tu broker.

🎥 🔥 Mira cómo funciona aquí 👇
https://youtube.com/@TradingAutomatizadoo""","precio":"""💰 Planes de Automatización

📦 Automatizar tu indicador:
💳 39 USDT — Pago único
🔹 Convertimos tu indicador en un sistema automático listo para operar

📦 Desarrollar desde cero + automatizar:
💳 49 USDT — Pago único
🔹 Creamos tu estrategia y la dejamos funcionando en automático

📌 Plan Opcional – Ajustes Ilimitados

📦 Ajustes Ilimitados (Opcional)
💳 15 USDT adicional — Pago único

Podrás realizar:

🔹 Cambios de broker
🔹 Modificación de reglas
🔹 Ajustes visuales (flechas, colores, etc.)
🔹 Optimización de parámetros

✔️ Con este plan, puedes solicitar cualquier modificación futura sin volver a pagar

⚠️ Importante:
Si eliges solo automatizar tu indicador, cada ajuste futuro se considera una nueva programación."""},
    "4": {"key":"copytrade","tipo":"sistema","nombre":"Copy Trade","info":"""📥 Activación de Copy Trade

🔹 Debes crear una cuenta con nuestro link 🔗  
🔹 Si ya tienes cuenta en Pocket Option, debes cerrarla y crear una nueva con otro correo

📌 Luego de registrarte  
🔹 Envíanos tu 🆔 de cuenta   
🔹 Verificamos tu registro y activamos el Copy Trade

🆓 Activación GRATUITA  
🔹 Copy Trade activo por tiempo ILIMITADO

⚠️ Si deseas conservar tu cuenta actual  
💳 El acceso tiene un costo de 35 USDT — Pago único

🎥 🔥 Mira cómo funciona aquí 👇
https://youtube.com/@CopyTradePocketOption""","enlace":"Link de Registro 👇🏼\n\n🔗 https://u3.shortink.io/register?utm_campaign=68917&utm_source=affiliate&utm_medium=sr&a=A4rIXrS1IW9PCf&ac=nuevoenlace2025&code=BQI667\n\n✨ Después de registrarte y realizar tu depósito, Habla con Nano para Verificar tu 🆔 y darte acceso completo 🔥\n\n8️⃣ Hablar con Nano 👨‍💻\n9️⃣ Volver al menú principal 👈🏼"},
    "5": {"key":"senales","tipo":"sistema","nombre":"Grupo de Señales","info":"""📥 Acceso al Grupo VIP de Señales

📊 Recibe señales precisas y acceso al grupo VIP de forma inmediata.

🔹 Debes crear una cuenta con nuestro link 🔗  
🔹 Si ya tienes cuenta en Pocket Option, puedes cerrarla y crear una nueva con otro correo

📌 Luego de registrarte  
🔹 Envíanos tu 🆔 de cuenta   
🔹 Verificamos tu registro y activamos tu acceso al grupo VIP

🆓 Acceso GRATUITO  
🔹 Registrándote con nuestro link

⚠️ Si deseas conservar tu cuenta actual  
💳 El acceso tiene un costo de 35 USDT — Pago único y acceso al grupo VIP para siempre

🚀 Tenemos algunos espacios disponibles todavía.""","enlace":"Link de Registro 👇🏼\n\n🔗 https://u3.shortink.io/register?utm_campaign=68917&utm_source=affiliate&utm_medium=sr&a=A4rIXrS1IW9PCf&ac=nuevoenlace2025&code=BQI667\n\n✨ Después de registrarte y realizar tu depósito, Habla con Nano para Verificar tu 🆔 y darte acceso completo 🔥\n\n8️⃣ Hablar con Nano 👨‍💻\n9️⃣ Volver al menú principal 👈🏼"},
    "6": {"key":"fdi","tipo":"sistema","nombre":"Fondo de Inversión FDI","info":"""📊 Fondo de Inversión FDI

💼 Participa en nuestro sistema de inversión donde operamos una cuenta propia en Pocket Option con un robot avanzado 🤖 diseñado para generar rendimientos consistentes.

💰 ¿Cómo funciona?

🔹 Inversión mínima: 90 USD  
🔹 Sin límite máximo de inversión  
🔹 Operamos tu capital durante 5 días

📈 Resultado  
Recibes el 50% de ganancia + el 100% de tu capital despues de los 5 días

🚀 Ejemplo  
Si inviertes 200 USD → recibes 300 USD  
(200 de capital + 100 de ganancia)

🔁 Puedes ingresar las veces que desees, sin restricciones.

⏳ El ciclo comienza el mismo día en que realizas tu depósito.

📊 Puedes ver pagos y testimonios aquí 👇  
https://t.me/inversionesFDI""","enlace":"""📋 Requisitos para ingresar al Fondo de Inversión FDI

Para comenzar es muy sencillo 👇

1️⃣ Realizas tu depósito en nuestra cuenta de Pocket Option  
2️⃣ Completas un breve registro con tus datos  
3️⃣ Indicas la billetera donde deseas recibir tu pago  

💰 Una vez finalizado los 5 días:
Recibes el 50% de ganancia + 100% de tu capital directamente en tu billetera.

📊 Puedes ver pagos y testimonios aquí:
👉🏼 https://t.me/inversionesFDI

🚨 Deseas continuar o tienes alguna consulta?

7️⃣ Quiero hacer el depósito 💰  
8️⃣ Hablar con Nano 👨‍💻  
9️⃣ Volver al menú principal 👈🏼"""}
}

usuarios = {}

def cargar_usuarios():
    global usuarios
    usuarios = {}

    try:
        for user in usuarios_collection.find():
            user_id = str(user["_id"])
            user.pop("_id", None)
            usuarios[user_id] = user
    except Exception as e:
        print("Error cargando usuarios desde MongoDB:", e)


def guardar_usuarios():
    try:
        for user_id, data in usuarios.items():
            usuarios_collection.update_one(
                {"_id": str(user_id)},
                {"$set": data},
                upsert=True
            )
    except Exception as e:
        print("Error guardando usuarios en MongoDB:", e)

def guardar_usuario(user_id):
    try:
        usuarios_collection.update_one(
            {"_id": str(user_id)},
            {"$set": usuarios[user_id]},
            upsert=True
        )
    except Exception as e:
        print("Error guardando usuario:", e)

def registrar_usuario(user_id, nombre, sender):
    user_id = str(user_id)

    # ✅ SI ES NUEVO
    if user_id not in usuarios:
        usuarios[user_id] = {
            "nombre": nombre,
            "interes": None,
            "tipo": None,
            "ultimo_mensaje": time.time(),
            "bloqueado": False,
            "estado": "bot",
            "expira": 0,
            "recordatorio_enviado": False,
            "idioma": "es",
            "access_hash": sender.access_hash
        }

        guardar_usuario(user_id)
        return True

    # ✅ SI YA EXISTE
    else:
        usuarios[user_id]["ultimo_mensaje"] = time.time()
        usuarios[user_id]["recordatorio_enviado"] = False

        # 🔥 ACTUALIZAR ACCESS HASH SI FALTA O CAMBIÓ
        usuarios[user_id]["access_hash"] = sender.access_hash

        guardar_usuario(user_id)
        return False

async def recordatorios_async():
    while True:
        ahora = time.time()

        for user_id, user in usuarios.items():
            if not user.get("recordatorio_enviado") and ahora - user["ultimo_mensaje"] >= 86400:

                try:
                    idioma = user.get("idioma","es")
                    nombre = user.get("nombre","Amigo")
                    interes_key = user.get("interes")
                    saludo = obtener_saludo()

                    # 🔴 SIN INTERÉS
                    if not interes_key:
                        texto = mensaje_sin_interes(nombre, saludo)

                    # 🟢 CON INTERÉS 
                    else:
                        interes_nombre = obtener_nombre_interes(interes_key)

                        if interes_key == "fdi":
                            texto = f"""{saludo} {nombre} 👋

Te escribo nuevamente para comentarte un poco más sobre el Fondo de Inversión FDI 📊

Es un sistema donde operamos con un robot avanzado y generamos rendimientos en ciclos de 5 días.

💰 Puedes ver resultados reales aquí:
https://t.me/inversioneess

Cualquier duda, aquí estamos.

¡Saludos!"""

                        elif interes_key == "senales":
                            texto = f"""{saludo} {nombre} 👋

Te escribo nuevamente para compartirte resultados reales del grupo de señales 📊

Puedes verlos aquí 👇
https://t.me/senalessbinariass

Esto te ayudará a evaluar mejor el sistema 👍

Cualquier duda, aquí estamos.

¡Saludos!"""

                        else:
                            video = obtener_video_random(interes_key)

                            if video:
                                texto = f"""{saludo} {nombre} 👋

Te escribo nuevamente para compartirte un video sobre {interes_nombre} 📊

🎥 {video['titulo']}
{video['link']}

Creo que puede ayudarte a entender mejor cómo funciona 👍

Cualquier duda, aquí estamos.

¡Saludos!"""
                            else:
                                continue

                    texto = traducir_idioma_usuario(texto, idioma)

                    # ✅ ENVÍO CORRECTO (SIN THREADS)
                    from telethon.tl.types import InputPeerUser

                    peer = InputPeerUser(
                        int(user_id),
                        user["access_hash"]
                    )

                    await client.send_message(peer, texto)

                    print(f"✅ Enviado a {user_id}")

                    user["recordatorio_enviado"] = True
                    guardar_usuario(user_id)

                except Exception as e:
                    print(f"❌ Error enviando a {user_id}: {e}")

        # ✅ sleep async (NO time.sleep)
        await asyncio.sleep(300)

def obtener_saludo():
    tz = ZoneInfo("America/La_Paz")
    hora = datetime.now(tz).hour

    if 5 <= hora < 12:
        return "Buenos días"
    elif 12 <= hora < 19:
        return "Buenas tardes"
    else:
        return "Buenas noches"

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

def mensaje_sin_interes(nombre, saludo):
    return f"""Hola {nombre} 👋 {saludo}

Hace unos días estuvimos en contacto y quería saber si todavía te interesa ver algunas de nuestras herramientas o sistemas 📊

Seguimos activos y todo está disponible para que lo revises con calma 👍

Si quieres volver a ver el menú principal, solo escribe 9 y retomamos desde ahí 🙂

Estoy por aquí para ayudarte cuando lo necesites 🤝"""

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private:
        return

    sender=await event.get_sender()
    
    if sender.id in USUARIOS_BLOQUEADOS:
        return
    
    user_id=str(sender.id)
    nombre=sender.first_name or "Amigo"
    texto=event.raw_text.lower().strip()
    link_usuario = obtener_link_usuario(sender)

    es_nuevo = registrar_usuario(user_id, nombre, sender)
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
        guardar_usuario(user_id)
        return

    if user.get("bloqueado"):
        if time.time() > user.get("expira",0):
            user["bloqueado"] = False
            user["estado"] = "bot"
            guardar_usuario(user_id)

            interes = obtener_nombre_interes(user["interes"])

            await event.client.send_message(ADMIN_ID,
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

        await event.client.send_message(ADMIN_ID,
f"""🟢 CLIENTE QUIERE COMPRAR

👤 Nombre: {nombre}
🔗 Usuario: {link_usuario}
📦 Interés: {interes}
""")

        user["bloqueado"]=True
        user["estado"]="humano"
        user["expira"]=time.time()+86400
        guardar_usuario(user_id)

        if 0 <= time.localtime().tm_hour < 7:
            await responder(event, "🌙 En este horario Nano no está disponible, pero te atenderá lo más pronto posible. 🤝 Gracias por contactarnos.", user_id)
        else:
            await responder(event, """Perfecto 👌\n\nRecibimos USDT, USDC, BTC o cualquier criptomoneda 🌍🚀

Puedes enviar tu pago desde cualquier exchange o wallet de forma rápida y segura ⚡💼

📬 Escríbenos cuando estés listo y te facilitamos la dirección para completar tu envío sin complicaciones 🔐""", user_id)
        return

    if texto in ["8","soporte","nano"]:
        interes = obtener_nombre_interes(user["interes"])

        await event.client.send_message(ADMIN_ID,
f"""🟡 CLIENTE SOLICITA SOPORTE

👤 Nombre: {nombre}
🔗 Usuario: {link_usuario}
📦 Interés: {interes}
""")

        user["bloqueado"]=True
        user["estado"]="humano"
        user["expira"]=time.time()+86400
        guardar_usuario(user_id)

        if 0 <= time.localtime().tm_hour < 7:
            await responder(event, "🌙 En este horario Nano no está disponible, pero te atenderá lo más pronto posible. 🤝 Gracias por contactarnos.", user_id)
        else:
            await responder(event, "Genial 👍\n\nEnseguida lo atenderá 👨‍💻", user_id)
        return

    if texto in servicios:
        servicio=servicios[texto]

        user["interes"]=servicio["key"]
        user["tipo"]=servicio["tipo"]
        guardar_usuario(user_id)

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
    iniciar_web()

    print("BOT RESPONDER ACTIVO EN RENDER 🚀")

    print("Iniciando cliente...")
    client.start()
    print("Cliente conectado:", client.is_connected())

    # ✅ Ejecutar dentro del loop de Telethon
    client.loop.create_task(recordatorios_async())

    client.run_until_disconnected()

if __name__=="__main__":
    main()
