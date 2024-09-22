import random
from web3 import Web3
import json
import matplotlib.pyplot as plt
import csv

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Addresses of deployed contracts (replace these with actual addresses)
resource_pool_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
farmer_address = '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512'
builder_address = '0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0'
trader_address = '0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9'

with open('../artifacts/contracts/decentralizedSociety/ResourcePool.sol/ResourcePool.json') as f:
    resource_pool_abi = json.load(f)['abi']

with open('../artifacts/contracts/decentralizedSociety/Farmer.sol/Farmer.json') as f:
    farmer_abi = json.load(f)['abi']

with open('../artifacts/contracts/decentralizedSociety/Builder.sol/Builder.json') as f:
    builder_abi = json.load(f)['abi']

with open('../artifacts/contracts/decentralizedSociety/Trader.sol/Trader.json') as f:
    trader_abi = json.load(f)['abi']

resource_pool = w3.eth.contract(address=resource_pool_address, abi=resource_pool_abi)
farmer = w3.eth.contract(address=farmer_address, abi=farmer_abi)
builder = w3.eth.contract(address=builder_address, abi=builder_abi)
trader = w3.eth.contract(address=trader_address, abi=trader_abi)

# Simulation parameters
accounts = w3.eth.accounts
iterations = 50

class FarmerRLAgent:
    """
    Reinforcement Learning agent representing a farmer in the decentralized society.
    Responsible for making decisions (efficient or selfish farming) based on a model.
    """
    def __init__(self, account, model):
        """
        Initialize the FarmerRLAgent.

        Args:
            account: The Ethereum account controlled by the agent.
            model: The DQN model used for decision making.
        """
        self.account = account
        self.model = model  # Directly pass the DQN model instance

    def decide_action(self, obs):
        """
        Decide which action to take based on the model's prediction.

        Args:
            obs: The current observation from the environment.
        
        Returns:
            action: The action decided by the model (0 for efficient, 1 for selfish).
        """
        action, _ = self.model.predict(obs)
        return action

    def execute_action(self, action):
        """
        Execute the chosen action (farming efficiently or selfishly) on the blockchain.

        Args:
            action: The chosen action (0 for efficient farming, 1 for selfish farming).
        """
        if action == 0:
            tx_farm = farmer.functions.farmEfficient().transact({'from': self.account})
            print("Farmer chose to farm efficiently")
        else:
            tx_farm = farmer.functions.farmSelfish().transact({'from': self.account})
            print("Farmer chose to farm selfishly")
            
        w3.eth.wait_for_transaction_receipt(tx_farm)


class BuilderRLAgent:
    """
    Reinforcement Learning agent representing a builder in the decentralized society.
    Responsible for making decisions (efficient or selfish building) based on a model.
    """
    def __init__(self, account, model):
        """
        Initialize the BuilderRLAgent.

        Args:
            account: The Ethereum account controlled by the agent.
            model: The DQN model used for decision making.
        """
        self.account = account
        self.model = model  # Directly pass the DQN model instance

    def decide_action(self, obs):
        """
        Decide which action to take based on the model's prediction.

        Args:
            obs: The current observation from the environment.
        
        Returns:
            action: The action decided by the model (0 for efficient, 1 for selfish).
        """
        action, _ = self.model.predict(obs)
        return action

    def execute_action(self, action):
        """
        Execute the chosen action (building efficiently or selfishly) on the blockchain.

        Args:
            action: The chosen action (0 for efficient building, 1 for selfish building).
        """
        if action == 0:
            tx_build = builder.functions.buildEfficient().transact({'from': self.account})
            print("Builder chose to build efficiently")
        else:
            tx_build = builder.functions.buildSelfish().transact({'from': self.account})
            print("Farmer chose to build selfishly")
            
        w3.eth.wait_for_transaction_receipt(tx_build)

# Trader RL Agent class
class TraderRLAgent:
    """
    Reinforcement Learning agent representing a trader in the decentralized society.
    Responsible for making decisions (efficient or selfish trading) based on a model.
    """
    def __init__(self, account, model):
        """
        Initialize the TraderRLAgent.

        Args:
            account: The Ethereum account controlled by the agent.
            model: The DQN model used for decision making.
        """
        self.account = account
        self.model = model  # Directly pass the DQN model instance

    def decide_action(self, obs):
        """
        Decide which action to take based on the model's prediction.

        Args:
            obs: The current observation from the environment.
        
        Returns:
            action: The action decided by the model (0 for efficient, 1 for selfish).
        """
        action, _ = self.model.predict(obs)
        return action

    def execute_action(self, action):
        """
        Execute the chosen action (trading efficiently or selfishly) on the blockchain.

        Args:
            action: The chosen action (0 for efficient trading, 1 for selfish trading).
        """
        if action == 0:
            tx_trade = trader.functions.tradeEfficient().transact({'from': self.account})
            print("Trader chose to trade efficiently")
        else:
            tx_trade = trader.functions.tradeSelfish().transact({'from': self.account})
            print("Trader chose to trade selfishly")
            
        w3.eth.wait_for_transaction_receipt(tx_trade)

