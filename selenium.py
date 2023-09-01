import time
import warnings
import threading

from faker import Faker
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

warnings.filterwarnings('ignore')
fake = Faker('en_IN')
MUTEX = threading.Lock()


def sync_print(text):
    with MUTEX:
        print(text)


def get_driver():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_experimental_option("detach", True)
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1
    })
    driver = webdriver.Chrome("chromedriver", options=options)
    return driver


def driver_wait(driver, locator, by, secs=10, condition=ec.element_to_be_clickable):
    wait = WebDriverWait(driver=driver, timeout=secs)
    element = wait.until(condition((by, locator)))
    return element


def start(name, user, wait_time, meetingcode, passcode):
    print(f"{name} started!")

    # Set up Selenium Chrome WebDriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--use-fake-device-for-media-stream')
    chrome_options.add_argument('--use-fake-ui-for-media-stream')
    chrome_options.add_argument('--headless')  # To run headless (without a visible browser window)
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(f'https://zoom.us/wc/join/{meetingcode}')

        # Accept cookies
        try:
            accept_cookies_button = driver.find_element_by_id("onetrust-accept-btn-handler")
            accept_cookies_button.click()
        except Exception as e:
            pass

        # Agree to terms
        try:
            agree_button = driver.find_element_by_id("wc_agree1")
            agree_button.click()
        except Exception as e:
            pass

        # Enter user details
        try:
            user_input = driver.find_element_by_css_selector('input[type="text"]')
            user_input.send_keys(user)
            passcode_input = driver.find_element_by_css_selector('input[type="password"]')
            passcode_input.send_keys(passcode)
            join_button = driver.find_element_by_css_selector('button.preview-join-button')
            join_button.click()
        except Exception as e:
            pass

        # Join audio by computer
        try:
            join_audio_button = driver.find_element_by_xpath('//button[text()="Join Audio by Computer"]')
            join_audio_button.click()
            print(f"{name} mic aayenge.")
        except Exception as e:
            print(f"{name} mic nahe aayenge.")

        print(f"{name} sleep for {wait_time} seconds ...")
        while wait_time > 0:
            time.sleep(1)
            wait_time -= 1
        print(f"{name} ended!")

    finally:
        driver.quit()


def main():
    wait_time = sec * 60
    workers = []
    for i in range(number):
        try:
            user = fake.name()
        except IndexError:
            break
        wk = threading.Thread(target=start, args=(
            f'[Thread{i}]', user, wait_time))
        workers.append(wk)
    for wk in workers:
        wk.start()
    for wk in workers:
        wk.join()


if __name__ == '__main__':
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")
    sec = 5
    main()
