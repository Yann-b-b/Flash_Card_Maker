from src.utils.socket_server import ServerSocket
import src.utils.message as protocol
import asyncio
import subprocess

def get_summary_from_prompt(prompt_text):
    prompt = f"""Below is a description of something. Write a short summary of it for study purposes:

Text: "{prompt_text}"
Summary:"""
    result = subprocess.run(
        ["ollama", "run", "llama3.1:latest"],
        input=prompt,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

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
