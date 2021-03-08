from jsonrpcserver import method


@method
async def echo(*args):
    return args
