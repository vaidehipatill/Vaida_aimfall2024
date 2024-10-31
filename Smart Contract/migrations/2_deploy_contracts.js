const ProductAuth = artifacts.require("ProductAuth");

module.exports = async function (deployer, network, accounts) {
  try {
    await deployer.deploy(ProductAuth, { from: accounts[0] });
    const instance = await ProductAuth.deployed();
    console.log("ProductAuth deployed at:", instance.address);
  } catch (error) {
    console.error("Deployment failed:", error);
    throw error;
  }
};
