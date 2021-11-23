import sys

file = sys.argv[1:][0]


# def amount_of_moves(numbers):
# медленный алгоритм - перебираем все возможные варианты шагов. Сравниваем др с другом. Выбираем минимальный.
#     min_value = float("inf")
#     for i in range(len(numbers)):
#         tmp, min = numbers[i], 0
#         for num in numbers:
#             min += abs(tmp - num)
#         if min < min_value:
#             min_value = min
#     return min_value


def avg_number(numbers):
    if numbers:
        # вычисляем среднее арифметическое, от полученных цифр
        avg = sum(numbers)/len(numbers)
        # в полученном списке чисел ищем число, наиболее близкое, по значению, к среднему арифметическому
        min_number, min_avg = numbers[0], abs(avg - numbers[0])
        for i in numbers[1:]:
            if min_avg > abs(avg - i):
                min_number, min_avg = i, abs(avg - i)
        return min_number


def amount_of_moves(numbers, min_number):
    # для найденного числа определяем количество шагов, требуемых для приведения всех элементов к одному числу
    min_steps = 0
    for num in numbers:
        min_steps += abs(min_number - num)
    return min_steps


if __name__ == "__main__":
    with open(file, "r") as f:
        numbers = list(map(int, f.read().splitlines()))
    print(amount_of_moves(numbers, avg_number(numbers)), sep="\n")
