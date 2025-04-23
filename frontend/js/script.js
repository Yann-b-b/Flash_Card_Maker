const ws = new WebSocket("ws://localhost:5384");

ws.onopen = () => log("Connected to server");
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const flashcards = data?.data?.message;
  console.log("Received flashcards:", flashcards);
  if (Array.isArray(flashcards)) {
    let currentIndex = 0;
    const container = document.getElementById("flashcardContainer");
    console.log("flashcardContainer found:", container);

    const renderCard = () => {
      container.innerHTML = "";
      const { front, back } = flashcards[currentIndex];
      console.log("Rendering:", front, back);
      const card = document.createElement("div");
      card.className = "flashcard";
      card.setAttribute("tabindex", "0");
      card.innerHTML = `
        <div class="flashcard-inner">
          <div class="front">${front}</div>
          <div class="back">${back}</div>
        </div>
      `;
      container.appendChild(card);
      console.log("Card injected into DOM");
    };

    renderCard();
    document.getElementById("loading").style.display = "none";
    document.getElementById("overlay").style.height = "0%";
    document.getElementById("overlay").style.opacity = "0";

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
  document.getElementById("loading").innerHTML = `
    <span>⏳</span><span> </span><span>G</span><span>e</span><span>n</span><span>e</span><span>r</span><span>a</span><span>t</span><span>i</span><span>n</span><span>g</span><span> </span><span>.</span><span>.</span><span>.</span>
  `;
  document.getElementById("loading").style.display = "block";
  document.getElementById("overlay").style.height = "200%";
  document.getElementById("overlay").style.opacity = "1";
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
    // Accessibility: keyboard toggle for flipping
    container.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        const card = e.target.closest(".flashcard");
        if (card) {
          card.classList.toggle("flipped");
          e.preventDefault();
        }
      }
    });
  }
});