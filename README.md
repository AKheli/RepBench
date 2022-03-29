# Anomaly Clearning Benchmark Tool
Implements repair of anomalies with different data sets and injection scenarios


## Prerequisites
- The given bash script works for ubuntu 18 or 20 
- Clone this repository.

## Build
```bash
    $ sh install.sh
```
## Execution
```bash
$ python3 inject.py [arguments]
```
## Arguments


 | -data  | -a_type  | -scenario | -algo | 
 | -------- | -------- | -------- | -------- | 
 | stock10k.data     | amplitude_shift |"anomaly_size"| RPCA
 | SAGandStock    |distortion |  ts_length | SCREEN
 | BAFU20K.txt  | growth_change | ts_nbr |
 |            | point_outlier | base
 |            |  | all




### Remarks
- Data\
The data has to be in csv or txt  format.

The Results will be saved into the Results folder.
The data argument expects the data to be in the Data folder and the second argument
is the column starting at 0. ## todo


### Examples:
```bash
python3 run.py -scenario all  -col 0,1,2  -data batch10.txt -anom p -algo IMR
```

[comment]: <> (### Additional experimental run)

[comment]: <> (The file runc.py has an optional argument -cont where one can continue working on the same anomalies and -delete to delete an anomalie by index)

[comment]: <> (#### Example)

[comment]: <> (```bash)

[comment]: <> ($ python3 runc.py -data Data/stock10k.data -col 2 -cont)

[comment]: <> (-t a -l 10 )

[comment]: <> (-t d   )

[comment]: <> (-t g)

[comment]: <> (-an )

[comment]: <> (1 {'type': 'amplitude_shift', 'factor': 8, 'index_range': &#40;690, 699&#41;} )

[comment]: <> (2 {'type': 'distortion', 'factor': 8, 'index_range': &#40;11270, 11279&#41;} )

[comment]: <> (3 {'type': 'growth_change', 'factor': 8, 'index_range': &#40;5064, 5073&#41;} )

[comment]: <> (-delete 2 )

[comment]: <> (-an )

[comment]: <> (1 {'type': 'amplitude_shift', 'factor': 8, 'index_range': &#40;690, 699&#41;} )

[comment]: <> (3 {'type': 'growth_change', 'factor': 8, 'index_range': &#40;5064, 5073&#41;} )

[comment]: <> (-save continiousoutput)

[comment]: <> (exit)

[comment]: <> (```)


