import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { Counter } from "../target/types/counter";

describe("counter", () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const program = anchor.workspace.Counter as Program<Counter>;
  const counterAccount = anchor.web3.Keypair.generate();

  it("Is initialized!", async () => {
    await program.methods
      .initialize()
      .accounts({
        counter: counterAccount.publicKey,
        user: provider.wallet.publicKey,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .signers([counterAccount])
      .rpc();

    const account = await program.account.counter.fetch(
      counterAccount.publicKey
    );

    console.log("Счетчик инициализирован.");
  });

  it("Increment 3 times", async () => {
    for (let i = 0; i < 3; i++) {
      await program.methods
        .increment()
        .accounts({ counter: counterAccount.publicKey })
        .rpc();
      const account = await program.account.counter.fetch(
        counterAccount.publicKey
      );
      console.log(
        `Инкремент ${i + 1}: новое значение ${account.count.toNumber()}`
      );
    }

    const account = await program.account.counter.fetch(
      counterAccount.publicKey
    );

  });

  it("Decrement 1 time", async () => {
    await program.methods
      .decrement()
      .accounts({ counter: counterAccount.publicKey })
      .rpc();

    const account = await program.account.counter.fetch(
      counterAccount.publicKey
    );

    console.log(`Декремент: новое значение ${account.count.toNumber()}`);
  });

  it("Fetch final count", async () => {
    const account = await program.account.counter.fetch(
      counterAccount.publicKey
    );
    console.log(
      `Текущее значение счетчика в консоли: ${account.count.toNumber()}`
    );

  });
});
