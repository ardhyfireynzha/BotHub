"""
Carbon Scraper Plugin for Userbot. //text in creative way.
usage: .carbon //as a reply to any text message

Thanks to @NeoMatrix90 for vars

Type : .carbon1

"""
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from telethon import events
from urllib.parse import quote_plus
from urllib.error import HTTPError
import asyncio
import os
from uniborg.util import admin_cmd
from platform import python_version, uname
from sample_config import Config


CARBONLANG = "auto"
CARBON_BIN = Config.CARBON_BIN
CARBON_DRIVER = Config.CARBON_DRIVER


@borg.on(admin_cmd(pattern="crblang ?(.*)"))
async def setlang(prog):
    global CARBONLANG
    CARBONLANG = prog.pattern_match.group(1)
    await prog.edit(f"Language for carbon.now.sh set to {CARBONLANG}")


@borg.on(admin_cmd(pattern="carbon1 ?(.*)"))
async def carbon_api(e):
    """ A Wrapper for carbon.now.sh """
    await e.edit("`Processing..`")
    CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
    global CARBONLANG
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)  # Importing message to module
    code = quote_plus(pcode)  # Converting to urlencoded
    await e.edit("`Processing..\n25%`")
    if os.path.isfile("/root/userbot/.bin/carbon.png"):
        os.remove("/root/userbot/.bin/carbon.png")
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = CARBON_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {'download.default_directory': '/root/userbot/.bin'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=CARBON_DRIVER,
                              options=chrome_options)
    driver.get(url)
    await e.edit("`Processing..\n50%`")
    download_path = '/root/userbot/.bin'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': download_path
        }
    }
    command_result = driver.execute("send_command", params)
    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
   # driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
   # driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
    await e.edit("`Processing..\n75%`")
    # Waiting for downloading
    while not os.path.isfile("/root/userbot/.bin/carbon.png"):
        await sleep(0.5)
    await e.edit("`Processing..\n100%`")
    file = '/root/userbot/.bin/carbon.png'
    await e.edit("`Uploading..`")
    await e.client.send_file(
        e.chat_id,
        file,
        caption="Made using [Carbon](https://carbon.now.sh/about/),\
        \na project by [Dawn Labs](https://dawnlabs.io/)",
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )

    os.remove('/root/userbot/.bin/carbon.png')
    driver.quit()
    # Removing carbon.png after uploading
    await e.delete()  # Deleting msg
    
