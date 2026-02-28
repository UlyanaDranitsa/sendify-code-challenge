from contextlib import asynccontextmanager
from playwright.async_api import async_playwright

@asynccontextmanager
async def browser_manager():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            context = await browser.new_context()
            page = await context.new_page()
            yield page
        finally:
            await page.close()
            await context.close()
            await browser.close()