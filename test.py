from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, re

URL = "https://thuvienphapluat.vn/van-ban/Bo-may-hanh-chinh/Hien-phap-nam-2013-215627.aspx"

# ---- Init Chrome với options che banner automation một chút
opts = webdriver.ChromeOptions()
opts.add_argument("--disable-blink-features=AutomationControlled")
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option("useAutomationExtension", False)
opts.add_argument("--incognito")

driver = webdriver.Chrome(options=opts)
driver.set_window_size(1440, 900)
driver.set_window_position(0, 0)
wait = WebDriverWait(driver, 20)

driver.get(URL)
driver.set_page_load_timeout(30)

# ---- Helper: đóng popups nếu có (bấm X, hoặc nút “Bỏ qua”, v.v.)
def dismiss_popups():
    # thử các nút thường thấy
    candidates = [
        "button.close", "a.close", "div.modal [data-dismiss='modal']",
        "button[aria-label='Close']", "a[aria-label='Close']",
        "button:contains('Bỏ qua')", "a:contains('Bỏ qua')"
    ]
    # Selenium không hỗ trợ :contains trong CSS -> thử XPath cho chữ
    xpaths = [
        "//button[contains(.,'Bỏ qua')]",
        "//a[contains(.,'Bỏ qua')]",
        "//button[contains(.,'Đóng') or contains(.,'Close')]",
        "//div[contains(@class,'modal')]//button[contains(@class,'close')]",
        "//div[contains(@class,'modal')]//a[contains(@class,'close')]",
        "//span[text()='X' or text()='×' or text()='x']/ancestor::*[self::button or self::a]"
    ]
    # click các nút có thể có
    for xp in xpaths:
        try:
            el = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xp)))
            driver.execute_script("arguments[0].click();", el)
            time.sleep(0.2)
        except:
            pass

dismiss_popups()
time.sleep(0.5)

# ---- Cách 1: cố tìm container nội dung (danh sách selector phỏng đoán hợp lý)
content_selectors = [
    "div#NoiDung", "div#NoiDungVanBan", "div.noi-dung", "div.noidung",
    "div.vbContent", "div.vbNOIDUNG", "div.content", "div.content-detail",
    "article", "div#content", "div#main-content"
]

def get_inner_text(el):
    return driver.execute_script("return arguments[0].innerText;", el) or ""

def scrape_by_selectors():
    for sel in content_selectors:
        try:
            # chờ có ít nhất 1 element match
            els = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, sel)))
            texts = []
            for e in els:
                t = get_inner_text(e).strip()
                if len(t) > 500:   # heuristics: nội dung dài thật sự
                    texts.append(t)
            if texts:
                return "\n\n".join(texts), f"selector:{sel}"
        except:
            continue
    return None, None

text, how = scrape_by_selectors()

# ---- Cách 2 (fallback): lấy toàn bộ body rồi cắt theo mốc
if not text:
    body = driver.execute_script("return document.body.innerText;")
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()

    # Mốc đầu: tiêu đề/nút nội dung
    start_marks = [
        "HIẾN PHÁP",           # phần tiêu đề lớn
        "LỜI NÓI ĐẦU",         # đoạn mở đầu văn bản
        "Nội dung",            # tab nội dung
        "NỘI DUNG"             # uppercase
    ]
    start_idx = -1
    for mk in start_marks:
        i = body.find(mk)
        if i != -1:
            start_idx = i
            break
    if start_idx == -1:
        start_idx = 0  # đen thì lấy từ đầu

    # Mốc cuối: banner “Bạn Chưa Đăng Nhập…”/hướng dẫn tiện ích
    end_marks = [
        "Bạn Chưa Đăng Nhập Thành Viên!",
        "Quý khách chưa đăng nhập",
        "Mời Bạn trải nghiệm những tiện ích CÓ PHÍ",
    ]
    end_idx = len(body)
    for mk in end_marks:
        j = body.find(mk)
        if j != -1:
            end_idx = min(end_idx, j)
    cut = body[start_idx:end_idx].strip()
    text, how = cut, "fallback:body-slice"

# ---- Làm sạch nhẹ
lines = [ln.strip() for ln in text.splitlines()]
lines = [ln for ln in lines if ln]           # bỏ dòng rỗng dư
final_text = "\n".join(lines)

print(f"EXTRACT_MODE = {how}")
print(final_text[:3000])   # in thử 3000 ký tự đầu

# Nếu muốn ghi ra file:
# with open("hien_phap_2013.txt", "w", encoding="utf-8") as f:
#     f.write(final_text)

# driver.quit()  # đóng khi xong