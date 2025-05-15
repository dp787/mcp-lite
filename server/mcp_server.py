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

            elif command == "REVERSE":
                response = {"status": "success", "response": payload[::-1]}

            elif command == "UPPERCASE":
                response = {"status": "success", "response": payload.upper()}

            elif command == "LOWERCASE":
                response = {"status": "success", "response": payload.lower()}

            elif command == "LENGTH":
                response = {"status": "success", "response": str(len(payload))}

            elif command == "REPEAT":
                try:
                    text, count = payload.split("|")
                    repeated = text * int(count)
                    response = {"status": "success", "response": repeated}
                except:
                    response = {"status": "error", "response": "Use format 'word|number'"}

            else:
                response = {"status": "error", "response": "Unknown command"}

        except json.JSONDecodeError:
            response = {"status": "error", "response": "Invalid JSON"}

        await websocket.send(json.dumps(response))
