let followerChart = null;
let rawData = { followers: [], clips: [], notices: [] };
let currentMode = 'daily';

// 1. data.json 파일 불러오기
async function loadData() {
    try {
        const response = await fetch('data.json');
        if (response.ok) {
            rawData = await response.json();
        }
    } catch (e) {
        console.log("아직 수집된 data.json이 없거나 로드 중 오류 발생:", e);
    }
    
    renderChart(currentMode);
    renderNotices();
    renderClips();
}

// 2. 차트 그리기 및 일별/주별 변환
function renderChart(mode) {
    currentMode = mode;
    const ctx = document.getElementById('followerChart').getContext('2d');

    // 버튼 활성화 디자인 변경
    document.getElementById('btn-daily').className = mode === 'daily' ? 'active-btn' : '';
    document.getElementById('btn-weekly').className = mode === 'weekly' ? 'active-btn' : '';

    let labels = [];
    let dataCounts = [];

    if (mode === 'daily') {
        // 최근 10일 데이터 추출
        const recent = rawData.followers.slice(-10);
        labels = recent.map(item => item.date);
        dataCounts = recent.map(item => item.count);
    } else {
        // 주별 보기 (간단하게 7일 단위 혹은 전체 데이터 중 10개 추출)
        const recent = rawData.followers.slice(-70); // 최근 70일 치 가져와서
        let weeklyMap = {};
        recent.forEach(item => {
            // 주차별(혹은 간격별) 대략 묶기 로직 예시
            weeklyMap[item.date] = item.count;
        });
        labels = Object.keys(weeklyMap);
        dataCounts = Object.values(weeklyMap);
    }

    // 데이터가 아예 없을 때의 방어 코드
    if (labels.length === 0) {
        labels = ['데이터 수집 대기 중'];
        dataCounts = [0];
    }

    if (followerChart) {
        followerChart.destroy();
    }

    followerChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: mode === 'daily' ? '일별 애청자 수 (최근 10일)' : '주별 애청자 수',
                data: dataCounts,
                borderColor: '#00c7ae',
                backgroundColor: 'rgba(0, 199, 174, 0.1)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: false } }
        }
    });
}

function switchView(mode) {
    renderChart(mode);
}

// 3. 공지사항 렌더링
function renderNotices() {
    const noticeBox = document.getElementById('notice-box');
    if (rawData.notices && rawData.notices.length > 0) {
        noticeBox.innerHTML = rawData.notices.map(n => `<p>📢 <a href="${n.url}" target="_blank">${n.title}</a></p>`).join('');
    } else {
        noticeBox.innerHTML = "<p>등록된 공지사항이 없습니다.</p>";
    }
}

// 4. 최신 클립 렌더링
function renderClips() {
    const clipsContainer = document.getElementById('clips-container');
    if (rawData.clips && rawData.clips.length > 0) {
        clipsContainer.innerHTML = rawData.clips.map(c => `
            <div style="background:#f9f9f9; padding:10px; border-radius:8px;">
                <a href="${c.url}" target="_blank"><img src="${c.thumbnail}" style="width:100%; border-radius:6px;"></a>
                <p style="font-size:14px; font-weight:bold; margin:8px 0 0 0;">${c.title}</p>
            </div>
        `).join('');
    } else {
        clipsContainer.innerHTML = "<p>수집된 최신 클립이 없습니다.</p>";
    }
}

// 5. 방명록 기능 (로컬 저장소 활용)
function addPost() {
    const writer = document.getElementById('writer').value;
    const content = document.getElementById('content').value;

    if (!writer || !content) {
        alert('닉네임과 내용을 입력해주세요!');
        return;
    }

    const postList = document.getElementById('post-list');
    const li = document.createElement('li');
    li.innerHTML = `<strong>${writer}</strong>: ${content}`;
    postList.prepend(li);

    document.getElementById('writer').value = '';
    document.getElementById('content').value = '';
}

// 페이지 로드 시 실행
window.onload = function() {
    loadData();
};
