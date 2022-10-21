# generate-ham-radio-exams
```
usage: generate_exam.py [-h] -i INPUT -o OUTPUT -c {T,G,AE} [-k]

Converts JSON question pools into exams, which can be optionally exported to .xlsx

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Filename of question pool to be inported
  -o OUTPUT, --output OUTPUT
                        Directs the JSON to a name of your choice
  -c {T,G,AE}, --class {T,G,AE}
                        Dictate exam class (i.e. Technician, General, Amateur Extra)
  -k, --kahoot          Export to .xlsx to import into Kahoot!
  ```
