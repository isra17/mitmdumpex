from libmproxy.cmdline import *

def mitmdumpex():
    parser = mitmdump()

    # Add a mutually exlusive flag to existing parser
    outgroup = (group for group in parser._mutually_exclusive_groups \
                  if any(a for a in group._group_actions if a.dest == 'outfile')).next()
    outgroup.add_argument(
        '--split-flows',
        action='store', dest='outfile', type=lambda d: (d, 'split-flows'),
        help='Write flows to files splitted by clients'
    )

    parser.add_argument(
        '--rotate-logs',
        action='store_true',
        help='Rotate logs each day'
    )

    return parser

