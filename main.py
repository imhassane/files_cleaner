import enum
import os
import pathlib
import argparse
import datetime

class UnitOfTime(enum.Enum):
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    MONTH = "month"
    YEAR = "year"

    @staticmethod
    def is_valid(value):
        filtered = filter(
            lambda val: str.lower(val.name) == value, 
            [
                UnitOfTime.SECOND,
                UnitOfTime.MINUTE,
                UnitOfTime.HOUR,
                UnitOfTime.DAY,
                UnitOfTime.MINUTE,
                UnitOfTime.YEAR
            ]
        )

        return len(list(filtered)) > 0

class Cleaner:
    """
    Cleaner removes files that existed since a certain amount of time
    Parameters:
    ------------
    parser: ArgumentParser
        Parser to read the command line interface

    The parser requires the following parameters
    . --repertory : string The repertory to clean
    . --delay : number The amount of time from which a file has expired
    . --timeunit : second | minute | hour | day | month | year The unit of time of the delay
    . --target: creation | update Defines if the file timestamp to use is its creation time or update time 

    Usage:
    ----------
    python main.py --repertory RepertoryToClean --delay AmountOfTime --timeunit (second | minute | hour | day | month | year)  --target (update | creation)
    """
    def __init__(self, parser):
        parser.add_argument('--repertory', type=str, required=True)
        parser.add_argument('--delay', type=int, required=True)
        parser.add_argument('--timeunit', type=str, required=True)
        parser.add_argument('--target', type=str, required=False)

        print("""
        ..####...##......######...####...##..##..######..#####..
        .##..##..##......##......##..##..###.##..##......##..##.
        .##......##......####....######..##.###..####....#####..
        .##..##..##......##......##..##..##..##..##......##..##.
        ..####...######..######..##..##..##..##..######..##..##.
        ........................................................
        """)
        print("Step 1: Initialisation")
        self.args = parser.parse_args()
        self.delay = self.args.delay
        self.target = self.args.target if self.args.target is not None else "update"
        self.unit_of_time = str.strip(self.args.timeunit)
        self.repertory_to_clean = str.strip(self.args.repertory)

    def check(self):
        print("Step 2: Verification")

        if len(self.repertory_to_clean) == 0:
            raise ValueError("The repertory name is not valid")
        print("\t1. The repertory name is valid")

        if not UnitOfTime.is_valid(self.unit_of_time):
            raise ValueError("The unit of time is invalid, should be: second | minute | hour | day | month | year")
        print("\t2. The unit of time is valid")
        
        if self.delay == 0:
            raise ValueError("The delay must be greater than 0")
        print("\t3. The delay is valid")

        if not os.path.exists(self.repertory_to_clean):
            raise ValueError("The repertory does not exist")
        print("\t4. The repertory exists")

    def remove_files(self):
        print(str.format(
            "Step 3: Removing files existing for over {delay} {unit}{plural}",
            delay = self.delay,
            unit  = self.unit_of_time,
            plural = "s" if self.delay > 1 else ""
        ))
        nb_removed_files = 0

        for (dir, _, files) in os.walk(self.repertory_to_clean):
            for file in files:
                filename = r"" + dir + "/" + file
                filepath = pathlib.Path(filename)

                now = datetime.datetime.now()
                updated_date = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
                creation_date = datetime.datetime.fromtimestamp(os.path.getctime(filepath))

                target_date = updated_date if self.target == "update" else creation_date
                dates_difference = now - target_date
                delta_seconds = dates_difference.total_seconds()
                units = {
                    "second": delta_seconds,
                    "minute": int(delta_seconds / 60),
                    "hour": int(delta_seconds / 3600),
                    "day": int(delta_seconds / (3600 * 24)),
                    "month": int(delta_seconds / (3600 * 24 * 30)),
                    "year": int(delta_seconds / (3600 * 24 * 30 * 12))
                }

                if units[self.unit_of_time] > self.delay:
                    print(str.format(
                        "\t\tRemoving {filename} \t (last {target} time = {delay} {unit}{plural})",
                        filename = filename,
                        target = self.target,
                        delay = units[self.unit_of_time],
                        unit = self.unit_of_time,
                        plural = "s" if units[self.unit_of_time] > 1 else ""
                    ))

                    try:
                        os.remove(filepath)
                        nb_removed_files += 1
                    except:
                        print(str.format("\t\t\tError: {0} has not been removed", filename))
                    

        print(str.format("\t{0} file{1} removed", nb_removed_files, "s" if nb_removed_files > 1 else ""))

def run():
    parser = argparse.ArgumentParser()
    cleaner = Cleaner(parser)

    try:
        cleaner.check()
        cleaner.remove_files()
    except ValueError as error:
        print(str.format("Error: {0}", error))

if __name__ == "__main__":
    run()