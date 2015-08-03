import libmproxy
from libmproxy import flow
from libmproxy.dump import *
from .splitflowwriter import SplitFlowWriter
from .rotatedflowwriter import RotatedFlowWriter

class Options(libmproxy.dump.Options):
    rotate_logs = False


class DumpExMaster(DumpMaster):
    def __init__(self, server, options, outfile=sys.stdout):
        # Delay the stream setup, otherwise it gets overwriten by FlowMaster.__init__
        split_dir = None
        if options.outfile and options.outfile[1] == 'split-flows':
            split_dir = options.outfile[0]
            options.outfile = None

        # Delay the flows loading, otherwise we can't use our custom FlowWriter
        rfile = None
        if options.rfile:
            rfile = options.rfile
            options.rfile = None

        self.rotate_logs = options.rotate_logs

        super(DumpExMaster, self).__init__(server, options, outfile)

        if split_dir:
            self.start_split_stream(split_dir, self.filt)

        if rfile:
            options.rfile = rfile
            try:
                self.load_flows_file(options.rfile)
            except flow.FlowReadError as v:
                self.add_event("Flow file corrupted.", "error")
                raise DumpError(v)


    def start_split_stream(self, split_dir, filt):
        if self.rotate_logs:
            writer = RotatedFlowWriter
        else:
            writer = flow.FilteredFlowWriter

        self.stream = SplitFlowWriter(split_dir, writer, [filt])

    def start_stream(self, fp, filt):
        if self.rotate_logs:
            self.stream = RotatedFlowWriter(fp, filt)
        else:
            self.stream = FilteredFlowWriter(fp, filt)

    def stop_stream(self):
        if hasattr(self.stream, 'close'):
            self.stream.close()
        else:
            super(DumpExMaster, self).stop_stream(self)

