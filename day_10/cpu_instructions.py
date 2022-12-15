import logging
from typing import Generator


class Instruction:
    def __init__(self, cycle_time):
        self.cycle_time = cycle_time

    def func_to_register(self):
        def _callback(cpu: CPU):
            pass
        return _callback


class Noop(Instruction):
    DEFAULT_CYCLE_TIME = 1

    def __init__(self):
        super(Noop, self).__init__(self.DEFAULT_CYCLE_TIME)

    def __repr__(self):
        return 'noop'


class Addx(Instruction):
    DEFAULT_CYCLE_TIME = 2

    def __init__(self, add):
        self.add = add
        super(Addx, self).__init__(cycle_time=self.DEFAULT_CYCLE_TIME)

    def __repr__(self):
        return f"addx {self.add}"

    def func_to_register(self):
        def _callback(cpu: CPU):
            cpu.x += self.add
        return _callback


class CPU():
    def __init__(self, instruction_list: list[Instruction] = []):
        self.instruction_list = instruction_list
        self.x = 1
        self.cycle = 0
        self.registry_archive = [0]

    def record_registry(self):
        self.registry_archive.append(self.x)

    def total_signal_strength(self):
        return sum([cycle*register_value for cycle, register_value in enumerate(self.registry_archive) if cycle % 40 == 20])


class syncCPU(CPU):
    def do_cycle(self):
        current_instruction = self.instruction_list.pop()
        for c in range(current_instruction.cycle_time):
            self.cycle += 1
            self.record_registry()
        current_instruction.func_to_register()(self)


class asyncCPU(CPU):
    def __init__(self, instruction_list: list[Instruction] = []):
        super(asyncCPU, self).__init__(instruction_list)
        self.callbacks = [[None]]  # list of lists because multiple instructions can resolve on the same cycle

    def do_cycle(self):
        self.register_callback()
        self.cycle += 1
        self.record_registry()
        self.compute_instruction_results()

    def register_callback(self):
        instruction = self.instruction_list[self.cycle]
        if instruction:
            _callback = instruction.func_to_register()
            expected_completion_cycle = self.cycle + instruction.cycle_time
            if expected_completion_cycle >= len(self.callbacks):
                # extend the list of results if there are no resolutions until this one
                self.callbacks.extend([[] for i in range(expected_completion_cycle - len(self.callbacks) + 1)])
            self.callbacks[expected_completion_cycle].append(_callback)

    def compute_instruction_results(self):
        try:
            callbacks = self.callbacks[self.cycle]
        except IndexError:
            return
        for callback in callbacks:
            try:
                callback(self)
            except TypeError:
                logging.warn(f'Skipping invalid callback {callback} on cycle {self.cycle}.')
                continue


def get_input(file='input.txt') -> Generator[Instruction, None, None]:
    for line in open(file, 'r'):
        cmd = line.replace('\n', '')
        if cmd == 'noop':
            instruction = Noop()
        elif cmd.startswith('addx'):
            size = int(cmd[5:])
            instruction = Addx(size)
        else:
            raise Exception(f'Unknown instruction: {cmd}')
        yield instruction


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    cpu = syncCPU()
    for instruction in get_input('input.txt'):
        cpu.instruction_list.append(instruction)
        cpu.do_cycle()
    total_strength = cpu.total_signal_strength()
    logging.info('\n'.join([f"{cycle}: {value}" for cycle, value in enumerate(cpu.registry_archive)]))
    print(total_strength)
