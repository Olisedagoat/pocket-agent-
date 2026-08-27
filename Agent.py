import json
import urllib.request

def fetch_top_tech_trends():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req) as response:
        story_ids = json.loads(response.read().decode())[:5]
    
    trends = []
    for s_id in story_ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
        with urllib.request.urlopen(item_url) as res:
            item = json.loads(res.read().decode())
            trends.append({
                "title": item.get("title"),
                "score": item.get("score"),
                "url": item.get("url", f"https://news.ycombinator.com/item?id={s_id}")
            })
            
    print("\n" + "="*50)
    print("🔥 ТОП-5 АКТУАЛЬНЫХ ТЕХНОЛОГИЧЕСКИХ ТРЕНДОВ:")
    print(json.dumps(trends, indent=2, ensure_ascii=False))
    print("="*50 + "\n")

if __name__ == "__main__":
    fetch_top_tech_trends()
