import argparse
import datetime

__author__ = 'Ryan'

class Argument(object):
    """
    Basic class to store arguments
    """
    pass


def handle_arguments(arguments):
    if arguments.timespan == "all":
        # Run for all time
        pass
    elif arguments.timespan == "year":
        # Handle defaults
        if arguments.year is 0:
            arguments.year = datetime.datetime.now().year
            print "No year was provided, defaulting to", arguments.year

        # Run for the year
        pass
    elif arguments.timespan == "month":
        # Handle defaults
        if arguments.year is 0:
            arguments.year = datetime.datetime.now().year
            print "No year was provided, defaulting to", arguments.year
        if arguments.month is 0:
            arguments.month = datetime.datetime.now().month
            print "No month was provided, defaulting to", arguments.month

        # Run for the month
        pass


def create_parser():
    parser = argparse.ArgumentParser(description="Finds the top posts on care-tags.org")
    parser.add_argument('-t', '--timespan',
                        default='all',
                        choices=['all', 'year', 'month'],
                        dest='timespan',
                        help="What time span should be used? Defaults to all-time.")
    parser.add_argument('-y', '--year',
                        # Default is 0 so we can set to current year later
                        # TODO: see if it's possible to set default to current year here
                        default=0,
                        type=int,
                        dest='year',
                        help="What year should be used? Defaults to current year. Ignored if timespan is all.")
    parser.add_argument('-m', '--month',
                        # Default is 0 so we can set to current month
                        default=0,
                        type=int,
                        dest='month',
                        help="What month should be used? Defaults to current month. Ignored if timespan is all or year.")
    return parser


if __name__ == '__main__':
    parser = create_parser()

    arguments = Argument()
    parser.parse_args(args="-t month".split(), namespace=arguments)

    handle_arguments(arguments)