## Description
Chess is implemented using OOP paradigm and Layered Architecture.\
Application testing is fully covered.\
The game offers 3 game modes:
- [x] Player vs Player;
- [x] Player vs Computer;
- [x] Computer vs Computer.

<p align="center">
  <img src="https://user-images.githubusercontent.com/74305289/105626338-a9358000-5e37-11eb-8e1e-5ba88ec2206c.png" alt="Chess game screenshot"/>
</p>

## AI
The Chess Engine was designed applying the min-max algorithm, enhanced with alpha-beta pruning.
Chessboard Evaluation is computed by scoring the board, taking into consideration:
- Piece values;
- Piece mobility;
- Piece placement.

Hence, more base value, more available squares to move to and better placement makes a piece valuable.\
Forced checkmate sequences are always prioritized.\
Stalemates are always avoided when winning, but desired when losing. 

## Setup
The game's settings can be changed in the settings.properties file.\
Optimal depth: 4\
Higher depth gives slower, more accurate moves.\
Lower depth gives quicker, less accurate responses.
