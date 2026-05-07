# Palindrome Detector - Debrief

## Per-Module Explanation

### `palindrome.py`
Single module with one public function:

#### `is_palindrome(text: str) -> bool`
- **Input Validation:**
  - Type check: `isinstance(text, str)` → raises `TypeError` if not
  - ASCII check: iterate through chars, reject if `ord(char) > 127` → raises `ValueError`
  - Alphanumeric check: if input is non-empty but has no alphanumeric chars, raise `ValueError`
  - Exception: empty string is allowed and returns `True`

- **Normalization:**
  - Convert to lowercase: `.lower()`
  - Extract alphanumeric only: `char.isalnum()`
  - Preserve order for palindrome check

- **Comparison:**
  - Compare normalized string with its reverse: `normalized == normalized[::-1]`
  - O(n) time, O(n) space for normalized string

- **Edge Cases Handled:**
  - Empty string → `True` (per requirements)
  - Single character → `True` (automatically, since char == char reversed)
  - Mixed case → normalized to lowercase before compare
  - Spaces/punctuation → removed during normalization
  - Numbers → treated as alphanumeric and included
  - Non-ASCII → rejected with `ValueError`
  - Only spaces/punctuation → rejected with `ValueError`

## Patterns Used

### Fail-Fast Validation
All input checks happen before any computation. Invalid inputs raise exceptions immediately.

### Type Hints
Full annotations on function signature clarify intent and enable IDE support.

### Parametrized Testing
30 test cases organized by concern (validation, basic palindromes, case/spaces, punctuation, edge cases). Uses `@pytest.mark.parametrize` for DRY testing of multiple inputs.

### O(n) Time Complexity
Single pass for validation + single pass for normalization + single comparison = O(n), meeting the requirement.

## Tradeoffs & Decisions

### Why manual `isinstance` + char loop instead of regex?
- No external dependencies (stdlib-only)
- Clear intent: immediate ASCII rejection without side effects
- Validation failure surfaces early with specific error messages

### Why normalize then compare instead of two-pointer approach?
- Two-pointer would skip spaces/punctuation on-the-fly (clever but complex)
- Normalize-then-compare is clearer: separate validation from logic
- Memory trade-off (O(n) space) is acceptable given 4MB constraint and 1M char input size
- O(n) time still meets requirement

### Why reject non-ASCII instead of normalizing accents?
- Per requirements: non-ASCII should raise exception
- Simpler than Unicode decomposition (NFD/NFC)
- Avoids edge cases with different normalization forms

### Why special-case empty string?
- Per requirements: empty string is a valid palindrome (returns True)
- All other strings with no alphanumeric chars raise ValueError
- Logic: `if text and not normalized` allows "" to pass through

## What I'd Change With More Time

1. **Support Unicode with normalization flag** — Add optional parameter `allow_unicode=False`. When True, normalize accents using `unicodedata.normalize()` instead of rejecting non-ASCII.

2. **Support custom character filters** — Add optional `include_chars` parameter to customize what counts as "alphanumeric" (e.g., allow underscores, hyphens).

3. **Better error messages** — Include the index or context of the non-ASCII character in the error message for debugging.

4. **Optimization for very long strings** — Use two-pointer approach starting from both ends to bail out early on mismatch (saves memory for non-palindromes, though still O(n) time).

5. **Docstrings** — Add explicit docstrings documenting inputs, outputs, exceptions, and examples.

## Test Coverage

30 tests covering:
- **Validation:** 5 tests (type errors, ASCII validation, alphanumeric requirement)
- **Basic Palindromes:** 11 tests (simple cases, single/double chars, numbers)
- **Case & Spaces:** 4 tests (mixed case, multiple spaces)
- **Punctuation:** 5 tests (various punctuation marks, assignment example)
- **Edge Cases:** 5 tests (empty string, single char, mixed everything)

All tests pass. Code is linted clean (`ruff check`). Time complexity is O(n) as required.
