# Java RMI

This is a Java RMI implementation. The method accessed is a upload method. You can choose between four diferent file sizes to upload e see how much time its time to do it. To run the program, you need to diffenrets computers connected in the same network. One is the server and the another one is the client.

## Running
1. Clone this reposioty in two different computers

2. Use ifconfig in the server side to get the server IP address

3. Run the following command in client side to create files
```
make create-files
```
4. Run the following command in both sides to compile the program
```
make
```

4. Run the following command to start the server
```
java Server
```

4. Run the following command to start the client

```
java Client
```

5. Chosse an option to upload file e see how much time it takes