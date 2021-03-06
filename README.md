# Chess application

## Description
- The application is built on top of object oriented programming and layered architecture
- The Chess game can be played either Human vs Computer, Human vs Human or Computer vs Computer
- The game's settings can be changed in the settings.properties file
- Optimal depth for the application is depth 4! Higher depth will take substantially more time to receive an answer. Lower depth will have a quicker but less accurate response
- The principal interface of the application is the GUI, although the application can be started using the console.

## AI Description
- The chess engine works using the MinMax Algoritm, to which the Alpha-Beta pruning was applied.
- The chessboard evaluation is computed using piece values, piece mobility values and piece placement values. That means that the more valuable a piece is (King, Queen, Rook, Bishop, Knight, Pawn), the more mobility it has (available squares to move to) and the more well placed it is on the chessboard the more valuable it is.
- The chess engine avoids checkmate whenever possible. It also checkmates whenever possible, avoiding stalemates. (With a depth of 4 moves)

<p align="center">
  <img src="https://user-images.githubusercontent.com/74305289/105626338-a9358000-5e37-11eb-8e1e-5ba88ec2206c.png" alt="Chess game screenshot"/>
</p>
