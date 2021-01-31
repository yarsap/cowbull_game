Cowbull game
=======================

A console number guessing game in websockets.

Requires Python >= 3.6

Before run
=======================

1. `python3 -m venv /path/to/new/virtual/environment`
2. Activate venv (`source venvpath/bin/activate`)
3. `pip install -r requirements.txt`

Run
=======================

`python server.py`

In another terminal
  `python client.py`
  
Rules
=======================
 
 Aim is to guess 4-digit (unique digits) number of your opponent. Each guess is followed by a response: how many digits you guessed and how many of them on the right place. 
 
 Example:
 
 Let's say, if opponent's number is 1345

```
Guess the number: 1234
```

with `1234` input we will get:

```
< Guessed: 3
< Placed: 1
```
 
 which means we guessed [1,3,4], but only [1] is right placed 
