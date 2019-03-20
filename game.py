def check(guess, target):
    guessed = 0
    placed = 0
    for idx, digit in enumerate(guess):
        if digit in target:
            guessed+=1
        
        if digit is target[idx]:
            placed+=1
    
    return {'guessed': guessed,
            'placed': placed}
        

    def validate_entry(user_input):
        for i in user_input:
            if tt_list.count(i) > 1:
                raise
            

