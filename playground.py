#Was ist ein Generator
# ========================================================================
# GENERATOREN (Python): Werte EINZELN liefern statt alle auf einmal
# ========================================================================
# Ausführen: python 01_generatoren_grundlagen.py
#
# Eine normale Funktion rechnet ALLES aus und gibt mit "return" eine
# komplette Liste zurück. Ein GENERATOR liefert mit "yield" immer nur EINEN
# Wert, pausiert und macht erst weiter, wenn der nächste Wert gebraucht wird.
# In Python sind Generatoren besonders verbreitet - range(), open() und
# zip() arbeiten alle nach diesem Prinzip.
#
# Bild dazu: Eine normale Funktion ist ein Bäcker, der 1000 Brötchen backt
# und sie dir alle auf einmal in die Arme drückt. Ein Generator backt jedes
# Brötchen erst, wenn du eins haben willst.

import os
import sys
import tempfile
import time

# ------------------------------------------------------------------
# 1. Normale Funktion vs. Generator
# ------------------------------------------------------------------

def zahlen_als_liste(amount):       # "normale Funktion"
    liste = []
    for i in range(amount):
        liste.append(i + 1)         # alles wird in der Liste gesammelt
    return liste                    # ... und am Ende komplett zurückgegeben

def zahlen_als_generator(amount):
    for i in range(amount):
        print("next")
        yield i + 1                 # EINEN Wert liefern, dann hier pausieren
        print("Done")

# Merksatz: Sobald in einer Funktion "yield" steht, ist sie ein Generator.
# Beim Aufruf läuft noch KEIN Code - man bekommt nur ein Generator-Objekt.
numGen = zahlen_als_generator(10)


# ------------------------------------------------------------------
# 2. Was passiert beim Pausieren? (Schritt für Schritt mit next())
# ------------------------------------------------------------------

# def log_gen(fn):
#     def wrapper(*args, **kwargs):
#         for i in fn(*args, **kwargs):
#             print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#             yield i
#     return wrapper
#
# def phases():
#     # RED = "\033[31m"
#     # YELLOW = "\033[33m"
#     # GREEN = "\033[32m"
#
#     R = "🔴\n⚫\n⚫\n\n"
#     RY = "🔴\n🟡\n⚫\n\n"
#     G = "⚫\n⚫\n🟢\n\n"
#     Y = "⚫\n🟡\n⚫\n\n"
#
#     phases = [R, RY, G, Y]
#     while True:
#         for phase in phases:
#             if phase == R:
#                 yield phase
#                 time.sleep(3)
#
#             if phase == G:
#                 yield phase
#                 time.sleep(3)
#
#             if phase == Y or phase == RY:
#                 yield phase
#                 time.sleep(1)
#
# @log_gen
# def ampel():
#     a = phases()
#     while True:
#         yield next(a)
#
# ampel = ampel()
#
# while True:
#     print(next(ampel))


# import time
#
#
# def semaforo():
#     while True:
#         yield "🚦"
#         time.sleep(1)
#         yield "🔴"
#         time.sleep(3)
#         yield "🟡"
#         time.sleep(2)
#         yield "🟢"
#         time.sleep(1)
#
#
# luces = semaforo()
#
# while True:
#     print(next(luces))


import webbrowser


def ampel():
    while True:
        yield "rot"
        yield "rotgelb"
        yield "gruen"
        yield "gelb"
        yield "pink"


generator = ampel()

farben = [next(generator) for _ in range(10)]

html = f"""
<html>
<head>
    <style>
        .ampel {{
            background: black;
            width: 100px;
            padding: 15px;
            border-radius: 15px;
        }}

        .licht {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: gray;
            margin: 10px;
            transition: background 0.5s;
        }}
    </style>
</head>

<body>
    <h2>Meine Ampel</h2>

    <div class="ampel">
        <div id="rot" class="licht"></div>
        <div id="gelb" class="licht"></div>
        <div id="gruen" class="licht"></div>
    </div>

    <br>
    <button onclick="weiter()">Weiter</button>

    <script>
        const farben = {farben};
        let position = 0;

        function weiter() {{
            let farbe = farben[position];

            document.getElementById("rot").style.background = "gray";
            document.getElementById("gelb").style.background = "gray";
            document.getElementById("gruen").style.background = "gray";

            if (farbe === "rot" || farbe === "rotgelb") {{
                document.getElementById("rot").style.background = "red";
            }}

            if (farbe === "gelb" || farbe === "rotgelb") {{
                document.getElementById("gelb").style.background = "yellow";
            }}

            if (farbe === "gruen") {{
                document.getElementById("gruen").style.background = "lime";
            }}

            if (farbe === "pink") {{
                document.getElementById("gruen").style.background = "magenta";
            }}

            position = (position + 1) % farben.length;
        }}

        weiter();
    </script>
</body>
</html>
"""

with open("ampel.html", "w", encoding="utf-8") as datei:
    datei.write(html)

webbrowser.open("ampel.html")
# ------------------------------------------------------------------
# EXECUTE
# ------------------------------------------------------------------



