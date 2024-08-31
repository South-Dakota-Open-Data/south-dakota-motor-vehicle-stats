from datetime import date

import pdfplumber
import pandas as pd

pd.options.mode.chained_assignment = None


FILEPATH_REPORT_LINKS = 'report_links.csv'
REPORTS_DIR = 'reports'
FILEPATH_STUB = 'south-dakota-motor-vehicle-stats'
FILEPATH_OUT_CSV = f'{FILEPATH_STUB}.csv'

REQ_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0'
}

THIS_YEAR = date.today().year


def get_sd_fips_lookup():
    df = pd.read_csv(
        'https://raw.githubusercontent.com/cjwinchester/sd-voter-registration-data/main/us-county-fips.csv',
        dtype={
            'state_fips': str,
            'county_fips': str
        }
    )

    sd = df[df['state_abbr'] == 'SD']
    sd['fips'] = sd['state_fips'] + sd['county_fips']
    sd['county_name'] = sd['county_name'].str.replace(' County', '')

    return {x[1].get('county_name'): x[1].get('fips') for x in sd.iterrows()}


headers = [
    'county',
    'county_fips',
    'year',
    'passenger_low_speed',
    'pickup_suv_van',
    'truck',
    'bus',
    'trailer',
    'motorcycle',
    'off_road',
    'recreational',
    'snowmobile',
    'boat',
    'commercial_plate',
    'gross_vehicle_weight',
    'irp_with_prorate_plate',
    'electric',
    'titles'
]

lookup = get_sd_fips_lookup()


class Report:

    def __init__(self, filepath, fips_lookup=lookup):
        self.filepath = filepath
        self.year = filepath.split('.')[0].split('-')[-1]
        self.lookup = fips_lookup

    def extract_data(self):
        data = []

        with pdfplumber.open(self.filepath) as pdf:
            pages_data = pdf.pages[3:]
    
            for page in pages_data:
        
                words = page.extract_words()
        
                if words[0].get('text').lower() != 'titles':
                    continue
        
                county = [words[3].get('text')]

                for word in words[4:]:
                    if word.get('text').lower() == 'vehicle':
                        break
                    else:
                        county.append(word.get('text'))

                county = ' '.join(county)
                self.county = county

                county_fips = self.lookup.get(county, '')
                self.county_fips = county_fips

                table = page.extract_table()

                if self.year == 'historical':
                    for line in table:
                        line = [x for x in line if x]

                        if 'CY' not in line[0]:
                            continue

                        line = [int(x.replace('CY ', '').replace(',', '')) for x in line]

                        year = line[0]

                        # fix one line that's off
                        if county == 'Ziebach' and year == 2015:
                            line.insert(4, 0)
        
                        line_data = [county, county_fips] + line
                        data.append(dict(zip(headers, line_data)))
                else:
                    total_line = [x for x in table if x[0] == 'Total'][0]
                    total_line = [int(x.replace(',', '')) for x in total_line if x and x != 'Total']
        
                    page_data = [county, county_fips, self.year] + total_line
                    data.append(dict(zip(headers, page_data)))
    
        self.data = data
        self.df = pd.DataFrame(data)
        self.df_flat = pd.melt(
            self.df,
            id_vars=['county', 'county_fips', 'year'],
            var_name='registration_type',
            value_name='total'
        )

        return self.data

    def __str__(self):
        return f'{self.year}'
