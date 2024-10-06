# Auction Simulation Project

This project is a simulation of an Ethereum-based decentralized society system. The project involves deploying a smart contract to a local Ethereum network, placing bids, and determining the decentralized society winner through a Python script. This README file will guide you through the setup and usage of the project.

## Prerequisites

Before you begin, ensure you have the following software installed on your system:

- **Node.js**: A JavaScript runtime environment (https://nodejs.org/)
- **npm**: Node Package Manager, installed with Node.js (https://www.npmjs.com/)
- **Python 3.x**: The programming language used to run the decentralized society simulation (https://www.python.org/)

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

## Setup

1. **Start Ethereum Localhost Node**
   To simulate the Ethereum network locally, we'll use Hardhat, an Ethereum development environment.

   Open a terminal and run the Ethereum localhost node:

   ```bash
   npx hardhat node
   ```

   This command will initiate a local Ethereum node, connecting you to a local snapshot of the Ethereum network. The node will provide you with several accounts preloaded with test Ether, which you can use for testing and development.

2. **Deploy Smart Contracts**

   Open a second terminal and navigate to your project directory:

   ```bash
   cd marl
   npx hardhat run scripts/decentralizedSociety.ts --network localhost
   ```

   This will output the addresses of the deployed contracts:

   ```
   Deploying contracts with the account: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
   ResourcePool deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3
   Farmer deployed to: 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512
   Builder deployed to: 0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0
   Trader deployed to: 0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9
   ```

## Configuration

Update the contract addresses in your simulation script:

```python
# In decentralized_society_with_agents.py
resource_pool_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
farmer_address = '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512'
builder_address = '0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0'
trader_address = '0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9'
```

## Training the Model

If you need to retrain the model:

```python
# Uncomment to retrain
model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="./tensorboard_logs/")
callback = CustomTrainingCallback(verbose=1)
model.learn(total_timesteps=10000, callback=callback)
model.save("decentralized_society_model")
```

## Running the Simulation

To run the simulation, execute:

```bash
python3 decentralized_society_with_agents.py
```

The simulation script will:

- **Deploy the Auction Contract:** It will compile and deploy the Auction contract to the local Ethereum node.
- **Place Bids:** It will automatically place bids from randomly selected accounts until the decentralized society ends.
- **Determine the Winner:** After the decentralized society ends, the script will display the winner and the winning bid for each round.

Observe the output in the two terminals to see the live simulation.

## Comparison with Baseline

To compare the results with a baseline scenario using random decision-making:

```bash
python3 decentralized_society_without_agents.py
```

## Analyzing the Results

For detailed analysis, you can use TensorBoard:

```bash
tensorboard --logdir=./tensorboard_logs/
```

Open your browser and navigate to `http://localhost:6006/` to view the training and simulation metrics.

---

## Running the Local Ethereum Node

To simulate the Ethereum network locally, we'll use Hardhat, an Ethereum development environment.

1. Start the local Ethereum node using Hardhat.

   ```bash
   npx hardhat node
   ```

   This command will initiate a local Ethereum node, connecting you to a local snapshot of the Ethereum network. The node will provide you with several accounts preloaded with test Ether, which you can use for testing and development.

2. Keep this terminal open and running as it serves as the backend for deploying contracts and running the decentralized society simulation.

## Running the Auction Simulation

The decentralized society simulation script places bids on the deployed decentralized society contract using randomly generated accounts. The simulation will run through several rounds, each representing a separate decentralized society.

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
   - **Place Bids:** It will automatically place bids from randomly selected accounts until the decentralized society ends.
   - **Determine the Winner:** After the decentralized society ends, the script will display the winner and the winning bid for each round.

## Project Structure

- **contracts/:** Contains the `decentralizedSociety` Solidity contracts
- **scripts/:** Contains deployment and other utility scripts.
- **marl/:** Contains the Python script `decentralized_society_with_agents.py` for running the decentralized society simulation.
- **artifacts/:** Contains compiled contract files (generated automatically).
- **hardhat.config.js:** Configuration file for Hardhat.
- **deploy_contract.py:** Python script for deploying the Auction contract.
- **README.md:** Project documentation.

## How It Works

- **Local Ethereum Node:** The `npx hardhat node` command starts a local Ethereum node, which mimics the behavior of the real Ethereum network but in a controlled environment. This allows you to deploy and interact with smart contracts without needing to pay for gas fees or worry about real Ether.

- **Auction Contract:** The `Auction` contract is a simple smart contract that allows users to place bids on an item. The highest bidder wins the decentralized society when the time runs out.

- **Python Simulation:** The Python script `run_simulation.py` automates the bidding process. It uses Web3.py to interact with the deployed contract, places bids, and determines the winner when the decentralized society ends.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
