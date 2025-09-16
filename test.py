from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Creates an options object.
options = webdriver.ChromeOptions()

options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Opens the browser in the incognito mode.
options.add_argument("--incognito")

driver = webdriver.Chrome(options=options)

# Sets windows size.
driver.set_window_size(1440, 900)

# Sets windows position.
driver.set_window_position(0, 0)

# Opens the browser.
driver.get("https://thuvienphapluat.vn/van-ban/Bo-may-hanh-chinh/Hien-phap-nam-2013-215627.aspx")

# Sets timeout threshold.
driver.set_page_load_timeout(30)

# Sets up driver (Chrome)
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

def get_full_text(driver, selectors, wait_strategy="presence"):
    """
    selectors: list[str] CSS selector của div cần hút
    wait_strategy: "presence" (nhanh) hoặc "visible" (an toàn hơn)
    return: dict {selector: [list các đoạn text theo từng element]}
    """
    strat = EC.presence_of_all_elements_located if wait_strategy=="presence" else EC.visibility_of_all_elements_located
    out = {}

    for sel in selectors:
        elems = wait.until(strat((By.CSS_SELECTOR, sel)))
        texts = []
        for e in elems:
            # Dùng JS lấy innerText cho sạch, giữ xuống dòng tự nhiên hơn .text
            t = driver.execute_script("return arguments[0].innerText;", e)
            # Làm sạch khoảng trắng thừa
            if t: 
                t = "\n".join(line.strip() for line in t.splitlines() if line.strip())
            texts.append(t)
        out[sel] = texts
    return out

