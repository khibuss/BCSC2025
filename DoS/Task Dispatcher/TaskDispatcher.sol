// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TaskDispatcher {
    address[] public workers;

    function registerWorker(address w) external {
        workers.push(w);
    }

    function dispatchTask(string memory job) external {
        for (uint256 i = 0; i < workers.length; i++) {
            (bool ok, ) = workers[i].call(abi.encodeWithSignature("onTask(string)", job));
            require(ok, "Worker failed to accept task");
        }
    }
}
