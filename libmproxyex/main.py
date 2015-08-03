from __future__ import print_function
import sys, signal
from . import cmdline
from libmproxy import main
from libmproxy.proxy import process_proxy_options

def mitmdumpex(args=None):
    from . import dumpex
    parser = cmdline.mitmdumpex()

    options = parser.parse_args(args)
    if options.quiet:
        options.verbose = 0
        options.flow_detail = 0

    proxy_config = process_proxy_options(parser, options)
    dump_options = dumpex.Options(**cmdline.get_common_options(options))
    dump_options.flow_detail = options.flow_detail
    dump_options.keepserving = options.keepserving
    dump_options.filtstr = " ".join(options.args) if options.args else None

    dump_options.rotate_logs = options.rotate_logs

    server = main.get_server(dump_options.no_server, proxy_config)

    try:
        master = dumpex.DumpExMaster(server, dump_options)

        def cleankill(*args, **kwargs):
            master.shutdown()

        signal.signal(signal.SIGTERM, cleankill)
        master.run()
    except dumpex.DumpError as e:
        print("mitmdump: %s" % e, file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        pass

