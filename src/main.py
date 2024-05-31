""" Main executable for bodyBinder """

from backend import *
from frontend import *


def main():
    print(f'explorer /select,"{os.path.join(os.getcwd(), "data\output", "output.json")}"')
    print('explorer /select,"C:\\Users\BOULETG\PycharmProjects\BodyBinder\data\output\output.json"')
    MainApp()


if __name__ == "__main__":
    main()
    save_progress()