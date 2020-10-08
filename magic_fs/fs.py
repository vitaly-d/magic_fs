from functools import lru_cache
from typing import BinaryIO, Text, SupportsInt, Union, TypeVar

import magic

from fs.base import FS
from fs.osfs import OSFS as _OSFS
from fs.subfs import SubFS as _SubFS
from fs.memoryfs import MemoryFS as _MemoryFS
from fs.tarfs import ReadTarFS as _ReadTarFS
from fs.zipfs import ReadZipFS as _ReadZipFS


from .rar import ReadRarFS as _ReadRarFS

_MAGIC_READ = 4096
_ENC = "utf-8"

FileSystem = TypeVar("FileSystem", bound="FS", covariant=True)


class MagicMixin:
    """adds magic() to a FS

    It might be useful to override getinfo, but, it was decided to implement
    a separate method because file.read() is called to access 'magic bytes'
    """

    @staticmethod
    def _create_magic(mime=True, uncompress=False):
        return magic.Magic(mime=mime, uncompress=uncompress)

    def magic(
        self,
        path: Text,
        mime: bool = False,
        uncompress=False,
        bytes_to_read: int = _MAGIC_READ,
    ) -> Text:
        """
        path: file path
        mime: return mimeType
        bytes_to_read: "recommend using at least the first 2048 bytes, as less can produce incorrect identification",
                        see https://pypi.org/project/python-magic/


        """
        _path = self.validatepath(path)
        f = self._create_magic(mime=mime, uncompress=uncompress)
        return f.from_buffer(self.open(_path, "rb").read(bytes_to_read))


class OSFS(_OSFS, MagicMixin):
    def __init__(
        self,
        root_path: Text,
        create: bool = False,
        create_mode: SupportsInt = 0o777,
        expand_vars: bool = True,
    ):
        super().__init__(root_path, create, create_mode, expand_vars)


class SubFS(_SubFS, MagicMixin):
    def __init__(self, parent_fs: FileSystem, path: Text):
        super().__init__(parent_fs, path)


class MemoryFS(_MemoryFS, MagicMixin):
    def __init__(self):
        super().__init__()


class ReadTarFS(_ReadTarFS, MagicMixin):
    def __init__(self, file: Union[BinaryIO, Text], encoding: Text = _ENC):
        super().__init__(file, encoding)


class ReadZipFS(_ReadZipFS, MagicMixin):
    def __init__(self, file: Union[BinaryIO, Text], encoding: Text = _ENC):
        super().__init__(file, encoding)


class ReadRarFS(_ReadRarFS, MagicMixin):
    def __init__(self, file: Union[BinaryIO, Text], encoding: Text = _ENC):
        super().__init__(file, encoding)


_known_ext = {
    ".zip": "application/zip",
    ".rar": "application/x-tar",
    ".tar": "application/x-tar",
    ".gz": "application/gzip",
    ".bz2": "application/x-bzip2",
    # force --mime-type -z for files without ext
    "": "application/gzip",
}

_compressed = {"application/x-bzip2", "application/gzip"}

_supported_mime_types = {
    "application/zip": ReadZipFS,
    "application/x-tar": ReadTarFS,
    "application/x-rar": ReadRarFS,
    # "application/x-lzh-compressed": TODO
}


@lru_cache(maxsize=8)
def _archive_type(parent_fs, path):

    # if tuple(parent_fs.getinfo(path).suffixes)[-2:] in _unsupported_formats_2:
    #     return "unsupported"

    mime = _known_ext.get(parent_fs.getinfo(path).suffix, None)
    if mime is not None:
        # refine mime-type using magic bytes
        mime = parent_fs.magic(path, mime=True, uncompress=mime in _compressed)

    return mime


def is_archive(parent_fs, path):

    return _archive_type(parent_fs, path) in _supported_mime_types


def mount_archive(parent_fs, path):

    mount_fs = _supported_mime_types.get(_archive_type(parent_fs, path), None)
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
