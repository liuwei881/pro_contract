$(document).ready(function() {  
            var name = getCookie("myChk");
            //$("#username")[0].value=name;   
            $("#myChk").val(name);
  
            /* 
            * 当点击登录按钮时 判断是否勾选记住用户名  
            * 如果勾选  则将用户名保存在Cookie中 否则删除  
            */  
            $("#sub").click(function() {  
                if ($("#myChk").attr("checked") == true) {
                    //获得用户名   
                    var username = $("#myChk").val();
                    //设置cookie  
                    setCookie("myChk", username);
                } else {  
                    //删除cookie  
                    delCookie("myChk")
                }  
            })  
            function setCookie(name, value) {  
                var Days = 60; //cookie 将被保存两个月   
                var exp = new Date(); //获得当前时间   
                exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000); //换成毫秒  
                document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();  
            }  
            function getCookie(name) {  
                //取出cookie   
                var strCookie = document.cookie;  
                //cookie的保存格式是 分号加空格 "; "  
                var arrCookie = strCookie.split("; ");  
                for ( var i = 0; i < arrCookie.length; i++) {  
                    var arr = arrCookie[i].split("=");  
                    if (arr[0] == "myChk") {
                        return arr[1];  
                    }  
                }  
                return "";  
            }  
            function delCookie(name) {  
                var exp = new Date(); //当前时间   
                exp.setTime(exp.getTime() - 1); //删除cookie 只需将cookie设置为过去的时间    
                var cval = getCookie(name);  
                if (cval != null)  
                    document.cookie = name + "=" + cval + ";expires="+ exp.toGMTString();  
            }  
        })  