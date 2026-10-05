
"""Lab 04 — STARTER. Complete the 3 TODOs, then run: all CHECK lines must print OK.

    python3 bitcoin_explorer_starter.py          # online (Internet)
    python3 bitcoin_explorer_starter.py --offline # replay from ./data/ (no Internet)

Only stdlib + requests (`pip install requests`). / Chỉ cần stdlib + requests.
API docs: https://github.com/Blockstream/esplora/blob/master/API.md
"""
import hashlib
import json
import os
import sys

API = "https://blockstream.info/api"  # mirror: https://mempool.space/api
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OFFLINE = "--offline" in sys.argv
PINNED_HEIGHT = 840_000  # the 2024 halving block / block halving 2024


def get(path: str, as_json: bool = True):
    """GET API+path (or replay the saved copy in ./data/ with --offline)."""
    if OFFLINE:
        fname = os.path.join(DATA, path.strip("/").replace("/", "_") + (".json" if as_json else ".txt"))
        with open(fname, "r", encoding="utf-8") as fh:
            return json.load(fh) if as_json else fh.read().strip()
    import requests
    r = requests.get(API + path, timeout=30)
    r.raise_for_status()
    return r.json() if as_json else r.text.strip()


def dsha256(b: bytes) -> bytes:
    """Bitcoin's double SHA-256. / SHA-256 kép của Bitcoin."""
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def check(name: str, ok: bool):
    print(f"  CHECK {name}: {'OK' if ok else 'FAIL'}")


#  Task 4.1
def task1():
    tip = int(get("/blocks/tip/height", as_json=False))
    print(f"chain tip height: {tip:,}")

    blk_hash = get(f"/block-height/{PINNED_HEIGHT}", as_json=False)
    blk = get(f"/block/{blk_hash}")
    print(f"block #{PINNED_HEIGHT:,}: {blk_hash}  bits=0x{blk['bits']:08x}")

    header = bytes.fromhex(get(f"/block/{blk_hash}/header", as_json=False))  # 80 bytes
    my_hash = dsha256(header)[::-1].hex()  # [::-1] = display order / thứ tự hiển thị
    check("recomputed hash == block id", my_hash == blk["id"])

    # ---- TODO 1: decode compact `bits` into the 256-bit target ------------
    exponent = blk["bits"] >> 24
    mantissa = blk["bits"] & 0xFFFFFF
    target = mantissa * (256 ** (exponent - 3))

    print(f"target = {target:064x}")
    check("PoW: int(hash) < target", int(my_hash, 16) < target)
    return blk_hash, blk


#  Task 4.2
def task2(blk_hash: str):
    txids = get(f"/block/{blk_hash}/txids")
    tx = get(f"/tx/{txids[1]}")  # first non-coinbase tx / tx thường đầu tiên

    # ---- TODO 2: compute the fee and the fee rate -------------------------
    total_input = sum(vin["prevout"]["value"] for vin in tx["vin"])
    total_output = sum(vout["value"] for vout in tx["vout"])
    fee = total_input - total_output
    vsize = (tx["weight"] + 3) // 4

    print(f"tx {txids[1][:16]}…  fee = {fee:,} sat  vsize = {vsize:,} vB  "
          f"rate = {fee/vsize:,.1f} sat/vB")
    check("our fee == API 'fee' field", fee == tx["fee"])
    return txids


#  Task 4.3
def merkle_root(txids: list[str]) -> str:
    level = [bytes.fromhex(t)[::-1] for t in txids]  # display -> internal byte order

    #  TODO 3: fold the level list up to a single 32-byte root
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        next_level = []
        for i in range(0, len(level), 2):
            parent = dsha256(level[i] + level[i + 1])
            next_level.append(parent)
        level = next_level

    return level[0][::-1].hex()  # internal -> display order


def task3(blk_hash: str, txids: list[str], blk: dict):
    root = merkle_root(txids)
    print(f"computed root: {root}")
    print(f"header root  : {blk['merkle_root']}")
    check("computed merkle root == header merkle_root", root == blk["merkle_root"])


# main
if __name__ == "__main__":
    blk_hash, blk = task1()
    txids = task2(blk_hash)
    task3(blk_hash, txids, blk)