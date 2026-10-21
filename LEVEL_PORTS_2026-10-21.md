# LEVEL_PORTS

Date: 2026-10-21

Port the curriculum from [`yancouto/functional`](https://github.com/yancouto/functional/tree/master/src/levels) into this game. Preserve its section sequence, translate expressions and test cases into this game's syntax, and keep challenge IDs and prerequisites consistent with saved aliases.

## Porting notes

- The Rust game defines 57 levels in seven ordered sections.
- Existing challenges covered 11 Rust levels before this port: Identity, Two arguments (our `SWAP`), Squaring (`SQR`), all five Boolean levels, and Pair, FST, and SND (our `SCD`).
- `ANYTHING` has been added as a syntax-only introductory challenge; `INDIRECTION` and `SIMPLE_LIST` are also implemented.
- That leaves 43 Rust levels to port, in Pair and List through Trees.
- Add section/order metadata before or alongside the larger imports so the curriculum can be presented in Rust's section order. Keep the existing prerequisite-based unlock behavior and consider how older saved progress will behave.
- Some Rust exercises rely on expression syntax or constants not present here. Translate these into lambda syntax supported by our parser, and test behavior by applying functions to representative inputs rather than relying on exact variable names.
- Add hints where an exercise introduces a substantial new concept; test edge cases such as empty and singleton lists, zero numerals, and empty trees.

## Sequence

### 1. Basic

- [x] Anything — accept any well-formed expression without evaluating it (`ANYTHING`).
- [x] Identity — already covered by `ID`.
- [x] Two arguments — already covered by `SWAP`.
- [x] Squaring — already covered by `SQR`.
- [x] Indirection — apply a supplied two-argument function with its arguments reversed (`INDIRECTION`).

### 2. Boolean

- [x] If — `IF`.
- [x] Not — `NOT`.
- [x] And — `AND`.
- [x] Or — `OR`.
- [x] Xor — `XOR`.

### 3. Pair and List

- [x] Pair — `PAIR`.
- [x] First projection — `FST`.
- [x] Second projection — `SCD` (Rust calls this `snd`).
- [x] Simple list — traverse pair-encoded lists and return the third item (`SIMPLE_LIST`).
- [ ] Any.
- [ ] Push.
- [ ] Pop.
- [ ] Empty.

### 4. Recursion

- [ ] Creating recursion.
- [ ] Strip prefix.
- [ ] Acc.
- [ ] All.
- [ ] Map.
- [ ] None.
- [ ] Filter.
- [ ] Zip.
- [ ] Eqblist.
- [ ] Concat.
- [ ] Reverse.

### 5. Numerals

- [ ] Suc.
- [ ] Zero.
- [ ] Pre.
- [ ] Add.
- [ ] Sub.
- [ ] Mul.
- [ ] Div.
- [ ] Eq.
- [ ] Min.
- [ ] Max.

### 6. More Numerals

- [ ] Is odd.
- [ ] Increasing list.
- [ ] Decomposition.
- [ ] Primes.
- [ ] Sort.

### 7. Trees

- [ ] Node.
- [ ] Lef.
- [ ] Rig.
- [ ] Val.
- [ ] Bempty.
- [ ] Find.
- [ ] Bsize.
- [ ] Build.
- [ ] Preorder.
- [ ] Inorder.
- [ ] Split.
- [ ] Kth.
- [ ] Inverse6.

The Rust game treats Trees as optional content. Consider retaining that distinction when adding it here.
