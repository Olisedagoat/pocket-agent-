import json
import os
import urllib.request
import urllib.parse

def send_telegram_message(text):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Ошибка: токен или Chat ID не переданы.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true"
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload)
    with urllib.request.urlopen(req) as resp:
        print("Сообщение успешно доставлено в Telegram!")

def fetch_and_report():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req) as response:
        story_ids = json.loads(response.read().decode())[:5]
    
    report_lines = ["🚀 <b>ТОП ТЕХНОЛОГИЧЕСКИХ ТРЕНДОВ:</b>\n"]
    for i, s_id in enumerate(story_ids, 1):
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
        with urllib.request.urlopen(item_url) as res:
            item = json.loads(res.read().decode())
            title = item.get("title", "Без названия")
            link = item.get("url", f"https://news.ycombinator.com/item?id={s_id}")
            score = item.get("score", 0)
            report_lines.append(f"{i}. <a href='{link}'>{title}</a> (Очки: {score})")
            
    message_text = "\n".join(report_lines)
    print(message_text)
    send_telegram_message(message_text)

if __name__ == "__main__":
    fetch_and_report()
