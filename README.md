JVM Objects
==========

Dec 06. 2013, all future work has been moved to bitbucket (https://bitbucket.org/JunjieQian/java-vm-work). Please come and check later, once we publish the paper the full version implementation will be release here.

Bloat memory usage of Java VM objects caused inefficient memory usage. This project is to explore how this comes and propose one solution for this.
Started at Jan. 2013.

First step: generate the memory footprint of Java VM objects.
    Patches: changes to JikesRVM 3.1.3 to get both the read and write barriers, along with operation mode and system time.
    Finished at Mar. 2013.

Second step: analyze the memory trace obtained, problem is this trace is extremely huge.
    anaylzation tools: python code to analyze the trace files


