import { ethers } from "hardhat";

async function main() {
  const CEIFixedChainWallet = await ethers.getContractFactory(
    "CEIFixedChainWallet"
  );
  const ceiFixedChainWallet = await CEIFixedChainWallet.deploy();
  await ceiFixedChainWallet.deployed();
  console.log("CEIFixedChainWallet deployed to:", ceiFixedChainWallet.address);

  const MutexFixedChainWallet = await ethers.getContractFactory(
    "MutexFixedChainWallet"
  );
  const mutexFixedChainWallet = await MutexFixedChainWallet.deploy();
  await mutexFixedChainWallet.deployed();
  console.log(
    "MutexFixedChainWallet deployed to:",
    mutexFixedChainWallet.address
  );
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
