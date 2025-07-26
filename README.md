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

Questo software è distribuito sotto licenza MIT.
© 2025 Alberto Olla

Per i dettagli, consulta il file [LICENSE](./LICENSE).