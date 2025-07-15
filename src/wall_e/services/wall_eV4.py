import asyncio
import re
from playwright.async_api import async_playwright
from multiprocessing import Pool, cpu_count


def start(username):
    return f"https://letterboxd.com/{username}/watchlist"


def end(page_num):
    return f"/by/rating/page/{page_num}/"


def scrap_single_page_wrapper(args):
    username, page_num, genre_url = args
    return asyncio.run(scrap_single_page(username, page_num, genre_url))


async def scrap_single_page(username, page_num, genre_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        url = start(username) + end(page_num)
        if genre_url:
            url = start(username) + f"/genre/{genre_url}" + end(page_num)

        await page.goto(url)
        try:
            await page.wait_for_selector(".poster-container", timeout=4000)
        except Exception:
            await browser.close()
            return []

        titles = await page.locator(".frame-title").all_text_contents()
        await browser.close()

        films = []
        for value in titles:
            match = re.match(r"^(.*)\s\((\d{4})\)$", value)
            if match:
                films.append({"title": match.group(1), "date": match.group(2)})
        return films


async def get_total_pages(username, genre_url=""):
    url = f"https://letterboxd.com/{username}/watchlist/by/rating/"
    if genre_url:
        url = start(username) + f"/genre/{genre_url}/by/rating/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await (await browser.new_context()).new_page()
        await page.goto(url)
        try:
            await page.wait_for_selector(".paginate-page", timeout=4000)
        except Exception:
            await browser.close()
            return 0
        pages = await page.locator(".paginate-page").all_text_contents()
        await browser.close()
        page_numbers = [int(p) for p in pages if p.isdigit()]
        return max(page_numbers) if page_numbers else 1


def scrap_watch_list(username, genres=[], workers=None):
    genre_url = "+".join(genres)
    total_pages = asyncio.run(get_total_pages(username, genre_url))
    args = [(username, i, genre_url) for i in range(1, total_pages + 1)]

    with Pool(processes=workers or cpu_count()) as pool:
        results = pool.map(scrap_single_page_wrapper, args)

    all_films = []
    for films in results:
        all_films.extend(films)
    return all_films
