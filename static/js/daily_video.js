// daily_video.js
// Integração simples com Daily.co para sala_consulta.html
// https://docs.daily.co/docs/embed-daily-video-calls

const DAILY_DOMAIN = 'medlive.daily.co';
const DAILY_API_KEY = 'baae64f822d51b73b4465878605a7c0d13b930452989f5611a1dca7f1a09d0d4';

function createDailyRoom(callback) {
    fetch('https://api.daily.co/v1/rooms', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + DAILY_API_KEY
        },
        body: JSON.stringify({
            properties: {
                enable_chat: true,
                enable_screenshare: true,
                start_video_off: false,
                start_audio_off: false
            }
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data && data.url) {
            callback(data.url);
        } else {
            alert('Erro ao criar sala de vídeo.');
        }
    })
    .catch(() => alert('Erro de conexão com Daily.co'));
}

function joinDailyRoom(roomUrl) {
    const container = document.getElementById('daily-video-container');
    if (!container) return;
    container.innerHTML = `<iframe allow="camera; microphone; fullscreen; speaker; display-capture" src="${roomUrl}" style="width:100%;height:100%;border:0;border-radius:15px;"></iframe>`;
}

// Exemplo de uso:
// createDailyRoom(joinDailyRoom);
// Ou, se já tiver uma sala criada, use joinDailyRoom('https://medlive.daily.co/room-name');
