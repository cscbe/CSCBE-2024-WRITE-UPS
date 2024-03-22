import asyncio
import threading

from playwright.async_api import async_playwright


class Bot(threading.Thread):
    def __init__(self, uuid: str):
        threading.Thread.__init__(self)
        self.uuid = uuid
        threading.Thread(target=self.start).start()

    async def run_bot(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto("http://127.0.0.1:1337/login")
            await page.locator("xpath=//input[@id='username']").fill("admin")
            await page.locator("xpath=//input[@id='password']").fill(
                "icapxbxtgRF4umPqr5S4"
            )
            await page.locator("xpath=//button[@type='submit']").click()

            await page.goto("http://127.0.0.1:1337/notes/view?uuid=" + self.uuid)
            await page.wait_for_timeout(10000)

            await page.close()

    def start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run_bot())
        loop.close()
