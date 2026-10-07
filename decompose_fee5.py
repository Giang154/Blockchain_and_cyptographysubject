from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

# Kết nối RPC TrustKeys L1
rpc_url = "https://l1testnet.trustkeys.network"
w3 = Web3(Web3.HTTPProvider(rpc_url))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

# Dán hash giao dịch thật vừa copy vào đây
tx_hash = "0xc11206175951dd046bb21dccd6d1228630d687562c89854d30b1448a23130f86" 

rcpt = w3.eth.get_transaction_receipt(tx_hash)
tx = w3.eth.get_transaction(tx_hash)
blk = w3.eth.get_block(rcpt["blockNumber"])

base_fee = blk["baseFeePerGas"]
gas_used = rcpt["gasUsed"]
eff_price = rcpt["effectiveGasPrice"]

paid = gas_used * eff_price
burned = gas_used * base_fee
tip = gas_used * (eff_price - base_fee)

print(f"Transaction Hash : {tx_hash}")
print(f"Gas used         : {gas_used}")
print(f"Base fee per gas : {base_fee} wei")
print(f"Effective price  : {eff_price} wei")
print("-" * 50)
print(f"Paid   : {paid} wei")
print(f"Burned : {burned} wei (rời khỏi lưu thông)")
print(f"Tip    : {tip} wei (trả cho proposer)")
print(f"CHECK  : paid == burned + tip ? -> {paid == burned + tip}")