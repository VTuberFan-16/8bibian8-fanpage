import requests
import json
import os

streamer_id = '8bibian8'
# SOOP Open API 및 Catch/Clip 정보를 가져오는 요청
url = f"https://vod.sooplive.co.kr/script/subscribe/get_catch_list.php?bjid={streamer_id}&page=1"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

clips = []

try:
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        # 데이터 수집
        raw_clips = data.get('data', [])
        for item in raw_clips[:12]: # 최신 12개 가져오기
            clip_no = item.get('title_no') or item.get('file_no')
            clips.append({
                'id': str(clip_no),
                'title': item.get('title', '제목 없음'),
                'thumb': item.get('thumb', 'https://placehold.co/400x225'),
                'date': item.get('reg_date', '')[:10].replace('-', '.'),
                'views': str(item.get('read_cnt', 0)),
                'duration': item.get('display_time', '00:00'),
                'clipUrl': f"https://vod.sooplive.co.kr/player/{clip_no}",
                'embedUrl': f"https://vod.sooplive.co.kr/embed/{clip_no}"
            })
except Exception as e:
    print(f"Error fetching clips: {e}")

# 만약 API 실패 시 기본 빈 파일 생성 방지
if not clips:
    print("No clips fetched or error occurred.")

# clips.json 저장
with open('clips.json', 'w', encoding='utf-8') as f:
    json.dump(clips, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(clips)} clips to clips.json")
