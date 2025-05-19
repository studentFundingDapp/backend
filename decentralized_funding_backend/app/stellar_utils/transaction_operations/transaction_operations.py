# app/stellar_utils/stellar_transactions.py or update your existing transaction_operations.py

from stellar_sdk import Server, Keypair, TransactionBuilder, Payment, Network, Asset
# Removing SubmitTransactionError import as it consistently fails in your environment
# We will handle submission errors using a general Exception catch.
from stellar_sdk.exceptions import NotFoundError

# --- Configuration ---
# Assuming your Horizon URL and Network Passphrase are configured elsewhere
# e.g., in app/stellar_utils/connection.py or config.py
# Ensure these match your Testnet setup as in the working code snippet you provided.
# Example content for app/stellar_utils/connection.py:
HORIZON_URL = "https://horizon-testnet.stellar.org"
NETWORK_PASSPHRASE = Network.TESTNET_NETWORK_PASSPHRASE # Or "Test SDF Network ; September 2015" if Network.TESTNET_NETWORK_PASSPHRASE fails
# from .connection import HORIZON_URL, NETWORK_PASSPHRASE


# Modified to align with the synchronous working code snippet provided by the user,
# while keeping the async structure for FastAPI integration.
# Note: Removing 'await' from load_account and fetch_base_fee might not be
# standard for async SDK usage but matches the user's working example behavior.
async def send_stellar_payment(
    source_secret: str,
    destination_public: str,
    amount: str, # Amount must be a string
    asset_code: str = "XLM",
    asset_issuer: str = None, # Required for non-XLM assets
    memo_text: str = None # Optional memo
):
    """Sends a Stellar payment from a source account (using its secret key)
       to a destination account.
    """
    try:
        # Initialize Server. Network passphrase will be set in TransactionBuilder opts.
        server = Server(horizon_url=HORIZON_URL)

        # 1. Get the source account keypair from the secret key
        source_keypair = Keypair.from_secret(source_secret)
        source_public = source_keypair.public_key # Get public key from keypair
        print(f"Using source public key derived from secret key: {source_public}")

        # 2. Load the source account from Horizon to get its current sequence number
        # Aligning with user's working code - removed 'await'.
        # This might behave synchronously in certain SDK/environment configurations.
        source_account = server.load_account(account_id=source_public)
        print(f"Source account {source_public} loaded. Sequence number: {source_account.sequence}")

        # 3. Define the base fee (hardcoded as in user's working example)
        # Aligning with user's working code - hardcoded fee and removed 'await'.
        base_fee = 100
        print(f"Using hardcoded base fee: {base_fee}")


        # 4. Define the asset to send
        if asset_code == "XLM":
            asset_to_send = Asset.native() # Standard way to get native asset
        else:
            if not asset_issuer:
                raise ValueError("Asset issuer is required for non-XLM assets.")
            asset_to_send = Asset(code=asset_code, issuer=asset_issuer)

        # 5. Create a Payment operation
        payment_operation = Payment(
            destination=destination_public,
            asset=asset_to_send,
            amount=amount
        )
        print("Payment operation created.")

        # 6. Build the transaction
        transaction_builder = TransactionBuilder(
            source_account=source_account,
            opts={
                "fee": base_fee,
                # Pass network passphrase via opts as in user's working example
                "network_passphrase": NETWORK_PASSPHRASE,
                "timeout": 30, # Set a reasonable timeout
            },
        )
        # Use add_operation as it's general, though append_payment_op is also valid
        transaction_builder.add_operation(payment_operation)

        # Add memo if provided (using add_text_memo as in user's working example)
        if memo_text:
             transaction_builder.add_text_memo(memo_text)

        transaction = transaction_builder.build()
        print("Transaction built.")


        # 7. Sign the transaction with the source account's secret key
        transaction.sign(source_keypair)
        print("Transaction signed.")

        # 8. Submit the signed transaction to Horizon
        print("Submitting transaction to Horizon...")
        # Catch any exception during submission as SubmitTransactionError import fails
        # Using a general Exception catch as a fallback for submission errors
        try:
             response = await server.submit_transaction(transaction)
             print("\nTransaction successful!")
             print("Transaction hash:", response["hash"])
             print("Ledger:", response["ledger"])
             return {"hash": response["hash"], "successful": True, "error": None, "result_codes": None}
        except Exception as e: # This will catch SubmitTransactionError if it occurs but cannot be imported
            print(f"An error occurred during submission: {e}")
            # Note: Cannot reliably access e.extras.result_codes here without
            # a successful SubmitTransactionError import or type check.
            return {"hash": None, "successful": False, "error": str(e), "result_codes": None}


    except NotFoundError:
        print(f"Error: Source account {source_public} or destination account {destination_public} not found on the network or not funded (min 1 XLM).")
        return {"hash": None, "successful": False, "error": "Account not found or not funded."}
    except Exception as e:
        print(f"An error occurred during transaction preparation: {e}")
        return {"hash": None, "successful": False, "error": str(e)}

