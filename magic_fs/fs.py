from typing import BinaryIO, Text, SupportsInt, Union

import magic

from fs.osfs import OSFS as _OSFS
from fs.tarfs import ReadTarFS as _ReadTarFS
from fs.zipfs import ReadZipFS as _ReadZipFS


from .rar import ReadRarFS as _ReadRarFS

_MAGIC_READ = 4096
_ENC = "utf-8"


class MagicMixin:
    """adds magic() to a FS

    It might be useful to override getinfo, but, it was decided to implement
    a separate method because it requres reading a file content to get magic
    """

    def magic(self, path, mime=False):
        _path = self.validatepath(path)
        return magic.from_buffer(self.open(_path, "rb").read(_MAGIC_READ), mime=mime)


class OSFS(_OSFS, MagicMixin):
    def __init__(
        self,
        root_path: Text,
        create: bool = False,
        create_mode: SupportsInt = 0o777,
        expand_vars: bool = True,
    ):
        super().__init__(root_path, create, create_mode, expand_vars)


class ReadTarFS(_ReadTarFS, MagicMixin):
    def __init__(self, file: Union[BinaryIO, Text], encoding: Text = _ENC):
        super().__init__(file, encoding)


class ReadZipFS(_ReadZipFS, MagicMixin):
    def __init__(self, file: Union[BinaryIO, Text], encoding: Text = _ENC):
        super().__init__(file, encoding)


class ReadRarFS(_ReadRarFS, MagicMixin):
    def __init__(self, file: Union[BinaryIO, Text], encoding: Text = _ENC):
        super().__init__(file, encoding)


def mount_archive(parent_fs, path):

    supported_formats = {
        (".zip",): ReadZipFS,
        (".tar", ".gz"): ReadTarFS,
        (".rar",): ReadRarFS,
    }

    mount_fs = supported_formats.get(tuple(parent_fs.getinfo(path).suffixes), None)
    if mount_fs:
        return mount_fs(parent_fs.open(path, "rb"))
    else:
        return None


# from magic_fs.fs import OSFS, mount_archive


# def walk(fs):
#     for path in fs.walk.files():
#         print(path, fs.magic(path))
#         archive_fs = mount_archive(fs, path)
#         if archive_fs is not None:
#             archive_fs.tree()
#             walk(archive_fs)


# walk(OSFS("/Volumes/T3/IEEE"))
