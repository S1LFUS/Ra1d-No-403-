import aiohttp
import asyncio
import time
from lib import Client
from os import system, name
from lib.helpers import device_id


email = input("Почта >>> ")
password = input("Пароль >>> ")


async def send(chat_id, message, message_type, community_id, client, i):
    await client.send_message(chat_id=chat_id,
                              message=message,
                              message_type=message_type,
                              community_id=community_id)
    print(f"Отправлено сообщение №{i}")


async def jls(chat_id, community_id, client):
    try:
        await asyncio.gather(*[client.join_chat(chat_id=chat_id, community_id=community_id), client.leave_chat(chat_id=chat_id, community_id=community_id)])
    except Exception as e:
        print(e)


async def main():
    async with aiohttp.ClientSession() as session:
        try:
            client = Client(session=session,
                            simple_account={
                                            "email": email,
                                            "password": password,
                                            "device_id": device_id()
                                            })
            
            res = await client.login()
            if res != True:
                print(res)
                exit()
            system("cls" if name == "nt" else "clear")
            link = input("Ссылка на чат (вы должны быть в чате, куда будите спамить) >>> ")
            result = await client.link_resolution(link)

            community_id = result["linkInfoV2"]["path"].split("/")[0]
            chat_id = result["linkInfoV2"]["extensions"]["linkInfo"]["objectId"]
            system("cls" if name == "nt" else "clear")
            choice = int(input("1. Типовой спам \n2. Ливрейд\n\n>>> "))
            if choice == 1:
                system("cls" if name == "nt" else "clear")
                message = input("Ваше сообщение >>> ")
                system("cls" if name == "nt" else "clear")
                message_type = int(input("Тип сообщения (например 109) >>> "))
                system("cls" if name == "nt" else "clear")
                times = int(input("Сколько сообщений отправим (ставьте 10.000 для эффективности) >>> "))
                system("cls" if name == "nt" else "clear")
                await client.join_community(community_id)
                await client.join_chat(chat_id, community_id)
                await asyncio.gather(*[asyncio.create_task(send(chat_id=chat_id,
                                                                message=message,
                                                                message_type=message_type,
                                                                community_id=community_id.replace("x", ""),
                                                                client=client,
                                                                i=i+1)) for i in range(times)])
            elif choice == 2:
                raidtasks = []
                system("cls" if name == "nt" else "clear")
                times = int(input("Сколько раз входим и выходим (ставьте 10.000 для эффективности) >>> "))
                system("cls" if name == "nt" else "clear")
                await client.join_community(community_id)
                await asyncio.gather(*[asyncio.create_task(jls(chat_id=chat_id, community_id=community_id.replace("x", ""), client=client)) for _ in range(times)])
            print("DONE!!!\n\n\n")
            await main()
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())