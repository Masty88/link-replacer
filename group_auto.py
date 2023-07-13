import asyncio
from pyppeteer import launch

# async def main():
#     # Launch a new browser
#     browser = await launch()
#     page = await browser.newPage()
#
#     # # Go to the website that you want to copy from
#     # await page.goto('http://www.example.com')
#     #
#     # # Find the element that contains the text you want to copy
#     # element = await page.querySelector('#element_id')
#     #
#     # # Copy the text
#     # text = await page.evaluate('(element) => element.textContent', element)
#
#     # Go to the Drupal website
#     await page.goto('https://next.sib.swiss/user/login')
#
#     # Find the login form and enter your credentials
#     await page.type('#edit-name', 'emastaglia')
#     await page.type('#edit-pass', '!EC&6zrLdW%x*5')
#
#     # Submit the form
#     await page.click('#edit-submit')
#
#     page_content = await page.content()
#     print(page_content)
#
#     # Wait for the page to load
#     await asyncio.sleep(5)  # adjust this value as needed
#
#     # Check if you're logged in
#     logout_button = await page.querySelector('.toolbar-bar')  # replace with the actual selector
#     if logout_button:
#         print("Logged in successfully.")
#     else:
#         print("Failed to log in.")
#
#
#     # Close the browser
#     await browser.close()
#
# asyncio.get_event_loop().run_until_complete(main())

import scrapy


class LoginSpider(scrapy.Spider):
    name = 'login_spider'
    start_urls = ['']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'name': '', 'pass': ''},
            callback=self.after_login
        )

    def after_login(self, response):
        # verifica il login riuscito
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return

        # continua scraping con autenticazione
        else:
            self.logger.error("Login successful")
            # adesso puoi accedere alle pagine protette
