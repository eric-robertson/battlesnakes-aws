# Brute force tree search

Algorithm:

- Encodes the board as a numpy array. 
- Starts a tree search of every possible board state. 
- Scores each state for each snake
- Select the move that maximised your long term score

Todo:

- Do the whole tree search thing ( currently doesnt )
- Write a better score function ( uses health right now which sucks )
- Cache the board states, would be a major speed-up
- Add cuttoff to guarantee response within time limit