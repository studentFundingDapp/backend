# Assuming 'server' is initialized from 2.1.2
from stellar_sdk.exceptions import NotFoundError

def get_account_balances(account_id: str):
    """Queries the balances for a given Stellar account ID."""
    try:
        account = server.load_account(account_id=account_id)
        balances = account.balances
        return balances # This is a list of Balance objects
    except NotFoundError:
        print(f"Account {account_id} not found on the network.")
        return None
    except Exception as e:
        print(f"Error fetching account balances: {e}")
        return None

# Example usage:
# student_public_key = "G..." # Get from your database
# account_info = get_account_balances(student_public_key)
# if account_info:
#     for balance in account_info:
#         print(f"Asset: {balance.asset_code}, Balance: {balance.balance}")