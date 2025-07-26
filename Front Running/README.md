# Front Running 

Questa cartella contiene esempi pratici di vulnerabilità di tipo **Front Running** in contratti Ethereum, insieme a script per testarne l'effettiva exploitabilità sulla testnet **Sepolia**.

## Esempi disponibili

### `BuySellTokens`

- Simula un exchange semplificato dove gli utenti possono acquistare e vendere token.
- Un attaccante può monitorare la mempool e anticipare la transazione dell’amministratore che modifica il prezzo dei token, eseguendo un’operazione più vantaggiosa prima.

🔗 Vai alla cartella: [`BuySellTokens`](./BuySellTokens)

---

### `FindThisHash`

- Simula un gioco in cui bisogna indovinare quale stringa produce un determinato hash, per vincere un premio in ether.
- Un attaccante può intercettare una transazione in mempool con la soluzione corretta, copiarla e inviarla con una fee più alta per vincere al posto del partecipante onesto.
- ⚠️ Questo contratto è basato su un esempio pubblicato da **[Cyfrin](https://www.cyfrin.io/)** per illustrare le vulnerabilità di tipo *Front Running* nei contratti Ethereum.


🔗 Vai alla cartella: [`FindThisHash`](./FindThisHash)

---
