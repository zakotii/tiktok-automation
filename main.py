import asyncio
import logging
import os
import random
import sys

from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError
)
from dotenv import load_dotenv

# ─── Завантажуємо .env ───────────────────────────────────────────────────────────
load_dotenv()

TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")
TIKTOK_PASSWORD = os.getenv("TIKTOK_PASSWORD")
SEARCH_QUERY    = os.getenv("SEARCH_QUERY", "dance")
SKIP_PERCENT    = int(os.getenv("SKIP_PERCENT", 12))
MAX_VIDEOS      = int(os.getenv("MAX_VIDEOS", 20))
SEARCH_WAIT     = 20000   # ms на завантаження результатів пошуку
VIDEO_WAIT      = 15000   # ms на підвантаження сторінки відео

# ─── Налаштування логування ─────────────────────────────────────────────────────
log_fmt = "%(asctime)s | %(levelname)s | %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_fmt,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("tiktok_automation.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("tiktok_bot")


async def main():
    logger.info("🚀 Початок автоматизації TikTok")
    logger.info(f"🔎 Пошуковий запит: {SEARCH_QUERY}, skip% = {SKIP_PERCENT}, max videos = {MAX_VIDEOS}")

    async with async_playwright() as p:
        # Відкриваємо браузер у режимі з GUI, щоб вручну залогінитись
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="./user_data",
            headless=False,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()

        # ─── КРОК 1: АВТОРИЗАЦІЯ ──────────────────────────────────────────────
        await page.goto("https://www.tiktok.com/login", timeout=SEARCH_WAIT, wait_until="networkidle")
        logger.info("🔐 Будь ласка, увійдіть в свій TikTok акаунт у відкритому вікні.")
        # чекаємо, поки користувач нажме Enter у консолі
        await asyncio.get_event_loop().run_in_executor(None, input, "Після входу натисніть ENTER тут…")
        logger.info("✅ Авторизацію завершено")

        # ─── КРОК 2: ПОШУК ───────────────────────────────────────────────────
        # Переходимо на сторінку пошуку
        search_url = f"https://www.tiktok.com/search?q={SEARCH_QUERY}"
        logger.info(f"🌐 Відкриваємо {search_url}")
        try:
            await page.goto(search_url, timeout=SEARCH_WAIT, wait_until="networkidle")
            # очікуємо принаймні один результат
            await page.wait_for_selector("a[href*='/video/']", timeout=SEARCH_WAIT)
            logger.info("✅ Результати пошуку завантажено")
        except PlaywrightTimeoutError:
            logger.error("⚠️ Не вдалося завантажити результати пошуку")
            await browser.close()
            return

        # ─── КРОК 3: ЗБІР ПОСИЛАНЬ ────────────────────────────────────────────────
        # трохи скролимо, щоб підвантажити більше відео
        for _ in range(3):
            await page.mouse.wheel(0, 1000)
            await asyncio.sleep(1)

        anchors = await page.query_selector_all("a[href*='/video/']")
        links = []
        seen = set()
        for a in anchors:
            href = await a.get_attribute("href") or ""
            if href.startswith("https://") and href not in seen:
                seen.add(href)
                links.append(href)
            if len(links) >= MAX_VIDEOS:
                break

        if not links:
            logger.warning("⚠️ Не знайдено жодної посилання на відео")
            await browser.close()
            return

        logger.info(f"📄 Зібрано посилань: {len(links)}")

        # ─── КРОК 4: ПРОГЛЯД / ПРОПУСК ───────────────────────────────────────────
        total = len(links)
        watched = skipped = 0

        for idx, video_url in enumerate(links, start=1):
            tag = f"{idx}/{total}"
            if random.randint(1, 100) <= SKIP_PERCENT:
                skipped += 1
                logger.info(f"{tag} | {video_url} | ПРОПУЩЕНО")
                continue

            watched += 1
            logger.info(f"{tag} | {video_url} | ПРОСМОТР…")
            video_page = await browser.new_page()
            try:
                await video_page.goto(video_url, timeout=VIDEO_WAIT, wait_until="networkidle")
                # чекаємо появи тега <video>
                await video_page.wait_for_selector("video", timeout=VIDEO_WAIT)
                # імітуємо перегляд (людська затримка 15–45s)
                watch_time = random.randint(15, 45)
                await asyncio.sleep(watch_time)
                logger.info(f"{tag} | {video_url} | ПРОСМОТРЕНО за {watch_time}s")
            except PlaywrightTimeoutError:
                logger.error(f"{tag} | {video_url} | ТАЙМАУТ ЗАВАНТАЖЕННЯ ВІДЕО")
            except Exception as e:
                logger.error(f"{tag} | {video_url} | ПОМИЛКА ПРИ ПРОСМОТРІ: {e}")
            finally:
                await video_page.close()

        # ─── ФІНАЛЬНА СТАТИСТИКА ───────────────────────────────────────────────
        logger.info("=== СТАТИСТИКА ===")
        logger.info(f"Всього оброблено: {total}")
        logger.info(f"Переглянуто повністю: {watched}")
        logger.info(f"Пропущено: {skipped}")
        logger.info(f"Процент пропусків: {skipped/total*100:.1f}%")

        await browser.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("🚫 Скрипт зупинено користувачем")
