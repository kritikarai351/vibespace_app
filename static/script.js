document.addEventListener("DOMContentLoaded", () => {
    fetchStories();
    fetchChat();

    document.getElementById("sendBtn").addEventListener("click", sendMessage);
    document.getElementById("messageInput").addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    document.getElementById("addStoryBtn").addEventListener("click", addStory);
    document.getElementById("aiBtn").addEventListener("click", getAiSuggestion);
});

async function fetchChat() {
    const res = await fetch("/api/chat?user=Sam");
    const data = await res.json();
    const chatDisplay = document.getElementById("chatDisplay");
    chatDisplay.innerHTML = "";

    data.messages.forEach(msg => {
        const div = document.createElement("div");
        div.className = "msg-line";
        div.innerHTML = `<span class="msg-sender">${msg.sender}:</span> ${msg.text}`;
        chatDisplay.appendChild(div);
    });
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById("messageInput");
    const text = input.value.trim();
    if (!text) return;

    const res = await fetch("/api/chat/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sender: "Alex_Vibe", recipient: "Sam", text: text })
    });

    const data = await res.json();
    if (res.status === 403) {
        alert("⚠️ Content Warning: " + data.message);
    } else {
        input.value = "";
        fetchChat();
    }
}

async function fetchStories() {
    const res = await fetch("/api/stories");
    const data = await res.json();
    const container = document.getElementById("storiesContainer");
    container.innerHTML = "";

    data.stories.forEach(s => {
        const div = document.createElement("div");
        div.className = "story-card";
        div.innerHTML = `<div class="story-user">@${s.user} • ${s.time}</div><div>${s.text}</div>`;
        container.appendChild(div);
    });
}

async function addStory() {
    const text = prompt("Share a moment for your story:");
    if (!text) return;

    const res = await fetch("/api/stories", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user: "Alex_Vibe", text: text })
    });

    const data = await res.json();
    if (res.status === 403) {
        alert("⚠️ Content Warning: " + data.message);
    } else {
        fetchStories();
    }
}

async function getAiSuggestion() {
    const res = await fetch("/api/ai/outfit?user=Sam");
    const data = await res.json();
    document.getElementById("aiOutput").innerText = data.suggestion;
}