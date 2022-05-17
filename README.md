# Anomaly Repair Benchmark Tool
This benchmark implements five different anomaly repair techniques in time series and evaluates their precision and runtime on various real-world time series datasets using different repair scenarios.

- The benchmark implements the following algorithms
- All the datasets used in this benchmark can be found [here](https://github.com/althausLuca/RepairBenchmark/tree/master/Data).
- The full list of recovery scenarios can be found [here](https://github.com/eXascaleInfolab/bench-vldb20/blob/master/TestingFramework/README.md).


[**Prerequisites**](#prerequisites) | [**Build**](#build) | [**Execution**](#execution) 


___

## Prerequisites
- Ubuntu 16 or Ubuntu 18 (including Ubuntu derivatives, e.g., Xubuntu).
- Clone this repository.

___

## Build
```bash
    $ sh install.sh
```
___
## Execution
```bash
$ python3 TestingFramework.py [arguments]
```
### Arguments


 | -d  | -a  | -scen | -algo | 
 | -------- | -------- | -------- | -------- | 
 | bafu5k     | shift |ts_len| rpca
 | humidity    |distortion |  a_size | scree
 | msd1_5          | growth | a_rate | imr
 | msd_hc     | outlier | ts_nbr | cdrec
 | all       |all  | cts_nbr | all
 |            |  | all | 

### Data

- The data has to be in csv  format.
- The data argument expects the Data to be in the Data folder.


### Results
All results and plots will be added to `Results` folder. The accuracy results of all algorithms will be sequentially added for each scenario and dataset to: `Results/.../.../error/`. The runtime results of all algorithms will be added to: `Results/.../.../runtime/`. The plots of the repaired blocks will be added to the folder `Results/.../.../recovery/plots/`.





### Examples
1.  Run a single algorithm (cdrec) on a single dataset (bafu5k) using one scenario (number of time series) and one anomaly (shift)

```bash
python3 TestingFramework.py -scen ts_nbr -data bafu5k -anom shift -alg cdrec
```
2. Run two algorithms (cdrec, rpca) on two dataset (bafu5k,msd) using one scenario (a_rate) and two anomalies (shift,outlier)

```bash
python3 TestingFramework.py -scen ts_nbr -data bafu5k,msd -anom shift,outlier -alg cdrec,rpca
```
 3. Run the whole benchmark: all the algorithms , all the dataset on all scenarios with all anomalies

```bash
python3 TestingFramework.py -scen all -data all -anom all -alg all
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


