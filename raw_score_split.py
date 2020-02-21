import csv
from functools import total_ordering

@total_ordering
class Score():
    def __init__(self, csv_list):
        """
        Initialize Score object from raw score CSV line
        @param csv_list list object from csv.reader
        """
        self.row = csv_list
        self.student_id = csv_list[1]

        # Fix up the names of the subjective events
        if self.row[0] == '7':
            self.row[0] = 'Essay'
        elif self.row[0] == '8':
            self.row[0] = 'Speech'
        elif self.row[0] == '9':
            self.row[0] = 'Interview'

    def __lt__(self, other):
        if self.student_id == other.student_id:
            return self.row[0] < other.row[0]
        else:
            return self.student_id < other.student_id

    def __eq__(self, other):
        return ( self.student_id == other.student_id ) and (self.row[0] == self.row[0])

    def __repr__(self):
        return "<Score("+self.row+")>"

    def school(self):
        """
        Derive the school ID from the student ID
        @return School ID String
        """
        # Strip off the last two digits of the student ID to obtain the school ID
        school_id_len = len(self.student_id) - 2

        return self.student_id[0:school_id_len]


def main():
    school_list = dict()

    file_list = {'EssayScore.csv',
                 'InterviewScore.csv',
                 'ObjectiveScore.csv',
                 'SpeechScore.csv'}

    for file_name in file_list:
        with open(file_name, 'rb') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                score = Score(row)
                if score.school() not in school_list:
                    school_list[score.school()] = list()

                school_list[score.school()].append(score)

    for key, value in school_list.iteritems():
        output_filename = "{0}.csv".format(key)
        print("Writing {0}".format(output_filename))
        with open(output_filename, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
            for score in sorted(value):
                # print score.row()
                csvwriter.writerow(score.row)


if __name__ == "__main__":
    main()
