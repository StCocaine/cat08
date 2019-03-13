/**
 * 查询数据只展示
 */
$(function(){
    //通知弹出
    $("#showTongzhi").off("click").on("click",function(){
        var data = {"title":"通知","list":[
            {"title":"测试欢迎通知","body":"欢迎来到猫8,后面会呈上精选的猫咪相关的视频,文章,后台还在开发中."},
            {"title":"2019年01月09日16:15:27 网页视频聊天室下载地址","body":"不提供网页视频聊天室在线体验了,<a href='https://github.com/js1688/cat/' target='_blank'>点击下载网页聊天室源码</a>"},
            {"title":"2019年01月19日15:45:03 后续规划","body":"优先级,<br/>1.丰富内容种类,后续增加音乐,文章,等类型.<br/>2.把封面背景弄起来,每天不一样的背景,一个背景一个小故事.<br/>3.尝试把视频播放的清晰度调高.<br/>4.提供与当前在线陌生人webrtc文字,视频,语音,文件传输等功能,<br/>5.提供程序员经常使用到的在线小工具"},
            {"title":"2019年01月22日19:13:11 1.2版本更新","body":"1.增加文章,小视频."},
            {"title":"2019年01月25日15:44:49 1.3版本更新","body":"增加bing搜索,搜索引擎最优选择是谷歌,但是因为谷歌搜索在中国没有服务器所以暂时不能使用,相比百度的不专业,以及广告满天飞,bing搜索是代替它的最好选择,bing是微软公司的产品.没有多余的广告,以及搜索的专业程度也是超越了百度,为什么百度不专业,是因为它的心思已经不再是做搜索上面了,所以你很难搜到想要的东西,所以默认搜索设置为bing."},
            {"title":"2019年01月31日17:33:04 1.4版本更新","body":"完善背景图片,数据取自bing,我觉得bing搜索的每天一个不一样的背景,并且告诉背景的来源,这个很好,所以搬过来了.(￣▽￣)"},
            {"title":"2019年03月11日20:03:03 1.5版本更新","body":"将以前做的webrtc网页聊天一对一版搬过来了,信令服务器用python做的,区域与以前基本上就是这个版本代码更好理解,源码后面会公布,python做信令服务器比java更麻烦一些,需要做一些稍微麻烦的动作."}
        ]};
        $("#showModal").find("h4[name='showTitle']").html(data.title);//更改标题
        var group = $("<div class='panel-group' id='tongzhi_list'>");
        for(var i = data.list.length - 1; -1 < i; i--){
            var defaultDiv = $("<div class='panel panel-default'>");
            var heading = $("<div class='panel-heading'>");
            var title = $("<h4 class='panel-title'>");
            var collapse_tile = $("<a data-toggle='collapse' data-parent='#tongzhi_list' href='#tongzhi_li_"+i+"'>");
            collapse_tile.html(data.list[i].title);
            title.append(collapse_tile);
            heading.append(title);
            defaultDiv.append(heading);
            var collapse_body = $("<div id='tongzhi_li_"+i+"' class='panel-collapse collapse "+(i == (data.list.length - 1) ? "in":"")+"'>");
            var collapse_body_body = $("<div class='panel-body'>");
            collapse_body_body.html(data.list[i].body);
            collapse_body.append(collapse_body_body);
            defaultDiv.append(collapse_body);
            group.append(defaultDiv);
        }
        $("#showModal").find("div[name='showBody']").html(group);//更改展示内容
        $("#showModal").modal('show');
    });
    //弹出设置主页方法
    $("#setHome").off("click").on("click",function(){
        $("#showModal").find("h4[name='showTitle']").html("将猫8设置成浏览器主页");//更改标题
        $("#showModal").find("div[name='showBody']").html("<a href='https://www.baidu.com/cache/sethelp/help.html' target='_blank'>打开百度设置参照</a>根据百度的提示一步步操作<br/>在填写网页地址的时候 由 <br/>https://www.baidu.com 改成 https://www.cat08.com");//更改展示内容
        $("#showModal").modal('show');
    });
    //弹出背景信息的由来
    $("#showBackgroundInfo").off("click").on("click",function(){
        $("#showModal").find("h4[name='showTitle']").html($("body").attr("backImageTitle"));//更改标题
        var body = $("#showModal").find("div[name='showBody']");
        body.html(getBingBackImgStoryHtml($("body").attr("currentDate")));//更改展示内容
        //#删除不必要的元素
        $("#hpBingAppQR").remove();
        $(".hplaCopy").remove();
        $("#hplaDL").remove();
        $("#showModal").modal('show');
    });
    //弹出二维码
    $("#showZanzhu").off("click").on("click",function(){
        $("#showModal").find("h4[name='showTitle']").html("谢谢鼓励,[woshitanjun@icloud.com]欢迎提建议.");//更改标题
        $("#showModal").find("div[name='showBody']").html("<div style='height:250px;'><img src='images/erweima/wx.JPG' width='250px;' height='250px;' style='float:left;'/><img src='images/erweima/zfb.JPG' width='250px;' height='250px;' style='float:right;'/>");//更改展示内容
        $("#showModal").modal('show');
    });
    //视频播放弹出被关闭后执行
    $('#videoModal').on('hidden.bs.modal', function () {
        $(this).find("video[name='video']").attr("src","");
        $(this).find("h6[name='title']").html("");
        $(this).find("a[name='videoUrl']").attr("href","");
        $(this).find("div[name='desc']").html("");
    })
});

/**
 * 给查询视频结果的每一行绑定点击事件
 */
var showVideoOnClick = function(){
    $(".showVideo").off("click").on("click",function(){
        var videoModal = $("#videoModal");
        videoUrl = getBilibiliVideoUrl($(this).attr("data_id"));
        videoModal.find("video[name='video']").attr("src",videoUrl);
        videoModal.find("h6[name='title']").html($(this).attr("data_title"));
        videoModal.find("a[name='videoUrl']").attr("href",$(this).attr("data_videoUrl"));
        videoModal.find("div[name='desc']").html($(this).attr("data_desc"));
        videoModal.modal('show');
    });
}

/**
 * 给查询视频结果的每一行绑定点击事件
 */
var showMinVideoOnClick = function(){
    $(".showMinideo").off("click").on("click",function(){
        var videoModal = $("#videoModal");
        videoUrl = getBilibiliMinVideoUrl($(this).attr("data_id"));
        videoModal.find("video[name='video']").attr("src",videoUrl);
        videoModal.find("h6[name='title']").html($(this).attr("data_title"));
        videoModal.find("a[name='videoUrl']").attr("href",$(this).attr("data_url"));
        videoModal.modal('show');
    });
}