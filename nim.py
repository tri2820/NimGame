#!/usr/bin/python39
from random import randint

N_HEAP = (2,5)
N_ITEMS = 1000
PLAYER_START_FIRST = True

# Random N_ITEMS into heaps
def distribute(num_heap, n_items):
    borders = []
    for _ in range(1,num_heap):
        while True:
            b = randint(0,n_items)
            if b not in borders: break
        borders.append(b)
    borders = sorted([0] + borders + [n_items])
    heaps = [b-a for a, b in zip(borders,borders[1:])]
    return heaps

# Bitwise XOR function over heaps
def XOR(heaps):
    X = heaps[0]
    for h in heaps[1:]: 
        X = X ^ h
    return X

# Find optimal move 
def move(heaps):
    X = XOR(heaps)
    # Optimal move (with Charles Bouton strategy) does not exist
    # if XOR of heaps is zero
    assert not X == 0
    for j,h in enumerate(heaps): 
        # Find a reducible heap
        if X^h < h:
            return j, h-(X^h)
    # Obligatory exception
    raise Exception("ImplementationError.")

# Remove `u` items from the `i`th heap
def apply_move(i,u,heaps):
    assert i in range(0, num_heap)
    assert heaps[i] >= u
    heaps[i] -= u

def game_loop(heaps, player_turn=True):
    while True:
        # Print out the heaps at the beginning of each turn
        print(heaps)

        if player_turn:
            print("From the _th heap, I want to remove _ items: ", end='')
            i,u = [int(x) for x in input().split()]
            apply_move(i, u, heaps)
        else:
            if XOR(heaps) == 0:
                # Either Player moves first with initial non-zero XOR 
                # Or Computer moves first with zero XOR
                print("Computer still has mover order disadvantage, computer tries random move!")
                i = randint(0,num_heap)
                u = randint(0, heaps[i])
                apply_move(i, u, heaps)
            else:
                # Computer finds the optimal move 
                i,u = move(heaps)
                print(f"From the {i}th heap, Computer removes {u} items.")
                apply_move(i, u, heaps)
                assert XOR(heaps)==0

        # If not item left in heaps then end game
        if sum(heaps) == 0: return player_turn

        player_turn = not player_turn

if __name__=="__main__":
    M = {
        False: "Computer",
        True: "Player"
    }
    num_heap = randint(*N_HEAP)
    init_heaps = distribute(num_heap, N_ITEMS)
    winner = game_loop(init_heaps, player_turn=PLAYER_START_FIRST)
    print(f"We found a winner: {M[winner]}")