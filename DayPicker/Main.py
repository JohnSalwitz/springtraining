__author__ = 'JSalwitz'

import argparse, os, sys
from BuildLog import *
from TextToList import *
from CreateHTML import *

def listdir_full_path(folder):
    return [os.path.join(folder, fn) for fn in os.listdir(folder)]

def latest_file(folder, extension):
    files = listdir_full_path(folder)
    return max(files)


def main():
    exit_code = 0
    try:
        parser = argparse.ArgumentParser(description="Identifies the best days to go to spring training")
        parser.add_argument('schedule_folder', help='Location of schedule files')
        parser.add_argument('report_folder', help='Location of report files')
        args = parser.parse_args()

        # get most recent history file...
        source_file = latest_file(args.schedule_folder, '.txt')

        BuildLog.header("Finding Best Spring Training Days")

        BuildLog.step("Parsing "+ source_file)

        schedule_list = text_file_to_list(source_file)
        schedule, days = schedule_parser(schedule_list)
        schedule, agenda = score_schedule(schedule, days, 4)

        print_to_html(source_file, args.report_folder, schedule, agenda)


    except BaseException as error:
        print('An exception occurred: {}'.format(error))

    except:
        exit_code = 1

    finally:
        sys.exit(exit_code)

if __name__ == "__main__":
    main()
