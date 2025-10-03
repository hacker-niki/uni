import { Raydium, TxVersion, CurveCalculator, FeeOn, } from "@raydium-io/raydium-sdk-v2";
import BN from 'bn.js';
import { clusterApiUrl, Connection, Keypair, PublicKey } from "@solana/web3.js";
import { NATIVE_MINT } from "@solana/spl-token";
import { secret } from "./secret.js";
const txVersion = TxVersion.V0;
const poolId = '5Tr7e68KCc2gkTViJpNBMbu4vH41z8Kgtfb6c1SjL2ER';
const inputAmount = new BN(9000);
const inputMint = "qKhxiRpZ2VcHPEzqGjn3XDYKqfviX9HX4t6ugZWbKQX";
const connection = new Connection(clusterApiUrl('devnet'));
const owner = Keypair.fromSecretKey(secret);
const raydium = await Raydium.load({
    owner: owner,
    connection: connection,
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
let poolInfo;
let poolKeys;
let rpcData;
const data = await raydium.cpmm.getPoolInfoFromRpc(poolId);
poolInfo = data.poolInfo;
poolKeys = data.poolKeys;
rpcData = data.rpcData;
const baseIn = inputMint === poolInfo.mintA.address;
const swapResult = CurveCalculator.swapBaseInput(inputAmount, baseIn ? rpcData.baseReserve : rpcData.quoteReserve, baseIn ? rpcData.quoteReserve : rpcData.baseReserve, rpcData.configInfo.tradeFeeRate, rpcData.configInfo.creatorFeeRate, rpcData.configInfo.protocolFeeRate, rpcData.configInfo.fundFeeRate, rpcData.feeOn === FeeOn.BothToken || rpcData.feeOn === FeeOn.OnlyTokenB);
console.log('swap result', Object.keys(swapResult).reduce((acc, cur) => ({
    ...acc,
    [cur]: swapResult[cur].toString(),
}), {}));
const { execute, transaction } = await raydium.cpmm.swap({
    poolInfo,
    poolKeys,
    inputAmount,
    swapResult,
    slippage: 0.001,
    baseIn,
    txVersion: TxVersion.V0,
});
const { txId } = await execute({ sendAndConfirm: true });
console.log(`swapped: ${poolInfo.mintA.symbol} to ${poolInfo.mintB.symbol}:`, {
    txId: `https://explorer.solana.com/tx/${txId}`,
});
//# sourceMappingURL=4_swap.js.map