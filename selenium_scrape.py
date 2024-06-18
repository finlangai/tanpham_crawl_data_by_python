from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import os
import requests
from selenium.common.exceptions import NoSuchElementException

def fetch_pdf_links(url):
    # Khởi tạo trình duyệt (bạn cần driver phù hợp với trình duyệt của bạn)
    driver = webdriver.Chrome()

    # Mở URL
    driver.get(url)
    
    # In URL hiện tại để kiểm tra
    print('URL hiện tại:', driver.current_url)

    # Chờ đợi cho đến khi tất cả các liên kết PDF xuất hiện, tối đa 10 giây
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href$='.pdf']"))
    )
    
    # Phân tích cú pháp HTML với BeautifulSoup ngay từ mã nguồn trang web
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Tìm và in ra các liên kết PDF
    pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))
    
    # Kiểm tra và in ra số lượng liên kết PDF tìm thấy
    print('Số lượng liên kết PDF tìm thấy:', len(pdf_links))
    
    for link in pdf_links:
        print(link['href'])

        # Tạo danh sách các URL PDF
    pdf_urls = [link['href'] for link in pdf_links]
    print('danh sách PDF đã tạo:', len(pdf_urls))

    # Đóng trình duyệt
    # driver.quit()

    # Trả về danh sách các URL PDF
    return pdf_urls

def download_pdfs(pdf_links, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for link in pdf_links:
        # Lấy tên file từ URL
        filename = link.split('/')[-1]
        response = requests.get(link)
        
        # Kiểm tra response trước khi tải xuống
        if response.status_code == 200:
            filepath = os.path.join(download_folder, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f'File đã được tải xuống: {filepath}')
        else:
            print(f'Lỗi khi tải xuống file: {link}')


if __name__ == "__main__":
    url = 'https://s.cafef.vn/cong-bo-thong-tin.chn'
    download_folder = 'pdf_downloads'  # Thay đổi theo đường dẫn thư mục mong muốn của bạn
    
    # Lấy các link PDF
    pdf_links = fetch_pdf_links(url)
    print('danh sách PDF đã trả về:', len(pdf_links))

    # Tải xuống các file PDF và lưu vào thư mục
    download_pdfs(pdf_links, download_folder)