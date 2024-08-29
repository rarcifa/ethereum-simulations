import hre from "hardhat";

/**
 * This function creates a new random wallet, deploys the Auction contract with the wallet as the beneficiary,
 * and logs the necessary deployment details.
 */
async function main() {
  /**
   * Generate a new random Ethereum wallet.
   * @returns {Object} Wallet object containing the address and private key.
   */
  const wallet = hre.ethers.Wallet.createRandom();

  console.log(`Address: ${wallet.address}`);
  console.log(`Private Key: ${wallet.privateKey}`);

  /**
   * Get the contract factory for the Auction contract.
   * @returns {Promise<ContractFactory>} A promise that resolves to the Auction contract factory.
   */
  const Auction = await hre.ethers.getContractFactory("Auction");

  /**
   * Deploy the Auction contract.
   * @param {number} biddingTime - The duration of the auction in seconds.
   * @param {string} beneficiary - The address of the beneficiary who will receive the highest bid.
   * @returns {Promise<Contract>} A promise that resolves to the deployed Auction contract.
   */
  const auction = await Auction.deploy(30, wallet.address);

  await auction.deployed();

  console.log("Auction deployed to:", auction.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
