import statistics

def get_average(values: list[float]) -> float | None:
    """Повертає середнє значення списку."""
    return round(statistics.mean(values), 2) if values else None

def get_min(values: list[float]) -> float | None:
    """Повертає мінімальне значення."""
    return min(values) if values else None

def get_max(values: list[float]) -> float | None:
    """Повертає максимальне значення."""
    return max(values) if values else None

def get_median(values: list[float]) -> float | None:
    """Повертає медіану."""
    return round(statistics.median(values), 2) if values else None

def detect_jumps(values: list[float], timestamps: list[str], threshold: float) -> list[str]:
    """Повертає часові мітки різких перепадів."""
    jumps = []

    for i in range(1, len(values)):
        difference = abs(values[i] - values[i - 1])

        if difference > threshold:
            jumps.append(timestamps[i])

    return jumps

def print_table(parameter_name: str,data_dict: dict[str, float]) -> None:
    """Виводить таблицю початкових показників."""

    print(f"\nПоказники для параметра: {parameter_name}")
    print("+----------------------+-------------+")
    print(f"| {'Timestamp':<20} | {parameter_name:<11} |")
    print("+----------------------+-------------+")

    for timestamp, value in data_dict.items():
        print(f"| {timestamp:<20} | {value:<11} |")

    print("+----------------------+-------------+")

def print_results(parameter_name: str, results: dict) -> None:
    """Виводить результати розрахунків для показника."""

    print(f"\nРезультати для {parameter_name}:")
    print("-" * 35)

    for stat_name, value in results.items():
        print(f"{stat_name:<12}: {value}")

    print("-" * 35)

