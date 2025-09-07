import matplotlib.pyplot as plt
from sympy import Symbol, sinh
import sympy as sp

import diff_calc
import int_calc

z = Symbol('z')
f = sinh(1 / z)  # Example integrand function
l = 1  # Left bound of the interval
r = 2  # Right bound of the interval
tol = 1e-6  # Desired tolerance

# Call the integration methods and print the results
# print("Middle Rectangle Method:")
# result_mid_rect = int_calc.int_middle_rectangle(f, l, r, 1000)
# print("Approximate integral:", result_mid_rect)
# 
# print("\nTrapezoid Method:")
# result_trapezoid = int_calc.integral_trapezoid(f, l, r, 1000)
# print("Approximate integral:", result_trapezoid)
#
# print("\nSimpson's Method:")
# result_simpson = int_calc.integral_simpson(f, l, r, 1000)
# print("Approximate integral:", result_simpson)

# Initialize lists to store the values of n and the corresponding integral approximations
n_values = []
integral_values = []

# Calculate the integral for different values of n
for n in range(1, 1001, 10):
    integral = int_calc.int_middle_rectangle(f, l, r, 1 / n)
    n_values.append(1/n)
    integral_values.append(integral)

# Plot the integral values as a function of n
plt.plot(n_values, integral_values, marker='o')
plt.xlabel('n')
plt.ylabel('Approximate Integral')
plt.title('Approximate Integral using Middle Rectangle Method')
plt.grid(True)
plt.show()

n_values = []
trapezoid_integral_values = []
middle_rectangle_integral_values = []

# Calculate the integrals for different values of n
for n in range(1, 1001, 10):
    trapezoid_integral = int_calc.integral_trapezoid(f, l, r, 1 / n)
    middle_rectangle_integral = int_calc.int_middle_rectangle(f, l, r, 1 / n)
    n_values.append(1/n)
    trapezoid_integral_values.append(trapezoid_integral)
    middle_rectangle_integral_values.append(middle_rectangle_integral)

# Plot the integral values as a function of n
plt.plot(n_values, trapezoid_integral_values, label='Trapezoid Method', marker='o')
plt.plot(n_values, middle_rectangle_integral_values, label='Middle Rectangle Method', marker='o')
plt.xlabel('n')
plt.ylabel('Approximate Integral')
plt.title('Approximate Integral using Different Methods')
plt.legend()
plt.grid(True)
plt.show()

z = sp.symbols('z')
# f = (sp.tan(z))**0.5
f = sp.cosh(z)
f1 = sp.diff(f, z)
f2 = sp.diff(f1, z)
f3 = sp.diff(f2, z)
f4 = sp.diff(f3, z)
middle_dot = 1.5


def delta(new_diff, known_number=f1.subs(z, middle_dot).evalf()):
    return abs(new_diff - known_number)


print(f"\nderivative of the first order: {f1.subs(z, middle_dot).evalf()}")
d1 = diff_calc.deriviative_first(f, middle_dot, f2, f3)
print(f"derivative with numerical differentiation: {d1.evalf()}"
      f"\n\tdelta = {delta(d1.evalf())}")

print(f"\nderivative of the second order = {f2.subs(z, middle_dot).evalf()}")
d2 = diff_calc.deriviative_second(f, middle_dot, f4).evalf()
print(f"derivative with numerical differentiation: {d2}"
      f"\n\tdelta = {delta(d2, f2.subs(z, middle_dot).evalf())}")
d2 = diff_calc.deriviative_second2(f, middle_dot, f2, f4).evalf()
print(f"derivative with numerical differentiation (second option): {d2}"
      f"\n\tdelta = {delta(d2, f2.subs(z, middle_dot).evalf())}")
