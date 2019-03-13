/**
 * 获取cat08搜索视频展示行模版
 * @param {string,视频id} id
 * @param {string,视频地址} videoUrl 
 * @param {string,快照图片地址} coversUrl 
 * @param {string,标题} title 
 * @param {string,作者} author 
 * @param {long,创建时间戳} createTime 
 * @param {string,视频长度} length 
 * @param {long,播放量} playAmount 
 */
var getCat08VideoRow = function (id,videoUrl,coversUrl,title,author,createTime,length,playAmount,desc) {
    var temp = "<div data_title=\"replace_title\" data_videoUrl=\"replace_videoUrl\" data_desc=\"replace_desc\" data_id=\"replace_id\" class=\"showVideo\"><img src=\"replace_coversUrl\" style=\"float: left;\"  width=\"150px;\" height=\"100px;\"/><table class=\"cat08show_table\"><tr><th>标题:</th><td colspan=\"2\">replace_title</td></tr><tr><th>作者:</th><td colspan=\"2\">replace_author</td></tr><tr><th>时间:</th><td colspan=\"2\">replace_createTime</td></tr><tr><th>时长:</th><td colspan=\"2\">replace_length</td></tr><tr><th>播放:</th><td>replace_playAmount</td><td><img src=\"images/type_video.png\" style=\"float:right;\"/></td></tr></table></div>";
    temp = temp.replace(/replace_id/g,id);
    temp = temp.replace(/replace_videoUrl/g,videoUrl);
    temp = temp.replace(/replace_desc/g,desc);
    temp = temp.replace(/replace_coversUrl/g,coversUrl);
    temp = temp.replace(/replace_title/g,title);
    temp = temp.replace(/replace_author/g,author);
    createTime = timeToYYYY_MM_DD_HH_mm_ss(createTime);
    temp = temp.replace(/replace_createTime/g,createTime);
    temp = temp.replace(/replace_length/g,length);
    temp = temp.replace(/replace_playAmount/g,playAmount);
    return temp;
}

/**
 * 获取cat08搜索文章展示行模版
 * @param {string,文章id} id 
 * @param {string,标题} title 
 * @param {string,作者} author 
 * @param {string,摘要} summary 
 * @param {string,封面地址} banner_url 
 * @param {string,创建时间戳} ctime 
 * @param {long,字数} words 
 * @param {string,原文章地址} url 
 * @param {long,阅读量} view 
 */
var getCat08ArticleRow = function(id,title,author,summary,banner_url,ctime,words,url,view){
    var temp = "<a href=\"replace_url\" target=\"_blank\" ><div data_title=\"replace_title\" data_videoUrl=\"replace_url\" data_desc=\"replace_summary\" data_id=\"replace_id\" class=\"showArticle\"><img src=\"replace_banner_url\" style=\"float: left;\"  width=\"150px;\" height=\"100px;\"/><table class=\"cat08show_table\"><tr><th>标题:</th><td colspan=\"2\">replace_title</td></tr><tr><th>作者:</th><td colspan=\"2\">replace_author</td></tr><tr><th>时间:</th><td colspan=\"2\">replace_ctime</td></tr><tr><th>字数:</th><td colspan=\"2\">replace_words</td></tr><tr><th>阅读:</th><td>replace_view</td><td><img src=\"images/type_article.png\" style=\"float:right;\"/></td></tr></table></div></a>";
    temp = temp.replace(/replace_id/g,id);
    temp = temp.replace(/replace_url/g,url);
    temp = temp.replace(/replace_summary/g,summary);
    temp = temp.replace(/replace_banner_url/g,banner_url);
    temp = temp.replace(/replace_title/g,title);
    temp = temp.replace(/replace_author/g,author);
    createTime = timeToYYYY_MM_DD_HH_mm_ss(ctime);
    temp = temp.replace(/replace_ctime/g,createTime);
    temp = temp.replace(/replace_words/g,words);
    temp = temp.replace(/replace_view/g,view);
    return temp;
}

/**
 * 获取cat08搜索小视频展示行模版
 * @param {string,视频id} id
 * @param {string,视频地址} videoUrl 
 * @param {string,快照图片地址} coversUrl 
 * @param {string,标题} title 
 * @param {string,作者} author 
 * @param {long,创建时间戳} createTime 
 * @param {string,视频长度} length 
 * @param {long,播放量} playAmount 
 */
var getCat08MinVideoRow = function (id,url,default0,title,uname,timestamp,video_time,watched_num) {
    var temp = "<div data_title=\"replace_title\" data_url=\"replace_url\" data_id=\"replace_id\" class=\"showMinideo\"><img src=\"replace_default\" style=\"float: left;\"  width=\"150px;\" height=\"100px;\"/><table class=\"cat08show_table\"><tr><th>标题:</th><td colspan=\"2\">replace_title</td></tr><tr><th>作者:</th><td colspan=\"2\">replace_uname</td></tr><tr><th>时间:</th><td colspan=\"2\">replace_timestamp</td></tr><tr><th>时长:</th><td colspan=\"2\">replace_video_time 秒</td></tr><tr><th>播放:</th><td>replace_watched_num</td><td><img src=\"images/type_video.png\" style=\"float:right;\"/></td></tr></table></div>";
    temp = temp.replace(/replace_id/g,id);
    temp = temp.replace(/replace_url/g,url);
    temp = temp.replace(/replace_default/g,default0);
    temp = temp.replace(/replace_title/g,title);
    temp = temp.replace(/replace_uname/g,uname);
    createTime = timeToYYYY_MM_DD_HH_mm_ss(timestamp);
    temp = temp.replace(/replace_timestamp/g,createTime);
    temp = temp.replace(/replace_video_time/g,video_time);
    temp = temp.replace(/replace_watched_num/g,watched_num);
    return temp;
}