# Timeseries Repair evaluation Tool

## Execution


## Build

- Build the Testing Framework using the installation script located in the root folder 

```bash
    $ sh install.sh
```



```bash
    $ cd Repair
    $ python3 TestingFramework.exe [arguments]
```

### Arguments

 | -alg  | -d  | 
 | -------- | -------- | 
 | imr    | BAFU        |  
 | scree  | YAHOO        |  
 |       | Humidity    |

 

[comment]: <> (### Results)

[comment]: <> (All results and plots will be added to `Results` folder. The accuracy results of all algorithms will be sequentially added for each scenario and dataset to: `Results/.../.../error/`. The runtime results of all algorithms will be added to: `Results/.../.../runtime/`. The plots of the recovered blocks will be added to the folder `Results/.../.../recovery/plots/`.)


### Examples
1. run imr onr the YAHOO dataset
```bash

python3 repair.py  -d YAHOO -algo imr

```
2. run IMR and SCREEN on the YAHOO and Humidity dataset
```bash
 python3 repair.py  -d YAHOO,Humidity -algo imr,screen
```

3. Multiple Parametrization run using the -algox command 
  on the data file multpile algos: \
! imr p tau k \
1 0.1  100000 \
2 0.1  100000 \
3 0.1  100000 \
5 0.1  100000 \
\
! screen t s \
1 2 \
2 1 \
1 1 \

```
```bash
python3 repair.py  -d YAHOO,Humidity -algox multiple_algos
```