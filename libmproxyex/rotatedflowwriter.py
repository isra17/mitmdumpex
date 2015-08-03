import os, signal
from datetime import datetime
from libmproxy import flow

class RotatedFlowWriter:
    def __init__(self, fo, filt, format='%y%m%d-'):
        self._writer = None
        self._fprefix = None
        self._fdir = os.path.dirname(fo.name)
        self._fname = os.path.basename(fo.name)
        self._format = format
        self._filt = filt
        fsize = fo.tell()
        fo.close()
        if fsize == 0:
            os.remove(fo.name)


    def add(self, f):
        self._check_rotation()
        self._writer.add(f)


    def flush(self):
        self._check_rotation()
        self._writer.fo.flush()


    def close(self):
        if self._writer:
            self._writer.fo.close()
            self._writer = None


    def _check_rotation(self):
        current_prefix = datetime.utcnow().strftime(self._format)
        if current_prefix != self._fprefix:
            if self._writer:
                self._writer.fo.close()
            f = file(os.path.join(self._fdir, current_prefix + self._fname), 'ab')
            self._writer = flow.FilteredFlowWriter(f, self._filt)
            self._fprefix = current_prefix

