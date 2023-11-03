var datekey = CryptoJS.enc.Utf8.parse('dacf107e4bdbbef0');
var dateiv = CryptoJS.enc.Utf8.parse('bcancid682e09aec');
function em(param) {
data:{'username':em(username)+'','password':em(password)+'','yzm':yzm,'convHtmlField':'username,password','loginType':'pcLogin','sessionID':sessionID},
    param = CryptoJS.AES.encrypt(param, datekey, {
        iv: dateiv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return param
}
function dm(param) {
    param = CryptoJS.AES.decrypt(param, datekey, {
        iv: dateiv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return param.toString(CryptoJS.enc.Utf8)
}
