# Anomaly Repair Benchmark 
This benchmark implements five different anomaly repair techniques in time series and evaluates their precision and runtime on various real-world time series datasets using different repair scenarios.

- The benchmark implements the following algorithms: [IMR](https://www.vldb.org/pvldb/vol10/p1046-song.pdf), [SCREEN](https://dl.acm.org/doi/pdf/10.1145/2723372.2723730), Robust PCA and CDrep.
- All the datasets used in this benchmark can be found [here](https://github.com/althausLuca/RepairBenchmark/tree/master/Data).
- The full list of repair scenarios can be found [here](https://github.com/althausLuca/RepairBenchmark/blob/master/Scenarios/README.md).


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


 | -d  | -a  | -scen | -alg | 
 | -------- | -------- | -------- | -------- | 
 | bafu5k     | shift   |ts_len     | rpca
 | humidity   |distortion  |  a_size | screen
 | msd1_5     | outlier    | a_rate | imr
 | msd_hc     | all        | ts_nbr | cdrec
 |  elec      |            |  cts_nbr | all
 |   all      |             | all |      


### Data

- The data has to have a csv format.
- The data argument expects the Data to be in the Data folder.


### Results
All results and plots will be added to `Results` folder. The accuracy results of all algorithms will be sequentially added for each scenario and dataset to: `Results/.../.../error/`. The runtime results of all algorithms will be added to: `Results/.../.../runtime/`. The plots of the repaired blocks will be added to the folder `Results/.../precision/repair/`.


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

#### Parametrized Run
  By defining a toml file (see algox.toml) one can run the Benchmark on customized algorithms.
  The following example runs the SCREEN algorithm with different parameters saved as screen1 and screen2
  on the bafu5k data set:
```bash
python3 TestingFramework.py -scen ts_len -data bafu5k -anom all -algx example_file
```
example_file.toml:
```tom
 [screen.screen1]
    t = 1
    smin = -0.1
    smax  = 0.1


[screen.screen2]
     t = 1
     smin = -0.01
     smax  = 0.01
```
