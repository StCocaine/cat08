#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Api.py
# @Author: Feng
# @Date  : 2019/1/15
# @User  : tanjun
# @Desc  :
from flask import Flask,request,abort,jsonify
from flask_cors import CORS
from Util import Util
import logging

logger = logging.getLogger("debug")

app = Flask(__name__);
CORS(app, resources=r'/*')

# 不区分类型搜索
@app.route(rule='/car08-webservice/search', methods=['POST'])
def search():
    param = request.json;
    if not param or "value" not in param or "pageindex" not in param or "pagesize" not in param or "type" not in param:
        abort(400);
    else:
        ret = {"total": 0, "body": []};
        try:
            doc_type = None if "all" == param.get("type") else param.get("type");
            res = Util.es.search(index="cat08",doc_type=doc_type,body=Util.esPageQuery(str(param.get("value").encode("utf-8")), param.get("pageindex"),param.get("pagesize")))
            total = res['hits']['total'];
            body = res['hits']['hits'];
            ret["total"] = total;
            ret["body"] = body;
            return jsonify(ret);
        except BaseException,e:
            logger.error("查询数据列表出错.",e)
        finally:
            return jsonify(ret);

# 通过av号获取视频真实资源地址
@app.route(rule='/car08-webservice/getBilibiliVideoUrl', methods=['POST'])
def getBilibiliVideoUrl():
    param = request.json;
    if not param or "av" not in param:
        abort(400);
    else:
        return Util.getBilibiliVideoUrl(str(param.get("av")).replace("bilibili",""));

# 通过vc号获取小视频真实资源地址
@app.route(rule='/car08-webservice/getBilibiliMinVideoUrl', methods=['POST'])
def getBilibiliMinVideoUrl():
    param = request.json;
    if not param or "vc" not in param:
        abort(400);
    else:
        return Util.getBilibiliMinVideoUrl(str(param.get("vc")).replace("bilibili",""));

# 获取今天的背景
@app.route(rule='/car08-webservice/getBingBackImgAndStoryUrl', methods=['GET'])
def getBingBackImgAndStoryUrl():
    return Util.getBingBackImgAndStoryUrl(0)

# 获取今天的背景
@app.route(rule='/car08-webservice/getBingBackImgStoryHtml', methods=['POST'])
def getBingBackImgStoryHtml():
    param = request.json;
    if not param or "currentDate" not in param:
        abort(400);
    else:
        return Util.getBingBackImgStoryHtml(str(param.get("currentDate")))

