import hre from "hardhat";

// scripts/deploy.js
async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying contract with the account:", deployer.address);
  console.log("Account balance:", (await deployer.getBalance()).toString());

  const DAO = await hre.ethers.getContractFactory("DAO");
  const dao = await DAO.deploy();

  console.log("DAO contract deployed to:", dao.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
