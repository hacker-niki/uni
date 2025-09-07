def parse_person_data(data):
    try:
        name, surname, age = data.split()
        age = int(age)
        return surname, name, age
    except ValueError:
        raise ValueError("Invalid format. Expected: 'name surname age'.")

def get_people_data(input_function=input):
    people = []
    while True:
        data = input("Введите имя, фамилию и возраст (или 'stop' для завершения): ")
        if data.lower() == 'stop':
            break
        try:
            people.append(parse_person_data(data))
        except ValueError as e:
            print(e)
    return people

def display_people_data(people):
    for surname, name, age in people:
        print(f"{surname} {name} {age}")

def calculate_age_statistics(people):
    if len(people) == 0:
        return None, None, None
    ages = [age for _, _, age in people]
    min_age = min(ages)
    max_age = max(ages)
    avg_age = sum(ages) / len(ages)
    return min_age, max_age, avg_age

def main():
    people = get_people_data()
    display_people_data(people)
    min_age, max_age, avg_age = calculate_age_statistics(people)
    print(f"Самый малый возраст: {min_age}")
    print(f"Самый большой возраст: {max_age}")
    print(f"Средний возраст: {avg_age:.2f}")

if __name__ == "__main__":
    main()