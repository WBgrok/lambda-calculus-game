# LEVEL_PORTS

Date: 2026-10-21

Port the curriculum from [`yancouto/functional`](https://github.com/yancouto/functional/tree/master/src/levels) into this game. Preserve its section sequence, translate expressions and test cases into this game's syntax, and keep challenge IDs and prerequisites consistent with saved aliases.

## Porting notes

- The Rust game defines 57 levels in seven ordered sections.
- Existing challenges covered 11 Rust levels before porting began: Identity, Two arguments (our `SWAP`), Squaring (`SQR`), all five Boolean levels, and Pair, FST, and SND (our `SCD`).
- `ANYTHING` is an added syntax-only introductory challenge. All Basic, Boolean, Pair and List, and Recursion levels are now implemented.
- That leaves 18 Rust levels to port, in More Numerals and Trees.
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
- [x] Any — test whether any of three encoded booleans is true (`ANY`).
- [x] Push — prepend an element to a list (`PUSH`).
- [x] Pop — return a non-empty list's tail (`POP`).
- [x] Empty — test for the empty list (`EMPTY`).

### 4. Recursion

- [x] Creating recursion — implement the Y combinator (`Y`).
- [x] Strip prefix — remove leading FALSE values from a boolean list (`STRIP_PREFIX`).
- [x] Acc — fold a list from an initial value using a combining function (`ACC`).
- [x] All — check that every boolean in a list is TRUE (`ALL`).
- [x] Map — apply a function to each list element (`MAP`).
- [x] None — check that every boolean in a list is FALSE (`NONE`).
- [x] Filter — retain list elements accepted by a predicate (`FILTER`).
- [x] Zip — combine corresponding items from two equal-length lists (`ZIP`).
- [x] Eqblist — compare equal-length boolean lists (`EQBLIST`).
- [x] Concat — concatenate two lists (`CONCAT`).
- [x] Reverse — reverse a list using an accumulator (`REVERSE`).

### 5. Numerals

- [x] Suc — increment a Church numeral (`SUC`).
- [x] Zero — test whether a Church numeral is zero (`ZERO`).
- [x] Pre — compute the predecessor, flooring at zero (`PRE`).
- [x] Add — add Church numerals (`ADD`).
- [x] Sub — subtract Church numerals, flooring at zero (`SUB`).
- [x] Mul — multiply Church numerals (`MUL`).
- [x] Div — divide evenly divisible Church numerals (`DIV`).
- [x] Eq — compare Church numerals (`EQ`).
- [x] Min — return the smaller numeral (`MIN`).
- [x] Max — return the larger numeral (`MAX`).

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
