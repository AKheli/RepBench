# Timeseries Repair evaluation Tool

## Execution
## Build

- Build the Testing Framework using the installation script located in the root folder 

```bash
    $ sh install.sh
```

```bash
    $ cd Repair
    $ python3 repair.py [arguments]
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
1. run imr on the YAHOO dataset
```bash

python3 repair.py  -d YAHOO -algo imr

```
2. run IMR and SCREEN on the YAHOO and Humidity dataset
```bash
 python3 repair.py  -d YAHOO,Humidity -algo imr,screen
```

3. Multiple Parametrization run using the -algox command 
 using the algorithms defined in the file multpile_algos: \

```bash
python3 repair.py  -d YAHOO,Humidity -algox multiple_algos
```