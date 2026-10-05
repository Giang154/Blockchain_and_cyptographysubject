# Merkle tree 
import hashlib

def sha256_hash(data: bytes) -> bytes:
    """Hàm băm SHA-256 trả về bytes."""
    return hashlib.sha256(data).digest()

# TODO 1: merkle_root

def merkle_root(leaves: list[bytes]) -> bytes:
    if not leaves:
        return b""
    current_level = list(leaves)
    while len(current_level) > 1:
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])
        next_level = []
        for i in range(0, len(current_level), 2):
            parent = sha256_hash(current_level[i] + current_level[i + 1])
            next_level.append(parent)
        current_level = next_level
    return current_level[0]

# TODO 2: merkle_proof
def merkle_proof(leaves: list[bytes], index: int) -> list[tuple[bytes, bool]]:
    proof = []
    current_level = list(leaves)
    idx = index
    while len(current_level) > 1:
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])
        
        is_even = (idx % 2 == 0)
        sibling_idx = idx + 1 if is_even else idx - 1
        is_left = not is_even  # Nếu nút hiện tại bên phải thì anh em nó bên trái
        proof.append((current_level[sibling_idx], is_left))
        
        # Lên tầng kế tiếp
        next_level = []
        for i in range(0, len(current_level), 2):
            next_level.append(sha256_hash(current_level[i] + current_level[i + 1]))
        current_level = next_level
        idx //= 2
    return proof

# TODO 3: verify_proof
def verify_proof(leaf_hash: bytes, proof: list[tuple[bytes, bool]], root: bytes) -> bool:
    curr = leaf_hash
    for sibling, is_left in proof:
        if is_left:
            curr = sha256_hash(sibling + curr)
        else:
            curr = sha256_hash(curr + sibling)
    return curr == root

# TEST 
if __name__ == "__main__":
    tx_data = [f"tx_{i}".encode() for i in range(7)]
    leaves = [sha256_hash(tx) for tx in tx_data]

    # Test 1: Merkle Root
    root = merkle_root(leaves)
    print("CHECK Root calculation:", "OK" if root else "FAIL")

    # Test 2 & 3: Merkle Proof & Verification cho từng nút lá
    all_ok = True
    for i in range(len(leaves)):
        proof = merkle_proof(leaves, i)
        is_valid = verify_proof(leaves[i], proof, root)
        if not is_valid:
            all_ok = False
            break
    print("CHECK Proof & Verification for all leaves:", "OK" if all_ok else "FAIL")

    # Test 4: Giả mạo dữ liệu phải trả về False
    fake_leaf = sha256_hash(b"fake_tx")
    proof_0 = merkle_proof(leaves, 0)
    fake_check = verify_proof(fake_leaf, proof_0, root)
    print("CHECK Tamper detection (Fake leaf):", "OK" if not fake_check else "FAIL")
