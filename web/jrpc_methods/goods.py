from jsonrpcserver import method
from common.db.models import *


@method
async def goods_list(context):
    objects = context['objects']
    query = Good.select().where(Good.good_moderating == False)
    goods = await objects.execute(query)
    return list(map(lambda g: {
        'good_id': g.good_id,
        'good_name': g.good_name,
        'good_description': g.good_description,
        'good_price': float(g.good_price)
    }, goods))


@method
async def moderating_goods_list(context):
    objects = context['objects']
    query = Good.select().where(Good.good_moderating == True)
    goods = await objects.execute(query)
    return list(map(lambda g: {
        'good_id': g.good_id,
        'good_name': g.good_name,
        'good_description': g.good_description,
        'good_price': float(g.good_price)
    }, goods))


@method
async def add_good(context, request):
    objects = context.get('objects')
    await objects.create(Good,
                         good_id=request.get('good_id'),
                         good_name=request.get('good_name'),
                         good_description=request.get('good_description'),
                         good_price=request.get('good_price'),
                         good_moderating=request.get('good_moderating'))
    return request
