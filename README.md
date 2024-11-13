# Artificial Intelligence in Videogames Final Project

## Introduction

Game in Python using Pygame library.
Mario Bros game with AI implemented using dijkstra algorithm and state machine.

## Installation

To install the project, you need to have Python 3.x

We recommend using a virtual environment to install the project.

```bash
python3 -m venv venv
source venv/bin/activate
```

Then, you need to install the dependencies.

```bash
pip install -r requirements.txt
```

> [!NOTE]\
> We use pygame library, it needs SDL2 library to be installed.
> MacOS: `brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf`
> Ubuntu: `sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev`
> Windows: Download and install the SDL2 development libraries from the [SDL2 website](https://www.libsdl.org/download-2.0.php). Make sure to follow the instructions for setting up the environment variables.

## Usage

To run the game, you need to execute the following command.

```bash
python3 src/main.py
```

## Testing

To run the tests, you need to execute the following command.

```bash
# todo
```

## Documentation

The documentation of the game is available in `gdd` folder.

It contains the following information:

| Description                            | Implemented |
| -------------------------------------- | ----------- |
| Main characters                        |             |
| Enemies                                |             |
| Scene’s description                    |             |
| The game mechanics or mechanics        |             |
| The algorithms used in the game        |             |
| In game images                         |             |
| Conclusion of each of the team members |             |

## Rubric

| Description                                                                    | Not implemented | Implementation has bugs | Correctly implemented |
| ------------------------------------------------------------------------------ | --------------- | ----------------------- | --------------------- |
| Start game menu                                                                |                 |                         |                       |
| Screen with game instructions                                                  |                 |                         |                       |
| Game credits                                                                   |                 |                         |                       |
| Transitions between game scenes and screens are seamless                       |                 |                         |                       |
| First algorithm implementation                                                 |                 |                         |                       |
| Second algorithm implementation                                                |                 |                         |                       |
| The game starts when the start option is selected in main menu                 |                 |                         |                       |
| In case of having more than one scene, the transition between them is seamless |                 |                         |                       |
| The game ends when the objectives are met                                      |                 |                         |                       |
| When the game ends, it returns to main menu                                    |                 |                         |                       |
