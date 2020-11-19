# Coding Challenge - Robots vs Dinosaurs

Grover is assembling an army of remote-controlled robots to fight the dinosaurs and the first step towards that is to run simulations on how they will perform. You are tasked with implementing a service that provides a REST API to support those simulations.

[Navigate to Quickstart](#quickstart)

## These are the features required:

- [x] Be able to create an empty simulation space - an empty 50 x 50 grid;
    * Create a default 50 by 50 grid if not specifying the dimension
    
- [x] Be able to create a robot in a certain position and facing direction;
    * Create at least one robot with specified position and direction or not
    
- [x] Be able to create a dinosaur in a certain position;
    * Create at least one dinosaur with specified position or not
    
- [x] Issue instructions to a robot - a robot can turn left, turn right, move forward, move backward, and attack;
    * The robot can move forward or backward (move one step in the grid)
    * The robot can rotate to the right or left (change direction only)
    
- [x] A robot attack destroys dinosaurs around it (in front, to the left, to the right or behind);
    * Robots can defeat opponents from front, back, left and right
    
- [x] No need to worry about the dinosaurs - dinosaurs don't move;
- [x] Display the simulation's current state;
- [x] Two or more entities (robots or dinosaurs) cannot occupy the same position;
- [x] Attempting to move a robot outside the simulation space is an invalid operation.

## Things we are looking for

- [x] Immutability/Referential transparency;
- [x] Idiomatic code;
- [x] Adherence to community/standard library style guides;
- [x] Separation of concerns;
- [x] Unit and integration tests;
- [x] API design;
- [x] Domain modeling;
- [x] Attention to possible concurrency issues;
- [x] Error handling.


---

##Quickstart
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
1. http error handling
2. interactive user interface


### Authors
* [@samuelTyh](https://samueltyh.github.io/#/)