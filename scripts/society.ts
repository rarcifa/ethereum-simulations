import hre from "hardhat";

// scripts/deploy.js
async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying contract with the account:", deployer.address);
  console.log("Account balance:", (await deployer.getBalance()).toString());

  const Society = await hre.ethers.getContractFactory("Society");
  const society = await Society.deploy();

  console.log("Society contract deployed to:", society.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
