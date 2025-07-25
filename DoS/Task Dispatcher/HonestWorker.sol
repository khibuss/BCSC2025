// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HonestWorker {
    string public lastJob = "Free time";

    event TaskReceived(string job);

    function onTask(string memory job) external {
        // Sovrascrive il job precedente
        lastJob = job;

        // Log dell’operazione
        emit TaskReceived(job);
    }
}