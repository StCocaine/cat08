#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : http.py
# @Author: Feng
# @Date  : 2019/1/11
# @User  : tanjun
# @Desc  : 从bilibili上获取视频信息
import json
import urllib2;
import logging
from Config import Constant

logger = logging.getLogger("debug")

class HttpClient:
    def __init__(self):
        # offset_dynamic_id 第一页是0, 然后拿出查找出来的数据,找到最后一个元素中的dynamic_id值,作为新的offset_dynamic_id 则代表查询下一页
        self.minvideoListUrl = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=?&offset_dynamic_id=?";
        # 小视频展示地址 加上vc号跳转原地址
        self.minvideoPlaybackUrl = "http://vc.bilibili.com/video/";
        # 文章展示地址 需要加上cv号 跳转到展示页面
        self.articlePlaybackUrl = "https://www.bilibili.com/read/cv";
        # 查找某位up主的文章专栏 pn 第几页,ps 页大小
        self.articleListUrl = "https://api.bilibili.com/x/space/article?mid=?&pn=?&ps=?&sort=publish_time&jsonp=jsonp";
        # 视频播放地址,需要加上av号,跳转到播放页面
        self.videoPlaybackUrl = "https://www.bilibili.com/video/av";
        # 查找某位up主的视频,需要传mid up用户id,pagesize一页的数据量
        self.videoListUrl = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid=?&tid=0&page=?&&order=pubdate&pagesize=?";

    # 获取一个av号播放地址
    def getVideoUrl(self,av):
        ret = self.videoPlaybackUrl + str(av);
        return ret;

    # 获取一个cv号的播放地址
    def getArticleUrl(self,cv):
        ret = self.articlePlaybackUrl + str(cv);
        return ret;
    def getMinvideoUrl(self,vc):
        ret = self.minvideoPlaybackUrl + str(vc);
        return ret;

    # 分页查询指定up主的视频列表
    def getVideoListUrl(self,mid,pagesize,page):
        ret = self.videoListUrl.replace("mid=?","mid=" + str(mid)).replace("pagesize=?","pagesize=" + str(pagesize)).replace("page=?","page=" + str(page));
        return ret;

    # 分页查询指定up主专栏列表
    def getArticleListUrl(self,mid,pagesize,page):
        ret = self.articleListUrl.replace("mid=?","mid=" + str(mid)).replace("pn=?","pn=" + str(page)).replace("ps=?","ps=" + str(pagesize));
        return ret;

    # 获取一个up主的小视频数据列表
    def getMinvideoListUrl(self,mid,offset):
        ret = self.minvideoListUrl.replace("host_uid=?","host_uid=" + str(mid)).replace("offset_dynamic_id=?","offset_dynamic_id=" + str(offset));
        return ret;

    # 获取一个up主id所有的视频数据数组   bilibili 视频单次查询最多100条
    def getVideoAllDatas(self,mid):
        header = {
            "User-Agent": Constant.userAgent
        }
        pageSize = 100;
        page = 1;
        totolPage = 99999;#临时值
        datas = [];
        try:
            while page <= totolPage:
                url = self.getVideoListUrl(mid=mid, pagesize=pageSize, page=page);
                request = urllib2.Request(url=url, headers=header);
                response = urllib2.urlopen(request);
                if response.code == 200:
                    reJson = json.loads(response.read());
                    totolPage = reJson.get("data").get("pages");
                    vlist = reJson.get("data").get("vlist");
                    for i in range(len(vlist)):
                        v = vlist[i];
                        datas.append(Constant.getVideoPO(
                            v.get("title"),
                            "https:" + v.get("pic"),
                            self.getVideoUrl(v.get("aid")),
                            v.get("author"),
                            v.get("length"),
                            str(v.get("play")),
                            str(v.get("created")),
                            v.get("description"),
                            "bilibili" + str(v.get("aid"))
                        ));
                    page += 1;
        except BaseException,e:
            logger.error("获取一个up主所有投稿视频出错,",e)
        finally:
            return datas;

    # 获取以为up主所有专栏内容 bilibili 单次查询最多100条
    def getArticleAllDatas(self, mid):
        header = {
            "User-Agent": Constant.userAgent
        }
        datas = [];
        try:
            url = self.getArticleListUrl(mid=mid, pagesize=99999, page=1);
            request = urllib2.Request(url=url, headers=header);
            response = urllib2.urlopen(request);
            if response.code == 200:
                reJson = json.loads(response.read());
                articles = reJson.get("data").get("articles");
                for i in range(len(articles)):
                    v = articles[i];
                    datas.append(Constant.getArticlePO(
                        "bilibili" + str(v.get("id")),
                        v.get("title"),
                        v.get("author").get("name"),
                        v.get("summary"),
                        v.get("banner_url"),
                        str(v.get("ctime")),
                        v.get("words"),
                        self.getArticleUrl(v.get("id")),
                        v.get("stats").get("view")
                    ));
        except BaseException,e:
            logger.error("获取up主专栏列表列表出错.", e)
        finally:
            return datas;

    # 获取一位up主的小视频列表数据
    def getMinvideoAllDatas(self,mid):
        header = {
            "User-Agent": Constant.userAgent
        }
        datas = [];
        try:
            thisOffset = None;  # 上次的偏移量
            nextOffset = 0;  # 下次偏移量 默认0 第一页
            while thisOffset != nextOffset:  # 如果上次偏移量不等于下次偏移量则代表还有数据
                url = self.getMinvideoListUrl(mid=mid, offset=nextOffset);
                request = urllib2.Request(url=url, headers=header);
                response = urllib2.urlopen(request);
                if response.code == 200:
                    reJson = json.loads(response.read());
                    cards = reJson.get("data").get("cards");
                    if cards == None:
                        break;
                    thisOffset = nextOffset;
                    nextOffset = cards[len(cards) - 1].get("desc").get("dynamic_id");
                    for i in range(len(cards)):
                        v = cards[i];
                        if 16 != v.get("desc").get("type"): # 类型为16是小视频的意思
                            continue;
                        else:
                            card = json.loads(v.get("card"));
                            datas.append(Constant.getMinvideoPO(
                                "bilibili" + str(v.get("desc").get("rid")),
                                card.get("item").get("description"),
                                v.get("desc").get("user_profile").get("info").get("uname"),
                                card.get("item").get("watched_num"),
                                card.get("item").get("video_time"),
                                card.get("item").get("cover").get("default"),
                                v.get("desc").get("timestamp"),
                                self.getMinvideoUrl(v.get("desc").get("rid")),
                            ));
        except BaseException,e:
            logger.error("获取up主小视频列表.", e)
        finally:
            return datas;