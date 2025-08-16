from typing import Iterable

def process_data(data: Iterable[str | None]) -> list[str]:
    """
    Retorna lista ordenada de strings únicas normalizadas.

    Processo:
    - Ignora valores None.
    - strip() para remover espaços das extremidades.
    - casefold() para normalização case-insensitive robusta (Unicode).
    - Ignora resultados vazios.
    - Mantém a ordem da primeira ocorrência e garante unicidade em O(n).

    :param data: Iterável de strings ou None.
    :return: Lista de strings únicas normalizadas.
    """
    seen: set[str] = set()
    result: list[str] = []
    for item in data:
        if item is None:
            continue
        processed = item.strip()
        if not processed:
            continue
        processed = processed.casefold()
        if processed in seen:
            continue
        seen.add(processed)
        result.append(processed)
    return result
