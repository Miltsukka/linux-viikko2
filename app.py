import os
import pymysql
from flask import Flask, render_template_string

app = Flask(__name__)

SIVU = """
<!DOCTYPE html>
<html lang="fi">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Millan Linux-projekti – Viikko 2</title>
    <style>
        body {
            margin: 0;
            padding: 40px 20px;
            background: #f5eee9;
            color: #352e32;
            font-family: Arial, sans-serif;
            line-height: 1.7;
        }
        main {
            max-width: 720px;
            margin: auto;
            padding: 32px;
            background: white;
            border-radius: 20px;
        }
        h1, h2 { color: #704b60; }
        h1 { line-height: 1.3; }
        .laskuri {
            padding: 20px;
            background: #f2e4eb;
            border-radius: 12px;
        }
        .numero { font-size: 36px; font-weight: bold; }
        a { color: #704b60; }
    </style>
</head>
<body>
<main>
    <p>Millan Linux-projekti / Viikko 2</p>
    <h1>Pieniä askelia palvelimen rakentamiseen</h1>
    <p>
        Tällä viikolla laajensin Ubuntu-palvelintani
        Python-verkkosovelluksella ja tietokantaan tallentuvalla
        käyntilaskurilla. Sivu toimii Flaskilla Nginxin takana.
    </p>

    <section class="laskuri">
        <h2>Sivun latauskerrat</h2>
        <div class="numero">{{ kaynnit }}</div>
        <p>Laskuri kasvaa yhdellä jokaisella tämän sivun latauksella.</p>
    </section>

    <h2>Miten laskuri toimii?</h2>
    <p>
        Latausmäärä tallennetaan MySQL-tietokannan
        kayntilaskuri-tauluun. Python-sovellus kasvattaa lukua
        ja hakee päivitetyn arvon sivulle jokaisella latauksella.
        Laskuri laskee latauksia, ei yksittäisiä kävijöitä.
    </p>

    <h2>Uudelleenkäynnistystesti</h2>
    <p>
        Uudelleenkäynnistystesti tehtiin 5.11.2026.
        Nginx, MySQL ja Python-sovellus käynnistyivät automaattisesti.
        Uudelleenkäynnistyksen jälkeen tietokannan laskurin arvo oli 2.
        Sivu avautui ja laskuri kasvoi sivua ladattaessa.
    </p>

    <h2>Projektin lähdekoodi</h2>
    <p><a href="https://github.com/Miltsukka/linux-viikko2">Projektin lähdekoodi GitHubissa</a></p>

    <p><a href="/">Takaisin viikon 1 sivulle</a></p>
</main>
</body>
</html>
"""

@app.get("/viikko2/")
def etusivu():
    yhteys = pymysql.connect(
        unix_socket="/var/run/mysqld/mysqld.sock",
        user="viikko2app",
        password=os.environ["DB_PASSWORD"],
        database="viikko2",
        charset="utf8mb4",
        autocommit=False,
    )
    try:
        with yhteys.cursor() as kursori:
            kursori.execute(
                "UPDATE kayntilaskuri SET kaynnit = kaynnit + 1 WHERE id = 1"
            )
            kursori.execute(
                "SELECT kaynnit FROM kayntilaskuri WHERE id = 1"
            )
            kaynnit = kursori.fetchone()[0]
        yhteys.commit()
    except Exception:
        yhteys.rollback()
        raise
    finally:
        yhteys.close()

    return render_template_string(SIVU, kaynnit=kaynnit)
