const fyers   = require("fyers-api-v2")
const url = require('url');
const fs = require('fs');

const app_id = "DO3OHPAO1D-100";
const redirect_url = "https://trade.fyers.in/api-login/redirect-uri/index.html";
const key = "6WMPXU4GKD";
var posId ="";

function setAccessTokenForMe(){
    fyers.setAppId(app_id);
    fyers.setRedirectUrl(redirect_url);
    fyers.generateAuthCode();
    const prompt = require("prompt-sync")({ sigint: true });
    //With readline
    const code = prompt("Enter Auth Code");
    const reqBody = {
        auth_code:code,
        secret_key:key
    }

    fyers.generate_access_token(reqBody).then((response)=>{
    console.log(response);
    var token=""+response.access_token;
    fs.writeFile('./accessToken.txt', token, err => {
        if (err) {
            console.error(err);
        }else{
            console.log("file written successfully");
        }
  // file written successfully
    });

})
}
setAccessTokenForMe();