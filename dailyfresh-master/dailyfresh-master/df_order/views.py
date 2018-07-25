# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.db import transaction
from datetime import datetime
from decimal import Decimal
from df_order.models import OrderInfo,OrderDetailInfo
from df_user.islogin import islogin
from df_cart.models import CartInfo
from df_goods.models import GoodsInfo
from df_user.models import UserInfo
from django.http import JsonResponse


# Create your views here.
@islogin
def order(request):
    """
    此函数用户给下订单页面展示数据
    接收购物车页面GET方法发过来的购物车中物品的id，构造购物车对象供订单使用
    """

    uid = request.session.get('user_id')
    user = UserInfo.objects.get(id=uid)

    # 获取勾选的每一个订单对象，构造成list，作为上下文传入下单页面
    orderid = request.GET.getlist('orderid')
    orderlist = []

    for id in orderid:
        orderlist.append(CartInfo.objects.get(id=int(id)))

    # 判断用户手机号是否为空，分别做展示
    if user.uphone == '':
        uphone = ''
    else:
        uphone = user.uphone[0:4] + \
            '****' + user.uphone[-4:]

    # 构造上下文
    context = {'title': '提交订单', 'page_name': 1, 'orderlist': orderlist,
               'user': user, 'ureceive_phone': uphone}

    return render(request, 'df_order/place_order.html', context)


#什么装饰器？->事务   一旦有一步操作失败，则回滚全部操作
'''
1. 创建订单对象
2. 判断商品的库存
3. 创建详单对象
4. 修改商品库存
5. 删除购物车
'''

@transaction.atomic()
@islogin
def order_handle(request):
    #保存一个事物点
    tran_id = transaction.savepoint()
    #接收购物车编号
    # 根据POST和session获取信息
    # cart_ids=post.get('cart_ids')
    try:
        post = request.POST
        orderlist = post.getlist('id[]')
        total = post.get('total')
        address = post.get('address')

        order=OrderInfo()
        now=datetime.now()
        uid = request.session.get('user_id')
        order.oid='%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id=uid
        order.odate=now
        order.ototal=Decimal(total)
        order.oaddress = address
        order.save()

        # 遍历购物车中提交信息，创建订单详情表
        for orderid in orderlist:
            cartinfo = CartInfo.objects.get(id=orderid)
            # good = GoodsInfo.objects.get(cartinfo__id=cartinfo.id)
            good = GoodsInfo.objects.get(pk=cartinfo.goods_id)
            # print '*'*10
            # print cartinfo.goods_id
            # 判断库存是否够
            if int(good.gkucun) >= int(cartinfo.count):
                # 库存够，移除购买数量并保存
                good.gkucun -= int(cartinfo.count)
                good.save()

                goodinfo = GoodsInfo.objects.get(cartinfo__id=orderid)

                # 创建订单详情表
                detailinfo = OrderDetailInfo()
                detailinfo.goods_id = int(goodinfo.id)
                detailinfo.order_id = int(order.oid)
                detailinfo.price = Decimal(int(goodinfo.gprice))
                detailinfo.count = int(cartinfo.count)
                detailinfo.save()

                # 循环删除购物车对象
                cartinfo.delete()
            else:
                # 库存不够出发事务回滚
                transaction.savepoint_rollback(tran_id)
                # 返回json供前台提示失败
                return JsonResponse({'status': 2})
    except Exception as e:
            # print '==================%s'%e
            transaction.savepoint_rollback(tran_id)
        # 返回json供前台提示成功
    return JsonResponse({'status': 1})

        #
    #     cart_ids1=[int(item) for item in cart_ids.split(',')]
    #     for id1 in cart_ids1:
    #         detail=OrderDetailInfo()
    #         detail.order=order
    #         #查询购物车信息
    #         cart=CartInfo.objects.get(id=id1)
    #         #判断商品库存
    #         goods=cart.goods
    #         if goods.gkuncun>=cart.count:
    #             #减少商品库存
    #             goods.gkuncun=cart.goods.gkuncun-cart.count
    #             goods.save()
    #             #完善订单信息
    #             detail.goods_id=goods.id
    #             detail.price=goods.gprice
    #             detail.count=cart.count
    #             detail.save()
    #             #删除购物车数据
    #             cart.delete()
    #         else:
    #             transaction.savepoint_rollback(tran_id)
    #             return redirect('/cart/')
    #             #return HttpResponse
    #     transaction.savepoint_commit(tran_id)
    # except Exception as e:
    #     print '==================%s'%e
    #     transaction.savepoint_rollback(tran_id)
    #
    # return redirect('/user/order/')





# @transaction.atomic()
def pay(request,oid):
    tran_id = transaction.savepoint()
    # try:
    order = OrderInfo.objects.get(oid=oid)
    order.zhifu = 1

    order.save()
    # except Exception as e:
    # print '==================%s' % e
    # transaction.savepoint_rollback(tran_id)
    # print '*' * 10
    # print order.zhifu
    # print order.oid
    context = {'oid': oid}
    return render(request, 'df_order/pay.html', context)