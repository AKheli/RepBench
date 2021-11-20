# Anomaly injection for Time Series  

## Prerequisites
To run the programm you need Python with pandas and matplotlib installed

- For ubuntu 18 or 20
- Clone this repository.
- in the folder run : 


## Execution
```bash
    $ cd my_injcetion
    $ python terminal.py [arguments]
```

## data Arguments
-data  yourdatapath 
### optional arguments 
-datacol  default: 0 has to be an index \
-seperator default: ","

### repeated Arguments
-type [amplitude_shift 
distortion ,
growth_change ,
extreme  ]


####folloed by optional arguments
-lenght int anomalyLength\
-factor int anomalyfactor\
-n int  anomalyRepetitions

When the first data row only contains numerical arguments There is assumed to be no header
###plotting and saving arguments:
-plot\
-legendoff\
-save filename  

### Examples:


$python .\terminal.py -d .\Data\stock10k.data -col 2 -type a -n 12 -l 100 -sa out -t d -n 3  -l 200 -plot -t g -n 4
