![](./img/Lemon.png)

# Lemon Game
![](https://img.shields.io/badge/code_style-garbage-brown)

possibly the dumbest multiplayer demo in python + pygame

---

## Protocol

Players can’t be differenciated from each other.

Once joined, the client constantly sends the local coordiantes to the server, and expects coordinates in the form of `X,Y;X,Y;` (repeating n times), excluding the local client.
