import hre from "hardhat";

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);

  // Deploy ResourcePool contract
  const ResourcePool = await hre.ethers.getContractFactory("ResourcePool");
  const resourcePool = await ResourcePool.deploy();
  await resourcePool.deployed();
  console.log("ResourcePool deployed to:", resourcePool.address);

  // Deploy Farmer contract with ResourcePool address
  const Farmer = await hre.ethers.getContractFactory("Farmer");
  const farmer = await Farmer.deploy(resourcePool.address);
  await farmer.deployed();
  console.log("Farmer deployed to:", farmer.address);

  // Deploy Builder contract with ResourcePool address
  const Builder = await hre.ethers.getContractFactory("Builder");
  const builder = await Builder.deploy(resourcePool.address);
  await builder.deployed();
  console.log("Builder deployed to:", builder.address);

  // Deploy Trader contract with ResourcePool address
  const Trader = await hre.ethers.getContractFactory("Trader");
  const trader = await Trader.deploy(resourcePool.address);
  await trader.deployed();
  console.log("Trader deployed to:", trader.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
