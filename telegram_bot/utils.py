import re
import aiohttp
import html
from g4f.client import Client


def chat(message):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
    )
    return (response.choices[0].message.content)


# print(chat("напиши привет на китайском"))
# print('Hi!')


def valid_link(link):
    tg_link = re.search(r"t.me\/[a-zA-Z0–9-_]+", link)
    print(tg_link)
    if tg_link:
        return tg_link.group(0)


async def read_posts(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://t.me/s/{link}') as responce:
            text = await responce.text()
            print(link)
            post_pattern = re.compile(
                r"<div class=\"tgme_widget_message_text js-message_text\".*?>(.*?)</div>", re.S)
            match = post_pattern.findall(text)
            if match:
                last_post = match[-1]
                last_post = html.escape(last_post)
                last_post = last_post.replace('\n', '<br>')
                return last_post
            return "ooops!"
