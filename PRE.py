import time
import warnings
from selenium import webdriver
from selenium_stealth import stealth
import indian_names
from joblib import Parallel, delayed
import requests

warnings.filterwarnings('ignore')
MUTEX = None

def sync_print(text):
    global MUTEX
    with MUTEX:
        print(text)

def get_driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option('w3c', True)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.binary_location = '/usr/bin/brave-browser'
    options.add_argument(f'--marionette-port=2828')  # Specify the port number here
    
    # Apply selenium-stealth to mimic a real browser
    driver = webdriver.Chrome(options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    
    return driver

def start(name, proxy, user, wait_time):
    sync_print(f"{name} started!")
    driver = get_driver()  # Create a new driver instance for each job
    driver.get(f'http://app.zoom.us/wc/join/{meetingcode}')
    time.sleep(10)
    
    # Simulate a GET request using requests (replace with your actual URL)
    url = f'http://app.zoom.us/wc/join/{meetingcode}'
    response = requests.get(url)

    time.sleep(1)
    inp = driver.find_element('xpath', '//input[@type="text"]')
    inp.send_keys(f"{user}")
    time.sleep(5)

    inp2 = driver.find_element('xpath', '//input[@type="password"]')
    inp2.send_keys(passcode)

    # Click the "Join" button using JavaScript
    join_button = driver.find_element('xpath', '//button[contains(@class,"preview-join-button")]')
    driver.execute_script("arguments[0].click();", join_button)

    sync_print(f"{name} sleep for {wait_time} seconds ...")
    time.sleep(wait_time)
    sync_print(f"{name} ended!")
    driver.quit()  # Quit the driver after the job has completed

def main():
    global MUTEX
    wait_time = sec * 60
    workers = []

    for i in range(number):
        try:
            proxy = proxylist[i]
        except Exception:
            proxy = None
        try:
            user = indian_names.get_full_name()
        except IndexError:
            break
        wk = delayed(start)(f'[Thread{i}]', proxy, user, wait_time)
        workers.append(wk)

    # Initialize MUTEX before Parallel execution
    with joblib.parallel_backend("threading", n_jobs=-1):
        global MUTEX
        MUTEX = joblib.parallel.Parallel()._effective_joblib_backend(MUTEX)

    Parallel(n_jobs=-1)(workers)

if __name__ == '__main__':
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")
    sec = 60
    try:
        main()
    except:
        pass
