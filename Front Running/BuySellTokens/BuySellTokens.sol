// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BuySellTokens {
    address public admin;
    uint256 public price = 1000; // prezzo in wei per token
    mapping(address => uint256) public balance;

    constructor() payable {
        admin = msg.sender;
    }

    function updatePrice(uint256 newPrice) external {
        require(msg.sender == admin, "Solo admin");
        price = newPrice;
    }

    function buy() external payable {
        require(msg.value > 0, "Invia ETH");
        uint256 tokens = msg.value * 1e18 / price;
        balance[msg.sender] += tokens;
    }

    function sell(uint256 tokens) external {
        require(balance[msg.sender] >= tokens, "Non hai abbastanza token");
        balance[msg.sender] -= tokens;
        uint256 ethToSend = tokens * price / 1e18;
        
        (bool sent, ) = msg.sender.call{value: ethToSend}("");
        require(sent, "Invio Ether fallito");
    }
}