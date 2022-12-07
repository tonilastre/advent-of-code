from aoc import run

class FileSystem:
    def __init__(self, name: str, file_size=None, parent_dir=None):
        self.name = name
        self.parent_dir = parent_dir
        self.is_file = file_size is not None
        self.file_size = file_size
        self.files = []

    @property
    def size(self):
        return sum(f.size for f in self.files) if self.file_size is None else self.file_size

    @property
    def depth(self):
        depth = 0
        node = self.parent_dir
        while node:
            node = node.parent_dir
            depth += 1
        return depth

    def add_file(self, name: str, file_size=None):
        existing_file = next((f for f in self.files if f.name == name), None)
        if existing_file:
            return existing_file

        file = FileSystem(name, file_size=file_size, parent_dir=self)
        self.files.append(file)
        return file

    def __repr__(self):
        prefix = ' ' * self.depth * 2
        context = f'file, size={self.file_size}' if self.is_file else 'dir'
        children = ('\n' + '\n'.join(repr(f) for f in self.files)).rstrip('\n')
        return f'{prefix}- {self.name} ({context}){children}'

def parse_input_as_file_system(lines):
    root = FileSystem('/')
    current = root

    for line in lines:
        if line.startswith('$ cd'):
            directory = line[4:].strip()
            if directory == '/':
                current = root
            elif directory == '..':
                current = current.parent_dir
            else:
                current = current.add_file(directory)
            continue

        if line.startswith('$ ls'):
            continue

        if line.startswith('dir'):
            current.add_file(line[4:].strip())
            continue

        size, filename = line.split(' ', maxsplit=1)
        current.add_file(filename, int(size))

    return root

def get_directory_sum(root, max_size):
    dir_sum = root.size if not root.is_file and root.size <= max_size else 0
    return dir_sum + sum(get_directory_sum(f, max_size) for f in root.files)

def get_min_deleted_directory_size(root, target_size):
    sizes = [get_min_deleted_directory_size(f, target_size) for f in root.files]
    if not root.is_file:
        sizes.append(root.size)
    return min((s for s in sizes if s >= target_size), default=0)

def get_first(lines):
    root = parse_input_as_file_system(lines)
    return get_directory_sum(root, 100000)

def get_second(lines):
    total_available_size = 70000000 - 30000000
    root = parse_input_as_file_system(lines)
    target_size = root.size - total_available_size
    return get_min_deleted_directory_size(root, target_size)

if __name__ == '__main__':
    run(get_first, get_second)
