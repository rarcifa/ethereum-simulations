import hre from "hardhat";

async function main() {
  const { ethers } = hre;

  // Addresses from deployment
  const chainWalletAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";
  const chainReentrancyAddress = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512";

  // Get balances after attack
  const chainWalletBalance = await ethers.provider.getBalance(
    chainWalletAddress
  );
  const chainReentrancyBalance = await ethers.provider.getBalance(
    chainReentrancyAddress
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
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
