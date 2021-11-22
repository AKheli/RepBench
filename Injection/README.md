# Anomaly injection for Time Series  
Support multiple injections of amplitude shift, distortion , growth change and extreme values of a single data column containing numerical values.


## Prerequisites
- The given bash script works for ubuntu 18 or 20 
- Clone this repository.

## Build
```bash
    $ sh install.sh
```
##E xecution
```bash
$ python3 inject.py [arguments]
```
## Arguments

 | -data  | -type   
 | -------- | -------- | 
 | stock10k.data 2    | amplitude_shift |
 | SAGandStock  2  |distortion |  
 |   | growth_change |
 |   | extreme |   
 




### Remarks
- Data\
The data has to be in csv style format. To specify a different separator use:
-sep  "separator"

The file will be saved into the Data/generated folder.
The data argument expects the data to be in the Data folder and the second argument
is the column starting at 0.
- Parameters\
The Parameter file specifies the default anomaly parameters.
For your own parameters modify the file or use:
-typex anomalies your_parameter_file.

- Arguments\
All the arguments try to match if only the beginning is given e.g.,  **a** insteaf of **amplitude_shift**.
One can use multiple anomalies at once e.g., -type a,a,d,d

- Plot and Save commands\
-withoutlegend\
-save filename\
-anomalydetails\
-plotoff
### Examples:
```bash
$ python3 inject.py -data stock10k.data 2 -type  amplitude_shift,distortion -anomalydetails

$ python3 inject.py -data stock10k.data 2 -type a,d 

$ python3 inject.py -data stock10k.data 2 -type a -save output 

$ python3 inject.py -data SAGandStock  2  -save "2shifts" -typex a,a Parameters -plotoff

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


