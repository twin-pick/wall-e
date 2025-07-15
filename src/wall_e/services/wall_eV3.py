import asyncio
import re
from playwright.async_api import async_playwright


async def scrap_watchlist_page(page, username, page_num, genre):

    url_start = f"https://letterboxd.com/{username}/watchlist/"
    sort = "/by/rating/page/"
    if genre:
        url = f"{url_start}genre/{genre}{sort}{page_num}/"
    else:
        url = f"{url_start}{sort}{page_num}/"

    await page.goto(url)
    try:
        await page.wait_for_selector(".poster-container", timeout=4000)
        await page.wait_for_timeout(200)
    except Exception:
        return []

    titles = await page.locator(".frame-title").all_text_contents()

    films = []
    for value in titles:
        match = re.match(r"^(.*)\s\((\d{4})\)$", value)
        if match:
            title = match.group(1)
            date = match.group(2)
            films.append({"title": title, "date": date})

    print(f"✅ Page {page_num} : {len(films)} movies")
    return films


def get_genres_str(list_genres):
    return "+".join(list_genres)


async def scrap_watchlist(username, genres=[], batch_size=5):
    all_films = []
    genre_url = get_genres_str(genres) if genres else ""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        page_num = 1
        while True:
            pages = [await context.new_page() for _ in range(batch_size)]
            tasks = [
                scrap_watchlist_page(
                    pages[i],
                    username,
                    page_num + i,
                    genre_url
                    )
                for i in range(batch_size)
            ]

            results = await asyncio.gather(*tasks)

            for page in pages:
                await page.close()

            is_empty = True
            for films in results:
                if films:
                    all_films.extend(films)
                    is_empty = False

            if is_empty:
                print("🛑 No other movie to scrap.")
                break

            page_num += batch_size

        await browser.close()

    return all_films


async def scrap_watch_list(username, genres=[]):

    films = await scrap_watchlist(username, genres, 20)
    print(f"\n🎬 {len(films)} movie found for {username}")
    for film in films[:5]:
        print(f"  - {film['title']} ({film['date']})")
    return films
