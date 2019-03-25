from constants import DIGITS

def check(guess, target):
    guessed = 0
    placed = 0
    for idx, digit in enumerate(guess):
        if digit in target:
            guessed+=1
        
        if digit is target[idx]:
            placed+=1
    
    return {'guessed': guessed,
            'placed': placed,
            'finished': guessed == placed == 4,
            'message': None}
        

def validate_entry(user_input):
    if len(user_input) != 4:
        return False
    
    for i in user_input:
        if user_input.count(i) > 1:
            return False
        
        if i not in DIGITS:
            return False
    
    return True
            

