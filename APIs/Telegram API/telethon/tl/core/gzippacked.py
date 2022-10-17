import gzip
import struct

from .. import TLObject


class GzipPacked(TLObject):
    CONSTRUCTOR_ID = 0x3072cfa1

    def __init__(self, data):
        """
        Initialize data.

        Args:
            self: (todo): write your description
            data: (todo): write your description
        """
        self.data = data

    @staticmethod
    def gzip_if_smaller(content_related, data):
        """Calls bytes(request), and based on a certain threshold,
           optionally gzips the resulting data. If the gzipped data is
           smaller than the original byte array, this is returned instead.

           Note that this only applies to content related requests.
        """
        if content_related and len(data) > 512:
            gzipped = bytes(GzipPacked(data))
            return gzipped if len(gzipped) < len(data) else data
        else:
            return data

    def __bytes__(self):
        """
        Return the gzip string.

        Args:
            self: (todo): write your description
        """
        return struct.pack('<I', GzipPacked.CONSTRUCTOR_ID) + \
               TLObject.serialize_bytes(gzip.compress(self.data))

    @staticmethod
    def read(reader):
        """
        Reads a gzip document.

        Args:
            reader: (todo): write your description
        """
        constructor = reader.read_int(signed=False)
        assert constructor == GzipPacked.CONSTRUCTOR_ID
        return gzip.decompress(reader.tgread_bytes())

    @classmethod
    def from_reader(cls, reader):
        """
        Deserialize a gzip document.

        Args:
            cls: (todo): write your description
            reader: (todo): write your description
        """
        return GzipPacked(gzip.decompress(reader.tgread_bytes()))

    def to_dict(self):
        """
        Return a dict representation of the dict.

        Args:
            self: (todo): write your description
        """
        return {
            '_': 'GzipPacked',
            'data': self.data
        }