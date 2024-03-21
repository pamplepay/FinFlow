// 아이디 validation
$(function() {
    $('[name="user_id"]').blur(function() {
        var user_id=$('[name="user_id"]').val()

        if (user_id.length<4 || user_id.length>16) {
            document.getElementById("id_error").innerHTML=
            "아이디 길이는 4~15자 사이여야 합니다.";
        }
        else {
            document.getElementById("id_error").innerHTML=
            "";

            $.ajax({
                type: "POST",
                url: "/api/v1/id-validation",
                data: {'user_id' : user_id},
                success: function(response) {

                    if (response.data == "exist") {
                        document.getElementById("id_error").innerHTML=
                        "중복되는 아이디 입니다. 다른 아이디를 사용해주세요.";
                    }
                    else {
                        document.getElementById("id_error").innerHTML=
                        "";
                    }
                },
                error: function(error) {
                    console.log("ID validation error!");
                }
            });
        }
    });
});

// 비밀번호 유효식 check
$(function() {
    $('[name="password2"]').blur(function() {
        var password2=$('[name="password2"]').val()
        const check_num = /^[0-9]+$/;
        const check_str = /^(?:[a-zA-Z\[\]\^\$\.\|\?\*\+\(\)\\~`\!@#%&\-_+={}'""<>:;,\n]+)$/;

        if (password2.length<8){
            document.getElementById("pw2_error").innerHTML=
            "비밀번호가 너무 짧습니다. 최소 8문자를 포함해야 합니다.";
        }
        else if(check_num.test(password2)){
            document.getElementById("pw2_error").innerHTML=
            "비밀번호는 숫자, 문자를 모두 포함해야합니다.";
        }
        else if(check_str.test(password2)){
            document.getElementById("pw2_error").innerHTML=
            "비밀번호는 숫자, 문자를 모두 포함해야합니다.";
        }
        else{
            document.getElementById("pw2_error").innerHTML=
            "";
        }
    });
});

// 비밀번호 확인
$(function() {
    $('[name="password1"]').blur(function() {
        var password1=$('[name="password1"]').val()
        var password2=$('[name="password2"]').val()

        if (password1 == password2) {
            document.getElementById("pw1_error").innerHTML=
            "";
        }
        else {
            document.getElementById("pw1_error").innerHTML=
            "비밀번호가 일치하지 않습니다.";
        }
    });
});

// 휴대폰 번호
$(function() {
    $('[name="hp"]').blur(function() {
        var hp=$('[name="hp"]').val()
        var patternPhone = /^01[016789]([0-9]{7,8})/;

        if (!patternPhone.test(hp)){
            document.getElementById("hp_error").innerHTML=
            "휴대폰번호 형식을 맞춰주세요.";
        }
        else{
            $.ajax({
                type: "POST",
                url: "/api/v1/hp-validation",
                data: {'hp' : hp},
                success: function(response) {
                    if (response.data == "exist") {
                        document.getElementById("hp_error").innerHTML=
                        "중복되는 번호입니다. 아이디 찾기를 이용해주세요.";
                    }
                    else{
                        document.getElementById("hp_error").innerHTML=
                        "";
                    }
                },
                error: function(error) {
                    console.log("HP validation error!");
                }
            });
        }
    });
});

// 인증번호 전송
function btnActive(){
    var hp=$('[name="hp"]').val()
    var patternPhone = /^01[016789]([0-9]{7,8})/;

    if (patternPhone.test(hp) && document.getElementById("hp_error").innerHTML=="") {
        const target = document.getElementById('id_auth');
        target.disabled = false;

        const txc = document.getElementById('timerDisplay');
        txc.style.color = "red";

        var minutes = 5;
        var seconds = 0;
        
        var timerId = setInterval(function() {
            if (minutes === 0 && seconds === 0) {
                clearInterval(timerId);
                txc.style.color = "rgba(255, 162, 162, 0.664)";
                return;
            }
            
            if (seconds === 0) {
                minutes--;
                seconds = 59;
            }
            else {
                seconds--;
            }
        
            document.getElementById("timerDisplay").innerHTML =
            minutes + ":" + (seconds < 10 ? "0" + seconds : seconds);}, 1000);
    }
}