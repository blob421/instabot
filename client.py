
from playwright.async_api import async_playwright
import asyncio
import os 
import json

CURRENT_DIR = os.path.dirname(__file__)

class WebClient():

    def __init__(self, creds):
        self.creds = None
        self.client = None
        self.main_url = 'https://www.instagram.com/'
        self.driver = None
        self.page = None
        self.creds:dict = creds
        self.target = None
        self.followers = set()
        self.previous_len = 0
        
        

    async def start(self):
        self.target = self.creds.get("target") or input('Enter a target username : ')
        self.client = await async_playwright().start()
        self.driver = await self.client.chromium.launch(headless=False)

        self.page = await self.driver.new_page()
        await self.page.goto(self.main_url)
       


    async def stop(self):
        await self.driver.close()
        await self.client.stop()

    async def start_login(self):
        try:
            email_field = self.page.locator('input[name="email"]') 
            await email_field.type(self.creds.get('username'))

            password_field = self.page.locator('input[name="pass"]')
            await password_field.type(self.creds.get('password'))
        

            login_btn = self.page.locator('div[aria-label="Log In"]')
            await login_btn.click()
      

        except Exception as e:
            print(e)

    async def wait_for_2fa(self):
        print('Waiting for 2fa')
        while True:
   
            url = self.page.url
       
            if url != 'https://www.instagram.com/':
                break

            await asyncio.sleep(4)

        while True:
            url = self.page.url
          
           
            if url == 'https://www.instagram.com/':
               return

            elif url == 'https://www.instagram.com/accounts/onetap/':
                return
            
            await asyncio.sleep(5)

    async def explore_profile(self):

        await self.page.goto(self.main_url + self.target)
        followers_link = self.page.locator('a[role="link"][href="#"]')

        await followers_link.nth(5).click()

        scroll_div = self.page.locator('div[style="--x-paddingInline: 48px; --x-paddingBottom: 28px;"]')

        await self.get_followers(scroll_div)


    async def get_followers(self, scrollable_element):
        height = await scrollable_element.evaluate('(el) => el.clientHeight')

        while True:

            await scrollable_element.evaluate(f'(el) => el.scrollTop += {height}')

            followers = self.page.locator('span[class="_ap3a _aaco _aacw _aacx _aad7 _aade"]')
            data = await followers.all()

            for f in data:
                self.followers.add(await f.inner_text())

            if self.previous_len and self.previous_len == len(self.followers):
                print('Finished getting all followers from target...')
                return 
            
            self.previous_len = len(self.followers)
            height += height
            await asyncio.sleep(2)
    
            
    def export(self):
        with open(os.path.join(CURRENT_DIR, 'exports', f'{self.target}.json'), 'w') as f:

            json.dump(list(self.followers), f, indent=4)
        print(len(self.followers))


