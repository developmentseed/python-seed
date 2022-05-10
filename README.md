# ipp-core sakura branch

Getting started;

Neo4j server set up:

Install Neo4j Server version: 4.4.6 (community). This can be downloaded from here:
https://neo4j.com/download-center/

Install the server. I installed it as a window service, you might want to do the same, then you can just start the service. If you want to start the server manually, there is a script in the bin directory of the installation. 

**Bear in mind that I already had java installed when I installed the neo4j server. You might need to install java to run the neo4j server.
If you do, please update these 'getting started' notes accordingly.
**


Set up username and password: neo4j:guest (if you do this it will work straight away with existing lazily hard-coded credentials)

In browser, navigate to localhost:7474 and you should see the neo4j browser, and an empty data base.



Python setup:
If you have not, get python 3.6 and a decent python IDE. 

Checkout this branch

install module requirements from 

requirements.txt

(This file has a few dependencies that we won't need, so will need some whittling down at some point)

This branch is part of a larger project, so there is an awful lot of stuff we can just ignore, and we should consider forking this branch into a smaller repo of its own.

The only python file that you'll need to run  at this early stage is ....

isharp/sakura/builder.py.

If you start the neo4j server and  run the above file with the following environmental parameters:

NEO4J_USERNAME=neo4j
NEO4J_PASSWORD	guest
NEO4J_BOLT_URL	bolt://localhost:7687

.. it will **delete** the  existing database and populate it with the instruments, strategies and trading centers that you'll find in the three yaml files in the same directory.

Once you have run this program ( should take a couple of seconds) check the database at localhost:7474 to ensure that the data has been loaded.

Let me know ASAP if you have any problems, then we can work together to refine these getting started notes.



















