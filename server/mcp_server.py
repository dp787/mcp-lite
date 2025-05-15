import asyncio
import websockets
import json
from datetime import datetime

async def handle_command(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
            command = data.get("command", "").upper()
            payload = data.get("data", "")

            if command == "EVAL":
                try:
                    result = eval(payload, {"__builtins__": {}})
                    response = {"status": "success", "response": str(result)}
                except Exception as e:
                    response = {"status": "error", "response": f"Invalid expression: {e}"}

            elif command == "ECHO":
                response = {"status": "success", "response": payload}

            elif command == "TIME":
                response = {"status": "success", "response": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

            else:
                response = {"status": "error", "response": "Unknown command"}

        except json.JSONDecodeError:
            response = {"status": "error", "response": "Invalid JSON"}

        await websocket.send(json.dumps(response))

async def main():
    async with websockets.serve(handle_command, "localhost", 8765):
        print("✅ MCP Lite Server running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
