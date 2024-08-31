# South Dakota motor vehicle stats
Creating [a tidy CSV](south-dakota-motor-vehicle-stats.csv) of [motor vehicle registration stats](https://sddor.seamlessdocs.com/sc/statistics/) in South Dakota by county by year.

PDF reports for each calendar year, [downloaded](download.py) from the Department of Revenue's website, are in `reports`, along with [a historical file](south-dakota-motor-vehicle-stats-historical.pdf) with annual totals for the past couple years for each county.

To combine them, the basic idea is, pull out annual totals from the historical file and then add data from the reports not represented in that file.

### File layout

[`south-dakota-motor-vehicle-stats.csv`](south-dakota-motor-vehicle-stats.csv):
- `county`: County name
- `county_fips`: County FIPS code
- `year`: Registration year
- `registration_type`: The type of registration, e.g. truck, bus, etc. (but also "title")
- `total`: The total number of registrations of that type for the county for the year

### Running the Python scripts

`download.py` checks for new reports (listed in `report_links.csv`) and downloads new ones and the current-year report, which is updated throughout the year with new monthly totals.

`extract_and_combine.py` extracts the data from each PDF and combines them into a flat file, [`south-dakota-motor-vehicle-stats.csv`](south-dakota-motor-vehicle-stats.csv).
