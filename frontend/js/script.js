const ws = new WebSocket("ws://localhost:5384");

ws.onopen = () => log("Connected to server");
ws.onmessage = (event) => log("Server: " + event.data);
ws.onclose = () => log("Disconnected");

function sendMessage() {
  const input = document.getElementById("inputBox").value;
  const msg = JSON.stringify({
    type: "ping",
    data: { message: input },
  });
  ws.send(msg);
}

function log(msg) {
  document.getElementById("log").textContent += msg + "\n";
}

document.addEventListener("DOMContentLoaded", () => {
  const card = document.querySelector(".flashcard");
  if (card) {
    card.addEventListener("click", () => {
      card.classList.toggle("flipped");
    });
  }
});