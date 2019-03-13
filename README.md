# cat08

www.cat08.com 猫8(￣３￣)a专业的吸猫场所.

里面有很多猫猫视频,累了就看看小猫咪吧,内容资源均来自bilibili,我自己也有一些投稿.

功能

  1.嵌入了几个搜索平台的搜索功能
	
  2.bilibili真实视频地址解析播放
	
  3.webrtc 网页在线聊天,目前只有一对一视频,语音,文字聊天,可以传输文件,需要看多人版的去 https://github.com/js1688/cat 老版本java后台的
	
  4.壁纸取自bing每日一换,每日一个壁纸故事,由于租用服务器能力问题,暂没有将所有高清壁纸缓存起来提供对外访问的api
 
运用到的技术

  1.html + css + jquery
	
  2.python
	
  3.webrtc
	
  4.elasticsearch
	
  5.nginx
  
整体架构

  1.html + css + jquery  前端代码
	
  2.nginx 各服务端代理,https协议,前端代码服务
	
  3.python bilibili内容爬虫,各功能api服务,webrtc信令服务
  
项目包说明

  1.cat08_client   前端代码
	
  2.cat08_spider   bilibili爬虫
	
  3.cat08_webservice    功能接口服务
	
  4.cat08_websocket    webrtc信令服务
