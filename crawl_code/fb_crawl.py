from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# 设置 Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 无头模式（不打开浏览器）
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

# 启动 WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 目标 Facebook 个人主页
lis = []
url_fb = ['https://www.facebook.com/profile.php?id=781098557',
          'https://www.facebook.com/profile.php?id=778927507',
          'https://www.facebook.com/profile.php?id=744428005',
          'https://www.facebook.com/profile.php?id=720134429',
          'https://www.facebook.com/profile.php?id=682300259',
          'https://www.facebook.com/profile.php?id=61555925010294',
          'https://www.facebook.com/profile.php?id=602741350',
          'https://www.facebook.com/profile.php?id=557406333',
          'https://www.facebook.com/profile.php?id=555026244',
          ]
for url in url_fb:
    # 访问网页
    driver.get(url)
    # time.sleep(5)  # 等待页面加载

    # 获取 HTML 源码
    html_source = driver.page_source
    print(html_source[:1000])
    lis.append(html_source)
print(li[:200] for li in lis )

# 关闭浏览器
driver.quit()
