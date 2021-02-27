from aiohttp import web


async def health(request):
    return web.Response(text="I'm alive!")
