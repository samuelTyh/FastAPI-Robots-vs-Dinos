# Robots vs Dinosaurs

This API service was built with Python 3.7, FastAPI and based on standard Python type hints. Aim to simulate the remote-controlled robots to fight the dinosaurs.  
The key features are:  
1. Flexible game grid: Create a game grid (default 50 by 50) with flexible dimensions (at least 2 by 2)
2. Quickstart 1 vs 1: Without specifying the positions on the grid of each role
3. Game grid display: Using a simple HTML table present the current state


[Navigate to project requirement](#features-required)

## Quickstart
[API document](https://robots-vs-dinos-e2rgcwogsq-ew.a.run.app/redoc)

### Run locally
* Prerequisites
    1. MacOS
    2. Python version: 3.7.4
    3. virtualenv
    4. GNU Make
```
#!/usr/bin/env bash

sudo apt install virtualenv
virtualenv -p python3 venv
source venv/bin/activate

cd /to/your/working/directory
make install  # install dependencies 
make start-local  # start fastapi service
```

###Run in docker container
```
#!/usr/bin/env bash

cd /to/your/working/directory

# Using Makefile
make init  # run docker compose and initialize the app
make logs  # inspect the logs in the container

# Or
docker-compose up -d --build
```

### Run testing
```
# Using Makefile
make test

# Or
python -m unittest discover tests
```

### TODO
1. interactive user interface


### Authors
* [@samuelTyh](https://samueltyh.github.io/#/)

---
## Features required

- [x] Be able to create an empty simulation space - an empty 50 x 50 grid;
    * Create a default 50 by 50 grid if not specifying the dimension
    
- [x] Be able to create a robot in a certain position and facing direction;
    * Create at least one robot with a specific or a random position and direction
    
- [x] Be able to create a dinosaur in a certain position;
    * Create at least one dinosaur with a specific or a random position
    
- [x] Issue instructions to a robot - a robot can turn left, turn right, move forward, move backward, and attack;
    * The robot can move forward or backward (move one step in the grid)
    * The robot can rotate to the right or left (change direction only)
    
- [x] A robot attack destroys dinosaurs around it (in front, to the left, to the right or behind);
    * Robots can defeat opponents from front, back, left and right
    
- [x] No need to worry about the dinosaurs - dinosaurs don't move;
- [x] Display the simulation's current state;
    * Get the response from every move, and use endpoint to display in html
- [x] Two or more entities (robots or dinosaurs) cannot occupy the same position;
    * Start checking mechanism during setting entities
- [x] Attempting to move a robot outside the simulation space is an invalid operation.
    * Start checking mechanism during moving entities