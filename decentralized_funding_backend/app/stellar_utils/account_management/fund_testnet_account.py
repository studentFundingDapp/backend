import requests

def fund_testnet_account(public_key: str):
    """Funds a Testnet account using Friendbot."""
    friendbot_url = f"https://friendbot.stellar.org/?addr={public_key}"
    try:
        response = requests.get(friendbot_url)
        response.raise_for_status() # Raise an exception for bad status codes
        print(f"Friendbot response: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error funding account with Friendbot: {e}")
        return False

# Example usage after creating keypair:
# success = fund_testnet_account(new_account_keys["public_key"])
# if success:
#     print("Account funded on Testnet.")
# else:
#     print("Failed to fund account on Testnet.")