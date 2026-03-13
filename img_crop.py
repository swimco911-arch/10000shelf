from PIL import Image, ImageDraw
import glob
import os

# 1. 폴더 및 파일 설정
input_path = "gemini_stories/story_*.png"
output_folder = "cropped_results"
corner_radius = 40  # 둥글기 정도 (숫자가 클수록 더 많이 깎임)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 2. 자르기 좌표 (사용자가 수정하신 좌표 유지)
crop_area = (345, 160, 855, 928)

# 3. 반복문을 통한 일괄 처리
file_list = glob.glob(input_path)
print(f"총 {len(file_list)}개의 파일을 찾았습니다.")

for file_path in file_list:
    # 이미지 열기 및 자르기
    img = Image.open(file_path).convert("RGBA") # 투명도 지원 모드로 변경
    cropped_img = img.crop(crop_area)
    
    # --- 둥근 모서리 마스크 생성 시작 ---
    width, height = cropped_img.size
    # 모든 곳이 투명(0)인 새 마스크 이미지 생성
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    # 1. 왼쪽 영역 (직각형으로 채우기)
    draw.rectangle((0, 0, width - corner_radius, height), fill=255)
    
    # 2. 오른쪽 상단 둥근 모서리
    draw.pieslice((width - 2*corner_radius, 0, width, 2*corner_radius), 270, 360, fill=255)
    
    # 3. 오른쪽 하단 둥근 모서리
    draw.pieslice((width - 2*corner_radius, height - 2*corner_radius, width, height), 0, 90, fill=255)
    
    # 4. 둥근 부분 사이 빈 공간 채우기
    draw.rectangle((width - corner_radius, corner_radius, width, height - corner_radius), fill=255)
    
    # 이미지에 마스크 적용
    cropped_img.putalpha(mask)
    # --- 둥근 모서리 마스크 생성 끝 ---
    
    # 파일명만 추출해서 저장 (투명도를 위해 반드시 .png로 저장)
    file_name = os.path.basename(file_path)
    cropped_img.save(os.path.join(output_folder, f"crop_{file_name}"))
    
    print(f"{file_name} 자르기 및 곡면 처리 완료!")

print("--- 모든 작업이 완료되었습니다 ---")