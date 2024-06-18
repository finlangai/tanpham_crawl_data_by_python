from selenium_scrape import fetch_pdf_links, download_pdfs
url = 'https://s.cafef.vn/cong-bo-thong-tin.chn'
download_folder = 'pdf_downloads'
# Gọi hàm fetch_pdf_links với URL cần cào dữ liệu
pdf_links = fetch_pdf_links('https://s.cafef.vn/cong-bo-thong-tin.chn')

print('danh sách PDF đã trả về:', len(pdf_links))

# Tải xuống các file PDF và lưu vào thư mục
download_pdfs(pdf_links, download_folder)