import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 1. 브라우저 설정
options = Options()
# options.add_argument("--headless") # 창을 보고 싶지 않으면 주석 해제
options.add_argument("--window-size=600,800") # 스토리북 보기에 적당한 크기

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 저장 폴더
save_dir = 'gemini_stories'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 2. 파일 읽기
with open("links.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f.readlines() if "gemini.google.com/share" in line]

# 3. 캡쳐 실행
for idx, url in enumerate(urls):
    try:
        print(f"[{idx+1}/{len(urls)}] 진행 중: {url}")
        driver.get(url)
        time.sleep(4) # 제미나이 페이지는 로딩이 좀 걸리므로 4~5초 권장

        # [중요] 제미나이 공유 페이지의 메인 컨텐츠 영역만 찾아서 캡쳐
        # 페이지 구조에 따라 'article' 또는 특정 'div'를 타겟팅합니다.
        try:
            # 공유된 대화 내용이 담긴 메인 요소 선택
            content = driver.find_element(By.CSS_SELECTOR, "main") 
            filename = f"{save_dir}/story_{idx+1}.png"
            content.screenshot(filename) # 전체 화면이 아닌 '메인 영역'만 크롭 저장
            print(f"✅ 저장 완료: {filename}")
        except:
            # 영역 찾기 실패 시 전체 화면이라도 저장
            driver.save_screenshot(f"{save_dir}/story_{idx+1}_full.png")
            print(f"⚠️ 영역 선택 실패, 전체 화면 저장")

    except Exception as e:
        print(f"❌ 에러 발생 ({url}): {e}")

driver.quit()
print("\n✨ 모든 스토리북 캡쳐가 끝났습니다!")
