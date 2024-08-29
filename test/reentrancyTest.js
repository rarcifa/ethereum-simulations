const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Reentrancy Attack", function () {
  let Reentrancy, reentrancy, Attacker, attacker;
  let ReentrancyGuarded, reentrancyGuarded, guardedAttacker;
  let owner, addr1, addr2;

  beforeEach(async function () {
    Reentrancy = await ethers.getContractFactory("Reentrancy");
    Attacker = await ethers.getContractFactory("Attacker");
    ReentrancyGuarded = await ethers.getContractFactory("ReentrancyGuarded");

    [owner, addr1, addr2, _] = await ethers.getSigners();

    reentrancy = await Reentrancy.deploy();
    await reentrancy.deployed();

    attacker = await Attacker.deploy(reentrancy.address);
    await attacker.deployed();

    reentrancyGuarded = await ReentrancyGuarded.deploy();
    await reentrancyGuarded.deployed();

    guardedAttacker = await Attacker.deploy(reentrancyGuarded.address);
    await guardedAttacker.deployed();

    await reentrancy.deposit({ value: ethers.utils.parseEther("10") });
    await reentrancyGuarded.deposit({ value: ethers.utils.parseEther("10") });
  });

  it("Should perform reentrancy attack", async function () {
    const attackerInitialBalance = await ethers.provider.getBalance(attacker.address);
    await attacker.attack({ value: ethers.utils.parseEther("1") });

    const attackerFinalBalance = await ethers.provider.getBalance(attacker.address);
    expect(attackerFinalBalance).to.be.above(attackerInitialBalance);
  });

  it("Should prevent reentrancy attack with reentrancy guard", async function () {
    try {
      await guardedAttacker.attack({ value: ethers.utils.parseEther("1") });
    } catch (error) {
      expect(error.message).to.include("Reentrant call");
    }

    const guardedAttackerBalance = await ethers.provider.getBalance(guardedAttacker.address);
    expect(guardedAttackerBalance).to.equal(ethers.utils.parseEther("1"));
  });
});
