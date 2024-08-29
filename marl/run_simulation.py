import time
import subprocess
import random
from web3 import Web3
import json
import os

# Set up web3 connection to local Hardhat node
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

def compile_and_get_abi():
    """
    Compiles the Auction contract using Hardhat and retrieves the ABI.
    
    Returns:
        dict: The ABI of the compiled Auction contract.
    """
    # Run Hardhat compilation task
    subprocess.run(["npx", "hardhat", "compile"], check=True)

    # Load ABI from the newly generated artifact
    with open('../artifacts/contracts/auction.sol/Auction.json', 'r') as abi_file:
        contract_json = json.load(abi_file)
        contract_abi = contract_json['abi']

    return contract_abi

def deploy_contract():
    """
    Deploys the auction contract using a Hardhat script.

    Returns:
        str: The deployed contract's address.

    Raises:
        Exception: If the contract address cannot be captured from the deployment output.
    """
    # Run the Hardhat deployment script and capture the output
    result = subprocess.run(
        ["npx", "hardhat", "run", "../scripts/auction.ts", "--network", "localhost"],
        capture_output=True, text=True
    )
    output = result.stdout

    # Extract the contract address from the output
    contract_address = None
    for line in output.splitlines():
        if "Auction deployed to:" in line:
            contract_address = line.split(": ")[1].strip()
            break

    if not contract_address:
        raise Exception("Failed to deploy contract and capture contract address.")

    return contract_address

def auction_is_active(auction_contract):
    """
    Checks if the auction is still active by querying the 'ended' public state variable.

    Args:
        auction_contract: The auction contract instance.

    Returns:
        bool: True if the auction is still active, False if it has ended.
    """
    return not auction_contract.functions.ended().call()

def wait_for_auction_end(auction_contract):
    """
    Waits until the auction ends by comparing the current time with the auction end time.

    Args:
        auction_contract: The auction contract instance.
    """
    auction_end_time = auction_contract.functions.auctionEndTime().call()
    current_time = web3.eth.get_block('latest')['timestamp']
    
    if current_time < auction_end_time:
        wait_time = auction_end_time - current_time
        print(f"Waiting for {wait_time} seconds until auction ends...")
        time.sleep(wait_time + 1)  # Wait a bit more to ensure the auction has ended

def get_auction_winner(auction_contract):
    """
    Retrieves the highest bidder and the highest bid from the auction contract.

    Args:
        auction_contract: The auction contract instance.

    Returns:
        tuple: The address of the highest bidder and the value of the highest bid.
    """
    highest_bidder = auction_contract.functions.highestBidder().call()
    highest_bid = auction_contract.functions.highestBid().call()
    return highest_bidder, highest_bid

def generate_dynamic_bid(current_highest_bid, min_increment, max_increment):
    """
    Generates a new bid dynamically based on the current highest bid.

    Args:
        current_highest_bid (int): The current highest bid in wei.
        min_increment (int): The minimum increment for the new bid.
        max_increment (int): The maximum increment for the new bid.

    Returns:
        int: The new bid value in wei.
    """
    increment = random.uniform(min_increment, max_increment)
    new_bid = current_highest_bid + increment
    return new_bid

def run_simulation():
    """
    Runs the auction simulation across multiple rounds.
    Deploys the auction contract, places bids, waits for auction to end, and announces the winner.
    """
    # Compile the contract and retrieve its ABI
    contract_abi = compile_and_get_abi()

    # Example item worths for each round, in wei
    item_worths = [
        web3.to_wei(5, 'ether'),
        web3.to_wei(10, 'ether'),
        web3.to_wei(7, 'ether'),
        web3.to_wei(12, 'ether'),
        web3.to_wei(8, 'ether')
    ]

    for round_num in range(5):
        print(f"Starting round {round_num + 1}")

        # Deploy a new auction contract and get the contract address
        contract_address = deploy_contract()
        print(f"Auction contract deployed at {contract_address} for round {round_num + 1}")

        # Initialize contract instance
        auction_contract = web3.eth.contract(address=contract_address, abi=contract_abi)

        item_worth = item_worths[round_num]
        print(f"Item worth for round {round_num + 1}: {web3.from_wei(item_worth, 'ether')} ETH")

        for bid_num in range(25):
            if auction_is_active(auction_contract):
                current_highest_bid = auction_contract.functions.highestBid().call()
                current_highest_bidder = auction_contract.functions.highestBidder().call()

                # Randomly select an account for bidding
                chosen_account = random.choice(web3.eth.accounts)

                # Check if the chosen account is already the highest bidder
                if chosen_account == current_highest_bidder:
                    print(f"Skipping bid {bid_num + 1}: {chosen_account} is already the highest bidder.")
                    continue

                new_bid = generate_dynamic_bid(
                    current_highest_bid,
                    web3.to_wei(0.1, 'ether'),
                    web3.to_wei(1, 'ether')
                )

                # Log a warning if the bid exceeds the item's worth
                if new_bid > item_worth:
                    print(f"Warning: Bid {web3.from_wei(new_bid, 'ether')} ETH exceeds the item worth of {web3.from_wei(item_worth, 'ether')} ETH.")

                print(f"Placing Bid {bid_num + 1} with value {web3.from_wei(new_bid, 'ether')} ETH from account {chosen_account}")

                # Set the chosen account as the default account for the transaction
                web3.eth.default_account = chosen_account
                tx_hash = auction_contract.functions.bid().transact({
                    'from': web3.eth.default_account,
                    'value': int(new_bid)
                })
                web3.eth.wait_for_transaction_receipt(tx_hash)
                print(f"Bid {bid_num + 1} placed by {chosen_account} with value {web3.from_wei(new_bid, 'ether')} ETH")

                # Simulate a short delay before the next bid
                time.sleep(1)
            else:
                print(f"Auction ended before bid {bid_num + 1}. Finalizing auction.")
                break  # Exit the bidding loop since the auction has ended

        # Wait until the auction naturally ends
        wait_for_auction_end(auction_contract)

        # Ensure the auction is ended
        if auction_is_active(auction_contract):
            print("Attempting to end the auction.")
            web3.eth.default_account = web3.eth.accounts[0]
            tx_hash = auction_contract.functions.auctionEnd().transact({
                'from': web3.eth.default_account,
                'gas': 2000000
            })
            web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Auction ended for round {round_num + 1}.")

        # After the auction ends, display the winner
        if not auction_is_active(auction_contract):
            winner, winning_bid = get_auction_winner(auction_contract)
            print(f"The winner of round {round_num + 1} is {winner} with a bid of {web3.from_wei(winning_bid, 'ether')} ETH.")
        else:
            print("Auction is still active, no winner to display yet.")

        # Short pause before starting the next round
        time.sleep(5)

if __name__ == "__main__":
    run_simulation()