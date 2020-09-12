from pulp import *

# Создает список всех узлов снабжения
sclad = int(input("Введите кол-во складов: "))
print(sclad)
Warehouses = []
for i in range(sclad):
    name = input("Введите название скалада: ")
    Warehouses.append(name)
print(Warehouses)
# Warehouses = ["A", "B"]

# Создает словарь количества единиц снабжения для каждого узла снабжения
supply = {}
for i in range(sclad):
    value_sclad = input("Введеите кол-во единиц снабжения для склада " + Warehouses[i] + ": ")
    supply[Warehouses[i]] = int(value_sclad)
print(supply)
# supply = {"A": 1000,
#           "B": 4000}

# Создает список всех узлов спроса
bars_col = int(input("Введите кол-во баров: "))
Bars = []
for i in range(1, bars_col + 1):
    Bars.append(str(i))
print(Bars)
# Bars = ["1", "2", "3", "4", "5"]

# Создает словарь для количества единиц спроса для каждого узла спроса
demand = {}
for i in range(bars_col):
    spros = input("Введите необходимое кол-во поставки для бара " + Bars[i] + ":")
    demand[Bars[i]] = int(spros)
print(demand)
# demand = {"1": 500,
#           "2": 900,
#           "3": 1800,
#           "4": 200,
#           "5": 700, }

# Создает список затрат на каждый транспортный путь
costs = []
for i in range(sclad):
    print("Список затрат на доставку со склада: " + Warehouses[i])
    cost_sclad_transport = []
    for i in range(bars_col):
        c = int(input("Стоимость доставки: "))
        cost_sclad_transport.append(c)
    costs.append(cost_sclad_transport)
print(costs)

# costs = [  # Бары
#     # 1 2 3 4 5
#     [2, 4, 5, 2, 1],  # A   Складские помещения
#     [3, 1, 3, 2, 3]  # B
# ]

# Данные о стоимости превращаются в словарь
costs = makeDict([Warehouses, Bars], costs, 0)

# Создает переменную 'prob' для хранения данных о проблеме
prob = LpProblem("Проблема распределения пива", LpMinimize)

# Создает список кортежей, содержащий все возможные маршруты транспорта
Routes = [(w, b) for w in Warehouses for b in Bars]

# Создан словарь под названием Vars, содержащий ссылочные переменные (маршруты).
vars = LpVariable.dicts("Маршрут", (Warehouses, Bars), 0, None, LpInteger)

# Целевая функция сначала добавляется к 'prob'
prob += lpSum([vars[w][b] * costs[w][b] for (w, b) in Routes]), "Sum_of_Transporting_Costs"

# Максимальные ограничения предложения добавляются в вероятность для каждого узла снабжения (склада).
for w in Warehouses:
    prob += lpSum([vars[w][b] for b in Bars]) <= supply[w], "Sum_of_Products_out_of_Warehouse_%s" % w

# Ограничения минимума спроса добавляются в вероятность для каждого узла спроса (бара).
for b in Bars:
    prob += lpSum([vars[w][b] for w in Warehouses]) >= demand[b], "Sum_of_Products_into_Bar%s" % b

# Данные о проблеме записываются в файл .lp.
prob.writeLP("files/BeerDistributionProblem.lp")

# Проблема решается с помощью выбора Решателя PuLP.
prob.solve()

# Статус решения выводится на экран.
print("Статус:", LpStatus[prob.status])

# Каждая переменная печатается с ее оптимальным значением.
for v in prob.variables():
    print(v.name, "=", v.varValue)

# Оптимизированное значение целевой функции выводится на экран.
print("Общая стоимость перевозки = ", value(prob.objective))
