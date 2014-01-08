from repreader import RepReader
from operator import itemgetter
from displayer import Displayer
from optparse import OptionParser
import sys

usage = "Usage: %prog -u <USERNAME> -p <PASSWORD> -n <USERNUMBER TO DISPLAY>"
parser = OptionParser(usage)

parser.add_option(
    "-u",
    "--username",
    dest="user",
    help="Needs a username to login with",
    default=None)

parser.add_option(
    "-p",
    "--password",
    dest="pw",
    help="Need the password to login user",
    default=None)

parser.add_option(
        "-n",
        "--number",
        dest="usernum",
        help="The user number to look up",
        type="int",
        default=2)

if not len(sys.argv) == 7:
    parser.print_help()
    sys.exit()

(options, args) = parser.parse_args()

test = RepReader(options.user,options.pw)
display = Displayer()

allrep = sorted(test.receivedrep(options.usernum),key=itemgetter(1),reverse=True)
display.displayAllRep(allrep)

mostrep = test.mostrepped(options.usernum)
display.displayMostRepped(mostrep)
