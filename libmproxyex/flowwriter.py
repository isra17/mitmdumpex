import os, signal
from datetime import datetime
from libmproxy import flow, tnetstring


def _ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)


class FlowWriter(object):
    def __init__(self, filepath):
        pass

    def add(self, f):
        pass

    def flush(self):
        pass

    def close(self):
        pass


class FileFlowWriter(FlowWriter):
    def __init__(self, path, mode='wb'):
        self.fo = file(path, mode)

    def add(self, flow):
        d = flow.get_state()
        tnetstring.dump(d, self.fo)

    def flush(self):
        self.fo.flush()

    def close(self):
        self.fo.close()


class FilteredFlowWriter(FileFlowWriter):
    def __init__(self, path, filt, mode='wb'):
        super(FilteredFlowWriter, self).__init__(path, mode)
        self.filt = filt

    def add(self, f):
        if self.filt and not f.match(self.filt):
            return
        super(FilteredFlowWriter, self).add(f)


class RotatedFlowWriter:
    def __init__(self, fdir, filt, format='%y-%m-%d'):
        self._writer = None
        self._fname = None

        self._fdir = fdir
        _ensure_dir(self._fdir)

        self._format = format
        self._filt = filt

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
        current_name = datetime.utcnow().strftime(self._format)
        if current_name != self._fname:
            if self._writer:
                self._writer.fo.close()

            self._fname = current_name
            f = file(os.path.join(self._fdir, self._fname), 'ab')
            self._writer = flow.FilteredFlowWriter(f, self._filt)


class SplitFlowWriter():
    def __init__(self, split_dir, flow_writer_factory, flow_writer_args=[]):
        self._flow_writer_args = flow_writer_args
        self._flow_writer_factory = flow_writer_factory
        self._split_dir = split_dir
        self._writers = {}

    def add(self, f):
        writer = self._client_writer(f.client_conn)
        writer.add(f)

    def flush(self):
        for k,w in self._writers.iteritems():
            w.flush()

    def close(self):
        for k,w in self._writers.iteritems():
            w.close()
        self._writers.clear()

    def _client_writer(self, client_conn):
        client_ip = client_conn.address.address[0] if client_conn else 'unknown'
        if client_ip not in self._writers:
            fp = os.path.join(self._split_dir, client_ip)
            args = [fp] + self._flow_writer_args
            self._writers[client_ip] = self._flow_writer_factory(*args)

        return self._writers[client_ip]

