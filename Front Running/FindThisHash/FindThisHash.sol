// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FindThisHash {
    bytes32 public constant hash = 0x564ccaf7594d66b1eaaea24fe01f0585bf52ee70852af4eac0cc4b04711cd0e2; // "Ethereum"
    address public winner;

    constructor() payable {}

    function solve(string memory solution) public {
        require(winner == address(0), "Gioco gia' risolto");
        require(
            hash == keccak256(abi.encodePacked(solution)),
            "Risposta errata"
        );

        winner = msg.sender;

        (bool sent, ) = msg.sender.call{value: 0.00001 ether}("");
        require(sent, "Invio Ether fallito");
    }

    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
    }
}