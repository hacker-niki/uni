import "dotenv/config";
import { Connection, clusterApiUrl, PublicKey, Transaction, Keypair, } from "@solana/web3.js";
import { createCreateMetadataAccountV3Instruction } from "@metaplex-foundation/mpl-token-metadata";
import { secret } from "./secret.js";
const clusterName = "devnet";
const tokenAddress = "AdJ2eqBkEg7zecU7Y8iQsf6nWtHnza4FuzZQNuZiEZCV";
const metadataData = {
    name: "keypop",
    symbol: "K-POP",
    uri: "https://raw.githubusercontent.com/LoDesFire/python-lab-works/refs/heads/main/kpop.json",
    sellerFeeBasisPoints: 0,
    creators: null,
    collection: null,
    uses: null,
};
const owner = Keypair.fromSecretKey(secret);
console.log(`Public key is: ${owner.publicKey.toBase58()}`);
const connection = new Connection(clusterApiUrl(clusterName));
const TOKEN_METADATA_PROGRAM_ID = new PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s");
const tokenMintAccount = new PublicKey(tokenAddress);
const metadataPDAAndBump = PublicKey.findProgramAddressSync([
    Buffer.from("metadata"),
    TOKEN_METADATA_PROGRAM_ID.toBuffer(),
    tokenMintAccount.toBuffer(),
], TOKEN_METADATA_PROGRAM_ID);
const metadataPDA = metadataPDAAndBump[0];
const tx = new Transaction().add(createCreateMetadataAccountV3Instruction({
    metadata: metadataPDA,
    mint: tokenMintAccount,
    mintAuthority: owner.publicKey,
    payer: owner.publicKey,
    updateAuthority: owner.publicKey,
}, {
    createMetadataAccountArgsV3: {
        collectionDetails: null,
        data: metadataData,
        isMutable: true,
    },
}));
const recentBlockhash = await connection.getLatestBlockhash();
tx.feePayer = owner.publicKey;
tx.recentBlockhash = recentBlockhash.blockhash;
tx.sign(owner);
const txSignature = await connection.sendRawTransaction(tx.serialize());
console.log(`Transaction confirmed, ID is: ${txSignature}!`);
//# sourceMappingURL=create-token-metadata.js.map