from __future__ import absolute_import
from __future__ import print_function

from teststar.command import TestStarCommand
from teststar.utils import bugreport


def main():
    try:
        teststar = TestStarCommand()
        teststar.execute_from_commandline()
    except:
        import sys
        print(bugreport(), file=sys.stderr)
        raise


if __name__ == "__main__":
    main()