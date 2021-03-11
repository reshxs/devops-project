from jsonrpcserver import method


@method
async def echo(context, *request):
    return request
