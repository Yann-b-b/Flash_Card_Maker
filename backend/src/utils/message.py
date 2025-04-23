import json
import warnings

class Message:
    """
        Protocol message class to communicate between the server and the client.
    """

    def __init__(self, type, message):
        self.type = type
        self.content = message

    def __repr__(self):
        message = str(self.content)[:min(50, len(str(self.content)))]
        return f"[Message<{self.type}>]: {message}"
    
    def to_json(self):
          return json.dumps({"type": self.type, "data": {"message": self.content}})
    
    @staticmethod
    def from_json(json_str):
        """
            Dynamically create a message from a json string.
            Can return a different protocole type, but always a protocol class.
        """

        data = json.loads(json_str)

        if "type" not in data or "data" not in data:
            # warning in yellow
            warnings.warn(f"\033[93mInvalid message: {data}\033[0m", stacklevel=2)
            return Error("Invalid message")

        if data["type"] not in TYPES_MAP or TYPES_MAP[data["type"]] == Message:
            return Message(data["type"], message=data["data"])
        return TYPES_MAP[data["type"]].from_json(json_str)
    
class Error(Message):
    def __init__(self, message):
        super().__init__("error", message)

    def to_json(self):
        return json.dumps({
            "type": self.type,
            "data": {
                "message": self.content
            }
        })

    @staticmethod
    def from_json(data):
        return Error(data["data"]["message"])

TYPES_MAP = {
    "error": Error,
    "message": Message,
}