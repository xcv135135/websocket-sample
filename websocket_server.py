#! /usr/bin/python3

import asyncio
import json
import logging
import websockets

logging.basicConfig()
WEBSOCKET_SERVER_IP = "0.0.0.0"
WEBSOCKET_SERVER_PORT = 5678


class WebsocketServer:
    def __init__(self):
        self.STATE = {"value": 0}
        self.USERS = set()
        self.start_server = websockets.serve(self.counter, WEBSOCKET_SERVER_IP, WEBSOCKET_SERVER_PORT)

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()

    async def counter(self, websocket, path):
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            await websocket.send(self.state_event())
            async for message in websocket:
                data = json.loads(message)
                if data["action"] == "minus":
                    self.STATE["value"] -= 1
                    await self.notify_state()
                elif data["action"] == "plus":
                    self.STATE["value"] += 1
                    await self.notify_state()
                else:
                    logging.error("unsupported event: {}", data)
        finally:
            await self.unregister(websocket)

    def state_event(self):
        return json.dumps({"type": "state", **self.STATE})

    def users_event(self):
        return json.dumps({"type": "users", "count": len(self.USERS)})

    async def notify_state(self):
        if self.USERS:  # asyncio.wait doesn't accept an empty list
            message = self.state_event()
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def notify_users(self):
        if self.USERS:  # asyncio.wait doesn't accept an empty list
            message = self.users_event()
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def register(self, websocket):
        self.USERS.add(websocket)
        await self.notify_users()

    async def unregister(self, websocket):
        self.USERS.remove(websocket)
        await self.notify_users()


def websocket_server_start():
    websocket_server = WebsocketServer()
    websocket_server.start()


if __name__ == "__main__":
    websocket_server_start()
