# Maximum Common Edge Subgraph Implementation

This repository hosts our implementation of the research paper The Maximum Common Edge Subgraph Problem: A Polyhedral Investigation by Bahiense et al., as our group course project for Combinatorial Optimization at Rice University, Fall 2024. The project is conducted under the instruction of Dr. Illya V. Hicks.

## Group Members
- Gonzalo Gomez Abejon
- Saber Dinpazhouh
- Boris Shapoval
- Noah Lichtenberg

## Repository Contents

- `marenco_formulation.py`: Implements the first integer programming (IP) formulation discussed in the paper, referred to as the previous polyhedral study, section 2.
- `brazil_formulation.py`: Implements the second integer programming (IP) formulation discussed in the paper, referred to as the new IP formulation, section 3.
- `tester.py`: A utility script designed to test the two formulations with various options.
- `instances/`: Contains two sets of test cases:
  - `Marenco/`: Benchmark test cases used in the paper.
  - `Isomorphic/`: Test cases we generated to solve the graph isomorphism problem using the MCES framework.

## How to Run the Code
- To run all test cases, execute `tester.py`.
- To explore the project with examples, see the scripts `marenco_formulation.py` and `brazil_formulation.py`.
