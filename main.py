from client import WebClient
import asyncio
import json
import os 

CURRENT_DIR = os.path.dirname(__file__)

async def main():
    CONFIG_PATH = os.path.join(CURRENT_DIR, 'credentials.json')

    if not os.path.exists(CONFIG_PATH):
        print('No config found, generating config.json at root ...')
        print('Enter your credentials and restart the program')

        with open(CONFIG_PATH, 'w') as f:
            json.dump({"username": None, "password": None, "target": None}, f)
        
        os._exit(0)

    with open(CONFIG_PATH) as j:
        creds = json.load(j)

    print('\n1. Gather followers for a target')
    print('2. Use existing followers data')

    while True:
        choice = input('\nChoose an option : ')

        try:
            way = int(choice)
            assert way in (1,2)
            break

        except Exception:
            print('Wrong choice , try again')


    client = WebClient(creds)
   
    await client.start()


    if way == 1:
        await gather_followers()
    if way == 2:
        await follow(client)

    await client.stop()

    
async def follow(webclient):
    await webclient.start_login()
    await webclient.wait_for_2fa() 

    datasets = os.listdir(os.path.join(CURRENT_DIR, 'exports'))
    print(datasets)
    print('\n')
    for idx, f in enumerate(datasets):
        print(f'{idx}     {f}')

    while True:
        choice = input('Choose a dataset : ')
        try:
            index = int(choice)
            assert index < len(datasets)
            break
        except:
            print('Index out of range , try again')

    with open(os.path.join(CURRENT_DIR, 'exports', datasets[index])) as f:
        data = json.load(f)

    await webclient.follow_users(data, limit=1)



async def gather_followers(webclient):


    await asyncio.sleep(4)

    await webclient.start_login()
    await webclient.wait_for_2fa()
    await webclient.explore_profile()
    webclient.export()

asyncio.run(main())