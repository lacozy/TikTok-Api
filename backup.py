from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, LikeEvent, FollowEvent, GiftEvent, JoinEvent, ShareEvent, MoreShareEvent

import os
import sys
import psutil
import asyncio
import threading
import time

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

filename = ""
process_id = ""
streamer_name=""
game_over = False

# Instantiate the client with the user's username
client: TikTokLiveClient = TikTokLiveClient(unique_id="caseohgames")


@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)


async def on_comment(event: CommentEvent):
    print(f"{event.user.nickname} -> {event.comment}")

async def on_like(event: LikeEvent):
    print("LIKE EVENT" + event.user.nickname)
    write_to_file("LIKE: " + event.user.nickname.encode('utf-8','ignore').decode("utf-8"))

async def on_follow(event: FollowEvent):
    print("FOLLOW EVENT " + event.user.nickname)

async def on_gift(event: GiftEvent):
    print(event.gift, end='\n')
    print("GIFT EVENT" + f"{event.user.nickname} -> {event.gift.info.description}")

async def on_join(event: JoinEvent):
    print("JOIN EVENT" + event.user.nickname)
    write_to_file("JOIN: " + event.user.nickname.encode('utf-8','ignore').decode("utf-8"))

async def on_share(event: ShareEvent):
    print("SHARE EVENT" + event.user.nickname)

async def more_share(event: ShareEvent):
    print("MORE SHARE EVENT" + event.user.nickname)

# Define handling an event via a "callback"
client.add_listener("comment", on_comment)
client.add_listener("like", on_like)
client.add_listener("follow", on_follow)
client.add_listener("gift", on_gift)
client.add_listener("join", on_join)
client.add_listener("share", on_share)
client.add_listener("more_share", more_share)

def write_to_file(input):
    with open(filename, "a", encoding='utf-8') as f:
        f.write(input + "\n")


def is_process_running(pid):
    try:
        process = psutil.Process(pid)
        return process.is_running()
    except psutil.NoSuchProcess:
        return False

def check_process_continuously(pid, interval=1):
    while True:
        if is_process_running(pid) is False:
        #     print(f"Process with PID {pid} is still running.")
        # else:
            print(f"Process with PID {pid} is not running.")
            os._exit(0)
        time.sleep(interval)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    print("""
          Games for Stream! TikTok Client
          Please do not exit this window while the game is running.
          Enjoy!
          """)
    
    if len(sys.argv)>1:
        print(sys.argv[1])
        filename=sys.argv[1]
        process_id=sys.argv[2]
    process_check_thread = threading.Thread(target=check_process_continuously, args=(int(process_id),))
    process_check_thread.daemon = True
    process_check_thread.start()
    client.run()

