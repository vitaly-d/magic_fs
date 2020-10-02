from typing import BinaryIO, Text, Union, Optional

from fs import errors
from fs.base import FS
from fs.zipfs import ReadZipFS
from fs.memoryfs import MemoryFS

from rarfile import RarFile


class ReadRarFS(ReadZipFS):
    @errors.CreateFailed.catch_all
    def __init__(self, file: Union[BinaryIO, Text], encoding: Text = "utf-8"):

        """

        The interface of rarfile "is made as zipfile-like as possible"
        see - https://rarfile.readthedocs.io/api.html

        Thus this init code is a 'copy of' ReadZipFS.__init__
            that initilizes self._zip as
                self._zip = rarfile.RarFile(file)
            instead
                self._zip = zipfile.ZipFile(file, "r")

        The rest of ReadZipFS can be re-used

        Don't forget to install the 'unrar' utility the RarFile impl rely on
        """

        # skip ReadZipFS.init() by calling FS.__init__ explicitely
        FS.__init__(self)

        self._file = file
        self.encoding = encoding
        self._zip = RarFile(file)
        self._directory_fs = None  # type: Optional[MemoryFS]
