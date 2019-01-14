# WCET_Generator
Generate WCET for ALF Statements based on SWEET Tool.

## Method
- details see SWEET manual 4.14.

## Requirement
- Python (version 3+).
- SWEET.

## File Resource
- clt : insertsort.clt provided by SWEET manual.
- std_hll.alf: for 64bit (see SWEET manual)
  - get 32bit std_hll.alf in SWEET manual.

## How To Use：
> ./wctg [.alf]

Remember to give "wctg" permission to execute. 
> chmod a+x wctg

- The alf slices folder and wcet time table(.wct) will be generated in folder where your alf file imported.
- unspported:
    - Some Statements like "dyn_alloc" are not supported yet.



## WCET_Generator V2.3

- Fix Bugs.
- Add rules according to ALF paper.

## WCET_Generator V2.2

- Fix Calculation of Call.

## WCET_Generator V2.1

- unspported: Call.