# Initialize agents
agent_farmer = FarmerRLAgent(accounts[0], "model") 
agent_builder = BuilderRLAgent(accounts[2], "model")
agent_trader = TraderRLAgent(accounts[2], "model")

# Initialize tracking variables for both MARL and random simulations
total_resources_over_time = []
farmer_rewards = []
builder_rewards = []
trader_rewards = []
efficient_actions = {'farmer': 0, 'builder': 0, 'trader': 0}
selfish_actions = {'farmer': 0, 'builder': 0, 'trader': 0}

def simulate():
    """
    Simulate the decentralized society by having agents make decisions for a set number of iterations.
    Track total resources and agent actions over time.
    """
    for i in range(iterations):
        print(f"\nIteration {i+1}")

        # Step 1: Farmer's choice: either farm efficiently or selfishly
        try:
            if random.choice([True, False]):  # Randomly choose efficient or selfish
                tx_farm = farmer.functions.farmEfficient().transact({'from': accounts[0]})
                print("Farmer chose to farm efficiently")
                efficient_actions['farmer'] += 1
                farmer_rewards.append(5)  # Reward for efficient farming
            else:
                tx_farm = farmer.functions.farmSelfish().transact({'from': accounts[0]})
                print("Farmer chose to farm selfishly")
                selfish_actions['farmer'] += 1
                farmer_rewards.append(-5)  # Penalty for selfish farming
            w3.eth.wait_for_transaction_receipt(tx_farm)
        except Exception as e:
            print(f"Farmer failed to farm: {e}")
            farmer_rewards.append(-10)  # Penalty for failure

        # Step 2: Check total resources in society
        total_resources = resource_pool.functions.getTotalResources().call()
        print(f"Total Resources in Society: {total_resources}")
        total_resources_over_time.append(total_resources)

        # Step 3: Builder's choice: either build efficiently or selfishly
        if total_resources >= 5:  # Assuming builder needs at least 5 resources
            try:
                if random.choice([True, False]):  # Randomly choose efficient or selfish
                    tx_build = builder.functions.buildEfficient().transact({'from': accounts[1]})
                    print("Builder chose to build efficiently")
                    efficient_actions['builder'] += 1
                    builder_rewards.append(5)  # Reward for efficient building
                else:
                    tx_build = builder.functions.buildSelfish().transact({'from': accounts[1]})
                    print("Builder chose to build selfishly")
                    selfish_actions['builder'] += 1
                    builder_rewards.append(-5)  # Penalty for selfish building
                w3.eth.wait_for_transaction_receipt(tx_build)
            except Exception as e:
                print(f"Builder failed to build: {e}")
                builder_rewards.append(-10)  # Penalty for failure
        else:
            print("Not enough resources for building")
            builder_rewards.append(0)  # No action taken

        # Step 4: Trader's choice: either trade efficiently or selfishly
        if total_resources >= 10:  # Ensuring enough resources for a selfish trade
            try:
                if random.choice([True, False]):  # Randomly choose efficient or selfish
                    tx_trade = trader.functions.tradeEfficient().transact({'from': accounts[2]})
                    print("Trader chose to trade efficiently")
                    efficient_actions['trader'] += 1
                    trader_rewards.append(7)  # Reward for efficient trading
                else:
                    tx_trade = trader.functions.tradeSelfish().transact({'from': accounts[2]})
                    print("Trader chose to trade selfishly")
                    selfish_actions['trader'] += 1
                    trader_rewards.append(-7)  # Penalty for selfish trading
                w3.eth.wait_for_transaction_receipt(tx_trade)
            except Exception as e:
                print(f"Trader failed to trade: {e}")
                trader_rewards.append(-10)  # Penalty for failure
        else:
            print("Not enough resources for trading")
            trader_rewards.append(0)  # No action taken

        # Print final resources after actions
        total_resources = resource_pool.functions.getTotalResources().call()
        print(f"Total Resources after trading: {total_resources}")

    # Plot results or write them to a CSV for further analysis
    plot_results()

def plot_results():
    """
    Plot the simulation results.
    """
    # Plot total resources over time
    plt.plot(total_resources_over_time, label="Total Resources")
    plt.title("Total Resources Over Time")
    plt.xlabel("Iteration")
    plt.ylabel("Resources")
    plt.legend()
    plt.show()

    # Optionally: Write metrics to CSV
    with open('simulation_results_no_agents.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Iteration', 'Total Resources', 'Farmer Reward', 'Builder Reward', 'Trader Reward'])
        for i in range(len(total_resources_over_time)):
            csv_writer.writerow([i+1, total_resources_over_time[i], farmer_rewards[i], builder_rewards[i], trader_rewards[i]])

# Run the simulation
simulate()
