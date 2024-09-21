import json
import numpy as np
from web3 import Web3
from stable_baselines3 import DQN
import subprocess
import gym
from gym import spaces
import random

class DAOVotingEnv(gym.Env):
    """
    Custom Environment for DAO Voting, compatible with OpenAI Gym.
    This environment simulates voting on proposals within a DAO (Decentralized Autonomous Organization).
    """
    def __init__(self, contract):
        """
        Initializes the DAOVotingEnv environment.

        Args:
            contract: A Web3 contract object representing the DAO smart contract.
        """
        super(DAOVotingEnv, self).__init__()
        self.contract = contract
        self.proposal_id = 0
        self.action_space = spaces.Discrete(2)  # Two actions: Vote for or against
        self.observation_space = spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)

    def reset(self):
        """
        Resets the environment to an initial state and returns an initial observation.

        Returns:
            observation: A random float between 0 and 1, representing a new proposal.
        """
        self.proposal_id += 1
        observation = np.array([random.random()])
        return observation

    def step(self, action):
        """
        Executes one step within the environment.

        Args:
            action: An integer representing the action to take (0 for voting against, 1 for voting for).
        
        Returns:
            observation: A new random float observation.
            reward: Reward for the action taken (1 for vote for, -1 for vote against).
            done: Boolean indicating whether the episode is finished.
            info: An empty dictionary for additional info.
        """
        done = False
        reward = 0

        # Simulate voting based on the action
        if action == 0:
            # Vote Against
            tx = self.contract.functions.vote(self.proposal_id, False).transact()
            reward = -1  # Example reward for voting against (modify as needed)
        elif action == 1:
            # Vote For
            tx = self.contract.functions.vote(self.proposal_id, True).transact()
            reward = 1  # Example reward for voting for (modify as needed)

        # Example: End the episode after one action
        done = True

        # Return the next state (new observation), reward, done, and any additional info
        observation = np.array([random.random()])
        return observation, reward, done, {}

    def render(self, mode='human', close=False):
        """
        Renders the environment. Currently, no rendering is implemented.
        """
        pass
    
# Connect to local Hardhat node
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
print("Connected to Ethereum:", web3.is_connected())

def compile_and_get_abi():
    """
    Compiles the smart contract using Hardhat and loads the ABI (Application Binary Interface).

    Returns:
        contract_abi: ABI of the compiled contract.
    """
    # Run Hardhat compilation task
    subprocess.run(["npx", "hardhat", "compile"], check=True)

    # Load ABI from the newly generated artifact
    with open('../artifacts/contracts/dao.sol/Dao.json', 'r') as abi_file:
        contract_json = json.load(abi_file)
        contract_abi = contract_json['abi']

    return contract_abi

def deploy_contract():
    """
    Deploys the DAO contract using Hardhat and retrieves its address.

    Returns:
        contract_address: The address of the deployed contract.
    
    Raises:
        Exception: If the contract address cannot be retrieved from the deployment output.
    """
    result = subprocess.run(
        ["npx", "hardhat", "run", "../scripts/dao.ts", "--network", "localhost"],
        capture_output=True, text=True
    )
    output = result.stdout
    contract_address = None
    for line in output.splitlines():
        if "DAO contract deployed to:" in line:
            contract_address = line.split(": ")[1].strip()
            break
    if not contract_address:
        raise Exception("Failed to deploy contract and capture contract address.")
    return contract_address

# Load contract ABI and address
contract_address = deploy_contract()
contract = web3.eth.contract(address=contract_address, abi=compile_and_get_abi())

# Initialize the custom Gym environment
env = DAOVotingEnv(contract)

# Initialize DQN RL model
model = DQN("MlpPolicy", env, verbose=1)

