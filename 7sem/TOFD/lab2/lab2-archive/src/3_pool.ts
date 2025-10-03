import {
    Raydium,
    DEVNET_PROGRAM_ID,
    getCpmmPdaAmmConfigId,
    TxVersion,
} from "@raydium-io/raydium-sdk-v2";
import BN from 'bn.js'
import { clusterApiUrl, Connection, Keypair, PublicKey } from "@solana/web3.js";
import { secret } from "./secret.js";

const txVersion = TxVersion.V0

const mintAAddress = 'DGkr4kPRRnU6stzoeU7ZCpuB1tuA4Hbxgt9hAXQRuTBh'
const mintBAddress = 'So11111111111111111111111111111111111111112'


const connection = new Connection(clusterApiUrl('devnet'))

const owner = Keypair.fromSecretKey(secret);

const raydium = await Raydium.load(
    {
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
    }
)

const mintA = await raydium.token.getTokenInfo(mintAAddress)
const mintB = await raydium.token.getTokenInfo(mintBAddress)
const feeConfigs = await raydium.api.getCpmmConfigs()
feeConfigs.forEach((config) => {
    config.id = getCpmmPdaAmmConfigId(DEVNET_PROGRAM_ID.CREATE_CPMM_POOL_PROGRAM, config.index).publicKey.toBase58()
})


const { execute, extInfo, transaction } = await raydium.cpmm.createPool({
    programId: DEVNET_PROGRAM_ID.CREATE_CPMM_POOL_PROGRAM,
    poolFeeAccount: DEVNET_PROGRAM_ID.CREATE_CPMM_POOL_FEE_ACC,
    mintA,
    mintB,
    mintAAmount: new BN(10_000),
    mintBAmount: new BN(500_001),
    startTime: new BN(0),
    feeConfig: feeConfigs[0]!,
    associatedOnly: false,
    ownerInfo: {
        useSOLBalance: false,
    },
    txVersion,
})


const { tId } = await execute({ sendAndConfirm: true })

console.log('pool created: ', {
    tId,
    poolKeys: Object.keys(extInfo.address).reduce(
        (acc, cur) => ({
            ...acc,
            [cur]: extInfo.address[cur as keyof typeof extInfo.address].toString(),
        }),
        {}
    ),
})
