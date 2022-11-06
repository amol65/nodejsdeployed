public class FYERS
{

    public static void main(String args[])  //static method
    {
        String client_id-"DO3OHPAO1D-100";
        String redirect_uri-"https://trade.fyers.in/api-login/redirect-uri/index.html";
        curl  https://api.fyers.in/api/v2/generate-authcode?client_id=sample_client_id&  redirect_uri=redirect_uri&response_type=code&state=sample_state

        System.out.println("Static method");
    }
}