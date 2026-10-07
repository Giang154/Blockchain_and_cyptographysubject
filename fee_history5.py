from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

# Kết nối RPC TrustKeys L1
rpc_url = "https://l1testnet.trustkeys.network"
w3 = Web3(Web3.HTTPProvider(rpc_url))

# Bắt buộc nạp middleware PoA để tránh ExtraDataLengthError
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

# Lấy block mới nhất
blk = w3.eth.get_block("latest")
base_fee = blk.get("baseFeePerGas", 0)
print(f"Connected: {w3.is_connected()}")
print(f"Latest Block: {blk['number']}")
print(f"baseFeePerGas = {base_fee} wei ({w3.from_wei(base_fee, 'gwei')} gwei)\n")

# Lấy lịch sử 20 block gần nhất
fh = w3.eth.fee_history(20, "latest", [10, 50, 90])
oldest = fh["oldestBlock"]

print(f"{'Block':<10} | {'Base Fee (wei)':<15} | {'Gas Used Ratio':<15}")
print("-" * 45)
for i, base in enumerate(fh["baseFeePerGas"][:-1]):
    ratio = fh["gasUsedRatio"][i]
    print(f"{oldest + i:<10} | {base:<15} | {ratio:.2%}")

# Đánh giá trạng thái mạng
avg_ratio = sum(fh["gasUsedRatio"]) / len(fh["gasUsedRatio"])
verdict = "BUSY" if avg_ratio > 0.5 else "quiet"
print(f"\nAverage Gas Used Ratio: {avg_ratio:.2%}")
print(f"Verdict: Chain is {verdict}")