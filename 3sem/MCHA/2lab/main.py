import addons
from simpleIterations import simple_iterations
from zeidel import zeidel_method

c = addons.read_matrix_from_file('c.mcha')
d = addons.read_matrix_from_file('d.mcha')
b = addons.read_matrix_from_file('b.mcha').T

a = 10 * c + d
print("Изначальная матрица")
print(a)

print("Ответ методом простых итераций")
ans = simple_iterations(a, b)
print(ans)

print("Ответ методом Зейделя")
ans = zeidel_method(a, b)
print(ans)

print("Запуск проверки методов:")
print("Введите количество тестов")
n = int(input())
addons.test_methods(n)

# print("\n\n\n\n")
# addons.test_methods(n, check=False)
