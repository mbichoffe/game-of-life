# Conway's Game of Life with PyScript and D3.js

#### [Hosted on GitHub Pages](https://mbichoffe.github.io/game-of-life/)


### Introduction

The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead (or populated and unpopulated, respectively). 
Every cell interacts with its eight neighbors, which are the cells that are horizontally, vertically, or diagonally adjacent. 
![Moore Neighborhood With Cardinal Directions](src/images/440px-Moore_neighborhood_with_cardinal_directions.svg.png)

At each step in time, the following transitions occur:

    Any live cell with fewer than two live neighbors dies, as if by underpopulation.
    Any live cell with two or three live neighbors lives on to the next generation.
    Any live cell with more than three live neighbors dies, as if by overpopulation.
    Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules simultaneously to every cell in the seed, live or dead; births and deaths occur simultaneously.

Each generation is a pure function of the preceding one. The rules continue to be applied repeatedly to create further generations. 

The simultaneity means that when each cell counts the number of live neighbors around it, it uses its neighbors' old states before the update, not their new states after the update.


### Development Setup
PyScript does not require any development environment other than a web browser (it is only tested in Chrome as of this writing) and a text editor.

### Installation

There is no installation required.


### Sources:
* https://docs.pyscript.net/latest/
* https://d3js.org/
* https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
* https://playgameoflife.com/info
* https://mathworld.wolfram.com/CellularAutomaton.html
* https://plato.stanford.edu/entries/cellular-automata/

### Notes

This is a small side project, and it's a WIP full of quirks and issues.
Additionally, Pyscript is currently in alpha, so there's a possibility that this project might break in the future.

Feel free to fork the repository and make it your own. If you do use or build upon this project, a mention would be greatly appreciated.
