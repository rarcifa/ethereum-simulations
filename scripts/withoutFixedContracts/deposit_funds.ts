import hre from "hardhat";

async function main() {
  const { ethers } = hre;

  // Addresses from deployment
  const chainWalletAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

  // Attach to deployed ChainWallet
  const ChainWallet = await ethers.getContractAt(
    "ChainWallet",
    chainWalletAddress
  );

  // Deposit funds
  const depositAmount = ethers.utils.parseEther("10");
  await ChainWallet.deposit({ value: depositAmount });
  console.log(`Deposited ${depositAmount} to ChainWallet`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
