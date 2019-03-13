/**
 * 各搜索按钮
 */
$(function(){
    //必应搜索
    $("#search_bing").off("click").on("click",function(){
        $("#search_bing_value").submit();
    });
    //百度搜索
    $("#search_baidu").off("click").on("click",function(){
        $("#search_baidu_value").submit();
    });

    //谷歌搜索
    $("#search_google").off("click").on("click",function(){
        $("#search_google_value").submit();
    });

    //cat08搜索
    $("#search_cat08").off("click").on("click",function(){
        cat08SearchGo(true);
    });

    //cat08文本框按回车,搜索
    $("#cat08").find("input[name='cat08_value']").off("keyup").on("keyup",function(){
        if(event.keyCode ==13){
            cat08SearchGo(true);
        }
    });

    //切换到cat08搜索,执行查询
    $("#cat08tab").on("shown.bs.tab", function(e){
        if($(".cat08show").html().length == 0){
            cat08SearchGo(true);
        }else{
            $(".cat08show").css("display","block");
            $(".typenav").css("display","block");
        }
    });

    //切换到百度搜索
    $("#baidutab").on("shown.bs.tab", function(e){
        $(".cat08show").css("display","none");
        $(".typenav").css("display","none");
    });

    //切换到谷歌搜索
    $("#googletab").on("shown.bs.tab", function(e){
        $(".cat08show").css("display","none");
        $(".typenav").css("display","none");
    });
    //切换到必应搜索
    $("#bingtab").on("shown.bs.tab", function(e){
        $(".cat08show").css("display","none");
        $(".typenav").css("display","none");
    });
    //cat08搜索,展示框滚动条到底部触发查询
    $(document).ready(function (){
        var nScrollHight = 0; //滚动距离总长(注意不是滚动条的长度)
        var nScrollTop = 0;   //滚动到的当前位置
        var nDivHight = $(".cat08show").height();
        $(".cat08show").off("scroll").on("scroll",function(){
          nScrollHight = $(this)[0].scrollHeight;
          nScrollTop = $(this)[0].scrollTop;
 　　　　　 var paddingBottom = parseInt( $(this).css('padding-bottom') ),paddingTop = parseInt( $(this).css('padding-top') );
          if(nScrollTop + paddingBottom + paddingTop + nDivHight >= nScrollHight){
            cat08SearchGo(false);
          }
        });
    });

    //cat08搜索类型切换事件
    $(".typenav").find("input[type='radio'][name='searchTypes']").off("change").on("change",function(){
        cat08SearchGo(true);
    });
});

/**
 * 执行查询
 * @param {bool,是否执行清除查询记录} clean 
 */
var index_page_pageindex = 0;
var index_page_pagesize = 10;
var cat08SearchGo = function(clean){
    if(clean){
        $(".cat08show").html("");//清理数据
        index_page_pageindex = 0;
        $(".cat08show")[0].scrollTop = 0;
    }else{
        index_page_pageindex += 1;
    }
    $(".cat08show").css("display","block");
    $(".typenav").css("display","block");
    var type = $(".typenav").find("input[type='radio'][name='searchTypes']:checked").val();
    cat08Search(index_page_pageindex,index_page_pagesize,$("#cat08").find("input[name='cat08_value']").val(),type);
}