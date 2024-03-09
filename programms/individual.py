#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Использовать словарь, содержащий следующие ключи:
# название пункта назначения рейса; номер рейса; тип самолета.
# Написать программу, выполняющую следующие действия: ввод с клавиатуры
# данных в список, состоящий из словарей заданной структуры;
# записи должны быть размещены в алфавитном порядке по названиям
# пунктов назначения; вывод на экран пунктов назначения и номеров рейсов,
# обслуживаемых самолетом, тип которого введен с клавиатуры;
# если таких рейсов нет, выдать на дисплей соответствующее сообщение.

import json
import sys
import jsonschema


def add_flight():
    """
    Функция для добавления нового рейса в список.
    Запрашивает у пользователя название пункта назначения,
    номер рейса и тип самолета,
    создает новый рейс и добавляет его в общий список рейсов,
    сортируя по названию пункта назначения.
    """
    destination = input("Введите название пункта назначения: ")
    flight_number = int(input("Введите номер рейса: "))
    plane_type = input("Введите тип самолета: ")

    new_flight = {
        'destination': destination,
        'flight number': flight_number,
        'type of plane': plane_type
    }
    return new_flight


def list_flights(flights):
    """
    Функция для вывода списка рейсов на экран.
    Выводит табличное представление списка рейсов,
    включая номер, название пункта назначения,
    номер рейса и тип самолета.
    """
    if flights:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)

        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "No",
                "Пункт назначения",
                "Номер рейса",
                "Тип самолета"
            )
        )

        print(line)

        for idx, flight in enumerate(flights, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>20} |'.format(
                    idx,
                    flight.get('destination', ''),
                    flight.get('flight number', ''),
                    flight.get('type of plane', 0)
                )
            )
    else:
        print("Список рейсов пуст.")


def find_flights(flights):
    """
    Функция для поиска рейсов по типу самолета и вывода результатов на экран.
    Запрашивает у пользователя тип самолета,
    затем ищет все рейсы с этим типом и выводит их табличное представление.
    """
    find_type = input("Введите тип самолета для поиска: ")
    found = []

    for flight in flights:
        if flight['type of plane'] == find_type:
            found.append(flight)

    if not found:
        print(f"Рейсов на самолете типа '{find_type}' не найдено.")
    else:
        list_flights(found)


def save_flights(file_name, flights):
    """
    Сохранить всех работников в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(flights, fout, ensure_ascii=False, indent=4)


def load_flights(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "flight number": {"type": "integer"},
                "type of plane": {"type": "string"}
            },
            "required": ["destination", "flight number", "type of plane"]
        }
    }
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        loaded = json.load(fin)
    try:
        jsonschema.validate(loaded, schema)
        print(">>> Data is obtained!")
    except jsonschema.exceptions.ValidationError as e:
        print(">>> Error:")
        print(e.message)  # Ошибка валидацци будет выведена на экран
    return loaded


def main():
    """
    Главная функция программы.
    """
    flights = []
    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()
        # Выполнить действие в соответствие с командой.
        if command == "exit":
            break

        elif command == "add":
            # Запросить данные о рейсе.
            flight = add_flight()
            # Добавить словарь в список.
            flights.append(flight)
            # Отсортировать список в случае необходимости.
            if len(flights) > 1:
                flights.sort(key=lambda item: item.get('destination', ''))

        elif command == "list":
            list_flights(flights)

        elif command == "find":
            find_flights(flights)

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            save_flights(file_name, flights)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            flights = load_flights(file_name)

        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - добавить рейс;")
            print("list - вывести список рейсов;")
            print("find <тип> - запросить все рейсы обслуживаемые самолетом;")
            print("help - отобразить справку;")
            print("load - загрузить данные из файла;")
            print("save - сохранить данные в файл;")
            print("exit - завершить работу с программой.")
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
