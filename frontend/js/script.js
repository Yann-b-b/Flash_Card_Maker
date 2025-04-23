const ws = new WebSocket("ws://localhost:5384");

ws.onopen = () => log("Connected to server");
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const flashcards = data?.data?.message;
  if (Array.isArray(flashcards)) {
    let currentIndex = 0;
    const container = document.getElementById("flashcardContainer");

    const renderCard = () => {
      container.innerHTML = "";
      const { front, back } = flashcards[currentIndex];
      const card = document.createElement("div");
      card.className = "flashcard";
      card.innerHTML = `
        <div class="flashcard-inner">
          <div class="front">${front}</div>
          <div class="back">${back}</div>
        </div>
      `;
      container.appendChild(card);
    };

    renderCard();

    document.getElementById("prevBtn").onclick = () => {
      if (currentIndex > 0) {
        currentIndex--;
        renderCard();
      }
    };

    document.getElementById("nextBtn").onclick = () => {
      if (currentIndex < flashcards.length - 1) {
        currentIndex++;
        renderCard();
      }
    };
  } else {
    log("Server: " + event.data);
  }
};
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
  const container = document.getElementById("flashcardContainer");
  if (container) {
    container.addEventListener("click", (e) => {
      const card = e.target.closest(".flashcard");
      if (card) card.classList.toggle("flipped");
    });
  }
});