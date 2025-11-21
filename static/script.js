const EMOJI_MAP = {
    'グー': '👊',
    'チョキ': '✌️',
    'パー': '🖐',
    '王様': '👑',
    '農民': '🧑‍🌾' 
};

let localWinCount = 0;
let localLoseCount = 0;

async function play(moveIndex) {
    try {
        const response = await fetch('/play', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ move: moveIndex })
        });
        const data = await response.json();

        let userMoveName = data.user_move_name;
        let aiMoveName = data.ai_move_name;

        const userEmoji = EMOJI_MAP[data.user_move_name] || '❓';
        const aiEmoji = EMOJI_MAP[data.ai_move_name] || '❓';

        document.getElementById('user-move').innerHTML = 
            `<div class="move-emoji">${userEmoji}</div><div class="move-text-sub">${userMoveName}</div>`;
        document.getElementById('ai-move').innerHTML = 
            `<div class="move-emoji">${aiEmoji}</div><div class="move-text-sub">${aiMoveName}</div>`;

        const resultText = data.result;
        const statusElem = document.getElementById('status');
        statusElem.innerText = resultText;

        document.getElementById('user-win-mark').classList.remove('show');
        document.getElementById('ai-win-mark').classList.remove('show');

        if (resultText.includes("あなたの勝ち")) {
            statusElem.style.color = "#e74c3c";
            document.getElementById('user-win-mark').classList.add('show');
            localWinCount++;
        } else if (resultText.includes("AIの勝ち") || resultText.includes("負け")) {
            statusElem.style.color = "#2980b9";
            document.getElementById('ai-win-mark').classList.add('show');
            localLoseCount++;
        } else {
            statusElem.style.color = "#333";
        }

        // 勝率計算 (あいこを除外)
        const validGames = localWinCount + localLoseCount;
        let winRate = "0.0";
        if (validGames > 0) {
            winRate = (localWinCount / validGames * 100).toFixed(1);
        }
        document.getElementById('win-rate').innerText = winRate;
        
        document.getElementById('game-count').innerText = data.games_count;

        const chartContainer = document.getElementById('chart-container');
        if (data.games_count <= 5) {
            const remaining = 6 - data.games_count;
            chartContainer.innerHTML = 
                `<div style="text-align:center; color:#aaa;">
                    <p style="font-size:3vh;">📉 データ収集中...</p>
                    <p>AIの予測開始まであと <b>${remaining}</b> 回</p>
                </div>`;
        } else if (data.chart_img) {
            chartContainer.innerHTML = 
                `<img src="data:image/png;base64,${data.chart_img}" class="chart-img" />`;
        }

    } catch (e) {
        console.error("通信エラー:", e);
    }
}

async function resetGame() {
    if(confirm("学習データと戦績をリセットしますか？")){
        await fetch('/reset', { method: 'POST' });
        localWinCount = 0;
        localLoseCount = 0;
        location.reload();
    }
}

function openModal(id) {
    document.getElementById(id).classList.add('active');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}

function closeModalOutside(event, id) {
    if (event.target.classList.contains('modal')) {
        closeModal(id);
    }
}

// --- 以下、追加ロジック ---

// 初回自動表示
window.onload = function() {
    openModal('rule-modal');
};

// 50回ごとの自動モーダル
function checkMilestone() {
    const count = parseInt(document.getElementById("game-count").textContent);
    if (count > 0 && count % 50 === 0) {
        document.getElementById("milestone-win-rate").textContent =
            document.getElementById("win-rate").textContent;
        document.getElementById("milestone-count").textContent = count;
        openModal("milestone-modal");
    }
}

// play() を修正して、最後に checkMilestone() を追加
const originalPlay = play;
play = function(x) {
    originalPlay(x);
    checkMilestone();
};