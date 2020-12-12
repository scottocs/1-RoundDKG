# File structure
abedkg/: source code of Rouselakis and Waters multi-authority CP-ABE with NIZK proofs 

contracts/: smart contract run on EVM to verify the ciphertexts

test.py: test the gas consumption in the terminal

## Prerequisition:
    Ganache (2.3.0)
    solidity compiler (v0.5.17)
    web3

## Test example (10 participants (n=10) in the DKG protocol):
    python3 test.py

    result:

    !(https://github.com/scottocs/ABEDKG/blob/main/dkgresult.png?raw=true)

## Note

These codes support the paper "1-Round Distributed Key Generation Using Decentralized CP-ABE" submitted to TDSC.

All codes provided in this github are a proof of concept implementation and are not audited for implmentation bugs. Use with caution.