import re
from enum import Enum, auto

from anytree import AnyNode, Resolver, ChildResolverError, LevelOrderIter


class DirTreeCommandsParseError(BaseException):
    pass


class Dir(AnyNode):
    @property
    def size(self):
        if len(self.children) == 0:
            return 0
        return sum([child.size for child in self.children])


class File(AnyNode):
    def __init__(self, size, *args, **kwargs):
        AnyNode.__init__(self, *args, **kwargs)
        self.size = size


class ParseState(Enum):
    CD = auto()
    LS = auto()


class FileTree:
    def __init__(self, filename='input.txt'):
        self.filename = 'input.txt'
        self.root = None
        self.current = None
        self._state = None
        self.resolver = Resolver()

    def get_child_dir(self, dir: str) -> AnyNode():
        try:
            child_dir = self.resolver.get(self.current, dir)
        except ChildResolverError:
            child_dir = Dir(name=dir, parent=self.current)
        return child_dir

    def parse_file(self):
        for line in open(self.filename, 'r'):
            if line[-1] == '\n':
                line = line[0:-1]
            if line.startswith('$ cd'):
                self._state = ParseState.CD
                dir = line[5:]
                if dir == '..':
                    self.current = self.current.parent
                else:
                    if self.root is None:
                        self.root = Dir(name=dir)
                        self.current = self.root
                    else:
                        self.current = self.get_child_dir(dir)
            elif line == '$ ls':
                self._state = ParseState.LS
            elif line.startswith('dir'):
                dir = line[4:]
                self.get_child_dir(dir)
            else:
                m = re.match('([0-9]+)\\s+([a-zA-Z].*)', line)
                if not m:
                    raise DirTreeCommandsParseError(f'Unknown command format: {line}')
                size, filename = m.groups()
                File(size=int(size), name=filename, parent=self.current)


if __name__ == '__main__':
    THRESHOLD = 100000
    TOTAL_DISC_SPACE = 70000000
    NECESSARY_FREE_SPACE = 30000000
    filetree = FileTree()
    filetree.parse_file()

    # part 1
    small_dirs = [node for node in LevelOrderIter(filetree.root) if isinstance(node, Dir) and node.size <= THRESHOLD]
    total_size_small_dirs = sum([dir.size for dir in small_dirs])
    print(f"Total size to save: {total_size_small_dirs}")

    # part 2
    current_free_space = TOTAL_DISC_SPACE - filetree.root.size
    extra_space_necessary = NECESSARY_FREE_SPACE - current_free_space
    print("Extra space necessary:", extra_space_necessary)
    candidate_directories = [node for node in LevelOrderIter(filetree.root) if isinstance(node, Dir) and node.size >= extra_space_necessary]
    directory_to_delete = [dir for dir in candidate_directories if dir.size == min([dir.size for dir in candidate_directories])]
    print(directory_to_delete[0].path, directory_to_delete[0].size)
