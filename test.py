import asyncio
from bilibili_api import video

async def main():
    # 实例化一个Video对象
    v = video.Video(bvid="BV1uv411q7Mv") 
    # 获取视频信息
    info = await v.get_info()
    print(f"视频标题: {info['title']}")

if __name__ == "__main__":
    asyncio.run(main())