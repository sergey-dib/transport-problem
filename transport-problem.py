import sys
import numpy as np

d = {1: 80, 2: 270, 3: 250, 4: 160, 5: 180}  # потребительский спрос
M = {1: 500, 2: 500, 3: 500}  # мощность завода
I = [1, 2, 3, 4, 5]  # Клиенты
J = [1, 2, 3]  # Заводы
cost = {(1, 1): 4, (1, 2): 6, (1, 3): 9,
        (2, 1): 5, (2, 2): 4, (2, 3): 7,
        (3, 1): 6, (3, 2): 3, (3, 3): 3,
        (4, 1): 8, (4, 2): 5, (4, 3): 3,
        (5, 1): 10, (5, 2): 8, (5, 3): 4
        }  # транспортные расходы


# d = {1: 80, 2: 270, 3: 250, 4: 160, 5: 180}  # потребительский спрос
# M = {1: 500, 2: 1200}  # мощность завода
# I = [1, 2, 3, 4, 5]  # Клиенты
# J = [1, 2]  # Заводы
# cost = {(1, 1): 4, (1, 2): 6,
#         (2, 1): 5, (2, 2): 4,
#         (3, 1): 6, (3, 2): 3,
#         (4, 1): 8, (4, 2): 5,
#         (5, 1): 10, (5, 2): 8,
#         }  # транспортные расходы


''''
- переменные решения - количества товаров, которые должны быть отправлены с завода j покупателю i
 (положительные действительные числа)
- ограничения - общее количество товаров должно удовлетворять как потребительский спрос,
 так и производственные мощности фабрики (равенства / неравенства, которые имеют линейное выражение в левой части)
- целевая функция - найти такие значения переменных решения, при которых общая стоимость перевозки будет
 наименьшей (в данном случае линейное выражение)
'''

# для использования в SciPy необходимо преобразовать словарь стоимости в 2D-массив
cost2d = np.empty([len(I), len(J)])
for i in range(len(I)):
    for j in range(len(J)):
        cost2d[i, j] = cost[i + 1, j + 1]

# инициализировать переменные решения

x0 = np.ones(len(cost)) * 100
bounds = list((0, max(d.values())) for _ in range(cost2d.size))

print(bounds)


# объявить целевую функцию.

def objective(x):
    obj_func = sum(x[idx] * cost2d[idx // len(J), idx % len(J)] for idx in range(cost2d.size))
    return obj_func


# определить ограничения

# Ограничения: сумма товаров == покупательский спрос
def const1():
    tmp = []
    for idx in range(0, cost2d.size, len(J)):
        tmp_constr = {
            'type': 'eq',
            'fun': lambda x, idx: d[idx // len(J) + 1] - np.sum(x[idx: idx + len(J)]),
            'args': (idx,)
        }
        tmp.append(tmp_constr)
    return tmp


# Ограничения: сумма товаров <= мощность завода
def const2():
    tmp = []
    for idx in range(0, cost2d.size, len(I)):
        tmp_constr = {
            'type': 'ineq',
            'fun': lambda x, idx=idx: M[idx // len(I) + 1] - np.sum(x[idx: idx + len(I)])
        }
        tmp.append(tmp_constr)
    return tmp


list_of_lists = [const1(), const2()]
constraints = [item for sublist in list_of_lists for item in sublist]

from scipy.optimize import minimize

solution = minimize(fun=objective,
                    x0=x0,
                    bounds=bounds,
                    method='SLSQP',
                    constraints=constraints,
                    tol=None,
                    callback=None,
                    options={'full_output': False, 'disp': False, 'xtol': 1e-8}
                    )

# полученные результаты
if (solution.success) and (solution.status == 0):
    print("Решение возможно и оптимально")
    print("Значение целевой функции = ", solution.fun)
elif solution.status != 0:
    print("Не удалось найти решение. Код выхода", solution.status)
else:
    # что-то еще не так
    print(solution.message)
if solution.success:
    EPS = 1.e-6
    for i, _ in enumerate(solution.x):
        if solution.x[i] > EPS:
            print("количество отправки %10s с завода %3s заказчику %3s" % (
                round(solution.x[i]), i % len(J) + 1, i // len(J) + 1))
