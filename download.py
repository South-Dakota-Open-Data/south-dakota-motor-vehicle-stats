import os
import csv
import time

import requests

from report import (
    FILEPATH_REPORT_LINKS,
    REQ_HEADERS,
    FILEPATH_STUB,
    THIS_YEAR,
    REPORTS_DIR
)


def download_reports():

    with open(FILEPATH_REPORT_LINKS, 'r') as infile:
        reader = csv.DictReader(infile)
        reports = {x.get('year'): x.get('url') for x in list(reader)}

    for year in reports:
        url = reports[year]

        filepath = os.path.join(
            REPORTS_DIR,
            f'{FILEPATH_STUB}-{year}.pdf'
        )

        try:
            year = int(year)
        except ValueError:
            pass

        if os.path.exists(filepath) and year != THIS_YEAR:
            continue

        with requests.get(
            url,
            headers=REQ_HEADERS,
            stream=True
        ) as r:
            r.raise_for_status()
            time.sleep(1)
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)

            print(f'Wrote {filepath}')


if __name__ == '__main__':
    download_reports()
