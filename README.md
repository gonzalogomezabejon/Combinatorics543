This repository hosts the code associated with the research paper available [here](https://www.sciencedirect.com/science/article/pii/S0166218X12000340#:~:text=In%20the%20Maximum%20Common%20Edge,(1981)%20%5B2%5D).

## Repository Contents

- `marenco_formulation.py`: This script implements the first integer programming (IP) formulation discussed in the paper.
- `brazil_formulation.py`: This script implements the second integer programming (IP) formulation discussed in the paper.
- `tester.py`: A utility script designed to test the two formulations with various options.
- `instances/`: This directory contains two sets of test cases:
  - `Marenco/`: Contains the benchmark test cases used in the paper.
  - `Isomorphic/`: Contains test cases that we generated to address the graph isomorphism problem using the MCES framework.
