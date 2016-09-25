# webminingOnpe

This repository contains the program *makeOnpeWebmining.py* which downloads the Peruvian election results by district for both first and second rounds into pandas.DataFrames and csvs. 


## Motivation

The Peruvian Electoral Agency published the results of the election online by district. They did not, however, provide a summarized data set for the general public. 

The website requires individuals to individually select from topdown menus the geografical region of interest. Selecting a particular area, updates the page but does not alter the URL. Thus the webmining was carried out by calling selenium through python which allows for a real time control of a Firefox web browser.  

## Main Files

| File   | Description |
|:-------|:------|
| [./makeOnpeWebmining.py][makePy]   |    Main script   |
| [./scripts/functions.py][funtions]    | Functions called by main script |
| [./data/output/results_round_one.csv][csvone]    |     Results of round one of elections |
| [./data/output/results_round_two.csv][csvtwo]    |     Results of round two of elections  |


## Usage

The results are saved in ./data/output/results_round_one.csv and ./data/output/results_round_two.csv. The program can by run with the following command line 

```sh
python3.5 makeOnpeWebmining.py
```	

[makePy]: https://github.com/AlejandroKantor/webminingOnpe/tree/master/makeOnpeWebmining.py
[funtions]: https://github.com/AlejandroKantor/webminingOnpe/tree/master/scripts/functions.py
[csvone]: https://github.com/AlejandroKantor/webminingOnpe/tree/master/data/output/results_round_one.csv
[csvtwo]: https://github.com/AlejandroKantor/webminingOnpe/tree/master/data/output/results_round_two.csv




