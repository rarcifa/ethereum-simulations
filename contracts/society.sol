// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Society {
    struct Agent {
        uint256 resources;
        uint256 productivity;
    }

    mapping(address => Agent) public agents;
    address[] public agentAddresses;

    event ResourcesShared(address from, address to, uint256 amount);
    event ProductivityUpdated(address agent, uint256 productivity);

    function registerAgent(uint256 initialResources) public {
        require(agents[msg.sender].resources == 0, "Agent already registered");
        agents[msg.sender] = Agent({
            resources: initialResources,
            productivity: 100 // Starting productivity
        });
        agentAddresses.push(msg.sender);
    }

    function shareResources(address to, uint256 amount) public {
        require(
            agents[msg.sender].resources >= amount,
            "Insufficient resources"
        );
        require(to != msg.sender, "Cannot share with self");

        agents[msg.sender].resources -= amount;
        agents[to].resources += amount;

        emit ResourcesShared(msg.sender, to, amount);
    }

    function updateProductivity(uint256 newProductivity) public {
        agents[msg.sender].productivity = newProductivity;
        emit ProductivityUpdated(msg.sender, newProductivity);
    }

    function totalResources() public view returns (uint256) {
        uint256 total = 0;
        for (uint i = 0; i < agentAddresses.length; i++) {
            total += agents[agentAddresses[i]].resources;
        }
        return total;
    }
}
