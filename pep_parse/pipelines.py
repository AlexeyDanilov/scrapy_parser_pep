import csv
from collections import Counter
import datetime as dt

from pep_parse.settings import BASE_DIR

TIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:
    def open_spider(self, spider):
        self.storage = list()

    def process_item(self, item, spider):
        self.storage.append(item.get('status'))
        return item

    def close_spider(self, spider):
        result = Counter(self.storage)
        time = dt.datetime.now().strftime(TIME_FORMAT)
        file_dir = f'{BASE_DIR}/results'
        filename = 'status_summary_{}.csv'.format(time)
        file_path = f'{file_dir}/{filename}'
        file = csv.writer(open(file_path, 'w'))
        file.writerow(['Статус', 'Количество'])
        result['Total'] = sum(result.values())
        file.writerows(result.items())
