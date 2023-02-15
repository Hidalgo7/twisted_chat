# twisted_chat

App that simulates a chat room, implementing a client server protocol between a server and many simoultaneous clients using sockets.

The forbidden.txt files indicates which words will be censured in the chat room messages.

# Running instructions
1. Run the server
```bash
python serv_chat.py
```

2. Run clients
```bash
python chatcli/chatcli.py
```
When running the client a GUI will appear, to enter the chat room you must indicate the username in the textbox at the top left corner and
click the 'Connect' buttom at the top right corner.

Run at least two clients to see the interaction between them.


