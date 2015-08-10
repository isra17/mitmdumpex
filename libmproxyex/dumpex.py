import libmproxy, signal
from libmproxy import flow
from libmproxy.dump import *
from .flowwriter import *


class Options(libmproxy.dump.Options):
    rotate_logs = False
    outfileex = None
    rfileex = None


class DumpExMaster(DumpMaster):
    def __init__(self, server, options, outfile=sys.stdout):
        # Delay the stream setup, otherwise it gets overwriten by FlowMaster.__init__
        options.outfileex = options.outfile
        options.rfileex = options.rfile
        options.outfile = None
        options.rfile = None

        self.rotate_logs = options.rotate_logs

        super(DumpExMaster, self).__init__(server, options, outfile)

        if options.outfileex:
            if options.outfileex[1] == 'split-flows':
                self.start_split_stream(options.outfileex[0], self.filt)
            else:
                options.outfile = options.outfileex
                self.start_stream(options.outfile[0], options.outfile[1], self.filt)

        if options.rfileex:
            options.rfile = options.rfileex
            try:
                self.load_flows_file(options.rfile)
            except flow.FlowReadError as v:
                self.add_event("Flow file corrupted.", "error")
                raise DumpError(v)

        if self.rotate_logs:
            signal.signal(signal.SIGUSR1, lambda n,s: self.stream.flush())


    def start_split_stream(self, split_dir, filt):
        if self.rotate_logs:
            writer = RotatedFlowWriter
        else:
            writer = FilteredFlowWriter

        self.stream = SplitFlowWriter(split_dir, writer, [filt])

    def start_stream(self, fp, mode, filt):
        if self.rotate_logs:
            self.stream = RotatedFlowWriter(fp, filt)
        else:
            self.stream = FilteredFlowWriter(fp, filt, mode=mode)

    def stop_stream(self):
        self.stream.close()

