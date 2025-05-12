# A* Pathfinding Algorithm Visualizer

A Python implementation of the A* pathfinding algorithm with an interactive, resizable visualization interface using Pygame.

## Features

-  Interactive grid with start, end, and barrier placement
-  Multiple heuristic options (Manhattan, Euclidean, Chebyshev)
- ↔ Toggle diagonal movement
-  Resizable window with dynamic grid scaling
-  Real-time algorithm visualization
-  Color-coded nodes for different states

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/astar-pathfinding.git
   cd astar-pathfinding
   Controls
Action	Mouse/Key
Place Start Node	Left Click (1st)
Place End Node	Left Click (2nd)
Place Barriers	Left Click (subsequent)
Remove Nodes	Right Click
Start Pathfinding	SPACE
Clear Grid	C
Toggle Diagonal Move	D
Change Heuristic	H
Resize Window	Drag window edges
Heuristics
Manhattan: |x1-x2| + |y1-y2| (default)

Euclidean: Straight-line distance

Chebyshev: max(|x1-x2|, |y1-y2|)
