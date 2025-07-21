from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv
import json, os, time, csv
from datetime import datetime

# Impostazioni iniziali
load_dotenv()
PRIVATE_KEY_HONEST = os.getenv("PRIVATE_KEY_HONEST")
PRIVATE_KEY_ATTACKER = os.getenv("PRIVATE_KEY_ATTACKER")
ACCOUNT_HONEST = "0x0C695d7087e72f736FD84B31BC3335532Da23bb0"
ACCOUNT_ATTACKER = "0xDf3ba104c293020453c8Ebb4fb84CE226b6546E5"
CONTRACT_NAME = "FindThisHash"

w3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/854261bb8677458b9201b8062c8b74ad"))
chain_id = 11155111  # Sepolia
install_solc("0.8.0")

# Funzione per compilare il contratto
def compile_contract():
    with open(f"{CONTRACT_NAME}.sol", "r") as file:
        source_code = file.read()

    compiled = compile_standard({
    "language": "Solidity",
    "sources": {
        f"{CONTRACT_NAME}.sol": {
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

    abi = compiled["contracts"][f"{CONTRACT_NAME}.sol"][f"{CONTRACT_NAME}"]["abi"]
    bytecode = compiled["contracts"][f"{CONTRACT_NAME}.sol"][f"{CONTRACT_NAME}"]["evm"]["bytecode"]["object"]
    return abi, bytecode

# Funzione per il deploy del contratto
def deploy_contract(w3, abi, bytecode, sender, private_key, value_ether=0):
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(sender)

    tx = contract.constructor().build_transaction({
        "from": sender,
        "nonce": nonce,
        "chainId": chain_id,
        "gas": 3000000,
        "gasPrice": w3.to_wei(0.5, "gwei"),
        "value": w3.to_wei(value_ether, "ether")
    })

    signed = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print("📤 Deploy in corso...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("✅ Contratto deployato all'indirizzo:", receipt.contractAddress)
    return w3.eth.contract(address=receipt.contractAddress, abi=abi), receipt.contractAddress

# Transazione utente onesto
def send_honest_tx(contract):
    nonce = w3.eth.get_transaction_count(ACCOUNT_HONEST)
    tx = contract.functions.solve("Ethereum").build_transaction({
        'from': ACCOUNT_HONEST,
        'nonce': nonce,
        'gas': 100000,
        'gasPrice': w3.to_wei(0.5, 'gwei'),
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY_HONEST)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print("Honest TX inviata:", tx_hash.hex())
    return tx_hash.hex()

# Transazione attaccante
def send_attacker_tx(contract):
    nonce = w3.eth.get_transaction_count(ACCOUNT_ATTACKER)
    tx = contract.functions.solve("Ethereum").build_transaction({
        'from': ACCOUNT_ATTACKER,
        'nonce': nonce,
        'gas': 100000,
        'gasPrice': w3.to_wei(10, 'gwei'),
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY_ATTACKER)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print("Attacker TX inviata:", tx_hash.hex())
    return tx_hash.hex()


def init_log_file():
    if not os.path.exists("results.csv"):
        with open("results.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "contract_address", "honest_tx", "attacker_tx", "winner_address", "vincitore"])

def log_result(contract_address, honest_tx_hash, attacker_tx_hash, winner_address):
    if winner_address.lower() == ACCOUNT_ATTACKER.lower():
        vincitore = "attaccante"
        print("L'attaccante ha vinto")
    elif winner_address.lower() == ACCOUNT_HONEST.lower():
        vincitore = "onesto"
        print("L'utente onesto ha vinto")
    else:
        print("Vincitore sconosciuto")
        vincitore = "sconosciuto"

    with open("results.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            contract_address,
            "0x" + honest_tx_hash,
            "0x" + attacker_tx_hash,
            winner_address,
            vincitore
        ])

if __name__ == "__main__":
    init_log_file()

    abi, bytecode = compile_contract()
    #abi = open("temp/abi", "r").read()
    #bytecode = open("temp/bytecode", "r").read()
    contract, contract_address = deploy_contract(w3, abi, bytecode, ACCOUNT_ATTACKER, PRIVATE_KEY_ATTACKER, value_ether=0.00001)

    honest_tx = send_honest_tx(contract)
    time.sleep(2)  # Simula tempo d'osservazione
    attacker_tx = send_attacker_tx(contract)

    time.sleep(12)
    
    winner = contract.functions.winner()().call()
    log_result(contract_address, honest_tx, attacker_tx, winner)


            
    
