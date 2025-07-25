import requests
from bs4 import BeautifulSoup

def check_updates(urls, sent_news):
    updates = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            articles = soup.find_all(["a", "article", "div"], limit=10)
            for a in articles:
                title = a.get_text(strip=True)[:150]
                link = a.get("href") or url
                if not link.startswith("http"):
                    link = url.rstrip("/") + "/" + link.lstrip("/")
                if link in sent_news:
                    continue
                updates.append({
                    "source": url,
                    "title": title,
                    "link": link,
                    "date": "Без даты"  # Даты обрабатываются в будущем
                })
        except Exception as e:
            print(f"Ошибка при парсинге {url}: {e}")
    return updates