import asyncio
import json
import tkinter as tk
from tkinter import ttk
import threading
import websockets

async def send_command(command, data, output_widget):
    try:
        async with websockets.connect("ws://localhost:8765") as websocket:
            message = json.dumps({"command": command, "data": data})
            await websocket.send(message)
            response = await websocket.recv()
            output_widget.insert(tk.END, response + '\n')
    except Exception as e:
        output_widget.insert(tk.END, f"Error: {e}\n")

def on_send(entry_cmd, entry_data, output_widget):
    command = entry_cmd.get()
    data = entry_data.get()
    threading.Thread(target=lambda: asyncio.run(send_command(command, data, output_widget))).start()

def build_gui():
    root = tk.Tk()
    root.title("MCP Lite Client")
    root.geometry("400x300")

    ttk.Label(root, text="Command:").pack()
    entry_cmd = ttk.Entry(root)
    entry_cmd.pack(fill='x')

    ttk.Label(root, text="Data:").pack()
    entry_data = ttk.Entry(root)
    entry_data.pack(fill='x')

    send_btn = ttk.Button(root, text="Send", command=lambda: on_send(entry_cmd, entry_data, output))
    send_btn.pack(pady=5)

    output = tk.Text(root, height=10)
    output.pack(fill='both', expand=True)

    root.mainloop()

if __name__ == "__main__":
    build_gui()
