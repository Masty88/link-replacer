import asyncio
from pyppeteer import launch

import asyncio
from pyppeteer import launch

async def main():
    # Launch a new browser
    browser = await launch()
    page = await browser.newPage()

    # Go to the Drupal website
    await page.goto('https://next.sib.swiss/user/login')

    # Find the login form and enter your credentials
    await page.type('#edit-name', '')
    await page.type('#edit-pass', '')

    # Submit the form
    await page.click('#edit-submit')

    # Wait for the page to load
    await asyncio.sleep(5)  # adjust this value as needed

    # Check if you're logged in
    logout_button = await page.querySelector('.toolbar-bar')  # replace with the actual selector
    if logout_button:
        print("Logged in successfully.")
        # If logged in, navigate to the specified URL
        await page.goto('https://next.sib.swiss/groups/bioinformatics-proteogenomics')

        # Find the 'Edit' link and click it
        edit_link = await page.querySelector('a[data-drupal-link-system-path="node/493/edit"]')
        await edit_link.click()

        # Wait for the new page to load
        await asyncio.sleep(5)  # adjust this value as needed

        # Find the textbox, clear it, and type the new text
        text_box = await page.querySelector('.ck-editor__editable_inline')
        await page.evaluate('(element) => element.innerHTML = ""', text_box)
        await page.type('.ck-editor__editable_inline', 'Hello from py')

        # Click the 'Save' button
        save_button = await page.querySelector('input[data-drupal-selector="edit-submit"]')
        await save_button.click()

        print("Edited and saved successfully.")
    else:
        print("Failed to log in.")

    # Close the browser
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())


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
