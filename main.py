import json
import asyncio
from pyrogram import Client, filters
data = json.loads(open('setup.json', encoding='utf8').read())

async def main(api_id, api_hash, json):
    async with Client('Telegram', api_id, api_hash) as app:
        @app.on_message(filters.private)
        async def greet(client, message):
            if json['dm_message']['enabled']:
                print("Sent reply to " + str(message.from_user.first_name) + " " + str(message.from_user.last_name))
                await message.reply(json['dm_message']['message'])
        if json['send_on_start']:
            for item in json['setup']:
                if item['forward']:
                    print(f"Forwarding Message | {item['to_channel']} | {item['from_channel']} | {item['message_id']}")
                    try:
                        await app.forward_messages(item['to_channel'], item['from_channel'], item['message_id'])
                    except:
                        pass
                else:
                    print(f"Sending Message | {item['to_channel']}")
                    try:
                        await app.send_message(item['to_channel'], item['message'])
                    except:
                        pass
        i = 0
        while True:
            await asyncio.sleep(120)
            i = i + 1
            for item in json['setup']:
                if i % item['wait_time'] == 0:
                    if item['forward']:
                        print(f"Forwarding Message | {item['to_channel']} | {item['from_channel']} | {item['message_id']}")
                        try:
                            await app.forward_messages(item['to_channel'], item['from_channel'], item['message_id'])
                        except:
                            pass
                    else:
                        print(f"Sending Message | {item['to_channel']}")
                        try:
                            await app.send_message(item['to_channel'], item['message_id'])
                        except:
                            pass
            print(f"round {i} completed")


print("Starting")
asyncio.run(main(data['tele_api_id'], data['tele_api_hash'], data))
