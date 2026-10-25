 Lab Modules & Core Concepts
 1. Cryptography Foundations & Merkle Trees (Lab 3 & Lab 4)Cryptographic
 2. Hash Functions: Implementations exploring preimage resistance and cryptographic integrity checks across sequential blocks.Merkle Tree Construction & Verification
 3. (3_3merkle_starter.py):Building binary hash trees from leaf transactions up to the Merkle
 4. Root.Generating and verifying logarithmic Merkle Proofs O(log N) without scanning the entire dataset.Digital Signatures & Asymmetric Cryptography
 5. (lap4_1.py):Keypair generation (Private/Public Key).Signing transactions and verifying signatures against sender addresses.

Transaction Fee Dynamics & Mempool Analytics 
(Lab 5)EIP-1559 Fee Mechanics (decompose_fee5.py):Analyzing gas fee structures: Max Fee, Base Fee, and Priority Fee (miner/validator tip).Simulating and decomposing gas pricing calculations during state execution.Network Fee History Tracking (fee_history5.py):Fetching historic block fee data using EVM JSON-RPC calls (eth_feeHistory).Monitoring base fee trends across multiple blocks to assess network congestion.3. Smart Contract Development on EVM 
(Lab 6)File: ClassRegistry_remix (1).sol
Environment: Remix IDE (deployed on testnet via WalletConnect / EVM provider).Key Contract Features:Custom Struct Data Model: Encapsulates student identity (name, className, studentId).Dense Array & Mapping Pattern: Uses _members array coupled with a 1-based index mapping (_indexPlusOne) for gas-efficient membership verification and swap-and-pop deletion O(1) removal cost.Access 
Control & Custom Errors: Protects administrative functions (onlyOwner) using modern custom errors (AlreadyRegistered, NotRegistered, EmptyFields, NotOwner) to reduce execution revert gas costs.Event Logging: Emits indexed events (Registered, Deregistered) for off-chain indexing and auditability.

