import { ethers } from "hardhat";

async function main() {
  const ceiFixedChainWalletAddress =
    "0x959922bE3CAee4b8Cd9a407cc3ac1C251C2007B1"; // Replace with actual address
  const mutexFixedChainWalletAddress =
    "0x9A9f2CCfdE556A7E9Ff0848998Aa4a0CFD8863AE"; // Replace with actual address
  const chainWalletAddress = "0x9A676e781A523b5d0C0e43731313A708CB607508";

  // Attach to the deployed contracts
  const CEIFixedChainWallet = await ethers.getContractAt(
    "CEIFixedChainWallet",
    ceiFixedChainWalletAddress
  );
  const MutexFixedChainWallet = await ethers.getContractAt(
    "MutexFixedChainWallet",
    mutexFixedChainWalletAddress
  );
  const ChainWallet = await ethers.getContractAt(
    "ChainWallet",
    chainWalletAddress
  );

  const depositAmount = ethers.utils.parseEther("10");

  // Deposit funds into CEIFixedChainWallet
  await CEIFixedChainWallet.deposit({ value: depositAmount });
  console.log(`Deposited ${depositAmount} to CEIFixedChainWallet`);

  // Deposit funds into MutexFixedChainWallet
  await MutexFixedChainWallet.deposit({ value: depositAmount });
  console.log(`Deposited ${depositAmount} to MutexFixedChainWallet`);

  // Deposit funds into MutexFixedChainWallet
  await ChainWallet.deposit({ value: depositAmount });
  console.log(`Deposited ${depositAmount} to ChainWallet`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
