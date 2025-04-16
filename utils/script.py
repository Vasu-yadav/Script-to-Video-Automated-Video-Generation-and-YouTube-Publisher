import requests
import json

def get_script(topic):
    """
    Call the script generation API with the given topic
    
    Args:
        topic (str): The topic to generate a script about
        debug_mode (bool): Whether to enable debug mode
        base_url (str): Base URL of the API
        
    Returns:
        dict: The API response
    """

    debug_mode=True
    base_url="http://localhost:1502"

    endpoint = f"{base_url}/generate-script"
    
    payload = {
        "topic": topic,
        "debug_mode": debug_mode
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    proxies = {
            'http': None,
            'https': None
        }
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload), proxies=proxies)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        return data["content"]
    else:
        raise Exception(f"API call failed with status code {response.status_code}")