from collections import deque


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def process_chunk(chunk: str, buffer: deque, buffer_size=4):
    for no, char in enumerate(chunk):
        buffer.append(char)
        if len(buffer) == buffer_size and len(set(buffer)) == buffer_size:
            return no + 1, ''.join(buffer)
        elif len(buffer) == buffer_size:
            buffer.popleft()
    return None, ''


if __name__ == '__main__':
    chunk_size = 1024
    chunk_no = 0
    buffer = deque([])
    with open('input.txt', 'r') as f:
        for chunk in read_in_chunks(f, chunk_size=chunk_size):
            index, str_sequence = process_chunk(chunk, buffer, buffer_size=14)
            if index:
                print(f'Index number {index + chunk_no*chunk_size}, unique sequence {str_sequence}')
                break
            chunk_no += 1
