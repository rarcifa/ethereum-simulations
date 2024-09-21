// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./resourcePool.sol";

contract Farmer {
    ResourcePool public resourcePool;

    constructor(address _resourcePool) {
        resourcePool = ResourcePool(_resourcePool);
    }

    // Efficient farming that contributes more to the resource pool
    function farmEfficient() public {
        uint resourcesProduced = 10;
        resourcePool.addResources(resourcesProduced);
    }

    // Selfish farming that reduces resources in the pool
    function farmSelfish() public {
        uint resourcesReduced = 10; // Reducing resources by 20
        require(
            resourcePool.getTotalResources() >= resourcesReduced,
            "Not enough resources"
        );
        resourcePool.reduceResources(resourcesReduced);
    }
}
