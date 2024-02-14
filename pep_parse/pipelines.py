import csv
from collections import defaultdict
import datetime as dt
from pathlib import Path

from pep_parse.settings import BASE_DIR

TIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
FILE_DIR = 'results'
FILE_NAME = 'status_summary_{}.csv'


class PepParsePipeline:
    def open_spider(self, spider):
        self.storage = defaultdict(int)

    def process_item(self, item, spider):
        self.storage[item.get('status')] += 1
        return item

    def close_spider(self, spider):
        time = dt.datetime.now().strftime(TIME_FORMAT)
        file_dir_path = Path(BASE_DIR, FILE_DIR)
        filename = FILE_NAME.format(time)
        file_path = Path(file_dir_path, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            data = (
                ('Статус', 'Количество'),
                *self.storage.items(),
                ('Total', sum(self.storage.values()))
            )
            writer.writerows(data)
