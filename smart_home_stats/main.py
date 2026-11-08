import csv
import json
import configparser
import stats_utils as su

# Пороги для визначення різких перепадів
THRESHOLDS = {
    "temperature": 7,
    "humidity": 20,
    "pressure": 5000
}

def read_csv(filename):
    """Зчитує CSV-файл і повертає словник показників."""

    data = {
        "temperature": {},
        "humidity": {},
        "pressure": {}
    }

    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            timestamp = row["timestamp"]

            data["temperature"][timestamp] = float(row["temperature"])
            data["humidity"][timestamp] = float(row["humidity"])
            data["pressure"][timestamp] = float(row["pressure"])

    return data

def read_config(filename):
    """Зчитує налаштування з INI-файлу."""

    config = configparser.ConfigParser()
    
    loaded_files = config.read(filename, encoding="utf-8")

    if not loaded_files:
        raise FileNotFoundError(filename)


    settings = {}

    for parameter in config.sections():
        stats = config.get(parameter, "stats")
        settings[parameter] = [
            item.strip() for item in stats.split(",")
        ]

    return settings

def main():
    """Головна функція програми."""
  
    try:
        filename = input("Введіть назву CSV-файлу [data.csv]: ").strip()

        data = read_csv(filename or "data.csv")
        settings = read_config("config.ini")

    except FileNotFoundError as error:
        print(f"Помилка: файл не знайдено — {error.filename}")
        return

    except (ValueError, KeyError, configparser.Error) as error:
        print(f"Помилка у вхідних даних або налаштуваннях: {error}")
        return


    # 3. Словник для результатів
    results = {}

    # 4. Обробка показників
    for parameter, stats in settings.items():

        parameter_data = data[parameter]

        su.print_table(parameter, parameter_data)

        values = list(parameter_data.values())
        timestamps = list(parameter_data.keys())

        parameter_results = {}

        if "average" in stats:
            parameter_results["average"] = su.get_average(values)

        if "min" in stats:
            parameter_results["min"] = su.get_min(values)

        if "max" in stats:
            parameter_results["max"] = su.get_max(values)

        if "median" in stats:
            parameter_results["median"] = su.get_median(values)

        if "jumps" in stats:
            threshold = THRESHOLDS[parameter]
            parameter_results["jumps"] = su.detect_jumps(
                values, timestamps, threshold
            )

        results[parameter] = parameter_results
        su.print_results(parameter, parameter_results)

    # 5. Виведення результатів
    print("\nРезультати обчислень:")
    print(json.dumps(results, ensure_ascii=False, indent=4))

    # 6. Збереження результатів у JSON
    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    print("\nРезультати збережено у файлі results.json")    
if __name__ == "__main__":
    main()

