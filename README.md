# ossearch
Are you looking for embedded software within giant projects? Is using find and sha256sum returning too many false positives? Do you more structured searching?

If you answered yes to any of these questions then OS Search might be for you.

## Installation
The only requirements are Python3 and Docker, which if correctly set-up should make utilising this project a breeze. 
Just git clone the directory and ```pip install . --upgrade``` within the directory.

## Usage
OS Search is invoked by typing ```ossearch``` on the command line.

It has three commands:
- ```ossearch build```
- ```ossearch search```
- ```ossearch delete```

### Building
You first need to build a database from a source code directory with ```ossearch build -d ~/src0```

This can take some time, but it manages to generate a graph of the linux kernel in approximately 2 minutes.

### Searching
Once build you can search -- this involves typing ```osserach search -d ~/src1```

This will search the database looking for occurrences of src1 being embedded within src0. If any of the files match is will flag them if they're over a threshold similarity of 10%.

### Deleting
If you want to wipe the database you can either delete from a node down with ```ossearch delete -d ~/src0``` or purge everything with ```ossearch delete --purge```

*Note: If you prematurely end the build step then the database must be purged. This was an efficiency decision are its quicker to add vertices and edges separately.*

### Miscellaneous
There is an option to use another Tinkerpop instance by specifying the address and/or port number.

- ```ossearch build -a 192.168.0.1 -p 8182 -d ./directory```

You can also customarily set the threshold percentage by specifying the ```-t``` switch on searching.

- ```ossearch search -d ./directory -t 90```

By default the address is localhost and port 8182.

## Algorithm
TODO
