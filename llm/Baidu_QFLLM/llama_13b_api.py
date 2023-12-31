import requests
import json

API_KEY = "Your Key"

SECRET_KEY = "Your Secret"

def get_access_token():
        
    url = f"https://aip.baidubce.com/oauth/2.0/token?client_id={API_KEY}&client_secret={SECRET_KEY}&grant_type=client_credentials"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers = headers, data = payload)
    
    return response.json().get("access_token")
    
def entry(content: str) -> str:
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/llama_2_13b?access_token=" + get_access_token()
    
    payload = json.dumps({
         "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers = headers, data = payload)
    
    return response.json()["result"]

if __name__ == '__main__':
    entry()
