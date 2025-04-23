from src.utils.socket_server import ServerSocket
import src.utils.message as protocol
import asyncio
import subprocess

def get_summary_from_prompt(prompt_text):
    prompt = f"""
This is an example text:
The human circulatory system is responsible for transporting blood, nutrients, oxygen, carbon dioxide, and hormones throughout the body. It consists of the heart, blood, and blood vessels. The heart acts as a pump to move the blood, while arteries carry blood away from the heart and veins bring it back. Capillaries are small blood vessels where the exchange of substances occurs between blood and tissues. The circulatory system helps regulate body temperature and pH levels and is vital for homeostasis.

This is the flashcard I would make:
front: What is the main function of the circulatory system?
back: To transport blood, nutrients, oxygen, carbon dioxide, and hormones throughout the body

front: What are the main components of the circulatory system?
back: The heart, blood, and blood vessels

front: What is the function of the heart in the circulatory system?
back: It acts as a pump to move the blood

front: What type of blood vessel carries blood away from the heart?
back: Arteries

front: What type of blood vessel brings blood back to the heart?
back: Veins

front: Where does the exchange of substances between blood and tissues occur?
back: In the capillaries

front: Name two functions of the circulatory system besides transport.
back: Regulating body temperature and pH levels

front: Why is the circulatory system vital for homeostasis?
back: Because it maintains stable internal conditions by transporting essential substances and regulating temperature and pH

This is an example text:
"{prompt_text}"

This is the flashcard I would make:
"""
    result = subprocess.run(
        ["ollama", "run", "llama3.1:latest"],
        input=prompt,
        capture_output=True,
        text=True
    )
    output = result.stdout.strip()
    flashcards = []
    lines = output.splitlines()
    current_card = {}

    for line in lines:
        if line.startswith("front:"):
            if current_card:
                flashcards.append(current_card)
                current_card = {}
            current_card["front"] = line.replace("front:", "").strip()
        elif line.startswith("back:"):
            current_card["back"] = line.replace("back:", "").strip()

    if current_card:
        flashcards.append(current_card)

    return flashcards

class Server:
    def __init__(self):
        self.server = ServerSocket(_print=True)

    async def run(self):
        await self.server.start()

        self.server.on(
            ServerSocket.EVENTS_TYPES.on_message,
            "ping",
            lambda client, message: asyncio.create_task(
                self.server.send(
                    client,
                    protocol.Message(
                        "summary",
                        get_summary_from_prompt(message.content)
                    ).to_json()
                )
            ) if message.type == "ping" else None
        )

        while self.server.running:
            await asyncio.sleep(2)

if __name__ == "__main__":
    Server = Server()
    asyncio.run(Server.run())
