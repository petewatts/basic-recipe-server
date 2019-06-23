import csv
import re


re_datetime = re.compile(r'^(\d\d)/(\d\d)/(\d{4}) (\d\d):(\d\d):(\d\d)$')


class RecipeDAO(object):
    """
    Provides access to the recipe data.
    """

    def __init__(self):
        self.last_id = 0
        self.recipes = {}

    def import_file(self, data_file):
        with open(data_file) as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            headers = None
            count = 0
            for row in reader:
                count += 1
                if headers is None:
                    headers = row
                    continue
                data = dict(zip(headers, row))

                if not str.isdigit(data["id"]):
                    raise Exception(f"Data row {count} has an invalid 'id' field")

                def convert_field(k, v):
                    # Convert field to something sane
                    datetime_match = re_datetime.match(v)
                    if len(v) == 0:
                        return None
                    elif str.isdigit(v):
                        return int(v)
                    elif datetime_match:
                        day, month, year, hour, min, sec = datetime_match.groups()
                        v = f'{year}-{month}-{day}T{hour}:{min}:{sec}Z'
                    return v

                data = {k: convert_field(k, v) for k, v in data.items()}

                self.recipes[data["id"]] = data
                # Update the last id
                if data["id"] > self.last_id:
                    self.last_id = data["id"]

    def get(self, id):
        return self.recipes.get(id)