# --- You might also need a function to fund a new account ---
# This part remains similar to previous versions.
# app/stellar_utils/account_management.py (or similar)

# from stellar_sdk import Server, Network, Keypair, Operation
# import requests
#
# # Assuming HORIZON_URL and NETWORK_PASSPHRASE are imported from connection.py
# from .connection import HORIZON_URL, NETWORK_PASSPHRASE
#
# async def fund_testnet_account(public_key: str):
#     """Funds a Testnet account using Friendbot."""
#     # Note: This function might still need Network.TESTNET_PASSPHRASE if it uses Network checks
#     # or if Friendbot interaction requires specific network context.
#     # If Network.TESTNET_PASSPHRASE is unavailable, you might need to hardcode the passphrase string here too.
#     try:
#         # Attempt to use standard Network attribute if available
#         testnet_passphrase_check = Network.TESTNET_PASSPHRASE
#     except AttributeError:
#         # Fallback to string literal if attribute is missing
#         testnet_passphrase_check = "Test SDF Network ; September 2015"
#
#     if NETWORK_PASSPHRASE != testnet_passphrase_check:
#         print("Friendbot is only available on Testnet.")
#         return False
#
#     friendbot_url = f"https://friendbot.stellar.org/?addr={public_key}"
#     try:
#         # Using asyncio with requests might require a library like aiohttp or running in executor
#         # For simplicity, using sync requests here, but be mindful in an async FastAPI app
#         import requests # Ensure requests is imported if needed here
#         response = requests.get(friendbot_url)
#         response.raise_for_status() # Raise an exception for bad status codes
#         print(f"Friendbot response for {public_key}: {response.json()}")
#         return True
#     except requests.exceptions.RequestException as e:
#         print(f"Error funding account {public_key} with Friendbot: {e}")
#         return False
#
# async def fund_public_network_account(
#     source_secret: str, # Your app's funded account secret key
#     new_account_public_key: str,
#     starting_balance: str = "1.5" # Minimum required balance + some buffer
# ):
#     """Creates and funds a new account on the Public Network from a source account."""
#     try:
#         server = Server(horizon_url=HORIZON_URL)
#         # Use standard Network.use_network_passphrase if available, or pass in opts
#         try:
#             Network.use_network_passphrase(NETWORK_PASSPHRASE)
#         except AttributeError:
#             pass # Rely on opts
#
#         source_keypair = Keypair.from_secret(source_secret)
#         # This requires 'await' for async methods in standard SDK versions
#         source_account = await server.load_account(account_id=source_keypair.public_key)
#
#         # Create the CreateAccount operation
#         create_account_op = Operation.create_account(
#             account_id=new_account_public_key,
#             starting_balance=starting_balance
#         )
#
#         # Build, sign, and submit the transaction from the source account
#         # This requires 'await' for async methods in standard SDK versions
#         base_fee = await server.fetch_base_fee()
#         transaction = (
#             TransactionBuilder(
#                 source_account=source_account,
#                 opts={"fee": base_fee, "network_passphrase": NETWORK_PASSPHRASE, "timeout": 30},
#             )
#             .add_operation(create_account_op)
#             .build()
#         )
#
#         transaction.sign(source_keypair)
#         response = await server.submit_transaction(transaction)
#         print(f"Account creation transaction successful: {response['hash']}")
#         return True
#
#     except Exception as e:
#         print(f"Error creating and funding public network account {new_account_public_key}: {e}")
#         return False
