from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv
import json, os, time, csv
from datetime import datetime

# Impostazioni iniziali
load_dotenv()

PRIVATE_KEY_ADMIN = os.getenv("PRIVATE_KEY_ADMIN")
ACCOUNT_ADMIN = os.getenv("PUBLIC_KEY_ADMIN")

# Nomi dei contratti da deployare
DISPATCHER_CONTRACT_NAME = "TaskDispatcher"
HONEST_CONTRACT_NAME = "HonestWorker"
EVIL_CONTRACT_NAME = "EvilWorker"

RPC_URL = os.getenv("RPC_URL")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
chain_id = 11155111  # Sepolia
install_solc("0.8.0")

# Funzione per compilare il contratto
def compile_contract(contract_name):
    with open(f"{contract_name}.sol", "r") as file:
        source_code = file.read()

    compiled = compile_standard({
        "language": "Solidity",
        "sources": {
            f"{contract_name}.sol": {
                "content": source_code
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    }, solc_version="0.8.0")

    abi = compiled["contracts"][f"{contract_name}.sol"][f"{contract_name}"]["abi"]
    bytecode = compiled["contracts"][f"{contract_name}.sol"][f"{contract_name}"]["evm"]["bytecode"]["object"]
    return abi, bytecode

# Funzione per il deploy del contratto
def deploy_contract(w3, abi, bytecode, sender, private_key, name, value_ether=0):
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(sender, 'pending')

    tx = contract.constructor().build_transaction({
        "from": sender,
        "nonce": nonce,
        "chainId": chain_id,
        "gas": 3000000,
        "gasPrice": w3.to_wei(5, "gwei"),
        "value": w3.to_wei(value_ether, "ether")
    })

    signed = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"📤 Deploy in corso di {name}...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✅ {name} deployato all'indirizzo:", receipt.contractAddress)
    return w3.eth.contract(address=receipt.contractAddress, abi=abi)

def deploy_dispatcher():
    abi, bytecode = compile_contract(DISPATCHER_CONTRACT_NAME)
    contract = deploy_contract(w3, abi, bytecode, ACCOUNT_ADMIN, PRIVATE_KEY_ADMIN, DISPATCHER_CONTRACT_NAME)

    return contract

def deploy_honest_workers(num: int):
    workers = []

    abi, bytecode = compile_contract(HONEST_CONTRACT_NAME)
    for i in range(num):
        contract = deploy_contract(w3, abi, bytecode, ACCOUNT_ADMIN, PRIVATE_KEY_ADMIN, HONEST_CONTRACT_NAME)
        workers.append(contract)

    return workers

def deploy_evil_worker():
    abi, bytecode = compile_contract(EVIL_CONTRACT_NAME)
    contract = deploy_contract(w3, abi, bytecode, ACCOUNT_ADMIN, PRIVATE_KEY_ADMIN, EVIL_CONTRACT_NAME)
    
    return contract

def registerWorker(dispatcher_contract, worker_addr, worker_id):
    nonce = w3.eth.get_transaction_count(ACCOUNT_ADMIN, "pending")
    tx = dispatcher_contract.functions.registerWorker(worker_addr).build_transaction({
        "from": ACCOUNT_ADMIN,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.to_wei(5, "gwei"),
    })
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY_ADMIN)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"➡️  Registrazione worker {worker_id} inviata: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✅ Worker {worker_id} registrato")

def dispatchTask(dispatcher_contract, task):
    nonce = w3.eth.get_transaction_count(ACCOUNT_ADMIN, "pending")
    tx = dispatcher_contract.functions.dispatchTask(task).build_transaction({
        "from": ACCOUNT_ADMIN,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.to_wei(5, "gwei"),
    })
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY_ADMIN)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"➡️  Dispatch del task \"{task}\" inviato: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"📦 Task \"{task}\" processato (status: {receipt['status']})")

    return receipt

if __name__ == "__main__":
    # Compilazione e deploy dei contratti
    # Per il test verranno utilizzati 2 contratti onesti e 1 malevolo.
    dispatcher = deploy_dispatcher()
    honest_workers = deploy_honest_workers(2)
    evil_worker = deploy_evil_worker()


    #Inizialmente gli honest worker hanno "Free time"
    print("")
    print("📋 Stato iniziale dei workers:")
    for idx, worker in enumerate(honest_workers):
        print(f"Worker {idx}:{worker.functions.lastJob().call()}") 
    
    # Registrazione degli honest worker
    print("")
    print("🧾 Registrazione degli honest worker nel dispatcher")
    for idx, worker in enumerate(honest_workers):
        registerWorker(dispatcher, worker.address, idx)

    # Invio di un primo task
    print("")
    print("🚀 Dispatch di un nuovo task:")
    dispatchTask(dispatcher, "Esegui backup giornaliero")

    # Stato dopo il primo task
    print("")
    print("📋 Stato aggiornato dei worker:")
    for idx, worker in enumerate(honest_workers):
        print(f"Worker {idx+1}:{worker.functions.lastJob().call()}") 

    #Fin qua il contratto funziona, ora aggiungiamo un contratto malevolo
    print("")    
    print("⚠️ Aggiunta contratto malevolo")
    registerWorker(dispatcher, evil_worker.address, idx+1)

    #Se ora mandiamo il dispatch di un nuovo task tutto il contratto fallirà
    print("")
    print("🚀 Dispatch di un nuovo task:")
    receipt = dispatchTask(dispatcher, "Esegui scansione antivirus settimanale")

    if receipt["status"] == 0:
        print("✅ Attacco DoS RIUSCITO: il contratto è andato in errore")
    else:
        print("❌ Attacco DoS FALLITO: il task è stato gestito correttamente")

    # Stato finale dei worker
    # Che non sarà Esegui scansione antivirus settimanale in quanto c'è stato un revert
    print("")
    print("📋 Stato finale dei worker:")
    for idx, worker in enumerate(honest_workers):
        print(f"Worker {idx}:{worker.functions.lastJob().call()}") 