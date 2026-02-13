import { test } from "node:test";
import assert from "node:assert";
import { greet, add } from "./lib.js";

test("greet", () => {
  const result = greet("World");
  const expected = "Hello from Hildie JavaScript Library, World!";
  assert.strictEqual(result, expected, `Expected "${expected}" but got "${result}"`);
});

test("add", () => {
  const result = add(2, 3);
  const expected = 5;
  assert.strictEqual(result, expected, `Expected ${expected} but got ${result}`);
});
