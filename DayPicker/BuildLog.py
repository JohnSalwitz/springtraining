__author__ = 'JSalwitz'


import sys
import BuildLog

# ansi colors...
class ansi:

    ESC = '\033['
    CLEAR = '\033[m'

    TEXT_PLAIN = '0'
    TEXT_BOLD = '1'

    FOREGROUND_BLACK = '30'
    FOREGROUND_RED = '31'
    FOREGROUND_BLUE = '34'
    FOREGROUND_MAGENTA = '35'

    BACKGROUND_WHITE = ''
    BACKGROUND_BLACK = '40'
    BACKGROUND_RED = '41'
    BACKGROUND_CYAN = '46'


    def mode_string(self, text_attribute, foreground, background):
        return self.ESC + text_attribute + ';' + foreground + ';' + background + 'm'

    def clear_string(self):
        return self.mode_string(self.TEXT_PLAIN, self.FOREGROUND_BLACK, self.BACKGROUND_WHITE)



#
# Formats the build log output
#
def header(title):
    a = ansi()
    print("")
    print(a.mode_string(a.TEXT_BOLD, a.FOREGROUND_BLACK, a.BACKGROUND_WHITE) + title.upper() + ansi.CLEAR)
    sys.stdout.flush()

# creates a build step header (which is parsed in jenkins console reader)
def step(name):
    a = ansi()

    name = name.upper()
    print("")
    print("")

    print("-------------------------------------------------------------------------------------------------")
    print(a.mode_string(a.TEXT_BOLD, a.FOREGROUND_BLACK, a.BACKGROUND_CYAN) + "--> %s... " % name + a.CLEAR)
    print("-------------------------------------------------------------------------------------------------")
    sys.stdout.flush()

def info(contents):
    print("\t\t" + contents)
    sys.stdout.flush()

def warning(contents):
    a = ansi()
    print(a.mode_string(a.TEXT_BOLD, a.FOREGROUND_MAGENTA, a.BACKGROUND_WHITE) + "\t\tWARNING: " + contents + ansi.CLEAR)
    sys.stdout.flush()


def error(contents):
    a = ansi()
    print(a.mode_string(a.TEXT_BOLD, a.FOREGROUND_RED, a.BACKGROUND_WHITE) + "\t\tERROR: " + contents + ansi.CLEAR)
    sys.stdout.flush()

def trailer(message = None):
    print("=================================================================================================")
    print("")
    print("")
    print("")
    sys.stdout.flush()

