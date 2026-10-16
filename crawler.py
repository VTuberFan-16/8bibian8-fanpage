import requests
import json
import os

streamer_id = '8bibian8'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# ----------------------------------------------------
# 1. 클립 데이터 가져오기
# ----------------------------------------------------
clip_url = f"https://vod.sooplive.co.kr/script/subscribe/get_catch_list.php?bjid={streamer_id}&page=1"
clips = []

try:
    res = requests.get(clip_url, headers=headers, timeout=10)
    if res.status_code == 200:
        data = res.json()
        raw_clips = data.get('data', [])
        for item in raw_clips[:12]:
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

# clips.json 저장
with open('clips.json', 'w', encoding='utf-8') as f:
    json.dump(clips, f, ensure_ascii=False, indent=2)


# ----------------------------------------------------
# 2. 방송국 최신 게시글 데이터 가져오기
# ----------------------------------------------------
post_url = f"https://bjapi.sooplive.co.kr/api/{streamer_id}/titlelog?page=1"
posts = []

try:
    res = requests.get(post_url, headers=headers, timeout=10)
    if res.status_code == 200:
        data = res.json()
        raw_posts = data.get('data', [])
        for item in raw_posts[:10]: # 최신 글 10개 수집
            title_no = item.get('title_no')
            posts.append({
                'id': str(title_no),
                'title': item.get('title_name', '제목 없음'),
                'date': item.get('reg_date', '')[:10].replace('-', '.'),
                'views': str(item.get('read_cnt', 0)),
                'comments': str(item.get('comment_cnt', 0)),
                'postUrl': f"https://v.sooplive.co.kr/{streamer_id}/{title_no}" # 게시글 원본 링크
            })
except Exception as e:
    print(f"Error fetching posts: {e}")

# posts.json 저장
with open('posts.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print("Successfully updated clips.json and posts.json")
