var localhostHttpPath = "http://127.0.0.1:1400";
var domainHttpPath = "https://www.cat08.com";
var path = domainHttpPath;
/**
 * 搜索猫8的数据,并展示
 * @param {int,第几页,0为第一页} pageindex 
 * @param {int,页大小} pagesize 
 * @param {string,查询数据类型} type
 */
var cat08Search = function(pageindex,pagesize,value,type){
    $.ajax({
        type: "post",
        url:path + "/car08-webservice/search",
        contentType: "application/json;charset=utf-8",
        data :JSON.stringify({"pageindex":pageindex,"pagesize":pagesize,"value":value,"type":type}),
        dataType: "json",
        async: false,
        success: function (data) {
            for(var i = 0; i < data.body.length; i++){
                var body = data.body[i];
                var row = null;
                //区分数据类型
                if("video" == body._type){
                    row = getCat08VideoRow(body._source.id,body._source.videoUrl,body._source.coversUrl,body._source.title,body._source.author,body._source.createTime,body._source.length,body._source.playAmount,body._source.desc);
                }else if("article" == body._type){
                    row = getCat08ArticleRow(body._source.id,body._source.title,body._source.author,body._source.summary,body._source.banner_url,body._source.ctime,body._source.words,body._source.url,body._source.view);
                }else if("minvideo" == body._type){
                    row = getCat08MinVideoRow(body._source.id,body._source.url,body._source.default,body._source.title,body._source.uname,body._source.timestamp,body._source.video_time,body._source.watched_num);
                }
                $(".cat08show").append(row);
            }
            showVideoOnClick();
            showMinVideoOnClick();
        }
    });
}

/**
 * 通过av号查询到视频真实地址
 * @param { string} id 哔哩哔哩动画视频av号
 */
var getBilibiliVideoUrl = function(id){
    var videoUrl = null;
    $.ajax({
        type: "post",
        url:path + "/car08-webservice/getBilibiliVideoUrl",
        contentType: "application/json;charset=utf-8",
        data :JSON.stringify({"av":id}),
        dataType: "text",
        async: false,
        success: function (data) {
            videoUrl = data;
        }
    });
    return videoUrl;
}

/**
 * 通过vc号查询到小视频真实地址
 * @param { string} id 哔哩哔哩动画视频vc号
 */
var getBilibiliMinVideoUrl = function(id){
    var videoUrl = null;
    $.ajax({
        type: "post",
        url:path + "/car08-webservice/getBilibiliMinVideoUrl",
        contentType: "application/json;charset=utf-8",
        data :JSON.stringify({"vc":id}),
        dataType: "text",
        async: false,
        success: function (data) {
            videoUrl = data;
        }
    });
    return videoUrl;
}

/**
 * 获取今天的背景图片
 */
var getBingBackImgAndStoryUrl = function(){
    var backInfo = null;
    $.ajax({
        type: "get",
        url:path + "/car08-webservice/getBingBackImgAndStoryUrl",
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        async: false,
        success: function (data) {
            backInfo = data;
        }
    });
    return backInfo;
}

/**
 * 获取图片的故事
 */
var getBingBackImgStoryHtml = function(currentDate){
    var ret = null;
    $.ajax({
        type: "post",
        url:path + "/car08-webservice/getBingBackImgStoryHtml",
        contentType: "application/json;charset=utf-8",
        data :JSON.stringify({"currentDate":currentDate}),
        dataType: "html",
        async: false,
        success: function (data) {
            ret = data;
        }
    });
    return ret;
}