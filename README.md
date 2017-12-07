Dependencies of Python3, Flask, Flask-RESTful, requests

Dependencies can be installed with the installDependencies.sh script

Rowan Sutton
13330793

This project implements a NFS filesystem. Storage is performed on text files local to the fileserver. For all of the filesystems, the startServer.sh script must be run before the startClient.sh scripts. For directory service, the startServer1.sh and startServer2.sh scripts must be run before the startDirectoryService.sh script. After these are run, then the startClient.sh scripts can be run.The server has a serverData folder in its directory which contains the files to be provided to the clients by the server.

1. Transparent Distributed Filesystem:
For the transparent distributed file system, the server sets up two endpoints, one for access to the file list for file creation and listing available files, and the other for accessing and changing individual files. A library named clientLibrary was created to provide access to the functionality of these endpoints while giving transparency for the client. The client only needed to call functions to access file data and not construct individual RESTful requests. The functions allowed listing of all files on the server, printing of file data, editing file data, creation of new files, and deletion of existing files. 

2. Locking:
To implement locking, each client accessing the file server was allocated a client ID. The clients could request access to a file, after which they would be added to the end of a lock queue for that file. The first client in the lock queue would be given access to the file. Clients who were not the first member of the lock queue could not access the file for editing or deletion. This can be seen by editing a file and waiting after prompted for new file data, then attempting to edit or delete the file with another client. After the client was done with the file, they would inform the server that they were finished, and then the next client in the queue would be given access. The clients in the queue polled the server while the file was locked, and clients could abort their request for the file while polling which removed them from the queue. Locking was not implemented for reading or listing files since these operations do not change the file content.

3. Directory Service:
For directory service, the file servers start first, then the directory server, and then the clients. Upon initialisation, the directory server requests the file lists for the two fileservers (Fileserver 1 and Fileserver 2). Using this, it maps each file to the corresponding fileserver. Client requests are sent to the file server and the server responds with the server ip, port, and file name on that server. Given this information, the client then requests the file from the correct server. This is all incorporated in the clientLibrary to maintain transparency.


4. Caching:
Caching is performed by taking a separate copy of the data obtained from the file system when the client first requests the file data. In this implementation, file data is stored in a local cache in memory since it is faster than writing cache files to disk. For a large number of client-side files, disk storage would be preferable since memory may not have enough capacity. Reads and edits by the client are performed on the cached copy of the data since caching aims to reduce network demand. These edits can then be put on to the server by the client. In a more ideal solution, the server would check each client with that file to see if their cache is out of date. The checks in this implementation for expiry of data are done when the file is pushed to the server.




