import argparse
import logging
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
import online_testing as Online
import reports as Reports
import csvGenerator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", help="Database File", default="contest.db")
    parser.add_argument("--log", help="Logging level", default="ERROR", dest="loglevel")
    parser.add_argument(
        "--test", help="Use memory database for testing", action="store_true"
    )

    args = parser.parse_args()

    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % args.loglevel)
    logging.basicConfig(level=numeric_level)

    if args.test:
        engine = create_engine("sqlite:///:memory:", echo=True)
    else:
        engine = create_engine("sqlite:///{}".format(args.database), echo=False)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    session = Session()

    output_directory = Path("./outputs")

    # Ensure the output directory exists
    output_directory.mkdir(parents=True, exist_ok=True)

    if not args.test:
        Online.generate_SchoolInformationFile(session, output_directory)
        Online.generate_StudentTeamInformationFile(session, output_directory)
        csvGenerator.generate_TeamImportData(session, output_directory)
        csvGenerator.generate_CoachImport(session, output_directory)
        Reports.generate_rosters(session, output_directory)
        csvGenerator.generate_StudentRooms(session, output_directory)
        Reports.generate_room_schedules(session, output_directory)
        Reports.generate_volunteer_list(session, output_directory)
        Reports.generate_totals(session)


if __name__ == "__main__":
    main()
