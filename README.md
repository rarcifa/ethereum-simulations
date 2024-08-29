# Auction Simulation Project

This project is a simulation of an Ethereum-based auction system. The project involves deploying a smart contract to a local Ethereum network, placing bids, and determining the auction winner through a Python script. This README file will guide you through the setup and usage of the project.

## Prerequisites

Before you begin, ensure you have the following software installed on your system:

- **Node.js**: A JavaScript runtime environment (https://nodejs.org/)
- **npm**: Node Package Manager, installed with Node.js (https://www.npmjs.com/)
- **Python 3.x**: The programming language used to run the auction simulation (https://www.python.org/)

## Installation

Follow these steps to set up the project:

1. Clone the repository to your local machine.

   ```bash
   git clone https://github.com/rarcifa/ethereum-simulations.git
   cd ethereum-simulations
   ```

2. Install the necessary npm packages.

   ```bash
   npm install
   ```

## Running the Local Ethereum Node

To simulate the Ethereum network locally, we'll use Hardhat, an Ethereum development environment.

1. Start the local Ethereum node using Hardhat.

   ```bash
   npx hardhat node
   ```

   This command will initiate a local Ethereum node, connecting you to a local snapshot of the Ethereum network. The node will provide you with several accounts preloaded with test Ether, which you can use for testing and development.

2. Keep this terminal open and running as it serves as the backend for deploying contracts and running the auction simulation.

## Running the Auction Simulation

The auction simulation script places bids on the deployed auction contract using randomly generated accounts. The simulation will run through several rounds, each representing a separate auction.

1. Navigate to the marl directory.

   ```bash
   cd marl
   ```

2. Run the simulation script.

   ```bash
   python3 run_simulation.py
   ```

   The simulation script will:

   - **Deploy the Auction Contract:** It will compile and deploy the Auction contract to the local Ethereum node.
   - **Place Bids:** It will automatically place bids from randomly selected accounts until the auction ends.
   - **Determine the Winner:** After the auction ends, the script will display the winner and the winning bid for each round.

## Project Structure

**contracts/:** Contains the `Auction.sol` Solidity contract.
**scripts/:** Contains deployment and other utility scripts.
**marl/:** Contains the Python script `run_simulation.py` for running the auction simulation.
**artifacts/:** Contains compiled contract files (generated automatically).
**hardhat.config.js:** Configuration file for Hardhat.
**deploy_contract.py:** Python script for deploying the Auction contract.
**README.md:** Project documentation.

## How It Works

- **Local Ethereum Node:** The `npx hardhat node` command starts a local Ethereum node, which mimics the behavior of the real Ethereum network but in a controlled environment. This allows you to deploy and interact with smart contracts without needing to pay for gas fees or worry about real Ether.

- **Auction Contract:** The `Auction` contract is a simple smart contract that allows users to place bids on an item. The highest bidder wins the auction when the time runs out.

- **Python Simulation:** The Python script `run_simulation.py` automates the bidding process. It uses Web3.py to interact with the deployed contract, places bids, and determines the winner when the auction ends.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
