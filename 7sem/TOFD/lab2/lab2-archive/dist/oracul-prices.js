import { HermesClient } from "@pythnetwork/hermes-client";
import { Raydium } from "@raydium-io/raydium-sdk-v2";
import { clusterApiUrl, Connection, Keypair } from "@solana/web3.js";
import { secret } from "./secret.js";
const hermesConnection = new HermesClient("https://hermes.pyth.network", {});
const solanaConnection = new Connection(clusterApiUrl('devnet'));
const owner = Keypair.fromSecretKey(secret);
const raydium = await Raydium.load({
    owner: owner,
    connection: solanaConnection,
    cluster: "devnet",
    disableFeatureCheck: true,
    blockhashCommitment: "finalized",
    urlConfigs: {
        BASE_HOST: 'https://api-v3-devnet.raydium.io',
        OWNER_BASE_HOST: 'https://owner-v1-devnet.raydium.io',
        SWAP_HOST: 'https://transaction-v1-devnet.raydium.io',
        CPMM_LOCK: 'https://dynamic-ipfs-devnet.raydium.io/lock/cpmm/position',
    }
});
const poolId = 'CGjPGN5gSPp3mFH3quECiuHEDbn4PEZH1JVQPfoPkDXP';
// pubkeys для Pyth
const priceIds = {
    SOL: "ef0d8b6fda2ceba41da15d4095d1da392a0d2f8ed0c6c7bc0f4cfac8c280b56d",
    BTC: "e62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43",
    ETH: "ff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace",
    USDC: "eaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a",
};
async function getPricesFromPyth() {
    const result = await hermesConnection.getLatestPriceUpdates(Object.values(priceIds));
    const prices = {};
    for (let [symbol, id] of Object.entries(priceIds)) {
        const feed = result.parsed?.find(f => f.id === id);
        if (feed?.price?.price) {
            prices[symbol] = feed.price.price * (10 ** feed.price.expo); // нормализация
        }
    }
    return prices;
}
const pythPrices = await getPricesFromPyth();
console.log(pythPrices);
const kpopPoolInfo = await raydium.cpmm.getRpcPoolInfo(poolId);
const raydiumMainnet = await Raydium.load({
    owner: owner,
    connection: solanaConnection,
    cluster: "mainnet",
    disableFeatureCheck: true,
    blockhashCommitment: "finalized",
});
const usdcPoolInfo = await raydiumMainnet.api.fetchPoolById({ ids: "58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2" });
const kpopPrice = usdcPoolInfo[0]?.price / kpopPoolInfo.poolPrice;
console.log(`${kpopPrice * pythPrices["USDC"]} K-POP/USD`);
//# sourceMappingURL=oracul-prices.js.map