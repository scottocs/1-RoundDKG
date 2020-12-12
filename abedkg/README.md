## file structure
ma_abe.py: Rouselakis and Waters multi-authority CP-ABE with NIZK proofs using BN256 eliptic curve

sigma_protocol.py: use ma_abe.py to prove plaintext knowledge of ciphertext with the NIZK proofs

ma_abe2.py: Rouselakis and Waters multi-authority CP-ABE with NIZK proofs (removing the off-chain attestation which is time consuming)

sigma_protocol2.py: use ma_abe.py to prove plaintext knowledge of ciphertext with the NIZK proofs (removing the off-chain attestation which is time consuming)

## how to test
1. test ma_mabe: python3 ma_abe.py or python3 ma_abe2.py

2. test sigma protocol: python3 sigma_protocol.py or testsigma_protocol2

