import pulp

# parameters
products = ['wrenches', 'pliers']
price = [130, 100]
steel = [1.5, 1]
molding = [1, 1]
assembly = [0.3, 0.5]
capsteel = 27
capmolding = 21
LB = [0, 0]
capacity_ub = [15, 16]
steelprice = 58
scenarios = [0, 1, 2, 3]
pscenario = [0.25, 0.25, 0.25, 0.25]
wrenchearnings = [160, 160, 90, 90]
plierearnings = [100, 100, 100, 100]
capassembly = [8, 10, 8, 10]

production = [(j, i) for j in scenarios for i in products]
pricescenario = [[wrenchearnings[j], plierearnings[j]] for j in scenarios]
priceitems = [item for sublist in pricescenario for item in sublist]

# создавать словари для параметров
price_dict = dict(zip(production, priceitems))
capacity_dict = dict(zip(products, capacity_ub * 4))
steel_dict = dict(zip(products, steel))
molding_dict = dict(zip(products, molding))
assembly_dict = dict(zip(products, assembly))

# Создание переменные и параметры в виде словарей
production_vars = pulp.LpVariable.dicts("production", (scenarios, products), \
                                        lowBound=0, cat='Continuous')
steelpurchase = pulp.LpVariable("steelpurchase", lowBound=0, cat='Continuous')

# Создание файла
gemstoneprob = pulp.LpProblem("The Gemstone Tool Problem", pulp.LpMaximize)

# Целевая функция сначала добавляется в gemstoneprob.
gemstoneprob += pulp.lpSum([pscenario[j] * (price_dict[(j, i)] * \
                                            production_vars[j][i]) \
                            for (j, i) in production] - \
                           steelpurchase * steelprice), "Total cost"

for j in scenarios:
    gemstoneprob += pulp.lpSum([steel_dict[i] * production_vars[j][i] \
                                for i in products]) - \
                    steelpurchase <= 0, ("Steel capacity" + str(j))
    gemstoneprob += pulp.lpSum([molding_dict[i] * production_vars[j][i] \
                                for i in products]) <= capmolding, \
                    ("molding capacity" + str(j))
    gemstoneprob += pulp.lpSum([assembly_dict[i] * production_vars[j][i] \
                                for i in products]) <= capassembly[j], \
                    ("assembly capacity" + str(j))
    for i in products:
        gemstoneprob += production_vars[j][i] <= capacity_dict[i], \
                        ("capacity " + str(i) + str(j))

# Печать проблемі
print(gemstoneprob)

# Данные о проблеме записываются в файл .lp.
gemstoneprob.writeLP("files/gemstoneprob.lp")
# Проблема решается с помощью выбора Решателя PuLP.
gemstoneprob.solve()
# Статус решения выводится на экран.
print("Статус:", pulp.LpStatus[gemstoneprob.status])

# OUTPUT

# Каждая переменная печатается с ее оптимальным значением.
for v in gemstoneprob.variables():
    print(v.name, "=", v.varValue)
production = [v.varValue for v in gemstoneprob.variables()]

# Значение оптимизированной целевой функции выводится на консоль.
print("Итоговая цена= ", pulp.value(gemstoneprob.objective))
