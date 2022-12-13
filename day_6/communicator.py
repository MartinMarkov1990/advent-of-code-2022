from collections import deque


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def process_chunk(chunk: str, last_three: deque):
    for no, char in enumerate(chunk):
        print(f"{no+1}: {char}")
        last_three.append(char)
        if len(last_three) == 4 and len(set(last_three)) == 4:
            return no + 1, ''.join(last_three)
        elif len(last_three) == 4:
            last_three.popleft()
        print(''.join(last_three))
    return None, ''


if __name__ == '__main__':
    chunk_size = 1024
    chunk_no = 0
    last_three = deque([])
    with open('input.txt', 'r') as f:
        for chunk in read_in_chunks(f, chunk_size=chunk_size):
            index, str_sequence = process_chunk(chunk, last_three)
            if index:
                print(f'Index number {index + chunk_no*chunk_size}, unique sequence {str_sequence}')
                break
            chunk_no += 1
