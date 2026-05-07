# Palindrome Detector (Optimized) - Debrief

## Per-Module Explanation

### `palindrome.py`
Single module with one public function:

#### `is_palindrome(text: str) -> bool`
- **Input Validation:**
  - Type check: `isinstance(text, str)` → raises `TypeError` if not
  - ASCII check: iterate through chars, reject if `ord(char) > 127` → raises `ValueError`
  - Alphanumeric check: scan for at least one alphanumeric char (except empty string) → raises `ValueError` if none
  - Exception: empty string is allowed and returns `True`

- **Two-Pointer Comparison:**
  - Initialize: `left = 0`, `right = len(text) - 1`
  - While `left < right`:
    - Skip non-alphanumeric from left: `while text[left].isalnum()` is False, increment left
    - Skip non-alphanumeric from right: `while text[right].isalnum()` is False, decrement right
    - Compare (case-insensitive): `text[left].lower() != text[right].lower()` → return False
    - Move inward: `left += 1`, `right -= 1`
  - Return True (all compared chars matched)

- **Complexity Analysis:**
  - **Time:** O(n) — each character visited at most twice (validation + comparison)
  - **Space:** O(1) — only pointers and temp variables, no string allocations

- **Edge Cases Handled:**
  - Empty string → `True` (per requirements)
  - Single character → `True` (pointers start at 0, 0; left < right is False, so loop exits immediately)
  - Mixed case → normalized on-the-fly with `.lower()` during comparison
  - Spaces/punctuation → skipped by inner while loops
  - Numbers → treated as alphanumeric and compared
  - Non-ASCII → rejected with `ValueError`
  - Only spaces/punctuation → rejected with `ValueError`
  - Large inputs (1M chars) → O(1) space keeps peak memory under 500KB

## Patterns Used

### Fail-Fast Validation
All input validation happens before any computation. Invalid inputs raise exceptions immediately.

### Two-Pointer Technique
Compare from both ends moving inward, skipping non-alphanumeric characters without storing them. Classic space-efficient pattern.

### Type Hints
Full annotations on function signature for clarity and IDE support.

### On-the-Fly Filtering
Non-alphanumeric characters are skipped without creating a separate normalized string. Saves memory at the cost of slightly more complex pointer logic.

### Parametrized Testing with Memory Tracking
33 test cases using `@pytest.mark.parametrize` for DRY testing. `tracemalloc` module verifies peak memory stays within 500KB constraint even for 1M char inputs.

## Tradeoffs & Decisions

### Two-Pointer vs Normalization
**Chosen:** Two-pointer approach (O(1) space)

**Tradeoff:**
- **Pros:** Meets strict 500KB constraint; only ~100 bytes peak memory regardless of input size
- **Cons:** More complex logic (inner while loops to skip non-alphanumeric); harder to reason about at first glance

**Alternative (Normalization):**
- **Pros:** Simpler logic; easier to understand
- **Cons:** Would allocate ~1MB normalized string for 1M char input, violating 500KB constraint

**Decision Rationale:** Constraint is non-negotiable; complexity trade is worth it.

### Single Pass vs Separate Validation
**Chosen:** Separate validation pass before comparison

**Tradeoff:**
- **Pros:** Clear separation; validation errors surface early; simple to debug
- **Cons:** Two passes through string (O(n) is still O(n), but coefficient is doubled)

**Alternative:** Inline validation during comparison
- **Pros:** Single pass
- **Cons:** More complex; error handling mixed with logic

**Decision Rationale:** Clarity and debuggability matter more than reducing constant factors.

### Empty String Handling
**Chosen:** Empty string returns `True`

**Logic:** `if text and not has_alphanumeric` allows empty string through but rejects non-empty strings with no alphanumeric chars. This matches requirement: "empty string is a valid palindrome."

## What I'd Change With More Time

1. **Optimize validation** — Combine ASCII check with alphanumeric check in a single pass instead of two separate iterations.

2. **Early exit for short strings** — Strings under ~100 chars could use normalization approach (faster logic, negligible memory). Add a heuristic: `if len(text) < threshold: use_normalization_approach()`

3. **Streaming/chunked processing** — For extremely large files (> memory), could read in chunks, but this changes the interface (requires generator or callback pattern).

4. **Better error messages** — Include character position in non-ASCII error: `"non-ASCII character at position 5: 'é'"`

5. **Docstrings** — Add comprehensive docstrings with examples, complexity analysis, and constraint notes.

6. **Performance micro-benchmarks** — Add pytest benchmarks to track memory and speed across different input patterns (dense punctuation, sparse punctuation, all letters, etc.).

## Test Coverage

33 tests covering:
- **Validation:** 5 tests (type errors, ASCII validation, alphanumeric requirement)
- **Basic Palindromes:** 11 tests (simple cases, numbers, edge chars)
- **Case & Spaces:** 4 tests (mixed case, multiple spaces)
- **Punctuation:** 5 tests (various punctuation marks, assignment example)
- **Edge Cases:** 5 tests (empty string, single char, mixed everything)
- **Memory Constraint:** 3 tests (1M char palindrome, 1M char non-palindrome, complex large case) — all verify peak memory < 500KB

All tests pass. Code is linted clean. Time complexity is O(n). **Space complexity is O(1)**, well within 500KB constraint.
