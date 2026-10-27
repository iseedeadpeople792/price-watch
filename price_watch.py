"""Следит за ценой товара на странице и сообщает, когда она упала.
Пример:
  python price_watch.py https://example.com/item --pattern "data-price=\\"(\\d+[.,]?\\d*)\\""
Первый запуск запоминает цену, следующие сравнивают с сохранённой (prices.json).
"""
import argparse
import json
import re
import sys
import urllib.request

STATE = "prices.json"


def parse_price(html, pattern):
    """Достаёт число по regex с одной группой. Возвращает float или None."""
    m = re.search(pattern, html)
    if not m:
        return None
    return float(m.group(1).replace(" ", "").replace(",", "."))


def decide(old, new):
    """Что сделать: 'first' (первая цена), 'drop', 'rise' или 'same'."""
    if old is None:
        return "first"
    return "drop" if new < old else "rise" if new > old else "same"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "price-watch/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", "replace")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("url")
    p.add_argument("--pattern", required=True, help="regex с одной группой для цены")
    args = p.parse_args(argv)
    try:
        with open(STATE, encoding="utf-8") as f:
            state = json.load(f)
    except FileNotFoundError:
        state = {}
    price = parse_price(fetch(args.url), args.pattern)
    if price is None:
        sys.exit("Цена по шаблону не найдена")
    action = decide(state.get(args.url), price)
    print({"first": f"Запомнил цену: {price}", "drop": f"Цена упала: {state.get(args.url)} → {price}",
           "rise": f"Цена выросла: {state.get(args.url)} → {price}", "same": f"Цена не изменилась: {price}"}[action])
    state[args.url] = price
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
