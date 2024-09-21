// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./resourcePool.sol";

contract Trader {
    ResourcePool public resourcePool;

    constructor(address _resourcePool) {
        resourcePool = ResourcePool(_resourcePool);
    }

    // Efficient trade that benefits the resource pool
    function tradeEfficient() public {
        uint resourcesGained = 7;
        resourcePool.addResources(resourcesGained);
    }

    // Selfish trade that reduces resources in the pool
    function tradeSelfish() public {
        uint resourcesLost = 7; // Reducing resources by 10
        require(
            resourcePool.getTotalResources() >= resourcesLost,
            "Not enough resources"
        );
        resourcePool.reduceResources(resourcesLost);
    }
}