# RL Agent class
class RLAgent:
    """
    Reinforcement Learning Agent that interacts with the DAO environment.
    """
    def __init__(self, account, model):
        """
        Initializes the RL agent with an Ethereum account and a trained RL model.

        Args:
            account: Ethereum account to act on behalf of.
            model: A trained DQN model instance.
        """
        self.account = account
        self.model = model  # Directly pass the DQN model instance

    def decide_action(self, obs):
        """
        Decides which action to take based on the observation from the environment.

        Args:
            obs: The current state observation from the environment.
        
        Returns:
            action: The chosen action (0 for voting against, 1 for voting for).
        """
        action, _ = self.model.predict(obs)
        return action

    def execute_action(self, action, proposal_id):
        """
        Executes the chosen action (voting) on the blockchain.

        Args:
            action: The action to execute (0 for voting against, 1 for voting for).
            proposal_id: The proposal ID being voted on.
        """
        if action == 0:
            tx = contract.functions.vote(proposal_id, False).transact({'from': self.account, 'gas': 3000000})
        else:
            tx = contract.functions.vote(proposal_id, True).transact({'from': self.account, 'gas': 3000000})
        web3.eth.wait_for_transaction_receipt(tx)

    def propose(self, title, description):
        """
        Proposes a new DAO proposal on the blockchain.

        Args:
            title: The title of the proposal.
            description: The description of the proposal.
        """
        tx = contract.functions.propose(title, description).transact({'from': self.account, 'gas': 3000000})
        web3.eth.wait_for_transaction_receipt(tx)

class SimulatedDAOVotingEnv(gym.Env):
    """
    Simulated Environment for training the RL model outside the blockchain.
    Used to train the agent on voting behaviors without interacting with the actual blockchain.
    """
    def __init__(self):
        """
        Initializes the Simulated DAOVoting environment.
        """
        super(SimulatedDAOVotingEnv, self).__init__()
        self.proposal_id = 0
        self.action_space = spaces.Discrete(2)  # Two actions: Vote for or against
        self.observation_space = spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)

    def reset(self):
        """
        Resets the environment to an initial state and returns an initial observation.

        Returns:
            observation: A random float between 0 and 1, representing a new proposal.
        """
        self.proposal_id += 1
        observation = np.array([random.random()])
        return observation

    def step(self, action):
        """
        Simulates one step (voting) within the environment.

        Args:
            action: An integer representing the action to take (0 for voting against, 1 for voting for).
        
        Returns:
            observation: A new random float observation.
            reward: Reward for the action taken (1 for vote for, -1 for vote against).
            done: Boolean indicating whether the episode is finished.
            info: An empty dictionary for additional info.
        """
        done = False
        reward = 0

        # Simulate voting outcome
        if action == 0:
            reward = -1  # Example reward for voting against
        elif action == 1:
            reward = 1  # Example reward for voting for

        # End the episode after one action
        done = True

        # Return the next state (new observation), reward, done, and any additional info
        observation = np.array([random.random()])
        return observation, reward, done, {}

    def render(self, mode='human', close=False):
        """
        Renders the environment. Currently, no rendering is implemented.
        """
        pass

# Train the model on the simulated environment
train_env = SimulatedDAOVotingEnv()
model = DQN("MlpPolicy", train_env, verbose=1)

# Train the model (adjust the number of timesteps as needed)
model.learn(total_timesteps=10000)

# Save the trained model to disk
model.save("dao_voting_model")

# Load the trained model
model2 = DQN.load("dao_voting_model")

# Load the trained model
model = DQN.load("dao_voting_model")

def run_simulation():
    """
    Runs the DAO voting simulation by creating a proposal and having RL agents vote on it.
    """
    model = DQN.load("dao_voting_model")  # Load the model correctly here
    accounts = web3.eth.accounts
    proposer = RLAgent(accounts[0], model)  # Pass the model instance
    voters = [RLAgent(account, model) for account in accounts[1:19]]  # Pass the model instance to each voter

    print("Creating proposal...")
    proposer.propose("Test Proposal", "This is a test proposal")

    proposal_id = contract.functions.proposalCount().call() - 1
    print(f"Proposal ID: {proposal_id}")

    obs = env.reset()  # Get initial observation for each agent

    print("Voting on proposal...")
    for i, voter in enumerate(voters):
        action = voter.decide_action(obs)
        voter.execute_action(action, proposal_id)  # Execute action on the blockchain
        print(f"Voter {i + 1} ({voter.account}) voted")

    proposal_after_vote = contract.functions.proposals(proposal_id).call()
    print(f"Votes FOR: {proposal_after_vote[3]}, Votes AGAINST: {proposal_after_vote[4]}")

if __name__ == '__main__':
    env = DAOVotingEnv(contract)  # Ensure this environment is initialized here for testing/deployment
    run_simulation()
