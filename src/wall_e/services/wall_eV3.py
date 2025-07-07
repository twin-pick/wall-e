import asyncio
import re
from playwright.async_api import async_playwright

def getGenre(liste):
    return "+".join(liste)

# Fonction pour scraper une seule page
async def scrap_watchlist_page(page, username, page_num, genre_url):
    if genre_url:
        url = f"https://letterboxd.com/{username}/watchlist/genre/{genre_url}/by/rating/page/{page_num}/"
    else:
        url = f"https://letterboxd.com/{username}/watchlist/by/rating/page/{page_num}/"

    await page.goto(url)
    try:
        await page.wait_for_selector(".poster-container", timeout=8000)
    except:
        return []  # Timeout ou page vide

    titles = await page.locator(".frame-title").all_text_contents()

    films = []
    for value in titles:
        match = re.match(r"^(.*)\s\((\d{4})\)$", value)
        if match:
            nom = match.group(1)
            date = match.group(2)
            films.append({"title": nom, "date": date})

    print(f"✅ Page {page_num} : {len(films)} films")
    return films

# Fonction principale
async def scrap_watch_list(username, genres=[], batch_size=5):
    all_films = []
    genre_url = getGenre(genres) if genres else ""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        page_num = 1
        while True:
            # Crée les pages à l’avance
            pages = [await context.new_page() for _ in range(batch_size)]
            tasks = [
                scrap_watchlist_page(pages[i], username, page_num + i, genre_url)
                for i in range(batch_size)
            ]

            results = await asyncio.gather(*tasks)

            # Fermer les pages ouvertes pour libérer la mémoire
            for page in pages:
                await page.close()

            empty = True
            for films in results:
                if films:
                    all_films.extend(films)
                    empty = False

            if empty:
                print("🛑 Plus de films à scraper.")
                break

            page_num += batch_size

        await browser.close()

    return all_films

# Exemple d'appel
'''
async def main():
    username = "66Sceptre"
    genres = []  # ← Laisse vide si tu ne veux pas filtrer
    films = await scrap_watchlist(username, genres,20)
    print(f"\n🎬 {len(films)} films trouvés pour {username}")
    for film in films[:5]:
        print(f"  - {film['title']} ({film['date']})")
 

asyncio.run(main())
'''