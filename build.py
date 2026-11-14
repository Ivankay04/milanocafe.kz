#!/usr/bin/env python3
"""Сборка сайта «Милано»: template.html → index.html (русский) и kz.html (казахский), всё в одной папке.

  python3 build.py            — рабочая версия для хостинга (без полосы «пилот», без подписей на местах фото)
  python3 build.py --preview  — версия для просмотра (с полосой и подписями, что снимать)
"""
import re, sys, pathlib

DOMAIN = "milanocafe.kz"
# Адрес сервера на Railway (Settings → Networking), без «/» в конце. Пусто — заказы через WhatsApp.
API_URL = "https://milano-bot-production.up.railway.app"
SRC = pathlib.Path(__file__).parent
OUT = SRC
preview = "--preview" in sys.argv

tpl = (SRC / "template.html").read_text(encoding="utf-8")

LANGS = {
    "ru": dict(
        TITLE="Кафе «Милано», Риддер — пицца из печи, обеды, доставка",
        DESCRIPTION="Кафе-пиццерия «Милано» в Риддере с 2005 года. Пицца из печи, обеды по будням, доставка по городу и бронь столов. 3-й микрорайон, 9.",
        OG_TITLE="Кафе «Милано», Риддер", OG_LOCALE="ru_RU",
        CANONICAL=f"https://{DOMAIN}/", BASE="", ALT_URL="kz.html", ALT_LANG="kk", ALT_LABEL="Қаз",
    ),
    "kk": dict(
        TITLE="«Милано» кафесі, Риддер — пештен шыққан пицца, түскі ас, жеткізу",
        DESCRIPTION="Риддердегі «Милано» кафе-пиццериясы, 2005 жылдан бері. Пештен шыққан пицца, жұмыс күндері түскі ас, қала бойынша жеткізу және үстел брондау. 3-шағын аудан, 9.",
        OG_TITLE="«Милано» кафесі, Риддер", OG_LOCALE="kk_KZ",
        CANONICAL=f"https://{DOMAIN}/kz.html", BASE="", ALT_URL="./", ALT_LANG="ru", ALT_LABEL="Рус",
    ),
}

ELEM = re.compile(r"<(\w+)([^>]*?)\sdata-kk='([^']*)'([^>]*)>(.*?)</\1>", re.S)
PH = re.compile(r"""placeholder="[^"]*"([^>]*?)\sdata-kk-ph='([^']*)'""")

def build(lang):
    t = tpl
    v = dict(LANGS[lang], DOMAIN=DOMAIN, PILOT="true" if preview else "false")
    v["ORDER_URL"] = f"{API_URL}/order" if API_URL else ""
    v["STATUS_URL"] = f"{API_URL}/status" if API_URL else ""
    t = t.replace("showPhotoCodes: true", f"showPhotoCodes: {'true' if preview else 'false'}")
    if lang == "kk":
        t = t.replace('<html lang="ru">', '<html lang="kk">', 1)
        t = ELEM.sub(lambda m: f"<{m[1]}{m[2]}{m[4]}>{m[3]}</{m[1]}>", t)
        t = PH.sub(lambda m: f'placeholder="{m[2]}"{m[1]}', t)
    else:
        t = ELEM.sub(lambda m: f"<{m[1]}{m[2]}{m[4]}>{m[5]}</{m[1]}>", t)
        t = re.sub(r"\sdata-kk-ph='[^']*'", "", t)
    for k, val in v.items():
        t = t.replace("{{" + k + "}}", val)
    left = re.findall(r"\{\{\w+\}\}|data-kk", t)
    assert not left, f"{lang}: не заменено {set(left)}"
    return t

(OUT / "index.html").write_text(build("ru"), encoding="utf-8")
(OUT / "kz.html").write_text(build("kk"), encoding="utf-8")
print("ok:", OUT, "preview" if preview else "production")
