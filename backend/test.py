from atproto import Client, client_utils

client = Client()
client.login("enjop.bsky.social", "enjopsec")

with open('./D0002050015_00000_V_000.mp4', 'rb') as f:
    vid_data = f.read()

client.send_video(text='Post with video from Python', video=vid_data, video_alt='Text version of the video (ALT)')