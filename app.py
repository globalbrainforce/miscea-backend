""" APP """
import asyncio
import json
import logging
import websockets

# from events.auth import auth
from events.auth import auth

logging.basicConfig()

STATE = {"value": 0}

USERS = set()


# def state_event():
#     return json.dumps({"type": "state", **STATE})


# def users_event():
#     return json.dumps({"type": "users", "count": len(USERS)})


# async def notify_state():
#     if USERS:  # asyncio.wait doesn't accept an empty list
#         message = state_event()
#         await asyncio.wait([user.send(message) for user in USERS])


# async def notify_users():
#     if USERS:  # asyncio.wait doesn't accept an empty list
#         message = users_event()
#         await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    # await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    # await notify_users()

async def app(websocket, path):

    register(websocket)
    try:
        # await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            if path == 'auth':
                await auth.auth(USERS, data)
            # if data["action"] == "minus":
            #     STATE["value"] -= 1
            #     await notify_state()
            # elif data["action"] == "plus":
            #     STATE["value"] += 1
            #     await notify_state()
            # else:
            #     logging.error("unsupported event: {}", data)
    finally:
        unregister(websocket)


MAIN = websockets.serve(app, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(MAIN)
asyncio.get_event_loop().run_forever()
