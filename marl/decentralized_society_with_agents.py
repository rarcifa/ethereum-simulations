import numpy as np
from web3 import Web3
import json
from stable_baselines3 import DQN
import gym
from gym import spaces

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Addresses of deployed contracts (replace these with actual addresses)
resource_pool_address = '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512'
farmer_address = '0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0'
builder_address = '0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9'
trader_address = '0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9'

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

class DecentralizedSocietyEnv(gym.Env):
    """
    Custom Gym Environment representing a decentralized society interacting with Ethereum smart contracts.
    This environment facilitates interactions between Farmer, Builder, and Trader agents using a shared resource pool.

    Attributes:
        resource_pool: A Web3 contract object representing the Resource Pool.
        farmer: A Web3 contract object representing the Farmer contract.
        builder: A Web3 contract object representing the Builder contract.
        trader: A Web3 contract object representing the Trader contract.
        accounts: A list of Ethereum accounts.
        total_resources: An integer representing the total resources in the pool.
        last_action_success: A flag indicating the success of the last action (1 for success, 0 for failure).
        action_space: Discrete action space with 8 possible actions (combination of farmer, builder, and trader choices).
        observation_space: Box observation space representing the current total resources and last action success.
    """
    def __init__(self, resource_pool, farmer, builder, trader, accounts):
        """
        Initializes the decentralized society environment with smart contracts and Ethereum accounts.

        Args:
            resource_pool: The Web3 contract object for the Resource Pool.
            farmer: The Web3 contract object for the Farmer.
            builder: The Web3 contract object for the Builder.
            trader: The Web3 contract object for the Trader.
            accounts: A list of Ethereum accounts used for interacting with the contracts.
        """
        super(DecentralizedSocietyEnv, self).__init__()
        self.resource_pool = resource_pool
        self.farmer = farmer
        self.builder = builder
        self.trader = trader
        self.accounts = accounts

        # Use a single Discrete action space with 8 possible actions
        self.action_space = spaces.Discrete(8)
        
        # Observation space: total resources and last action success
        self.observation_space = spaces.Box(low=np.array([0, 0]), high=np.array([1000, 1]), dtype=np.float32)

        self.total_resources = 100  # Initial resources
        self.last_action_success = 1  # Last action success

    def reset(self):
        """
        Resets the environment to its initial state with default resources and action success.

        Returns:
            observation: A numpy array representing the total resources and last action success.
        """
        self.total_resources = 100
        self.last_action_success = 1
        return np.array([self.total_resources, self.last_action_success], dtype=np.float32)

    def step(self, action):
        """
        Executes one step in the environment based on the agent's action.

        Args:
            action: An integer representing the combined action of the farmer, builder, and trader.

        Returns:
            observation: A numpy array representing the current total resources and last action success.
            reward: A sum of the rewards obtained by the farmer, builder, and trader for their actions.
            done: A boolean flag indicating whether the simulation has reached a terminal state.
            info: A dictionary containing additional information (currently empty).
        """
        rewards = np.zeros(3)  # Initialize rewards for farmer, builder, and trader
        action_combination = [action % 2, (action // 2) % 2, (action // 4) % 2]
        
        # Process Farmer's action
        try:
            if action_combination[0] == 0:
                self.farmer.functions.farmEfficient().transact({'from': self.accounts[0]})
                rewards[0] = 5
            else:
                self.farmer.functions.farmSelfish().transact({'from': self.accounts[0]})
                rewards[0] = -5
        except Exception as e:
            print("Farmer action failed:", str(e))
            rewards[0] = -10  # Penalize for failed transaction

        # Process Builder's action
        try:
            if action_combination[1] == 0:
                self.builder.functions.buildEfficient().transact({'from': self.accounts[1]})
                rewards[1] = 5
            else:
                self.builder.functions.buildSelfish().transact({'from': self.accounts[1]})
                rewards[1] = -5
        except Exception as e:
            print("Builder action failed:", str(e))
            rewards[1] = -10  # Penalize for failed transaction

        # Process Trader's action
        try:
            if action_combination[2] == 0:
                self.trader.functions.tradeEfficient().transact({'from': self.accounts[2]})
                rewards[2] = 5
            else:
                self.trader.functions.tradeSelfish().transact({'from': self.accounts[2]})
                rewards[2] = -5
        except Exception as e:
            print("Trader action failed:", str(e))
            rewards[2] = -10  # Penalize for failed transaction

        self.total_resources = self.resource_pool.functions.getTotalResources().call()
        done = self.total_resources <= 0 or self.total_resources >= 1000
        return np.array([self.total_resources, self.last_action_success], dtype=np.float32), np.sum(rewards), done, {}


    def render(self, mode='human'):
        """
        Renders the current state of the environment to the console.
        
        Args:
            mode: Render mode (currently only 'human' is supported).
        """
        print(f"Total Resources: {self.total_resources}, Last Action Success: {self.last_action_success}")


    def get_observation(self):
        """
        Returns the current observation of the environment's state.
        
        Returns:
            A numpy array representing the total resources and last action success.
        """
        # This method should return an array-like object that matches the input shape of the model.
        # Example: Return the total resources and last action success as the current state observation.
        return np.array([self.total_resources, self.last_action_success], dtype=np.float32)


# Train the model on the simulated environment
env = DecentralizedSocietyEnv(
    resource_pool=resource_pool,
    farmer=farmer,
    builder=builder,
    trader=trader,
    accounts=w3.eth.accounts
)

model = DQN("MlpPolicy", env, verbose=1)

# Uncomment to retrain
# Train the model (adjust the number of timesteps as needed)
# model.learn(total_timesteps=10000)

# Save the trained model to disk
# model.save("decentralized_society_model")

# Load the trained model
model = DQN.load("decentralized_society_model")

from stable_baselines3 import DQN

class Agent:
    """
    Class representing an agent in the decentralized society, responsible for making decisions 
    and interacting with smart contracts (Farmer, Builder, Trader).

    Attributes:
        account: The Ethereum account associated with the agent.
        model: The DQN model instance used for making decisions.
        contract_function_efficient: The function to call when the agent chooses the 'efficient' action.
        contract_function_selfish: The function to call when the agent chooses the 'selfish' action.
    """
    def __init__(self, account, contract_function_efficient, contract_function_selfish, model):
        """
        Initializes the agent with its account, contract functions, and decision-making model.

        Args:
            account: The Ethereum account controlled by the agent.
            contract_function_efficient: The contract function for the efficient action.
            contract_function_selfish: The contract function for the selfish action.
            model: The DQN model for deciding which action to take.
        """
        self.account = account
        self.model = model
        self.contract_function_efficient = contract_function_efficient
        self.contract_function_selfish = contract_function_selfish

    def decide_and_act(self):
        """
        Determines which action to take (efficient or selfish) based on the DQN model's prediction
        and executes the corresponding smart contract function.
        """
        obs = env.get_observation()  # Get the current state observation
        action, _ = self.model.predict(obs, deterministic=True)  # Get action from the model
        try:
            if action == 0:
                tx = self.contract_function_efficient().transact({'from': self.account})
                print(f"{self.account[:6]} chose to act efficiently.")
            else:
                tx = self.contract_function_selfish().transact({'from': self.account})
                print(f"{self.account[:6]} chose to act selfishly.")
            w3.eth.wait_for_transaction_receipt(tx)
        except Exception as e:
            print(f"Action failed for {self.account[:6]}: {str(e)}")


def simulate():
    """
    Simulates the interactions of the decentralized society over multiple iterations. 
    Each iteration, the farmer, builder, and trader agents decide and execute their actions.
    """
    farmer_agent = Agent(accounts[0], farmer.functions.farmEfficient, farmer.functions.farmSelfish, model)
    builder_agent = Agent(accounts[1], builder.functions.buildEfficient, builder.functions.buildSelfish, model)
    trader_agent = Agent(accounts[2], trader.functions.tradeEfficient, trader.functions.tradeSelfish, model)

    for i in range(iterations):
        print(f"\nIteration {i+1}")

        # Agents decide and act
        farmer_agent.decide_and_act()
        total_resources = resource_pool.functions.getTotalResources().call()
        print(f"Total Resources in Society: {total_resources}")

        if total_resources >= 5:
            builder_agent.decide_and_act()

        if total_resources >= 10:
            trader_agent.decide_and_act()

        # Print final resources after actions
        total_resources = resource_pool.functions.getTotalResources().call()
        print(f"Total Resources after trading: {total_resources}")

# Run the simulation
simulate()