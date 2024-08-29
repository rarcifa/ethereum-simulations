// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// TODO: This is for reentrency simulations
contract MutexFixedChainWallet {
    mapping(address => uint256) private balances;

    bool internal locked;

    modifier noReentrant() {
        require(!locked, "No reentrancy");
        locked = true;
        _;
        locked = false; // Executes after `withdraw` function has finished.
    }

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    // FIX: Apply mutex lock
    function withdraw() public noReentrant {
        uint256 balance = getUserBalance(msg.sender);

        // Check user's balance
        require(balance > 0, "Insufficient balance");

        // Sends all the user's balance to them.
        (bool success, ) = msg.sender.call{value: balance}(""); // At this point, the caller's code is executed.
        require(success, "Failed to send Ether");

        // Updates the user's balance after sending them their entire balance.
        balances[msg.sender] = 0;
    }

    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }

    function getUserBalance(address _user) public view returns (uint256) {
        return balances[_user];
    }
}
