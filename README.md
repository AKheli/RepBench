# Anomaly Clearning Benchmark Tool
Implements repair of anomalies with different data.

- The Benchmark implements the follwing algorithms (in Python): SCREEN , IMR , CDrepair amd RobustPCA,
- All aviable datasets can befound [here](Data/).
- The list of different scenarios can be found here [here](Scenarios/README.md).

## Prerequisites
- The given bash script works for ubuntu 18 or 20 
- Clone this repository.

## Build
- build Testing Benchmark 
```bash
    $ sh install.sh
```
## Execution
```bash
$ python3 TestingFramework.py [arguments]
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

```bashs
python3 TestingFramework.py -scen ts_nbr -data bafu5k -anom shift -alg cdrec
```
 <li>
Run two algorithms (cdrec, rpca) on two dataset (bafu5k,msd) using one scenario (a_rate) and two anomalies (shift,outlier)
</li>

```bash
python3 TestingFramework.py -scen ts_nbr -data bafu5k,msd -anom shift,outlier -alg cdrec,rpca
```
 <li>
Run the whole benchmark: all the algorithms , all the dataset on all scenarios with all anomalies
</li>

```bash
python3 TestingFramework.py -scen all -data all -anom all -alg all
```

</ol>


#### Parametrized Run
  By defining a toml file (see algox.toml) one can run the Benchmark with different Parameters 
  with named algorithms.
 
  The following example runs the SCREEN algorithm algorithm with different parameters on the bafu5k data set:
```bash
python3 TestingFramework.py -scen ts_len -data bafu5k -anom all -algx algox
```
algox.toml:
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