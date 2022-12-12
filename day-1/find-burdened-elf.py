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


def find_burdened_elf():
    elf_foodstocks = fetch_elven_data()
    elf_calories = {k: sum(v) for k, v in elf_foodstocks.items()}
    return {elf_no: calories for elf_no, calories in elf_calories.items() if calories == max(elf_calories.values())}


if __name__ == '__main__':
    result = find_burdened_elf()
    max_calories = list(result.values())[0]
    max_elves = ', '.join([str(k) for k in result])
    output = f"Max calories: {max_calories}, for {'elf' if len(result) == 1 else 'elves'} number {max_elves}."
    print(output)
    with open('result.txt', 'w+') as f:
        f.write(output)
