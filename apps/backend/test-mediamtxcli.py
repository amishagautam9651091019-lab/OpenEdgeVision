import asyncio

from app.services.mediamtx import mediamtx_client


async def main():
    paths = await mediamtx_client.list_paths()
    print(paths)


asyncio.run(main())
