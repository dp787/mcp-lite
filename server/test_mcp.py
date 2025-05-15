import websocket
import json
import time

def test_mcp_server():
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:8765")

    test_commands = [
        {"command": "ECHO", "args": "Hello World"},
        {"command": "TIME"},
        {"command": "EVAL", "args": "2 + 3 * 4"},
        {"command": "EVAL", "args": "10 / 2 + (3 * 4)"},
        {"command": "EVAL", "args": "100 - 25"},
        {"command": "EVAL", "args": "'Hello ' + 'there!'"},
        {"command": "EXIT"},
        {"command": "EVAL", "args": "2 + "},
        {"command": "EVAL", "args": "import os"},
        {"command": "UNKNOWN"},
        {}
    ]

    for cmd in test_commands:
        message = json.dumps(cmd)
        print(f"\nSending: {message}")
        ws.send(message)
        try:
            response = ws.recv()
            print(f"Received: {response}")
        except Exception as e:
            print(f"Error receiving response: {e}")

        time.sleep(0.5)  # short delay between commands

    ws.close()

if __name__ == "__main__":
    test_mcp_server()
