import os
from datetime import date

import pandas as pd

from report import (
    Report,
    FILEPATH_STUB,
    FILEPATH_OUT_CSV,
    THIS_YEAR,
    REPORTS_DIR
)


def combine(years=[THIS_YEAR]):
    years.append('historical')

    df = pd.DataFrame()

    for year in years:
        filepath = os.path.join(
            REPORTS_DIR,
            f'{FILEPATH_STUB}-{year}.pdf'
        )

        report = Report(filepath)
        report.extract_data()
        df = pd.concat([df, report.df_flat])

    df.sort_values(
        ['county', 'year', 'registration_type'],
        ascending=[True, False, True],
        inplace=True
    )

    df.drop_duplicates(inplace=True)

    df.to_csv(
        FILEPATH_OUT_CSV,
        index=False
    )

    print(f'Wrote {FILEPATH_OUT_CSV}')

    return df


if __name__ == '__main__':
    combine()
