from pypresence import Presence
import time
import os

pass
"""
# PRESENCE -------------------------------------------------------------------------------------------------------------
cid = os.environ["CLIENT_ID"]
RPC = Presence(cid, pipe=0)
RPC.connect()

# TO SHOW CPU USAGE-----------------------------------------------------------------------------------------------------
while True:  # The presence will stay on as long as the program is running
    cpu_per = round(psutil.cpu_percent(),1) # Get CPU Usage
    mem = psutil.virtual_memory()
    mem_per = round(psutil.virtual_memory().percent,1)
    print(RPC.update(details="RAM: "+str(mem_per)+"%", state="CPU: "+str(cpu_per)+"%"))  # Set the presence
    time.sleep(15) # Can only update rich presence every 15 seconds
"""
# RICH PRESENCE IMAGES -------------------------------------------------------------------------------------------------
"""
You need to upload your image(s) here:
https://discordapp.com/developers/applications/<APP ID>/rich-presence/assets
"""
"""
# Make sure you are using the same name that you used when uploading the image
RPC.update(large_image="big-image", large_text="Large Text Here!",
            small_image="small-image", small_text="Small Text Here!")

while 1:
    time.sleep(15) #Can only update presence every 15 seconds
"""
# ----------------------------------------------------------------------------------------------------------------------
"""
# Setting `Playing ` status
await bot.change_presence(activity=discord.Game(name="a game"))

# Setting `Streaming ` status
await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))

# Setting `Listening ` status
await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))

# Setting `Watching ` status
await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))

# ----------------------------------------------------------------------------------------------------------------------
while True:
    print(RPC.update(state="Lookie Lookie", details="A test of pypresence!"))
    time.sleep(15)
"""