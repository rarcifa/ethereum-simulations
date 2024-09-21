// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./resourcePool.sol";

contract Builder {
    ResourcePool public resourcePool;

    constructor(address _resourcePool) {
        resourcePool = ResourcePool(_resourcePool);
    }

    // Efficient build that benefits the resource pool
    function buildEfficient() public {
        uint resourcesNeeded = 5;
        require(
            resourcePool.getTotalResources() >= resourcesNeeded,
            "Not enough resources"
        );
        resourcePool.useResources(resourcesNeeded);
    }

    // Selfish build that wastes extra resources
    function buildSelfish() public {
        uint resourcesNeeded = 5;
        uint resourcesWasted = 10; // Selfishly wasting extra resources
        require(
            resourcePool.getTotalResources() >=
                resourcesNeeded + resourcesWasted,
            "Not enough resources"
        );
        resourcePool.useResources(resourcesNeeded + resourcesWasted);
    }
}
