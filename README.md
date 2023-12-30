![](./img/Lemon.png)

# Lemon Game
![](https://img.shields.io/badge/code_style-garbage-brown)

possibly the dumbest multiplayer demo in python + pygame

created at #37c3

---

now with:
```
                            _           _
  ___  __ _  __ _ ___ _ __ | | ___  ___(_) ___  _ __  ___
 / _ \/ _` |/ _` / __| '_ \| |/ _ \/ __| |/ _ \| '_ \/ __|
|  __/ (_| | (_| \__ \ |_) | | (_) \__ \ | (_) | | | \__ \
 \___|\__, |\__, |___/ .__/|_|\___/|___/_|\___/|_| |_|___/
      |___/ |___/    |_|

```

## Protocol

Once joined, the client constantly sends the local coordiantes to the server, and expects coordinates in the form of `X,Y;X,Y;` (repeating n times), excluding the local client.
