import os
import time
import glob
from PIL import Image, ImageDraw
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- 1. 설정값 ---
output_folder = "cropped_results"
corner_radius = 40
# 사용자가 지정한 자르기 좌표 (좌, 상, 우, 하)
crop_area = (375, 160, 935, 925)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 브라우저 설정
options = Options()
options.add_argument("--window-size=660,800") # 캡처 품질을 위해 창 크기를 넉넉히 설정

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- 2. 파일 읽기 ---
try:
    with open("links_all.txt", "r", encoding="utf-8") as f:
        # "share" 키워드가 포함된 모든 라인을 가져오되, 공백을 제거합니다.
        urls = [line.strip() for line in f.readlines() if "share" in line and ("gemini.google.com" in line or "g.co" in line)]
        
    if not urls:
        print("⚠ 유효한 공유 링크를 찾지 못했습니다.")
except FileNotFoundError:
    print("❌ links_all.txt 파일을 찾을 수 없습니다.")
    urls = []

# --- 3. 캡처 및 즉시 가공 ---
for idx, url in enumerate(urls):
    try:
        print(f"[{idx+1}/{len(urls)}] 처리 중: {url}")
        driver.get(url)
        time.sleep(8) # 페이지 로딩 대기

        # 메인 영역 찾기
        content = driver.find_element(By.CSS_SELECTOR, "main")
        
        # 1. 메모리에 임시 저장 (스크린샷) 후 바로 열기
        temp_img_path = "temp_capture.png"
        content.screenshot(temp_img_path)
        img = Image.open(temp_img_path).convert("RGBA")

        # 2. 지정된 좌표로 자르기
        cropped_img = img.crop(crop_area)
        width, height = cropped_img.size

        # 3. 오른쪽 곡면 마스크 생성
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        # 왼쪽 사각형 영역
        draw.rectangle((0, 0, width - corner_radius, height), fill=255)
        # 오른쪽 상단 곡면
        draw.pieslice((width - 2*corner_radius, 0, width, 2*corner_radius), 270, 360, fill=255)
        # 오른쪽 하단 곡면
        draw.pieslice((width - 2*corner_radius, height - 2*corner_radius, width, height), 0, 90, fill=255)
        # 곡면 사이 채우기
        draw.rectangle((width - corner_radius, corner_radius, width, height - corner_radius), fill=255)

        # 4. 마스크 적용 및 최종 저장
        cropped_img.putalpha(mask)
        final_filename = f"story_{idx+1}.png"
        cropped_img.save(os.path.join(output_folder, final_filename))

        # 임시 파일 삭제
        os.remove(temp_img_path)
        print(f"✅ 완료: {final_filename}")

    except Exception as e:
        print(f"❌ 에러 발생 ({url}): {e}")

driver.quit()
print(f"\n✨ 모든 작업이 끝났습니다! 결과물은 '{output_folder}' 폴더를 확인하세요.")