import json

import asyncio
import os
from bilibili_api import Credential, video, homepage, sync

path = "/home/d0902/Documents/Recommendation-Reset-Robot/bilibili-frontend/auto-login/MyAccount.json"

with open(path, 'r', encoding='utf-8') as file:
    account_data = json.load(file)


async def main():
    credential_0 = Credential(sessdata=account_data["SESSDATA"],
                              bili_jct=account_data["bili_jct"],
                              buvid3=account_data["buvid3"])

    if not await Credential.check_valid(credential_0):
        print("Credential Invalid, please update it")
        return

    # try two times and compare if results are similar
    string_1 = sync(homepage.get_videos(credential=credential_0))
    string_2 = sync(homepage.get_videos(credential=credential_0))

    if string_1 == string_2:
        print("the same")
    else:
        print("not the same")


if __name__ == "__main__":
    asyncio.run(main())
