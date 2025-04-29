from src.utils.socket_server import ServerSocket
import src.utils.message as protocol
import asyncio
import subprocess


class Server:
    def __init__(self):
        self.server = ServerSocket(_print=True)
        self.current_process = None

    def stop_current_generation(self):
        if self.current_process and self.current_process.poll() is None:
            self.current_process.terminate()

    def get_summary_from_prompt(self, prompt_text):
        self.stop_current_generation()
        prompt = f"""
        ALWAYS INCLUDE 'front:' and 'back:'
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
"{prompt_text['message']}"
ALWAYS INCLUDE 'front:' and 'back:'
This is the flashcard I would make:
"""
        print("[INFO] Starting subprocess to run llama3.1:latest with the input prompt.")
        print(f"[DEBUG] Prompt being sent:\n{prompt}")
        self.current_process = subprocess.Popen(
            ["ollama", "run", "llama3.1:latest"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
        output, _ = self.current_process.communicate(input=prompt)
        print(f"[DEBUG] Raw model output:\n{output}")
        flashcards = []
        lines = output.strip().splitlines()
        current_card = {}
        for line in lines:
            if line.lower().startswith("front:"):
                if current_card:
                    flashcards.append(current_card)
                    current_card = {}
                current_card["front"] = line.replace("front:", "").strip()
            elif line.lower().startswith("back:"):
                current_card["back"] = line.replace("back:", "").strip()
        if current_card:
            flashcards.append(current_card)
        return flashcards

    async def run(self):
        await self.server.start()
        self.server.on(
            ServerSocket.EVENTS_TYPES.on_message,
            "ping",
            lambda client, message: asyncio.create_task(self.handle_ping(client, message))
        )
        while self.server.running:
            await asyncio.sleep(2)

    async def handle_ping(self, client, message):
        print("[INFO] Received ping message from client.")
        result = self.get_summary_from_prompt(message.content)
        await self.server.send(
            client,
            protocol.Message("summary", result).to_json()
        )

if __name__ == "__main__":
    Server = Server()
    asyncio.run(Server.run())
