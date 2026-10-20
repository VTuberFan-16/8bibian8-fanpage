import json
import os
from datetime import datetime
import urllib.request

# ==========================================
# 설정 영역 (본인 정보로 수정하세요)
# ==========================================
SOOP_CLIENT_ID = "685201eae589154749b480fd8263603f484010013b6d4b1b0eeace434cc176e0"  # 발급받은 SOOP Client ID
STREAMER_ID = "8bibian8"            # 예: afreecatv

DATA_FILE = "data.json"

def fetch_soop_data():
    # 1. 기존 데이터 불러오기 (없으면 빈 구조 생성)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"followers": [], "clips": [], "notices": []}
    else:
        data = {"followers": [], "clips": [], "notices": []}

    today_str = datetime.now().strftime("%Y-%m-%d")

    # 2. SOOP API 호출 (방송국 정보 - 애청자 수 등)
    try:
        url = f"https://openapi.sooplive.co.kr/api/{STREAMER_ID}/station"
        req = urllib.request.Request(url, headers={"Client-id": SOOP_CLIENT_ID})
        
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            fan_cnt = int(res_data.get("station", {}).get("fan_cnt", 0))
            
            # 오늘 날짜 데이터가 이미 있으면 갱신, 없으면 추가
            existing_today = next((item for item in data["followers"] if item["date"] == today_str), None)
            if existing_today:
                existing_today["count"] = fan_cnt
            else:
                data["followers"].append({"date": today_str, "count": fan_cnt})
                
    except Exception as e:
        print(f"애청자 데이터 수집 실패: {e}")

    # 3. 최신 클립 및 공지사항 수집 API 연동 (SOOP API 명세에 맞춰 확장 가능)
    # ※ 클립이나 공지 API 엔드포인트를 통해 가져온 데이터를 아래와 같이 append 해줍니다.
    # 예시 구조:
    # data["clips"] = [ { "title": "클립제목", "url": "링크", "thumbnail": "이미지" }, ... ]

    # 4. 파일에 저장
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"[{today_str}] SOOP 데이터 수집 및 갱신 완료!")

if __name__ == "__main__":
    fetch_soop_data()
