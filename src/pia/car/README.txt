Here is a readme for this program:

0. The files we are going to read in are in car folder, like "A.txt".  
The content of these files might be some integers.

1. At the beginning, we need to open a server by typing the command: 
java Cardinality2 server (called Terminal1).

2. After turning on a server, we open 2, 3 or more nodes using: 
java Cardinality2.  For instance, we want to use three nodes (Terminal2, 
3, and 4).  We assume IP addresses and ports of them are: 127.0.0.1:10001, 
127.0.0.1:10002, and 127.0.0.1:10003.  

3. For each node (i.e., Terminal 2-4), enter the ip address of its previous
node (in form X.X.X.X:XXXX, use ":" to separate ip and port, no space 
allowed).  For example, if node Terminal2's next node is Terminal3, enter 
127.0.0.1:10001 in Terminal3 since 127.0.0.1:10001 is IP and port of 
Terminal3's previous node, i.e., Terminal2.  Following this way, we finally
construct a ring where there are three nodes (i.e., Terminal2-4).

4. We now connect each of nodes to server.  At the server side terminal, 
we enter each node's IP address and port.  For our example, type 
127.0.0.1:10001 (return), 127.0.0.1:10002 (return), 
and 127.0.0.1:10003 (return).  By using this way, we actually input IP and 
port information of the three nodes line by line.

5. We now type "end" in server terminal in order to complete the key 
distributions.  After this, we do not need server terminal any more.

6. We type "s" at each node terminal (i.e., Terminal2-4), making them start
computing and sending encrypted and shuffled files to their next nodes.

7. After the above process, we type "c" on each of terminals (Terminal 2-4) 
in order to start computation of the # of intersection lines among all of 
files.  The final result should be shown on terminal.

8. Type "q" to exit.  
