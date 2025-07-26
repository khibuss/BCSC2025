# Strategie di rilevamento vulnerabilità e patching di Smart Contract Ethereum

Questo progetto fa parte del corso **Blockchain & Smart Contracts** del corso di laurea magistrale in Informatica. Lo scopo è analizzare e testare vulnerabilità comuni nei contratti smart su Ethereum, con particolare attenzione a:

- **Denial of Service (DoS)**
- **Front Running**

Ogni vulnerabilità è accompagnata da:
- Un contratto Solidity vulnerabile
- Uno script Python che sfrutta la vulnerabilità del contratto
- Un README di riferimento

## Requisiti

Per eseguire i test sono necessari:
- Python ≥ 3.8
- Librerie Python: **web3, py-solc-x, python-dotenv**

```bash
pip install web3 py-solc-x python-dotenv
```
## Licenza

Copyright (C) 2025 Alberto Olla

Si concede gratuitamente l'autorizzazione, a chiunque ottenga una copia di questo software e dei file di documentazione associati (il "Software"), di dare opera al Software senza restrizioni, compresi senza limitazione i diritti di utilizzare, copiare, modificare, unire, pubblicare, distribuire, concedere in sublicenza ovvero vendere copie del Software, e di consentire alle persone a cui il Software è fornito di fare altrettanto, posto che siano rispettate le seguenti condizioni:

l'avviso di copyright unitamente a questo avviso di licenza devono essere sempre inclusi in tutte le copie o parti sostanziali del Software.

IL SOFTWARE VIENE FORNITO "COSÌ COM'È" SENZA GARANZIE DI ALCUN TIPO, ESPLICITE O IMPLICITE, COMPRESE, MA NON SOLO, LE GARANZIE DI COMMERCIABILITÀ, IDONEITÀ AD UN PARTICOLARE SCOPO E NON VIOLAZIONE DI DIRITTI ALTRUI. IN NESSUN CASO GLI AUTORI DEL SOFTWARE O I TITOLARI DEL COPYRIGHT POTRANNO ESSERE RITENUTI RESPONSABILI DI RECLAMI, DANNI O ALTRE RESPONSABILITÀ, DERIVANTI DA O COLLEGATI A CONTRATTO, ILLECITO CIVILE O IN ALTRA RELAZIONE CON IL SOFTWARE O CON IL SUO UTILIZZO O CON ALTRE OPERAZIONI DEL SOFTWARE.