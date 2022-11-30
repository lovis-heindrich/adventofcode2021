from pathlib import Path
import argparse
import datetime
import webbrowser
from urllib.request import Request, urlopen

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", type=int, default=None)
    parser.add_argument("-d", "--day", type=int, default=None)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    date = datetime.date.today()
    year, day = date.year, date.day
    if args.year is not None:
        assert args.year >= 2015 and args.year <= year
        year = args.year
    if args.day is not None:
        assert args.day >= 1 and args.day <= 25
        day = args.day

    # Leading 0 for dates before 10th
    local_day = str(day) if day >= 10 else "0"+str(day)
    Path(f"./{year}/{local_day}").mkdir(parents=True, exist_ok=True)
    print(f"Setting up day {day} of year {year}")

    # Download input if needed
    input_path = Path(f"./{year}/{local_day}/input.txt")
    if not input_path.is_file():
        with open('session_cookie.txt', 'r') as file:
            cookie_value = file.read().strip()
            request = Request(f'https://adventofcode.com/{year}/day/{day}/input')
            request.add_header("cookie", f"session={cookie_value}")
            contents = urlopen(request).readlines()
        with open(input_path, 'wb') as f:
            f.writelines(contents)
        print("Downloaded and saved input")
    else:
        print("Input already downloaded")

    code_path = Path(f"./{year}/{local_day}/main.py")
    code_content = f"""if __name__ == "__main__":
    with open("input.txt") as f:
        input = [row for row in f.read().splitlines()]
    """

    # Create code file if needed
    if not code_path.is_file():
        with open(code_path, 'w') as f:
            f.write(code_content)
        print("Created python file")
    else:
        print("Python file already exists")

    # Open in browser
    print("Opening problem description")
    webbrowser.open(f'https://adventofcode.com/{year}/day/{day}')