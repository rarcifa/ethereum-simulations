import hre from "hardhat";

async function main() {
  const { ethers } = hre;

  const chainWalletAddress = "0x9A676e781A523b5d0C0e43731313A708CB607508";
  const chainReentrancyAddress = "0x0B306BF915C4d645ff596e518fAf3F9669b97016";
  const ceiFixedChainWalletAddress =
    "0x959922bE3CAee4b8Cd9a407cc3ac1C251C2007B1"; // Replace with actual address
  const mutexFixedChainWalletAddress =
    "0x9A9f2CCfdE556A7E9Ff0848998Aa4a0CFD8863AE"; // Replace with actual address

  // Get balances after attack
  const chainWalletBalance = await ethers.provider.getBalance(
    chainWalletAddress
  );
  const chainReentrancyBalance = await ethers.provider.getBalance(
    chainReentrancyAddress
  );
  const ceiFixedChainWalletBalance = await ethers.provider.getBalance(
    ceiFixedChainWalletAddress
  );
  const mutexFixedChainWalletBalance = await ethers.provider.getBalance(
    mutexFixedChainWalletAddress
  );

  console.log(
    `ChainWallet Contract Balance: ${ethers.utils.formatEther(
      chainWalletBalance
    )} ETH`
  );
  console.log(
    `ChainReentrancy Contract Balance: ${ethers.utils.formatEther(
      chainReentrancyBalance
    )} ETH`
  );
  console.log(
    `CEIFixedChainWallet Contract Balance: ${ethers.utils.formatEther(
      ceiFixedChainWalletBalance
    )} ETH`
  );
  console.log(
    `MutexFixedChainWallet Contract Balance: ${ethers.utils.formatEther(
      mutexFixedChainWalletBalance
    )} ETH`
  );
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
