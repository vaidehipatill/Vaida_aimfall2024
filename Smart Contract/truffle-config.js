module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545,
      network_id: "*", // Match any network id
    },
  },

  // Add the compilers section to specify the correct version of Solidity
  compilers: {
    solc: {
      version: "^0.8.0", // Fetch exact version from solc-bin
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
};
