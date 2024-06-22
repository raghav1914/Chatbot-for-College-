import requests

RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

def get_response_from_rasa(message, sender_id="user"):
    payload = {
        "sender": sender_id,
        "message": message
    }
    try:
        response = requests.post(RASA_SERVER_URL, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        response_json = response.json()
        print("Rasa Response JSON:", response_json)  # Print the full response for debugging
        if response_json and 'text' in response_json[0]:
            return response_json[0]['text']
        else:
            return "No response from bot"
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return f"Error: {e}"
    except (IndexError, KeyError) as e:
        print(f"Error parsing response JSON: {e}")
        return f"Error parsing response JSON: {e}"