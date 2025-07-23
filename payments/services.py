import requests
import base64
from datetime import datetime
from decouple import config

def get_mpesa_access_token():
    consumer_key = config('MPESA_CONSUMER_KEY')
    consumer_secret = config('MPESA_CONSUMER_SECRET')
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    r = requests.get(api_url, auth=(consumer_key, consumer_secret))
    return r.json().get('access_token')

def lipa_na_mpesa_online(phone_number, amount, order_id):
    access_token = get_mpesa_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    headers = {"Authorization": "Bearer %s" % access_token}
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = config('MPESA_SHORTCODE')
    passkey = config('MPESA_PASSKEY')
    
    password_str = shortcode + passkey + timestamp
    password = base64.b64encode(password_str.encode('ascii')).decode('utf-8')
    
    safaricom_phone = f"254{phone_number[-9:]}"
    callback_url = config('MPESA_CALLBACK_URL') # e.g. https://mydomain.com/api/v1/payments/callback/
    
    request = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": str(int(amount)),
        "PartyA": safaricom_phone,
        "PartyB": shortcode,
        "PhoneNumber": safaricom_phone,
        "CallBackURL": callback_url,
        "AccountReference": str(order_id),
        "TransactionDesc": f"Payment for Farmart Order #{order_id}"
    }
    
    response = requests.post(api_url, json=request, headers=headers)
    return response.json()