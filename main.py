from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl
import os
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


    # Excel dosyasının adı
    file_name = "sahibinden_verileri.xlsx"
    folder_path = os.path.dirname(os.path.abspath(__file__))  # Çalışan programın bulunduğu klasör
    full_path = os.path.join(folder_path, file_name)  # Tam dosya yolu

    # Excel dosyası mevcut mu kontrol et
    if os.path.exists(full_path):
        # Dosya varsa aç
        wb = openpyxl.load_workbook(full_path)
        sheet = wb.active
    else:
        # Dosya yoksa oluştur
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "Sahibinden Verileri"

        # Başlıkları ekle
        sheet['A1'] = "Tarih"
        sheet['B1'] = "Emlak Sayısı"
        sheet['C1'] = "Konut Sayısı"
        sheet['D1'] = "Arsa Sayısı"
        sheet['E1'] = "Kiralık Konut Sayısı"
        sheet['F1'] = "Satılık Konut Sayısı"

        # Başlık genişliklerini ayarla
        sheet.column_dimensions['A'].width = 20
        sheet.column_dimensions['B'].width = 15
        sheet.column_dimensions['C'].width = 15
        sheet.column_dimensions['D'].width = 15
        sheet.column_dimensions['E'].width = 20
        sheet.column_dimensions['F'].width = 20

    # Son satırın altına ekle
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Tarih ve saat

    new_row = [
        current_time,
        emlak_sayisi.strip('()'),
        konut_sayisi.strip('()'),
        arsa_sayisi.strip('()'),
        kiralik_sayisi.strip('()'),
        satilik_sayisi.strip('()')
    ]

    sheet.append(new_row)

    # Dosyayı kaydet
    wb.save(full_path)
    print(f"Veriler {full_path} dosyasına eklendi.")

except Exception as e:
    # Hata olduğunda ekran görüntüsü al
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"Test failed, screenshot saved as {filename}")
    print(f"Error: {e}")

finally:
    # Tarayıcıyı kapat
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_file_name = f"screenshot_{current_time}.png"
    folder_path = os.path.dirname(os.path.abspath(__file__))  # Çalışan programın bulunduğu klasör
    full_path = os.path.join(folder_path, screenshot_file_name)  # Tam dosya yolu
    #driver.save_screenshot(full_path)
    driver.quit()
