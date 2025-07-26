# Denial of Service (DoS)

Questa cartella raccoglie esempi pratici di vulnerabilità di tipo **Denial of Service (DoS)** nei contratti Ethereum, insieme a script per testarne l'effettiva exploitabilità sulla testnet **Sepolia**.

## Esempi disponibili

### `Task Dispatcher`

- Mostra come un singolo worker malevolo possa bloccare un intero sistema di dispatching, semplicemente eseguendo un `revert()` nella propria funzione `onTask()`.
- Include: contratto vulnerabile, worker onesto/malevolo, script di test.

🔗 Vai alla cartella: [`Task Dispatcher`](./Task%20Dispatcher)

---