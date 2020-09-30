from tkinter import *
from pulp import *

root = Tk()
root.title('Решение транспортной задачи')

sclad_enter = {}
sclad_name = {}
sc_supply_en = {}
sc_supply_lb = {}
bar_supply_en = {}
bar_supply_lb = {}
bar_cost_en = []
bar_cost_lb = []

l1 = Label(root, text="Колчиество поставщиков")
l1.grid(sticky=S)
e1 = Entry(root)
e1.grid(sticky=E)
l2 = Label(root, text="Колчиество получателей")
l2.grid(sticky=S)
e2 = Entry(root)
e2.grid(sticky=E)


def find_solution(Warehouses, supply, Bars, costs, demand):
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
    # prob.writeLP("files/BeerDistributionProblem.lp")

    # Проблема решается с помощью выбора Решателя PuLP.
    prob.solve()

    # Статус решения выводится на экран.
    print("Статус:", LpStatus[prob.status])
    Label(root, text="Статус: " + LpStatus[prob.status]).grid(row=0, column=4)
    Label(root, text="Общая стоимость перевозки = " + str(value(prob.objective))).grid(row=1, column=4)
    # Label(root, text=LpStatus[prob.status]).grid(sticky=S)

    # Каждая переменная печатается с ее оптимальным значением.
    # i = 2
    ValName = []
    for v in prob.variables():
        value_post = v.name + "= " + str(v.varValue)
        ValName.append(Label(root, text=value_post))

        print(v.name, "=", v.varValue)

    for v in range(len(ValName)):
        ValName[v].grid(row=v + 2, column=4)

    # Оптимизированное значение целевой функции выводится на экран.
    print("Общая стоимость перевозки = ", value(prob.objective))


def sclad_data(sclad, bars_col):
    # Склады
    Warehouses = []
    supply = {}
    for j in range(sclad):
        Warehouses.append(sclad_enter[j].get())
    for j in range(sclad):
        supply[Warehouses[j]] = int(sc_supply_en[j].get())
    print(Warehouses)
    print(supply)

    # Бары
    Bars = []
    demand = {}
    for i in range(1, bars_col + 1):
        Bars.append(str(i))
    print(Bars)
    for i in range(bars_col):
        demand[Bars[i]] = int(bar_supply_en[j].get())
    print(demand)

    # Стоимость
    costs = []
    for j in range(sclad):
        cost_sclad_transport = []
        for i in range(bars_col):
            cost_sclad_transport.append(int(bar_cost_en[j][i].get()))
        costs.append(cost_sclad_transport)
    print(costs)

    find_solution(Warehouses, supply, Bars, costs, demand)


def apply_data():
    sclad = int(e1.get())
    bars_col = int(e2.get())

    i = 0
    Label(root, text="Наименование складов").grid(sticky=S)
    for j in range(sclad):
        e = Entry(root)
        e.grid(sticky=E)
        sclad_enter[j] = e
        name_sclad = "Склад " + str(j + 1)
        lb = Label(root, text=name_sclad)
        lb.grid(row=i + 6, column=1)
        sclad_name[j] = lb
        i += 1
    Label(root, text="Введеите кол-во единиц снабжения для складов").grid(sticky=S)
    for j in range(sclad):
        e = Entry(root)
        e.grid(sticky=E)
        sc_supply_en[j] = e
        name_sclad = "Склад " + str(j + 1)
        lb = Label(root, text=name_sclad)
        lb.grid(row=i + 7, column=1)
        sc_supply_lb[j] = lb
        i += 1
    Label(root, text="Введите необходимое кол-во поставки для поставщиков").grid(sticky=S)
    for j in range(bars_col):
        e = Entry(root)
        e.grid(sticky=E)
        bar_supply_en[j] = e
        name_sclad = "Бар " + str(j + 1)
        lb = Label(root, text=name_sclad)
        lb.grid(row=i + 8, column=1)
        bar_supply_lb[j] = lb
        i += 1
    Label(root, text="Введите стоимость доставки").grid(sticky=S)
    for j in range(sclad):
        name_punct = "Введите стоимость доставки от Склада " + str(j + 1)
        Label(root, text=name_punct).grid(sticky=S)
        way_storage_en = []
        way_storage_lb = []
        for b in range(bars_col):
            e = Entry(root)
            e.grid(sticky=E)
            way_storage_en.append(e)
            name_way = "Дорога " + str(b + 1)
            lb = Label(root, text=name_way)
            lb.grid(row=i + 10 + j, column=1)
            way_storage_lb.append(lb)
            i += 1
        bar_cost_en.append(way_storage_en)
        bar_cost_lb.append(way_storage_lb)
    Button(root, text="Принять данные", command=lambda: sclad_data(sclad, bars_col)).grid(sticky=S)


b = Button(root, text="Принять", command=apply_data)
b.grid(sticky=S)



mainloop()
