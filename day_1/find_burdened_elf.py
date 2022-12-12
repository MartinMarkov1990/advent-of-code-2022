def fetch_elven_data():
    elf_foodstocks = {}
    elf_no = 1
    with open('input.txt', 'r') as f:
        line = f.readline()
        while line:
            if line == '\n':
                elf_no += 1
            else:
                line = int(line.replace('\n', ''))
                if elf_no not in elf_foodstocks:
                    elf_foodstocks[elf_no] = [line]
                else:
                    elf_foodstocks[elf_no].append(line)
            line = f.readline()
    return elf_foodstocks


def compute_total_calories(elf_foodstocks: dict) -> dict:
    return {k: sum(v) for k, v in elf_foodstocks.items()}


def find_burdened_elf(total_calories: dict) -> dict:
    return {elf_no: calories for elf_no, calories in total_calories.items() if calories == max(total_calories.values())}


def find_burdened_elves(total_calories: dict, count=3) -> dict:
    values = list(total_calories.items())
    values.sort(key=lambda x: x[1], reverse=True)
    return dict(values[0:count])


def main_1():
    elf_foodstocks = fetch_elven_data()
    total_calories = compute_total_calories(elf_foodstocks)
    result = find_burdened_elf(total_calories)
    max_calories = list(result.values())[0]
    max_elves = ', '.join([str(k) for k in result])
    output = f"Max calories: {max_calories}, for {'elf' if len(result) == 1 else 'elves'} number {max_elves}."
    print(output)
    with open('result.txt', 'w+') as f:
        f.write(output)


def main_2():
    elf_foodstocks = fetch_elven_data()
    total_calories = compute_total_calories(elf_foodstocks)
    result = find_burdened_elves(total_calories, 3)
    output = f"Total calories on the top 3 elves: {sum(result.values())}"
    print(output)
    with open('result_part_2.txt', 'w+') as f:
        f.write(output)


if __name__ == '__main__':
    main_2()
