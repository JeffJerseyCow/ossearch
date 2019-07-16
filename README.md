# ossearch
Are you looking for software embedded in large source code projects? Is using find/grep and sha256sum returning too many false positives? Do you require more structured searching?

If you answered yes to any of these questions then OS Search (ossearch) might be for you.

## Installation
The only requirements are Python3 and Docker, which if correctly set-up should make utilising this project a breeze. 
1. ```git clone https://github.com/JeffJerseyCow/ossearch.git```
2. ```pip install -r requirements.txt```
3. ```pip install --upgrde ossearch/``` on the cloned directory

*Note: Docker must be setup properly -- this means your user MUST be part of the Docker group or root.*

## Usage
OS Search is invoked by typing ```ossearch``` on the command line.

It has three commands:
- ```ossearch build```
- ```ossearch search```
- ```ossearch delete```

### Building
To search a project you first need to build a database from the reference source code project. 

```ossearch build -d ~/src_code_project```

This can take some time -- it can generate a database for the linux kernel in approximately 2 minutes.

### Searching
After building you can search. 

```osserach search -d ~/src_to_lookfor```

This will search the **reference** database looking for occurrences of **src_to_lookfor** within **src_code_project**. If a subtree within the reference source code project is found to have a matching similarity score above 10%, then it will be printed to stderr.

The threshold can be altered with the threshold flag.

```ossearch search -d ~/src_to_lookfor -t 80```

Now only similarity matching scores above 80% will be reported. 


### Deleting
If you want to wipe the database you can either delete a subtree from an originating node.

```ossearch delete -d ~/src_code_project``` 

Or purge the entire database with 

```ossearch delete --purge```

*Note: If you prematurely exit the build step then the database must be purged. This is an efficiency decision as it's quicker to create vertices then add edges separately.*

## Alternative Database
ossearch uses the graph database Apache Tinkerpop with a Neo4J back-end. By default ossearch spawns a Docker container listening on localhost over the TCP port 8182.

To specify a custom database address and/or port combination use the address and port flags like so. 

- ```ossearch build -a 192.168.0.1 -p 8182 -d ./directory```

## Algorithm
### Building
TODO
### Searching
TODO