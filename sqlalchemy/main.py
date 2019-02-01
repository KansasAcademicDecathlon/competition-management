import argparse
import distutils.dir_util
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
import reports as Reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', help='Database File',
                        default='contest.db')
    parser.add_argument('--log', help='Logging level',
                        default='ERROR', dest='loglevel')
    parser.add_argument(
        '--test', help='Use memory database for testing', action='store_true')

    args = parser.parse_args()

    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)
    logging.basicConfig(level=numeric_level)

    if args.test:
        engine = create_engine('sqlite:///:memory:', echo=True)
    else:
        engine = create_engine(
            'sqlite:///{0}'.format(args.database), echo=True)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    session = Session()

    # Ensure the output directory exists
    distutils.dir_util.mkpath("outputs")

    if not args.test:
        Reports.generate_TeamImportData(session)
        Reports.generate_CoachImport(session)
        Reports.generate_rosters(session)
        Reports.generate_StudentRooms(session)
        Reports.generate_room_schedules(session)
        Reports.generate_totals(session)
        Reports.generate_volunteer_list(session)


if __name__ == "__main__":
    main()
