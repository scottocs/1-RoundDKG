from typing import Dict, List, Tuple, Set, Optional
import sys
import time
import pprint
from solcx import get_installed_solc_versions, get_available_solc_versions,set_solc_version,compile_files
# from web3.providers.eth_tester import EthereumTesterProvider
import web3
from web3 import Web3
from solcx import compile_source
import utils
set_solc_version('v0.5.17')

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)


def deploy_contract(w3, contract_interface):
    # print(contract_interface)
    # accounts = web3.geth.personal.list_accounts()
    # if len(w3.eth.accounts) == 0:
    #     w3.geth.personal.new_account('123456')
    account=w3.eth.accounts[0]
    # w3.geth.personal.unlock_account(account,"123456")
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin'])
    tx_hash = contract.constructor().transact({'from': account, 'gas': 500_000_000})

    # tx_hash = contract.constructor({'from': account, 'gas': 500_000_000}).transact()
    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    return address


# w3 = Web3(EthereumTesterProvider())
w3=web3.Web3(web3.HTTPProvider('http://127.0.0.1:7545', request_kwargs={'timeout': 60 * 10}))

contract_source_path = './contracts/contract.sol'
compiled_sol = compile_source_file(contract_source_path)
# print(compiled_sol)

# #BN256G2.sol
# contract_id, contract_interface = compiled_sol.popitem()
# address = deploy_contract(w3, contract_interface)
# print("Deployed {0} to: {1}\n".format(contract_id, address))

#contract.sol
contract_id, contract_interface = compiled_sol.popitem()
address = deploy_contract(w3, contract_interface)
print("Deployed {0} to: {1}\n".format(contract_id, address))


ctt = w3.eth.contract(
   address=address,
   abi=contract_interface['abi'])
# print(contract_interface['abi'])

# gas_estimate = ctt.functions.simG2().estimateGas()
# print("Sending transaction to simG2()",gas_estimate)
# tx_hash = ctt.functions.simG2().transact({"from":w3.eth.accounts[0], 'gas': 500_000_000})


# exit()

from abedkg import newjson
from abedkg import util
import json

from abedkg import sigma_protocol2
# ct=newjson.dumps(sigma_protocol2.enc_and_proof())
sigma_protocol2.init()
ct=json.loads(newjson.dumps(sigma_protocol2.enc_and_proof()))

# import abedkg.setting
# bn128=abedkg.setting.getBn128()
# g11=(bn128.FQ(ct["C0"][1][0]),bn128.FQ(ct["C0"][1][1]))
# print("on is_on_curve",bn128.is_on_curve(g11,bn128.b))
# print(ct["egg"][1],ct["g1"],ct["g2"])

ctStr={
    "c": ct["c"],
    "cp": ct["cp"],
    "policy":ct["policy"],
    "ztilde":ct["ztilde"],
    "Mtilde":ct["Mtilde"],
    "dkg_pk":ct["dkg_pk"],
    "dkg_pkp":ct["dkg_pkp"],
    "h":ct["h"],
    "k":ct["k"],
    "j":ct["j"],
    # "eta":ct["eta"],
    # "etap":ct["etap"],
    "Mhat":ct["Mhat"],
    "zhat":ct["zhat"],
    "quotient": ct["quotient"],
    "C0_1":ct["C0"][1],
    "C0p_1":ct["C0p"][1],
    "egg_1":ct["egg"][1],
    "egga_1":[],
    "g1":ct["g1"][0]+ct["g1"][1],
    "g2":ct["g2"],
    "attr":[],
    "C1_1":[],
    "C1p_1":[],
    "C2":[],
    "CHat2":[],
    "C3":[],
    "CHat3":[],
    "C4":[],
    "C2p":[],
    "CHat2p":[],
    "C3p":[],
    "CHat3p":[],
    "C4p":[],
    "zero_shareshat":[],
    "secret_shareshat":[],
    "txhat":[],
    "attr_unpacked":ct["attr_unpacked"],
    "gy":[],
    "g2y":[]
    # "zero_shareshat": ct["zero_shareshat"],
    # "secret_shareshat": ct["secret_shareshat"],
    # "txhat": ct["txhat"],
}

# ctStr["CHat2"]+=(ct["CHat2"][attr][0], ct["CHat2"][attr][1])
#   print(ctStr["CHat2"])
#   ctStr["C2p"]+=(ct["C2p"][attr][0]+ct["C2p"][attr][1])
#   ctStr["CHat2p"]+=ct["CHat2p"][attr][0]
#   ctStr["C3"]+=(ct["C3"][attr][0]+ct["C3"][attr][1])
#   ctStr["CHat3"]+=ct["CHat3"][attr][0]
#   ctStr["C3p"]+=(ct["C3p"][attr][0]+ct["C3p"][attr][1])
#   ctStr["CHat3"]+=ct["CHat3"][attr][0]

