import argparse
import logging

import contest as ct


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', help='Database File',
                        default='contest.db')
    parser.add_argument('--log', help='Logging level',
                        default='ERROR', dest='loglevel')

    parser.add_argument('command', help='Action to perform',)

    args = parser.parse_args()

    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)
    logging.basicConfig(level=numeric_level)

    contest = ct.Contest()

    contest.open_database(args.database)

    if args.command == 'roster':
        contest.generate_roster_csv()
    if args.command == 'TeamImportData':
        contest.generate_TeamImportData()
    if args.command == 'CoachImport':
        contest.generate_CoachImport()


if __name__ == "__main__":
    main()
