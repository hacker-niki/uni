import random


def print_hello_world():
  """
  Печатает в консоль "Hello, world!"
  "And hi again!"
  "!!!!!!!!!"
  с случайным числом восклицательных знаков в третьей строке
  """
  print("Hello, world!")
  print("And hi again!")
  print("!" * random.randint(5, 50))