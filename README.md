## NY Employee Public Salaries

Data from 2008--2017 on Cities, Counties, New York City, Public Authorities,  Schools, Special Districts, State - Executive, State - Judicial, State - Legislative, Towns, and Villages.

The python script [new_york_salaries.py](new_york_salaries.py) iterates through the search results (n = 14,789,448 results) from http://seethroughny.net/payrolls/ and downloads a series of branch-year level CSVs to year folders. Each of the CSVs has the following columns: `name, employer_agency, total_pay, subagency_type, title, rate_of_pay, year, pay_basis, branch`.

### Running the Python script
```
pip install -r requirements.txt
python new_york_salaries.py
```

[ny.R](ny.R) merges the files within each of the yearly folders and produces yearly csvs.
