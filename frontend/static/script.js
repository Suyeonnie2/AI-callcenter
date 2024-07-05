const API_URL = 'http://localhost:5000';
let isConnected = false;
let recognition = null;
let isListening = false;
let utterance = null;

function connectAgent() {
    fetch(`${API_URL}/start_conversation`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                isConnected = true;
                appendMessage(data.message, 'ai');
                playAudio(data.audio_file);
                updateUIState();
            }
        })
        .catch(error => console.error('Error:', error));
}

function disconnectAgent() {
    isConnected = false;
    appendMessage("상담이 종료되었습니다. 다시 연결하려면 '상담원 연결' 버튼을 눌러주세요.", 'system');
    updateUIState();
}

function sendMessage() {
    if (!isConnected) return;

    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (message) {
        appendMessage(message, 'user');
        userInput.value = '';

        fetch(`${API_URL}/get_response`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({user_input: message}),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                appendMessage(data.message, 'ai');
                playAudio(data.audio_file);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function playAudio(audioFile) {
    if (audioFile && audioFile !== 'undefined') {
        const audio = new Audio(`${API_URL}/audio/${audioFile}`);
        audio.play().catch(error => console.error('Error playing audio:', error));
    }
}

function appendMessage(message, sender) {
    const conversationDiv = document.getElementById('conversation');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender + '-message');
    messageDiv.textContent = message;
    conversationDiv.appendChild(messageDiv);
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
}

function toggleVoiceInput() {
    if (isListening) {
        stopVoiceInput();
    } else {
        startVoiceInput();
    }
}

function startVoiceInput() {
    if (!isConnected) return;

    isListening = true;
    updateVoiceInputUI();

    fetch(`${API_URL}/get_voice_response`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            appendMessage(data.user_input, 'user');
            appendMessage(data.message, 'ai');
            playAudio(data.audio_file);
        }
    })
    .catch(error => console.error('Error:', error))
    .finally(() => {
        isListening = false;
        updateVoiceInputUI();
    });
}

function stopVoiceInput() {
    isListening = false;
    updateVoiceInputUI();
}

function playAudio(audioFile) {
    const audio = new Audio(`${API_URL}/audio/${audioFile}`);
    audio.onplay = () => {
        isPlaying = true;
        updateSpeakResponseUI();
    };
    audio.onended = () => {
        isPlaying = false;
        updateSpeakResponseUI();
    };
    audio.play();
}

function toggleSpeakResponse() {
    if (isPlaying) {
        pauseSpeakResponse();
    } else {
        resumeSpeakResponse();
    }
}

function pauseSpeakResponse() {
    if (utterance) {
        window.speechSynthesis.pause();
        isPlaying = false;
        updateSpeakResponseUI();
    }
}

function resumeSpeakResponse() {
    if (utterance) {
        window.speechSynthesis.resume();
        isPlaying = true;
        updateSpeakResponseUI();
    }
}


function updateUIState() {
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const connectButton = document.getElementById('connectButton');
    const disconnectButton = document.getElementById('disconnectButton');
    const voiceToggleButton = document.getElementById('voiceToggleButton');
    const speakToggleButton = document.getElementById('speakToggleButton');

    userInput.disabled = !isConnected;
    sendButton.disabled = !isConnected;
    connectButton.disabled = isConnected;
    disconnectButton.disabled = !isConnected;
    voiceToggleButton.disabled = !isConnected;
    speakToggleButton.disabled = !isConnected;
}

function updateVoiceInputUI() {
    const voiceToggleButton = document.getElementById('voiceToggleButton');
    voiceToggleButton.innerHTML = isListening ? '<i class="fas fa-stop"></i>' : '<i class="fas fa-microphone"></i>';
}

function updateSpeakResponseUI() {
    const speakToggleButton = document.getElementById('speakToggleButton');
    speakToggleButton.innerHTML = isPlaying ? '<i class="fas fa-pause"></i>' : '<i class="fas fa-play"></i>';
}

document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

updateUIState();