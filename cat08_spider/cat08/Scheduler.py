#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Scheduler.py
# @Author: Feng
# @Date  : 2019/1/14
# @User  : tanjun
# @Desc  : 启动定时拉数据入库

from Config import Constant
import elasticsearch.helpers
from apscheduler.schedulers.blocking import BlockingScheduler
from http import HttpClient
from datetime import datetime
import logging

logger = logging.getLogger("debug")

class Scheduler:
    # 初始化定时器对象
    def __init__(self):
        self.sched = BlockingScheduler();
        self.bilibiliHttp = HttpClient();

    # 启动定时任务入口
    def start(self):
        self.addJob(self.bilibili);
        self.sched.start();

    # 添加一个任务到定时器
    def addJob(self,fun):
        fun()
        self.sched.add_job(fun,"interval", seconds=600) #10分钟执行一次

    #bilibili 拉数据入口
    def bilibili(self):
        try:
            # es 连接对象
            mids = Constant.getMids();
            for bilibili in mids.get("video"):
                datas = self.bilibiliHttp.getVideoAllDatas(bilibili.get("mid"));
                actions = [
                    {
                        "_index": "cat08",
                        "_type": "video",
                        "_id": data.get("id"),
                        "_source": data
                    }
                    for data in datas
                ];
                elasticsearch.helpers.bulk(Constant.es, actions);
                logger.debug("已导入视频用户:" + bilibili.get("name").encode("utf-8"))
            for bilibili in mids.get("article"):
                datas = self.bilibiliHttp.getArticleAllDatas(bilibili.get("mid"));
                actions = [
                    {
                        "_index": "cat08",
                        "_type": "article",
                        "_id": data.get("id"),
                        "_source": data
                    }
                    for data in datas
                ];
                elasticsearch.helpers.bulk(Constant.es, actions);
                logger.debug("已导入专栏用户:" + bilibili.get("name").encode("utf-8"))
            for bilibili in mids.get("minvideo"):
                datas = self.bilibiliHttp.getMinvideoAllDatas(bilibili.get("mid"));
                actions = [
                    {
                        "_index": "cat08",
                        "_type": "minvideo",
                        "_id": data.get("id"),
                        "_source": data
                    }
                    for data in datas
                ];
                elasticsearch.helpers.bulk(Constant.es, actions);
                logger.debug("已导入小视频用户:" + bilibili.get("name").encode("utf-8"))
        except BaseException,e:
            logger.error("执行导入up主数据发生异常,",e)