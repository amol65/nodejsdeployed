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
        }
  // file written successfully
    });

})
}

function exitAllPositions(profit, loss, i){
        fyers.get_positions().then((response) => {
            var pl_total = response.overall.pl_total;
            console.log("P&L at "+i +" seconds = " +pl_total);
            if (pl_total <= loss || pl_total >= profit ){
                const reqBody = {
                     data:{},
                     app_id:app_id,
                     token:accessToken
                }
                const exitPosition=fyers.exit_position(reqBody).then((response) => {
                             console.log(response)
                })
            }

        })
}

function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
}

function getOpenPositions(){
    var positionList=[];
    fyers.get_positions().then((response) => {
        var positions = response.netPositions;
        for(let i=0; i<positions.length; i++){
            if (positions[i].realized_profit != positions[i].pl){
                   positionList.push(positions[i].id);
              }
        }
    })
    return positionList;
}


function exitIndividualPositions(posId, profit, loss,i){
    fyers.get_positions().then((response) => {
            var positions = response.netPositions;
            for(let i=0; i<positions.length; i++){
                if(posId == positions[i].id){
                var pl_individual = positions[i].pl;
                console.log("Individual P&L at "+i +" seconds = " +pl_individual);
                    if(pl_individual <= loss || pl_individual >= profit){
                    const reqBody = {
                                      data:{"id":posId},
                                      app_id:app_id,
                                      token:accessToken
                                }
                                const exitPosition = fyers.exit_position(reqBody).then((response) => {
                                                   console.log(response)
                                })
                    }

                }
            }
        })
    }

async function Tutor() {
   for (let i = 1; i <=60*2 ; i++) {
       await sleep(1000);
       exitAllPositions(profit, loss,i);
     //  if(isEmpty(getOpenPositions())){
      //     console.log("All positions are closed: ");
       //    break;
     //  }
//       exitIndividualPositions(posId,profit,loss,i);
   }
}

function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}

//setAccessTokenForMe();

fyers.setAppId(app_id);
fyers.setRedirectUrl(redirect_url);
fs.readFile('./accessToken.txt', 'utf8', (err, data) => {
                       if (err) {
                         console.error(err);
                         return;
                       }
                       fyers.setAccessToken(data);
                     });

const prompt = require("prompt-sync")({ sigint: true });
//With readline
let profit = Number(prompt("Enter profit you want: "));
let loss = 0-Number(prompt("Enter loss you can take: "));
console.log(loss);
Tutor();


