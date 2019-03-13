/**
 * 创建websocket对象,并传入对应事件的回调函数
 * @param {*} name 
 * @param {*} ws 
 * @param {*} onopen 
 * @param {*} onclose 
 * @param {*} onerror 
 * @param {*} onmessage 
 */
var createWebSocket = function(name,ws,onopen,onclose,onerror,onmessage){
    var socket = new WebSocket(ws,"cat08");//设置自定义子协议名称
    var int = null;
    socket.onopen = function(){
        console.log("WebSocket,建立连接成功,[" + name +"]");
        if(onopen){
            onopen();
        }
        int = setInterval(function(){
            send("a","");
        },30000);//三十秒心跳一次,防止nginx代理超时,没有用nginx可以去掉
    }; 
    socket.onclose = function(event){
        console.log("WebSocket,已关闭,[" + name +"]");
        if(onclose){
            onclose();
        }
        window.clearInterval(int);//关闭定时器
    }; 
    socket.onerror = function(event){
        console.log("WebSocket,异常,[" + name +"]");
        if(onerror){
            onerror();
        }
    };
    socket.onmessage = function(event){
        if(onmessage){
            onmessage(event.data);
        }
    };
    var send = function(type,msg){
        var max = 5;//前五个字节表示本条业务数据的字节长度,不足5个长度则补0,与服务端保持一致
        var msgSize = ("" + msg).getBytesLength() + "";
        for (var i = msgSize.length; i < max;i++){
            msgSize = "0" + msgSize;
        }
        socket.send(msgSize + type + msg);
    }
    return {"send":send};
}
