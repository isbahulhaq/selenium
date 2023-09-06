import time
import warnings
import threading

from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
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


def start(name, user, wait_time):
    sync_print(f"{name} started!")
    driver = get_driver()
    driver.get(f'https://zoom.us/wc/join/' + meetingcode)
    driver.execute_script(
        "navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => { console.log(stream) }).catch(error => { console.log(error) });")
    time.sleep(3)
    inp = driver.find_element(By.ID, 'inputname')
    time.sleep(1)
    inp.send_keys(f"{user}")
    time.sleep(2)

    inp2 = driver.find_element(By.ID, 'inputpasscode')
    time.sleep(1)
    inp2.send_keys(passcode)
    btn3 = driver.find_element(By.ID, 'joinBtn')
    time.sleep(1)
    btn3.click()
    time.sleep(5)
    btn3 = driver.find_element(By.ID, 'preview-audio-control-button').click()
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/button'))).click()
    time.sleep(5)
    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '/html/body/div[14]/div/div/div/div[2]/div/div/button'))).click()
    except:
        pass

    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="voip-tab"]/div/button'))).click()
    sync_print(f"{name} sleep for {wait_time} seconds ...")
    time.sleep(wait_time)
    sync_print(f"{name} ended!")


def main():
    global meetingcode, passcode
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")
    number = int(input("Enter number of Users: "))
    sec = 5
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
    main()
