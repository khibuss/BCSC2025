# Front Running - BuySellTokens

Questa cartella contiene un esempio pratico di vulnerabilità **Front Running** in un contratto Ethereum.

## Contenuto

- `BuySellTokens.sol`: contratto vulnerabile per l'acquisto vendita di token
- `test_BuySellTokens.py`: script Python per testare l’attacco di FR
- `.env`: file con le chiavi e l’endpoint per il nodo RPC per la testnet Sepolia

---

## Riproduzione del test

### 1. Clona la repository

Se non l'hai già fatto:

```bash
git clone https://github.com/khibuss/BCSC2025
cd BCSC2025/Front\ Running/BuySellTokens/
```

### 2.Installa le dipendenze

Assicurati di avere Python ≥ 3.8 e installa i pacchetti necessari:

```bash
pip install web3 python-dotenv py-solc-x
```

### 3. Crea un file .env

All'interno della cartella BuySellTokens, crea un file .env con il seguente contenuto:

```bash
PUBLIC_KEY_ADMIN=0x...
PRIVATE_KEY_ADMIN=0x...
PUBLIC_KEY_ATTACKER=0x...
PRIVATE_KEY_ATTACKER=0x...
RPC_URL=https://sepolia.infura.io/v3/<your-infura-id>
```
- Inserisci le chiavi pubbliche/private di due account Ethereum (admin e attaccante).

- Puoi ottenere un endpoint RPC registrandoti su infura.io.

### 4. Ricarica i tuoi account con Ether di test

I tuoi account devono avere un po’ di ETH sulla testnet Sepolia. Puoi usare un faucet come:

- https://sepolia-faucet.pk910.de/

### 5. Esegui il test

Lancia lo script Python:

```bash
python3 test_BuySellTokens.py
```

## Licenza

Copyright (C) 2025 Alberto Olla

Si concede gratuitamente l'autorizzazione, a chiunque ottenga una copia di questo software e dei file di documentazione associati (il "Software"), di dare opera al Software senza restrizioni, compresi senza limitazione i diritti di utilizzare, copiare, modificare, unire, pubblicare, distribuire, concedere in sublicenza ovvero vendere copie del Software, e di consentire alle persone a cui il Software è fornito di fare altrettanto, posto che siano rispettate le seguenti condizioni:

l'avviso di copyright unitamente a questo avviso di licenza devono essere sempre inclusi in tutte le copie o parti sostanziali del Software.

IL SOFTWARE VIENE FORNITO "COSÌ COM'È" SENZA GARANZIE DI ALCUN TIPO, ESPLICITE O IMPLICITE, COMPRESE, MA NON SOLO, LE GARANZIE DI COMMERCIABILITÀ, IDONEITÀ AD UN PARTICOLARE SCOPO E NON VIOLAZIONE DI DIRITTI ALTRUI. IN NESSUN CASO GLI AUTORI DEL SOFTWARE O I TITOLARI DEL COPYRIGHT POTRANNO ESSERE RITENUTI RESPONSABILI DI RECLAMI, DANNI O ALTRE RESPONSABILITÀ, DERIVANTI DA O COLLEGATI A CONTRATTO, ILLECITO CIVILE O IN ALTRA RELAZIONE CON IL SOFTWARE O CON IL SUO UTILIZZO O CON ALTRE OPERAZIONI DEL SOFTWARE.
