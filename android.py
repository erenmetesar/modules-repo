# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to android"""

import re
from requests import get
from bs4 import BeautifulSoup
from nicegrill import utils

GITHUB = 'https://github.com'
DEVICES_DATA = 'https://raw.githubusercontent.com/androidtrackers/' \
               'certified-android-devices/master/devices.json'


class Android:

    async def magiskxxx(request):
        """ magisk latest releases """
        magisk_dict = {
            "Stable":
            "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/stable.json",
            "Beta":
            "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/beta.json",
            "Canary (Release)":
            "https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/release.json",
            "Canary (Debug)":
            "https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/debug.json"
        }
        releases = 'Latest Magisk Releases:\n'
        for name, release_url in magisk_dict.items():
            data = get(release_url).json()
            releases += f"""{name}: <a href='{data["magisk"]["link"]}'>ZIP v{data["magisk"]["version"]}</a> | """ \
                        f"""<a href='{data["app"]["link"]}'>APP v{data["app"]["version"]}</a> | """ \
                        f"""<a href='{data["uninstaller"]["link"]}'>Uninstaller</a>\n"""
        await request.edit(releases)


    async def devicexxx(request):
        """ get android device basic info from its codename """
        textx = await request.get_reply_message()
        device = utils.get_arg(request)
        if device:
            pass
        elif textx:
            device = textx.text
        else:
            await request.edit("<code>Usage: .device <codename> / <model></code>")
            return
        found = [
            i for i in get(DEVICES_DATA).json()
            if i["device"] == device or i["model"] == device
        ]
        if found:
            reply = f'Search results for {device}:\n\n'
            for item in found:
                brand = item['brand']
                name = item['name']
                codename = item['device']
                model = item['model']
                reply += f'{brand} {name}\n' \
                    f'<b>Codename</b>: <code>{codename}</code>\n' \
                    f'<b>Model</b>: {model}\n\n'
        else:
            reply = f"<code>Couldn't find info about {device}!</code>\n"
        await request.edit(reply)


    async def codenamexxx(request):
        """ search for android codename """
        textx = await request.get_reply_message()
        brand = utils.get_arg(request).split()[0].lower()
        device = utils.get_arg(request).split()[1].lower()
        if brand and device:
            pass
        elif textx:
            brand = textx.text.split(' ')[0]
            device = ' '.join(textx.text.split(' ')[1:])
        else:
            await request.edit("<code>Usage: .codename <brand> <device></code>")
            return
        found = [
            i for i in get(DEVICES_DATA).json()
            if i["brand"].lower() == brand and device in i["name"].lower()
        ]
        if len(found) > 8:
            found = found[:8]
        if found:
            reply = f'Search results for {brand.capitalize()} {device.capitalize()}:\n\n'
            for item in found:
                brand = item['brand']
                name = item['name']
                codename = item['device']
                model = item['model']
                reply += f'{brand} {name}\n' \
                    f'<b>Codename</b>: <code>{codename}</code>\n' \
                    f'<b>Model</b>: {model}\n\n'
        else:
            reply = f"<code>Couldn't find {device} codename!</code>\n"
        await request.edit(reply)


    async def specsxxx(request):
        """ Mobile devices specifications """
        textx = await request.get_reply_message()
        brand = utils.get_arg(request).split(",")[0].lower()
        device = utils.get_arg(request).split(",")[1].lower()
        if brand and device:
            pass
        elif textx:
            brand = textx.text.split(',')[0]
            device = ' '.join(textx.text.split(',')[1])
        else:
            await request.edit("<code>Usage: .specs <brand> <device></code>")
            return
        all_brands = BeautifulSoup(
            get('https://www.devicespecifications.com/en/brand-more').content,
            'lxml').find('div', {
                'class': 'brand-listing-container-news'
            }).findAll('a')
        brand_page_url = None
        try:
            brand_page_url = [
                i['href'] for i in all_brands if brand == i.text.strip().lower()
            ][0]
        except IndexError:
            await request.edit(f'<code>{brand} is unknown brand!</code>')
        devices = BeautifulSoup(get(brand_page_url).content, 'lxml') \
            .findAll('div', {'class': 'model-listing-container-80'})
        device_page_url = None
        try:
            device_page_url = [
                i.a['href']
                for i in BeautifulSoup(str(devices), 'lxml').findAll('h3')
                if device in i.text.strip().lower()
            ]
        except IndexError:
            await request.edit(f"<code>can't find {device}!</code>")
        if len(device_page_url) > 2:
            device_page_url = device_page_url[:2]
        reply = ''
        for url in device_page_url:
            info = BeautifulSoup(get(url).content, 'lxml')
            reply = '\n<b>' + info.title.text.split('-')[0].strip() + '</b>\n\n'
            info = info.find('div', {'id': 'model-brief-specifications'})
            specifications = re.findall(r'<b>.*?<br/>', str(info))
            for item in specifications:
                title = re.findall(r'<b>(.*?)</b>', item)[0].strip()
                data = re.findall(r'</b>: (.*?)<br/>', item)[0]\
                    .replace('<b>', '').replace('</b>', '').strip()
                reply += f'<b>{title}</b>: {data}\n'
        await request.edit(reply)


    async def twrpxxx(request):
        """ get android device twrp """
        textx = await request.get_reply_message()
        device = utils.get_arg(request)
        if device:
            pass
        elif textx:
            device = textx.text.split(' ')[0]
        else:
            await request.edit("<code>Usage: .twrp <codename></code>")
            return
        url = get(f'https://dl.twrp.me/{device}/')
        if url.status_code == 404:
            reply = f"<code>Couldn't find twrp downloads for {device}!</code>\n"
            await request.edit(reply)
            return
        page = BeautifulSoup(url.content, 'lxml')
        download = page.find('table').find('tr').find('a')
        dl_link = f"https://dl.twrp.me{download['href']}"
        dl_file = download.text
        size = page.find("span", {"class": "filesize"}).text
        date = page.find("em").text.strip()
        reply = f'<b>Latest TWRP for {device}:</b>\n' \
            f'[{dl_file}]({dl_link}) - <i>{size}</i>\n' \
            f'<b>Updated:</b> <i>{date}</i>\n'
        await request.edit(reply)
