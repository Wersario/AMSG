const socket = new WebSocket(
    `ws://${window.location.host}/ws/chat/${CHAT_ID}/`
);

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    const node = document.createElement('div');
    node.innerText = `${data.sender}: ${data.content}`;

    document.getElementById('messages').appendChild(node);
}

function sendMessage() {
    const input = document.getElementById('message-input');

    socket.send(JSON.stringify({
        content: input.value,
    }));

    input.value = '';
}