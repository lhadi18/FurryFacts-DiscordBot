from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from cat_api import get_cat_fact, get_cat_image

load_dotenv()
TOKEN: Final[str] = os.getenv('TOKEN')

intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)

async def send_message(message: Message, user_message: str):
    if not user_message:
        print('(Msg empty, intents were not enabled)')
        return

    if user_message == "!catfact":
        # User requested a cat fact
        cat_fact = get_cat_fact()
        await message.channel.send(cat_fact)
    elif user_message == "!catimg":
        # User requested a cat image
        cat_image_url, cat_name, cat_description = get_cat_image()
        if cat_image_url:
            if cat_name is not None and cat_description is not None:
                response_message = f"Here's a cat named {cat_name}: {cat_description}\n{cat_image_url}"
            elif cat_name is not None:
                response_message = f"Here's a cat named {cat_name}\n{cat_image_url}"
            elif cat_description is not None:
                response_message = f"Here's a cat: {cat_description}\n{cat_image_url}"
            else:
                response_message = f"Here's a cat\n{cat_image_url}"
        else:
            response_message = "Sorry, I couldn't fetch a cat image at the moment."
        await message.channel.send(response_message)


@client.event
async def on_ready():
    print(f'{client.user} is now running')

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

def main():
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()