import asyncio
from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
import nest_asyncio
import random
import indian_names

nest_asyncio.apply()

# Flag to indicate whether the script is running
running = True

# Event to signal when the microphone button is pressed
microphone_pressed = asyncio.Event()

async def start(thread_name, wait_time, meetingcode, passcode):
    user = indian_names.get_full_name()
    print(f"{thread_name} started!")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream'])
        context = await browser.new_context(permissions=['microphone'])
        page = await context.new_page()
        await page.goto(f'https://zoom.us/wc/join/{meetingcode}', timeout=200000)

        try:
            await page.click('//button[@id="onetrust-accept-btn-handler"]', timeout=5000)
        except Exception as e:
            pass

        try:
            await page.click('//button[@id="wc_agree1"]', timeout=5000)
        except Exception as e:
            pass

        try:
            await page.wait_for_selector('input[type="text"]', timeout=200000)
            await page.fill('input[type="text"]', user)
            await page.fill('input[type="password"]', passcode)
            join_button = await page.wait_for_selector('button.preview-join-button', timeout=200000)
            await join_button.click()
        except Exception as e:
            pass

        try:
            query = '//button[text()="Join Audio by Computer"]'
            await asyncio.sleep(13)
            mic_button_locator = await page.wait_for_selector(query, timeout=350000)
            await asyncio.sleep(10)
            await mic_button_locator.evaluate_handle('node => node.click()')
            print(f"{thread_name} mic aayenge.")
            
            # Signal that the microphone button is pressed
            microphone_pressed.set()
        except Exception as e:
            print(f"{thread_name} mic nahe aayenge. ", e)

        print(f"{thread_name} sleep for {wait_time} seconds ...")
        while running and wait_time > 0:
            await asyncio.sleep(1)
            wait_time -= 1
        print(f"{thread_name} ended!")

        await browser.close()

async def main():
    global running
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")

    sec = 90
    wait_time = sec * 60

    tasks = []
    for i in range(number):
        # You can replace this with your own logic for generating a random name
        user = indian_names.get_full_name()
        task = start(f'[Thread{i}]', wait_time, meetingcode, passcode)
        tasks.append(task)

        # Wait for the microphone button to be pressed before starting the next thread
        await microphone_pressed.wait()
        microphone_pressed.clear()

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
