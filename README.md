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

`python3 server.py`

In another terminal
  `python3 client.py`
  
Rules
=======================
 
 Aim is to guess 4-digit (unique digits) number of your opponent. Each guess is followed by a response: how many digits you asked and how many of them on the right place. Let's say, if opponent's number 1345 and we're typed 1234, then it is 3 guessed and 1 placed ( we guessed [1,3,4], but only [1] is right placed ) 
