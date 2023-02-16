import json
import urllib.parse
import requests

from api import Apisetting as Apiset
from api.aes import md5_encrypt, aes_encrypt
import orjson
from api.sign import SignBase


def get_access_token():
    domin = Apiset.domin
    appId = Apiset.appId
    appsecret = Apiset.appsecret
    appsecret = urllib.parse.quote(appsecret)
    url = domin+"/api/auth-server/oauth/access-token?appId=%s&appSecret=%s"%(appId,appsecret)
    res = requests.post(url)
    res = eval(res.text)
    access_token = res["data"]['access_token']
    refresh_token = res["data"]['refresh_token']
    a=11
    return access_token

def generate_sign(encrypt_key: str, request_params: dict) -> str:
    """
    生成签名
    """
    canonical_querystring = format_params(request_params)
    md5_str = md5_encrypt(canonical_querystring).upper()
    sign = aes_encrypt(encrypt_key, md5_str)
    return sign

from typing import Union
def format_params(request_params: Union[None, dict] = None) -> str:
    if not request_params or not isinstance(request_params, dict):
        return ''
    canonical_strs = []
    sort_keys = sorted(request_params.keys())
    for k in sort_keys:
        v = request_params[k]
        if v == "":
            continue
        elif isinstance(v, (dict, list)):
            # 如果直接使用 json, 则必须使用separators=(',',':'), 去除序列化后的空格, 否则 json中带空格就导致签名异常
            # 使用 option=orjson.OPT_SORT_KEYS 保证dict进行有序 序列化(因为最终要转换为 str进行签名计算, 需要保证有序)
            canonical_strs.append(f"{k}={orjson.dumps(v, option=orjson.OPT_SORT_KEYS).decode()}")
        else:
            canonical_strs.append(f"{k}={v}")
    return "&".join(canonical_strs)

import copy
import time
from typing import Optional

def request(method:str,app_id:str,host:str,access_token: str, route_name: str,
            req_params: Optional[dict] = None,
            req_body: Optional[dict] = None):
        """
        :param access_token:
        :param route_name: 请求路径
        :param method: GET/POST/PUT,etc
        :param req_params: query参数放这里, 没有则不传
        :param req_body: 请求体参数放这里, 没有则不传
        :param kwargs: timeout 等其他字段可以放这里
        :return:
        """
        req_url = host + route_name
        # headers = kwargs.get('headers') or {"Content-Type": "application/json"}

        req_params = req_params or {}
        gen_sign_params = copy.deepcopy(req_body) if req_body else {}
        if req_params:
            gen_sign_params.update(req_params)

        sign_params = {
            "app_key": app_id,
            "access_token": access_token,
            "timestamp": f'{int(time.time())}',
        }
        gen_sign_params.update(sign_params)
        sign = SignBase.generate_sign(app_id, gen_sign_params)
        # sign = urllib.parse.quote(appsecret)
        sign_params["sign"] = sign

        req_params.update(sign_params)
        if method == "post":
            return requests.post(req_url,params=req_params,json=req_body)
        else:
            return requests.get(req_url, params=req_params, json=req_body)



def requesterp(body,method,domin,apiurl):
    if domin == 'domin':
        return request(method,Apiset.appId,Apiset.domin,get_access_token(),apiurl,{},body)
    else:
        return request(method, Apiset.appId,Apiset.domin_bill, get_access_token(), apiurl,{}, body)



class base_data(object):
    """
    基础数据类
    """
    def get_store_detail(param_dict):
        """
        查询店铺信息
        :请求方式："GEY"
        :文档地址：”https://openapidoc.lingxing.com/#/docs/BasicData/SellerLists“
        :return:
        """

        return requesterp(param_dict, "get", "dominapi", "/data/seller/lists")


class storage_getlist(object):
    """
    仓库查询类
    """

    def get_outbound(param_dict):
        """
        查询出库单
        :请求方式："POST"
        :文档地址：”https://openapidoc.lingxing.com/#/docs/Warehouse/OrderAddOut“
        :return:
        """
        return requesterp(param_dict,"post","dominapi","/routing/storage/outbound/getOrders")

    def get_inbound(param_dict):
        """
        查询入库单
        :请求方式："POST"
        :文档地址：”https://openapidoc.lingxing.com/#/docs/Warehouse/inboundgetOrders“
        :return:
        """
        return requesterp(param_dict, "post", "dominapi", "/routing/storage/inbound/getOrders")

    def getStorageProcess(param_dict):
        """
        查询加工单
        :请求方式："POST"
        :文档地址：”https://openapidoc.lingxing.com/#/docs/Warehouse/getProcessOrderLists“
        :return:
        """
        return requesterp(param_dict, "post", "dominapi", "/routing/inventoryReceipt/StorageProcess/getOrderLists")


    def getStorageAllocationList(param_dict):
        """
        查询调拨单
        :请求方式："POST"
        :文档地址：”https://openapidoc.lingxing.com/#/docs/Warehouse/getStorageAllocationList“
        :return:
        """
        return requesterp(param_dict, "post", "dominapi", "/routing/inventoryReceipt/StorageAllocation/getStorageAllocationList")


    def getStorageAdjustOrderList(param_dict):
        """
        查询调整单
        :请求方式："POST"
        :文档地址：”https://openapidoc.lingxing.com/#/docs/Warehouse/getStorageAdjustOrderList“
        :return:
        """
        return requesterp(param_dict, "post", "dominapi", "/routing/inventoryReceipt/StorageAdjustment/getStorageAdjustOrderList")

    def getInventoryCheck(param_dict):
        """
        查询盘点单
        :请求方式："POST"
        :文档地址：”https://openapidoc.lingxing.com/#/docs/Warehouse/checkGetOrderList“
        :return:
        """
        return requesterp(param_dict, "post", "dominapi",
                          "/routing/inventoryReceipt/InventoryCheck/getOrderList")

    def getcheckGetOrderDetail(param_dict):
        """
        查询盘点单详情
        :请求方式："POST"
        :文档地址：”https://openapidoc.lingxing.com/#/docs/Warehouse/checkGetOrderDetail“
        :return:
        """
        return requesterp(param_dict, "post", "dominapi",
                          "/routing/inventoryReceipt/InventoryCheck/getOrderDetail")

class sales_getlist(object):
    def get_listing(param_dict):
        """
        查询亚马逊listing
        :请求方式："POST"
        :文档地址：”https://openapidoc.lingxing.com/#/docs/Sale/Listing“
        :return:
        """
        return requesterp(param_dict, "post", "dominapi",
                          "/data/mws/listing")

    # def get_listing(param_dict):
    #     """
    #     查询亚马逊listing
    #     :请求方式："POST"
    #     :文档地址：”https://openapidoc.lingxing.com/#/docs/Sale/Listing“
    #     :return:
    #     """
    #     return requesterp(param_dict, "post", "dominapi",
    #                       "/data/mws/listing")


def run1():

    req_body = {
            "type":1
        }
    # a=request("post",Apiset.appId,"https://openapi.lingxing.com/erp/sc/",get_access_token(),"/routing/data/local_inventory/inventoryDetails",req_body)
    a = storage_getlist.getStorageProcess(req_body)
    data = a.text
    # data1 = eval(data)["data"]
    # df_data = pd.DataFrame()
    # for i in data1:
    #     df = pd.DataFrame(i)
    #     for j in df.index:
    #         storge = df.loc[j, 'ware_house_bak_name']
    #         process_sn = df.loc[j, 'process_sn']
    #         df.loc[j, 'product_list'] = str(df.loc[j, 'product_list'])
    #     df_data = df_data.append(df)
    a=11
    return data



# run1()

