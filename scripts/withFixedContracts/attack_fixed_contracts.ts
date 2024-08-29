import { ethers } from "hardhat";

async function main() {
  const chainReentrancyAddress = "0x0B306BF915C4d645ff596e518fAf3F9669b97016";

  // Addresses of the fixed contracts
  const ceiFixedChainWalletAddress =
    "0x959922bE3CAee4b8Cd9a407cc3ac1C251C2007B1";
  const mutexFixedChainWalletAddress =
    "0x9A9f2CCfdE556A7E9Ff0848998Aa4a0CFD8863AE";

  // Attach to the deployed ChainReentrancy contract
  const ChainReentrancy = await ethers.getContractAt(
    "ChainReentrancy",
    chainReentrancyAddress
  );

  // Attach to the fixed contracts
  const CEIFixedChainWallet = await ethers.getContractAt(
    "CEIFixedChainWallet",
    ceiFixedChainWalletAddress
  );
  const MutexFixedChainWallet = await ethers.getContractAt(
    "MutexFixedChainWallet",
    mutexFixedChainWalletAddress
  );

  // Perform the attack on CEI Fixed Chain Wallet
  console.log("Attacking CEIFixedChainWallet...");
  await ChainReentrancy.attack({ value: ethers.utils.parseEther("1") });
  console.log("Attack performed on CEIFixedChainWallet");

  // Perform the attack on Mutex Fixed Chain Wallet
  console.log("Attacking MutexFixedChainWallet...");
  await ChainReentrancy.attack({ value: ethers.utils.parseEther("1") });
  console.log("Attack performed on MutexFixedChainWallet");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
