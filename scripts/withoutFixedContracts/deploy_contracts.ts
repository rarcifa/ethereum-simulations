import hre from "hardhat";

async function main() {
  const { ethers } = hre;

  // Deploy vulnerable ChainWallet
  const ChainWallet = await ethers.getContractFactory("ChainWallet");
  const chainWallet = await ChainWallet.deploy();
  await chainWallet.deployed();
  console.log("ChainWallet deployed to:", chainWallet.address);

  // Deploy ChainReentrancy to attack ChainWallet
  const ChainReentrancy = await ethers.getContractFactory("ChainReentrancy");
  const chainReentrancy = await ChainReentrancy.deploy(chainWallet.address);
  await chainReentrancy.deployed();
  console.log("ChainReentrancy deployed to:", chainReentrancy.address);

  // Deploy CEI Fixed Wallet
  const CEIFixedChainWallet = await ethers.getContractFactory(
    "CEIFixedChainWallet"
  );
  const ceiFixedChainWallet = await CEIFixedChainWallet.deploy();
  await ceiFixedChainWallet.deployed();
  console.log("CEIFixedChainWallet deployed to:", ceiFixedChainWallet.address);

  // Deploy Mutex Fixed Wallet
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
