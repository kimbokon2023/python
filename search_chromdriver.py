from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# ChromeDriverManager를 통해 ChromeDriver를 자동으로 설치하고, Service 객체로 경로를 설정합니다.
# service = Service(ChromeDriverManager().install())

# 네 ㅎㅎ service = Service() 이렇게 manager를 지워보시겠어요? 크롬이 업데이트 되면서 ChromeDriverManager를 사용 시 발생하는 문제라고 하네요

service = Service()
driver = webdriver.Chrome(service=service)

# 이제 Selenium 스크립트를 작성하고 사용할 수 있습니다.
driver.get("https://www.google.com")
print(driver.title)

# 브라우저를 닫습니다.
driver.quit()
