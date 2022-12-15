from ..cpu_instructions import syncCPU, get_input


def test_cpu():
    cpu = syncCPU()
    for instruction in get_input('test_input.txt'):
        cpu.instruction_list.append(instruction)
        cpu.do_cycle()
    total_strength = cpu.total_signal_strength()
    expected_strength = 13140
    assert total_strength == expected_strength
