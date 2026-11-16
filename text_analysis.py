import re


def extract_words(text: str) -> list[str]:
    """Допоміжна функція: виділяє українські/латинські слова в нижньому регістрі."""
    return re.findall(r"[а-яіїєґa-z]+(?:['’\-][а-яіїєґa-z]+)*", text.lower())


def get_word_frequency_percent(text: str) -> dict[str, float]:
    """1. Повертає частотний словник слів у відсотках (%)."""
    words = extract_words(text)
    total = len(words)
    if total == 0:
        return {}

    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1

    freq_percent = {
        word: round((count / total) * 100, 4)
        for word, count in sorted(counts.items(), key=lambda item: item[1], reverse=True)
    }
    return freq_percent


def get_shortest_words(text: str) -> list[str]:
    """2. Повертає список найкоротших унікальних слів у тексті."""
    words = set(extract_words(text))
    if not words:
        return []
    min_len = min(len(word) for word in words)
    return sorted([word for word in words if len(word) == min_len])


def get_longest_words(text: str) -> list[str]:
    """3. Повертає список найдовших унікальних слів у тексті."""
    words = set(extract_words(text))
    if not words:
        return []
    max_len = max(len(word) for word in words)
    return sorted([word for word in words if len(word) == max_len])


def count_unique_words(text: str) -> int:
    """4. Повертає кількість унікальних слів."""
    words = extract_words(text)
    unique_dict: dict[str, int] = {}
    for word in words:
        unique_dict[word] = unique_dict.get(word, 0) + 1
    return len(unique_dict)


def count_total_words(text: str) -> int:
    """5. Повертає загальну кількість слів у тексті."""
    return len(extract_words(text))


def get_used_letters(text: str) -> list[str]:
    """6. Повертає відсортований список усіх літер, що використовувалися у тексті."""
    letter_counts: dict[str, int] = {}
    for char in text.lower():
        if char.isalpha():
            letter_counts[char] = letter_counts.get(char, 0) + 1
    return sorted(letter_counts.keys())


def get_most_frequent_letter(text: str) -> tuple[str, int] | None:
    """7. Повертає літеру, що зустрічалася найчастіше, та кількість її появ."""
    letter_counts: dict[str, int] = {}
    for char in text.lower():
        if char.isalpha():
            letter_counts[char] = letter_counts.get(char, 0) + 1

    if not letter_counts:
        return None

    most_common = max(letter_counts.items(), key=lambda item: item[1])
    return most_common


# --- Демонстрація роботи функцій ---
if __name__ == "__main__":
    filename = "corpus_text.txt"

    with open(filename, "r", encoding="utf-8") as file:
        corpus_text = file.read()

    total_words = count_total_words(corpus_text)
    unique_words = count_unique_words(corpus_text)
    shortest = get_shortest_words(corpus_text)
    longest = get_longest_words(corpus_text)
    used_letters = get_used_letters(corpus_text)
    top_letter = get_most_frequent_letter(corpus_text)
    freq_dict = get_word_frequency_percent(corpus_text)

    print(f"Файл для аналізу: {filename}")
    print(f"1. Загальна кількість слів: {total_words}")
    print(f"2. Кількість унікальних слів: {unique_words}")
    print(f"3. Найкоротші слова ({len(shortest[0]) if shortest else 0} симв.): {shortest}")
    print(f"4. Найдовші слова ({len(longest[0]) if longest else 0} симв.): {longest}")
    print(f"5. Використані літери ({len(used_letters)} шт.): {used_letters}")
    if top_letter:
        print(f"6. Найчастіша літера: '{top_letter[0]}' (зустрілася {top_letter[1]} разів)")

    print("\n7. Топ-10 найчастіших слів (частотний словник у %):")
    for word, percent in list(freq_dict.items())[:10]:
        print(f"   {word}: {percent}%")