# Programs for the paper "Simulating an n-body system of celestial bodies" by Jerry Schupp

## The following section describes the structure of this git page's organization.

### Final programs
- There are two final Python versions of the project, and two final Unity versions thereof.
- The Python programs are contained in the "/python" directory.
	- The direct simulation is in the "/direct" subdirectory.
	- The tree simulation is in the "/tree" subdirectory.
- The Unity programs are contained in the "/Unity" directory.
	- The direct simulation is in the "/direct" subdirectory.
	- The tree simulation is in the "/tree" subdirectory.
	
### Testing Programs
- This section contains all the program files used to test other things for the program.
- All of these programs are stored in the "/testing" directory.
- The files in the subdirectory "/data_processing" were used for various data processing functions throughout the project, including making simple graphs for some of the data
- The file "belt_maker.py" can create a procedural asteroid belt for the simulations to use
- The files "spread_reader.py" and "spread_reader_special.py" can read in the initial conditions set out in text files. Either may be necessary to use some of the Python versions of the simulation.