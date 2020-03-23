# Legendary Aim Assist

This project is an academic exercise in creating a utility to help PC players aim in a popular online game.
Currently, the project relies on several in-game mechanics that highlight enemies in red.

### Running the project
To run this project, first cd into `python` and install all Python 3 dependencies in `requirements.txt` -- I recommend a virtual environment for this. Then, simply run `main.py` as an administrator with Python 3.

### Using this project
I don't condone the use of this project in online play. 

That said, all buttons are documented in `actor/StateManager.py`, and the basics are here.
* You'll need to configure the delete key (or `actor.StateManager.shoot_key`) as an alternative button to shoot. 
* Then, hold Alt (`actor.StateManager.scope_key`) and hit a button (e.g. `actor.StateManager.x1t_key` or `actor.StateManager.x2_key`) to select an optic.
* Simply aim and use the middle mouse button (`actor.StateManager.shoot`) to shoot. 
* The aim assist will kick in if you're using a scope that highlights enemies, or have pressed 'Z' recently. If you're not playing a character where 'Z' highlights enemies, change `actor.StateManager.beast_key` to something else. Any time you activate "beast mode" with 'Z', you can hit 'Z' again to deactivate it. 
* `actor.StateManager.spray_mode` controls whether or not aim assit continues working while you hold down the `actor.StateManager.shoot_key` button.

