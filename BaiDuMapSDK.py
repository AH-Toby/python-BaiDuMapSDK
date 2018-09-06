# -*- coding: utf-8 -*-
# 第一行必须有，否则报中文字符非ascii码错误
"""
运行环境:python3.6.5
"""

import hashlib
from urllib import parse

import requests

AK = "yourAK"
SK = "yourSK"


class BaiDuMapSDK(object):
    """百度地图SDK"""

    def __new__(cls, *args, **kwargs):
        # 单例封装鉴权操作封初 鉴权只要一次
        if not hasattr(cls, 'instance'):  # 判断当前类是否存在instance
            obj = super(BaiDuMapSDK, cls).__new__(cls)

            # 判断鉴权
            if "address" in kwargs.keys():
                query_str = '/geocoder/v2/?address=%s&output=json&ak=%s' % (kwargs["address"], AK)
                print(query_str)
            else:
                # 以get请求为例http://api.map.baidu.com/geocoder/v2/?location=经,纬度&output=json&ak=yourak
                query_str = '/geocoder/v2/?location=%s,%s&output=json&ak=%s' % (kwargs["lat"], kwargs["lng"], AK)

            # 对queryStr进行转码，safe内的保留字符不转换
            encoded_str = parse.quote(query_str, safe="/:=&?#+!$,;'@()*[]")  # 去除多余的字符串

            # 在最后直接追加上sk
            raw_str = encoded_str + SK

            # md5计算出的sn值
            obj.SN = hashlib.md5(parse.quote_plus(raw_str).encode('utf-8')).hexdigest()

            cls.instance = obj

        return cls.instance

    def __init__(self, *args, **kwargs):
        self.url = 'http://api.map.baidu.com/geocoder/v2/?'

        if "address" in kwargs.keys():
            self.address = kwargs["address"]
        else:
            self.lat = kwargs["lat"]
            self.lng = kwargs["lng"]

    def get_address(self, *args):
        """获取到具体的地址"""
        url = '%slocation=%s,%s&output=json&ak=%s&sn=%s' % (self.url, self.lat, self.lng, AK, args[0])
        res = requests.request('GET', url)
        result = res.json()
        # print(result)  # 打印测试
        return result

    def get_longitude_latitude(self, *args):
        """获取到对应的地理位置"""
        url = '%saddress=%s&output=json&ak=%s&sn=%s' % (self.url, self.address, AK, args[0])
        res = requests.request('GET', url)
        result = res.json()
        # print(result)  # 打印测试
        return result

if __name__ == '__main__':
    # 更具地理位置获取对应的位置信息
    # sn = BaiDuMapSDK(lat=31.214159, lng=121.634925)
    # sn.get_address(sn.SN)

    # 根据位置信息获取对应的地理位置
    Sn = BaiDuMapSDK(address='上海市')
    print(Sn.SN)
    Sn.get_longitude_latitude(Sn.SN)
