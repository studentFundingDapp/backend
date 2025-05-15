from stellar_sdk import Operation, Asset

def create_payment_operation(destination_public_key: str, amount: str, asset_code: str = "XLM", asset_issuer: str = None):
    """Creates a Payment operation."""
    # amount must be a string
    if asset_code == "XLM":
        asset = Asset.native()
    else:
        if not asset_issuer:
             raise ValueError("Asset issuer is required for non-XLM assets.")
        asset = Asset(code=asset_code, issuer=asset_issuer)

    return Operation.payment(
        destination=destination_public_key,
        asset=asset,
        amount=amount
    )

# Example usage (sending 10 XLM):
# payment_op = create_payment_operation("GDESTINATION...", "10.0")

# Example usage (sending 50 USDC):
# usdc_issuer = "GA5ZSEJYB37JRC5SDYBYSSLKYAUT23PKYAQUM2SYWUE5MSULDDKH2JNQ" # Example USDC issuer on Testnet
# usdc_payment_op = create_payment_operation("GDESTINATION...", "50.0", asset_code="USDC", asset_issuer=usdc_issuer)