for attr in ct["C1"]:
  ctStr["attr"].append(attr)
  # print(util.hashToG1(attr))
  ctStr["C1_1"]+=ct["C1"][attr][1]
  ctStr["C1p_1"]+=ct["C1p"][attr][1]
  ctStr["C2"]+=(ct["C2"][attr][0]+ct["C2"][attr][1])
  # print(ctStr["C2"])
  ctStr["CHat2"]+=(ct["CHat2"][attr][0], ct["CHat2"][attr][1])
  # print(ctStr["CHat2"])
  ctStr["C2p"]+=(ct["C2p"][attr][0]+ct["C2p"][attr][1])
  ctStr["CHat2p"]+=(ct["CHat2p"][attr][0], ct["CHat2p"][attr][1])  
  ctStr["C3"]+=(ct["C3"][attr][0]+ct["C3"][attr][1])
  ctStr["CHat3"]+=(ct["CHat3"][attr][0], ct["CHat3"][attr][1])
  ctStr["C3p"]+=(ct["C3p"][attr][0]+ct["C3p"][attr][1])
  ctStr["CHat3p"]+=(ct["CHat3p"][attr][0], ct["CHat3p"][attr][1])
  ctStr["C4"]+=ct["C4"][attr]
  ctStr["C4p"]+=ct["C4p"][attr]
  ctStr["zero_shareshat"].append(ct["zero_shareshat"][attr])
  ctStr["secret_shareshat"].append(ct["secret_shareshat"][attr])
  ctStr["txhat"].append(ct["txhat"][attr])
  ctStr["egga_1"]+=ct["egga"][attr][1]  
  # print(type(ct["gy"]),ct["gy"])
  ctStr["gy"]+=(ct["gy"][attr][0]+ct["gy"][attr][1])
  ctStr["g2y"]+=(ct["g2y"][attr][0], ct["g2y"][attr][1])
# print(ctStr["C2p"])
# print(ctStr["C4"])
# print(ct)
# print(ctStr)
# a,b=utils.G2ToList(bn128.G2), utils.G1ToList(bn128.G1)
# a.extend(b)
# import json
# res=json.dumps({"g2":utils.G2ToList(bn128.G2),"g1":utils.G1ToList(bn128.G1)})
# ct = '{"outerKey": [{"g2": [1]}, {"innerKey2": "value"}]}'



def printRes(tx_hash):
    # print(tx_hash)
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("Was transaction successful? ",receipt['status'])
    # pprint.pprint(receipt['status'])
    rich_logs =ctt.events.Ciphertext().processReceipt(receipt)
    # print(rich_logs[0]['args'])
    print(rich_logs)
    print("\n")

# gas_estimate = ctt.functions.writeCT(ctStr).estimateGas()
# print("Sending transaction to writeCT(ctStr)",gas_estimate)
# tx_hash = ctt.functions.writeCT(ctStr).transact({"from":w3.eth.accounts[0], 'gas': 500_000_000})
# printRes(tx_hash)

ctC0={}
for key in ctStr:
  if key in ["Mtilde","egg_1","C0_1","C0p_1","ztilde","cp"]:
    ctC0[key]=ctStr[key]
gas_estimate = ctt.functions.checkC0(ctC0).estimateGas()
print("Sending transaction to checkC0(ctC0)",gas_estimate)
tx_hash = ctt.functions.checkC0(ctC0).transact({"from":w3.eth.accounts[0], 'gas': 500_000_000})
printRes(tx_hash)

ctC1={}
for key in ctStr:
  if key in ["C1_1","C1p_1","secret_shareshat","txhat","egg_1","egga_1","cp"]:
    ctC1[key]=ctStr[key]

gas_estimate = ctt.functions.checkC1(ctC1).estimateGas()
print("Sending transaction to checkC1(ctC1)",gas_estimate)
tx_hash = ctt.functions.checkC1(ctC1).transact({"from":w3.eth.accounts[0], 'gas': 500_000_000})
printRes(tx_hash)

ctC2={}
for key in ctStr:
  if key in ["g1","g2","C2","C2p","CHat2","CHat2p","txhat","cp"]:
    ctC2[key]=ctStr[key]

