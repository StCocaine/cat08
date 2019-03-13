#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Util.py
# @Author: Feng
# @Date  : 2019/1/15
# @User  : tanjun
# @Desc  : es的一些静态工具

from elasticsearch import Elasticsearch
import requests;
from requests.cookies import RequestsCookieJar
import time;
import json;
import logging
logger = logging.getLogger("debug")

class Util:
    # http请求头部设置客户端
    userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36";
    cookie = "LIVE_BUVID=AUTO2415386412681724; sid=4mdrut7f; im_notify_type_29874131=0; stardustvideo=1; buvid3=A4E796D4-DDF7-4C2C-AEDF-CFDB9838C8B9149013infoc; rpdid=impilwlqpqdoskqxpkoqw; fts=1540443243; CURRENT_FNVAL=16; DedeUserID=29874131; DedeUserID__ckMd5=9e350fbc9643c627; SESSDATA=612eef0c%2C1548049927%2Cd2b0e8c1; bili_jct=97d903a952bcbb96952972d18198a08b; finger=54bdb683; bp_t_offset_29874131=201656058943513179; _dfcaptcha=9f6faf1f95b42a2bf36d74d44857014c";
    # 获取bilibili真实视频地址
    bilibiliVideoUrl = "https://api.bilibili.com/playurl?callback=callbackfunction&aid=?&page=1&platform=html5&quality=1&vtype=mp4&type=jsonp";
    # 获取bilibili小视频真实视频地址
    bilibiliMinVideoUrl = "https://api.vc.bilibili.com/clip/v1/video/detail?video_id=?&need_playurl=1";
    bingDomain = "https://cn.bing.com"
    # 获取bing壁纸地址  idx 最多等于7
    bingBackImgUrl = bingDomain + "/HPImageArchive.aspx?format=js&idx=?&n=1";
    # 获取bing壁纸故事描述地址 currentDate 格式 yyyyMMdd
    bingBackStoryUrl = bingDomain + "/cnhp/life?currentDate=?";
    # es 连接对象
    es = Elasticsearch(["es79:1600"]);
    # 获取壁纸故事内容
    @staticmethod
    def getBingBackImgStoryHtml(currentDate):
        headers = {
            "User-Agent": Util.userAgent
        }
        try:
            url = Util.bingBackStoryUrl.replace("currentDate=?", "currentDate=" + str(currentDate))
            res = requests.get(url=url, headers=headers)
            if res.status_code == 200:
                ret = res.content.replace("href=\"","href=\"" + Util.bingDomain).replace("target=\"_blank\"","").replace("<a ","<a target=\"_blank\"").replace("color:#fff;","").replace("width:364px;","").replace("width=\"364\"","").replace("height=\"205\"","")
                return ret
        except BaseException, e:
            logger.error("获取bing壁纸故事出错",e)
        return None

    # 获取必应壁纸和故事的地址
    @staticmethod
    def getBingBackImgAndStoryUrl(idx):
        headers = {
            "User-Agent": Util.userAgent
        }
        try:
            url = Util.bingBackImgUrl.replace("idx=?","idx=" + str(idx))
            res = requests.get(url=url, headers=headers)
            if res.status_code == 200:
                data = json.loads(res.content);
                image = data.get("images")[0];
                currentDate = image.get("enddate");
                backImageUrl = image.get("url");
                backImageTitle = image.get("copyright");
                return json.dumps({"backImageTitle":backImageTitle,"currentDate":currentDate,"backImageUrl":Util.bingDomain + backImageUrl},ensure_ascii=False)
        except BaseException,e:
            logger.error("获取bing壁纸地址出错", e)
        return None

    # es分页查询条件查询数据
    @staticmethod
    def esPageQuery(value, pageindex, pagesize):
        must = {"match_all": {}};  # 默认没有查询条件
        sort = {"time": {"order": "desc"}};  # 没条件以创建时间为准
        if value != "" and value != None:
            must = {"query_string": {"default_field": "title", "query": value}};
            sort = {"_score": {"order": "desc"}};  # 有搜索条件,以搜索匹配度为准
        return {"query": {"bool": {"must": [must]}}, "size": pagesize, "from": (pageindex * pagesize), "sort": [sort]};

    # 参数av号,获取改av号视频真实地址
    @staticmethod
    def getBilibiliVideoUrl(av):
        headers = {
            "Cookie":Util.cookie,
            "User-Agent":Util.userAgent
        }
        try:
            url = Util.bilibiliVideoUrl.replace("aid=?","aid=" + str(av));
            res = requests.get(url=url, headers=headers)
            if res.status_code == 200:
                data = json.loads(res.content.replace("callbackfunction(", "").replace(");", ""));
                return data.get("durl")[0].get("url");
        except BaseException,e:
            logger.error("通过av号获取真实视频地址出错", e)
        return None;

    # 参数vc号,获取小视频真实地址
    @staticmethod
    def getBilibiliMinVideoUrl(vc):
        headers = {
            "Cookie": Util.cookie,
            "User-Agent": Util.userAgent
        }
        try:
            url = Util.bilibiliMinVideoUrl.replace("video_id=?","video_id=" + str(vc));
            res = requests.get(url=url, headers=headers)
            if res.status_code == 200:
                data = json.loads(res.content);
                return data.get("data").get("item").get("video_playurl");
        except BaseException,e:
            logger.error("通过vc号获取小视频真实地址出错.",e)
        return None;