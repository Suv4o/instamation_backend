import os
import asyncio
import requests
from pyppeteer import launch


async def main(file_url, description, user_name, password, temp_image_path):
    browser = await launch()
    page = await browser.newPage()
    await page.goto("https://www.instagram.com")
    await page.waitFor(3000)
    # Fill in the username
    await page.click("input[name='username']")
    await page.type("input[name='username']", user_name)
    # Fill in the password
    await page.click("input[name='password']")
    await page.type("input[name='password']", password)
    # Click on the login button
    await page.click("button[type='submit']")
    await page.waitForNavigation()
    # Click on the new button adding new post
    await page.click("svg[aria-label='New post']")
    await page.waitFor(2000)
    # Handle the file upload
    file_input = await page.querySelector('input[class="_ac69"][type=file]')
    file_path = os.path.abspath(f"{temp_image_path}/image-to-upload.png")
    response = requests.get(file_url)
    with open(file_path, "wb") as f:
        f.write(response.content)
    await file_input.uploadFile(file_path)
    await page.waitFor(10000)
    # Click on the next button
    await page.click("div[class='_ac7b _ac7d']")
    # Click on the next button
    await page.waitFor(1000)
    await page.click("div[class='_ac7b _ac7d']")
    # Write a caption
    await page.waitFor(1000)
    await page.click("div[class='x6s0dn4 x78zum5 x1n2onr6 xh8yej3']")
    await page.type("div[class='x6s0dn4 x78zum5 x1n2onr6 xh8yej3']", description)
    # Click on the share button
    await page.waitFor(1000)
    await page.click("div[class='_ac7b _ac7d']")
    await page.waitFor(10000)
    await browser.close()


def upload_image(file_url, description, user_name, password, temp_image_path):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(file_url, description, user_name, password, temp_image_path))
