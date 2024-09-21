// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ResourcePool {
    uint public totalResources;

    function addResources(uint amount) public {
        totalResources += amount;
    }

    function useResources(uint amount) public {
        require(totalResources >= amount, "Not enough resources");
        totalResources -= amount;
    }

    function reduceResources(uint amount) public {
        require(totalResources >= amount, "Not enough resources");
        totalResources -= amount;
    }

    function getTotalResources() public view returns (uint) {
        return totalResources;
    }
}
