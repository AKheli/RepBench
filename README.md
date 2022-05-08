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
$ python3 run.py [arguments]
```
## Arguments


 | -d  | -a  | -scen | -algo | 
 | -------- | -------- | -------- | -------- | 
 | bafu5k     | shift |ts_len| rpca
 | humidity    |distortion |  a_size | scree
 | msd1_5          | growth | a_rate | imr
 | msd_hc     | outlier | ts_nbr | cdrec
 | all       |all  | cts_nbr | all
 |            |  | all | 



### Remarks
- Data\
The data has to be in csv  format.
The Results will be saved into the Results folder.
The data argument expects the Data to be in the Data folder.


### Examples:
<ol>
  <li>
 Run a single algorithm (cdrec) on a single dataset (bafu5k) using one scenario (number of time series) and one anomaly (shift)
</li>

```bash
python3 run.py -scen ts_nbr -data bafu5k -anom shift -alg cdrec
```
 <li>
Run two algorithms (cdrec, rpca) on two dataset (bafu5k,msd) using one scenario (a_rate) and two anomalies (shift,outlier)
</li>

```bash
python3 run.py -scen ts_nbr -data bafu5k,msd -anom shift,outlier -alg cdrec,rpca
```
 <li>
Run the whole benchmark: all the algorithms , all the dataset on all scenarios with all anomalies
</li>

```bash
python3 run.py -scen all -data all -anom all -alg all
```

</ol>

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


