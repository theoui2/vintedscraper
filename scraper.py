import requests
import json

def fetch_vinted_ps3(max_results=30):
    items = []
    page = 1
    while len(items) < max_results:
        url = f"https://www.vinted.fr/api/v2/catalog/items?search_text=ps3&page={page}&per_page=50"
        resp = requests.get(url)
        if resp.status_code != 200:
            break
        data = resp.json()
        if "items" not in data:
            break

        # Filtrer uniquement les items avec "PS3" dans le titre (case insensitive)
        filtered = [item for item in data["items"] if "ps3" in item.get("title", "").lower()]
        items.extend(filtered)
        if not data.get("pagination", {}).get("has_more_items", False):
            break
        page += 1

    # Limiter et trier par prix croissant
    items = items[:max_results]
    items.sort(key=lambda x: x.get("price", {}).get("amount", 999999))

    # Format simplifié pour export JSON
    results = []
    for i in items:
        results.append({
            "id": i.get("id"),
            "title": i.get("title"),
            "price": i.get("price", {}).get("amount"),
            "currency": i.get("price", {}).get("currency"),
            "url": f'https://www.vinted.fr{ i.get("path", "") }',
            "image": i.get("photos", [{}])[0].get("url", "")
        })

    return results

if __name__ == "__main__":
    result = fetch_vinted_ps3()
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Exporté {len(result)} annonces PS3 dans output.json")