gas_estimate = ctt.functions.checkC2New(ctC2).estimateGas()
print("Sending transaction to checkC2New(ctC2)", gas_estimate)
tx_hash = ctt.functions.checkC2New(ctC2).transact({"from":w3.eth.accounts[0], 'gas': 500_000_000})
printRes(tx_hash)

ctC3={}
for key in ctStr:
  if key in ["cp","g1","g2","C3p","CHat3","CHat3p","txhat","g2y","zero_shareshat"]:
    ctC3[key]=ctStr[key]

gas_estimate = ctt.functions.checkC3New(ctC3).estimateGas()
print("Sending transaction to checkC3New(ctC3)", gas_estimate)
tx_hash = ctt.functions.checkC3New(ctC3).transact({"from":w3.eth.accounts[0], 'gas': 500_000_000})
printRes(tx_hash)

ctC4={}
for key in ctStr:
  if key in ["attr_unpacked","cp","C4","C4p","txhat"]:
    ctC4[key]=ctStr[key]

gas_estimate = ctt.functions.checkC4(ctC4).estimateGas()
print("Sending transaction to checkC4(ctC4)",gas_estimate)
tx_hash = ctt.functions.checkC4(ctC4).transact({"from":w3.eth.accounts[0], 'gas': 500_000_000})
printRes(tx_hash)


ctPK={}
for key in ctStr:
  if key in ["j","h","c","Mhat","quotient","dkg_pk","dkg_pkp"]:
    ctPK[key]=ctStr[key]

gas_estimate = ctt.functions.checkdkg_pk(ctPK).estimateGas()
print("Sending transaction to checkdkg_pk(ctPK)",gas_estimate)
tx_hash = ctt.functions.checkdkg_pk(ctPK).transact({"from":w3.eth.accounts[0], 'gas': 500_000_000})
printRes(tx_hash)

# gas_estimate = ctt.functions.checketa(ctStr).estimateGas()
# print("Sending transaction to checketa(ctStr)",gas_estimate)
# tx_hash = ctt.functions.checketa(ctStr).transact({"from":w3.eth.accounts[0], 'gas': 500_000_000})
# printRes(tx_hash)






# receipt = w3.eth.waitForTransactionReceipt(tx_hash)
# pprint.pprint(dict(receipt))  

# for i in range(0, len(ctStr["attr"])):
#     gas_estimate = ctt.functions.checkC2New(ctStr,4*i,4*i+4).estimateGas()
#     print("Sending transaction to checkC2(ctStr,4*i,4*i+4)", "[",4*i,4*i+4,"]", gas_estimate)
#     tx_hash = ctt.functions.checkC2New(ctStr,4*i,4*i+4).transact({"from":w3.eth.accounts[0], 'gas': 500_000_000})
#     printRes(tx_hash)
    
# for i in range(0, len(ctStr["attr"])):
#     gas_estimate = ctt.functions.checkC3(ctStr,4*i,4*i+4).estimateGas()  
#     print("Sending transaction to checkC3(ctStr,4*i,4*i+4)", "[",4*i,4*i+4,"]", gas_estimate)
#     tx_hash = ctt.functions.checkC3(ctStr,4*i,4*i+4).transact({"from":w3.eth.accounts[0], 'gas': 500_000_000})
#     printRes(tx_hash)

# for i in range(0, len(ctStr["attr"])):
#     gas_estimate = ctt.functions.checkC3(ctStr,4*i,4*i+4).estimateGas()
#     # print("Gas estimate to transact with checkC2: {0}\n".format(gas_estimate))

#     if gas_estimate < 100000*1000:
#         print("Sending transaction to checkC3(ctStr,4*i,4*i+4)", "[",4*i,4*i+4,"]")
#         tx_hash = ctt.functions.checkC3(ctStr,4*i,4*i+4).transact({"from":w3.eth.accounts[0], 'gas': 500_000_000})
#         receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#         # print("Transaction receipt mined: \n")
#         # pprint.pprint(dict(receipt))
#         print("Was transaction successful? ")
#         pprint.pprint(receipt['status'])

#         # myContract = web3.eth.contract(address=contract_address, abi=contract_abi)
#         # tx_hash = ctt.functions.myFunction().transact()
#         # receipt = web3.eth.getTransactionReceipt(tx_hash)
#         rich_logs =ctt.events.Ciphertext().processReceipt(receipt)
#         # print(rich_logs[0]['args'])
#         print(rich_logs)
#         print("\n")
#     else:
#         print("Gas cost exceeds 100000")

# print(ct["C0p"][1][0])