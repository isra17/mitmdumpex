import os
from libmproxy import tnetstring

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
            if hasattr(w, 'close'):
                w.flush()
            else:
                w.fo.flush()

    def close(self):
        for k,w in self._writers.iteritems():
            if hasattr(w, 'close'):
                w.close()
            else:
                w.fo.close()
        self._writers.clear()

    def _client_writer(self, client_conn):
        client_ip = client_conn.address.address[0] if client_conn else 'unknown'
        if client_ip not in self._writers:
            fo = file(os.path.join(self._split_dir, client_ip), 'wb')
            args = [fo] + self._flow_writer_args
            self._writers[client_ip] = self._flow_writer_factory(*args)

        return self._writers[client_ip]

