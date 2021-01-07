# File structure
abedkg/: source code of Rouselakis and Waters multi-authority CP-ABE with NIZK proofs 

contracts/: smart contract run on EVM to verify the ciphertexts

test.py: test the gas consumption in the terminal

## Prerequisition:
    1). Ganache (2.3.0)    
    2). solidity compiler (v0.5.17)
    3). web3

## Test example (10 participants (n=10) in the DKG protocol):
	1. open ganache
    2. python3 test.py
    3. result:
    ![image](https://github.com/scottocs/ABEDKG/blob/main/dkgresult.png?raw=true)

## Note
When CP-ABE algorithms or batch decryption are tested on PC, change lib_bn128 to optimized_bn128 in the setting.py. 

When ciphertexts and proofs are committed to Ganache, change lib_bn128 to bn128 in the setting.py. 

These codes support the paper "1-Round Distributed Key Generation Using Decentralized CP-ABE" submitted to TDSC.

All codes provided in this github are a proof of concept implementation and are not audited for implmentation bugs. Use with caution.
