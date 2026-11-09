from client import WebClient
import asyncio
import json
import os 

CURRENT_DIR = os.path.dirname(__file__)

async def main():
    with open(os.path.join(CURRENT_DIR, 'credentials.json')) as j:
        creds = json.load(j)

    client = WebClient(creds)
   
    await client.start()
    await asyncio.sleep(4)
    
    await client.start_login()
    await client.wait_for_2fa()
    await client.explore_profile()
    await client.export()

    await client.stop()
    





asyncio.run(main())