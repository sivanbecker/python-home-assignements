def is_palindrome(text: str) -> bool:
    if not isinstance(text, str):
        raise TypeError(f"input must be a string, got {type(text).__name__}")

    for char in text:
        if ord(char) > 127:
            raise ValueError(f"non-ASCII character not allowed: {char}")

    has_alphanumeric = any(char.isalnum() for char in text)
    if text and not has_alphanumeric:
        raise ValueError("string must contain at least one alphanumeric character")

    left = 0
    right = len(text) - 1

    while left < right:
        while left < right and not text[left].isalnum():
            left += 1
        while left < right and not text[right].isalnum():
            right -= 1

        if text[left].lower() != text[right].lower():
            return False

        left += 1
        right -= 1

    return True
