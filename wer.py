import re


def tokenize(text: str) -> list[str]:
    """Приводить текст до нижнього регістру, прибирає пунктуацію та ділить на слова."""
    text = text.lower()
    words = re.findall(r"[a-zа-яіїєґ0-9']+", text)
    return words


def calculate_wer(reference_text: str, hypothesis_text: str) -> dict:
    """
    Обчислює WER та повертає словник з метриками: WER, S, D, I, N.
    """
    ref = tokenize(reference_text)
    hyp = tokenize(hypothesis_text)

    n = len(ref)
    m = len(hyp)

    if n == 0:
        raise ValueError("Еталонний текст (reference) не може бути порожнім.")

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if ref[i - 1] == hyp[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                substitution = dp[i - 1][j - 1] + 1
                insertion = dp[i][j - 1] + 1
                deletion = dp[i - 1][j] + 1
                dp[i][j] = min(substitution, insertion, deletion)

    i, j = n, m
    substitutions = 0
    deletions = 0
    insertions = 0

    while i > 0 or j > 0:
        if i > 0 and j > 0 and ref[i - 1] == hyp[j - 1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            substitutions += 1
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            deletions += 1
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            insertions += 1
            j -= 1

    wer_value = (substitutions + deletions + insertions) / n

    return {
        "WER": round(wer_value, 4),
        "S": substitutions,
        "D": deletions,
        "I": insertions,
        "N": n,
    }