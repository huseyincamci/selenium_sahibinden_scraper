from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl
from datetime import datetime

# Tarayıcıyı başlatma
options = Options()
options.add_argument('--headless')  # Headless mod
options.add_argument('--disable-gpu')  # GPU'yu devre dışı bırak
options.add_argument('--no-sandbox')  # Güvenlik önlemlerini devre dışı bırak
options.add_argument('start-maximized')  # Tarayıcıyı tam ekran aç
options.add_argument('disable-infobars')  # Bilgilendirme çubuklarını devre dışı bırak
options.add_argument('--disable-extensions')  # Uzantıları devre dışı bırak
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(60)  # 10 saniye bekle

try:
    # Sahibinden.com'u aç
    driver.get("https://www.sahibinden.com")
    print(driver.page_source)

    # Toplam emlak sayısını al
    emlak_sayisi = driver.find_element(By.XPATH, '//*[@id="container"]/div[3]/div/aside/div[1]/nav/ul[5]/li[1]/span').text
    print(f"Toplam emlak sayısı: {emlak_sayisi}")

    # Toplam konut sayısını al
    konut_sayisi = driver.find_element(By.XPATH, '//*[@id="container"]/div[3]/div/aside/div[1]/nav/ul[5]/li[1]/ul/li[1]/span').text
    print(f"Toplam konut sayısı: {konut_sayisi}")

    # Toplam arsa sayısını al
    arsa_sayisi = driver.find_element(By.XPATH, '//*[@id="container"]/div[3]/div/aside/div[1]/nav/ul[5]/li[1]/ul/li[3]/span').text
    print(f"Toplam arsa sayısı: {arsa_sayisi}")

    driver.quit();

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(60)  # 10 saniye bekle

    
    driver.get("https://www.sahibinden.com/kategori/emlak-konut")

    # Kiralık konut sayısını al
    kiralik_sayisi = driver.find_element(By.XPATH, '//*[@id="container"]/div[1]/div[1]/div/div[2]/ul/div/div/li[2]/span').text
    print(f"Kiralık konut sayısı: {kiralik_sayisi}")

    # Satılık konut sayısını al
    satilik_sayisi = driver.find_element(By.XPATH, '//*[@id="container"]/div[1]/div[1]/div/div[2]/ul/div/div/li[1]/span').text
    print(f"Satılık konut sayısı: {satilik_sayisi}")


    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Sahibinden Verileri"

    sheet['A1'] = "Emlak Sayısı"
    sheet['B1'] = "Konut Sayısı"
    sheet['C1'] = "Arsa Sayısı"
    sheet['D1'] = "Kiralık Konut Sayısı"
    sheet['E1'] = "Satılık Konut Sayısı"

    sheet['A2'] = emlak_sayisi.strip('()')
    sheet['B2'] = konut_sayisi.strip('()')
    sheet['C2'] = arsa_sayisi.strip('()')
    sheet['D2'] = kiralik_sayisi.strip('()')
    sheet['E2'] = satilik_sayisi.strip('()')

    # Şu anki tarihi ve saati alalım
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Excel dosyasını tarih ve saat bilgisiyle kaydedelim
    file_name = f"sahibinden_verileri_{current_time}.xlsx"
    wb.save(file_name)

finally:
    # Tarayıcıyı kapat
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Excel dosyasını tarih ve saat bilgisiyle kaydedelim
    screenshot_file_name = f"screenshot_{current_time}.png"
    driver.save_screenshot(screenshot_file_name)
    driver.quit()
