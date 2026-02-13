/**
 * Hildie JavaScript CLI
 */

import { greet } from "./lib.js";

function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error("Usage: hildie-cli <name>");
    process.exit(1);
  }

  const name = args[0];
  console.log(greet(name));
}

main();
