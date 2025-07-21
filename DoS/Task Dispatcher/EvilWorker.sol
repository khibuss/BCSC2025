// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EvilWorker {
    function onTask(string memory) external pure {
        revert("I don't take orders.");
    }
}
