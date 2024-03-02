import dataclasses, collections, typing

File = collections.namedtuple("File", ["name", "size"])
DirEntry = collections.namedtuple("Directory", ["name", "folder"])

@dataclasses.dataclass
class Dir:
    directories: list = dataclasses.field(default_factory=list)
    files: list = dataclasses.field(default_factory=list)
    parent: 'typing.Any' = None

    @property
    def is_empty(self):
        return len(self.directories)==0 and len(self.files)==0
    
    def find_dir(self, dir_name):
        if dir_name == "/":
            folder = self
            while folder.parent is not None:
                folder = folder.parent
            return folder
        for d in self.directories:
            if d.name == dir_name:
                return d.folder
        return None
    
    def total_size(self):
        return sum(f.size for f in self.files) + sum(d.folder.total_size() for d in self.directories)

    def find_all_dirs(self):
        for d in self.directories:
            yield d
            yield from d.folder.find_all_dirs()

class Parse:
    def __init__(self, rows):
        self._file_system = Dir()
        current_dir = self._file_system
        current_ls = Dir()
        for row in rows:
            row = row.strip()
            if row[:2] == "$ ":
                self._push_ls(current_ls, current_dir)
                current_ls = Dir()
                if row[2:5] == "cd ":
                    dir_path = row[5:]
                    if dir_path == "/":
                        pass
                    elif dir_path == "..":
                        current_dir = current_dir.parent
                        if current_dir is None:
                            raise Exception("Backtracked too far")
                    else:
                        current_dir = current_dir.find_dir(dir_path)
                        if current_dir is None:
                            raise KeyError(dir_path)
                elif row[2:] == "ls":
                    pass
                else:
                    raise SyntaxError(row)
            else:
                if row[:4] == "dir ":
                    current_ls.directories.append(row[4:])
                else:
                    size, name = row.split()
                    current_ls.files.append(File(name, int(size)))
        self._push_ls(current_ls, current_dir)
        
    def _push_ls(self, cur_ls, current_dir):
        if cur_ls.is_empty:
            return
        current_dir.files.extend(cur_ls.files)
        for dir_name in cur_ls.directories:
            new_dir = Dir(parent=current_dir)
            current_dir.directories.append(DirEntry(name=dir_name, folder=new_dir)) 

    @property
    def file_system(self):
        return self._file_system
    
    def find_small_dirs(self, maxsize):
        for dentry in self.file_system.find_all_dirs():
            if dentry.folder.total_size() <= maxsize:
                yield dentry

    def sum_small_dirs(self, maxsize=100000):
        return sum(d.folder.total_size() for d in self.find_small_dirs(maxsize))
    
    def dir_to_delete(self, disk_size=70000000, needed_space=30000000):
        currently_free = disk_size - self.file_system.total_size()
        needed = needed_space - currently_free
        name, best = "/", self.file_system
        gap = best.total_size() - needed
        for dentry in self.file_system.find_all_dirs():
            newgap = dentry.folder.total_size() - needed
            if newgap >=0 and newgap < gap:
                name, best = dentry.name, dentry.folder
                gap = newgap
        return name, best
    

def main(second_flag):
    with open("input7.txt") as f:
        fs = Parse(f)
    if not second_flag:
        return fs.sum_small_dirs()
    _, d = fs.dir_to_delete()
    return d.total_size()
