#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Config.py
# @Author: Feng
# @Date  : 2019/1/11
# @User  : tanjun
# @Desc  : 静态
import json;
from elasticsearch import Elasticsearch;
import logging
logger = logging.getLogger("debug")


class Constant:
    # http请求头部设置客户端
    userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36";

    # es连接地址
    es = Elasticsearch(hosts=["es79:1600"],retry_on_timeout=False);

    # 视频数据存储格式
    @staticmethod
    def getVideoPO(title,coversUrl,videoUrl,author,length,playAmount,createTime,desc,id):
        return {"title":title,"coversUrl":coversUrl,"videoUrl":videoUrl,"author":author,"length":length,"playAmount":playAmount,"createTime":createTime,"desc":desc,"id":id,"time":createTime};

    # 专栏数据存储格式
    @staticmethod
    def getArticlePO(id,title,author,summary,banner_url,ctime,words,url,view):
        return {"id":id,"title":title,"author":author,"summary":summary,"banner_url":banner_url,"ctime":ctime,"words":words,"url":url,"view":view,"time":ctime};

    # 小视频数据存储格式
    @staticmethod
    def getMinvideoPO(id,title,uname,watched_num,video_time,default,timestamp,url):
        return {"id":id,"title":title,"uname":uname,"watched_num":watched_num,"video_time":video_time,"default":default,"timestamp":timestamp,"time":timestamp,"url":url};

    @staticmethod
    def getMids():
        try:
            file = open(name="ups-config.txt", mode="r");
            ups = json.loads(file.read());
            file.close();
            return ups;
        except BaseException,e:
            logger.error("读取up主列表配置文件出错,",e)
            return [];

    # es分页查询条件查询数据
    @staticmethod
    def esPageQuery(value,pageindex,pagesize):
        must = {"match_all":{}};#默认没有查询条件
        sort = {"createTime":{"order":"desc"}};#没条件以创建时间为准
        if value != "" and value != None :
            must = {"query_string": {"default_field": "title", "query": value}};
            sort = {"_score":{"order":"desc"}}; #有搜索条件,以搜索匹配度为准
        return {"query": {"bool": {"must": [must]}},"size":pagesize,"from":(pageindex * pagesize),"sort":[sort]};