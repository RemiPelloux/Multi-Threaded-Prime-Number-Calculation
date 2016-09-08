# Multi-Threaded-Prime-Number-Calculation
 File: process.pyc (Python 2.7)
 
 
'''
Prime process filter.
 
SYNOPSIS
 
    process [-t [-v]|-h|N]
 
 
    When called with parameter N, runs as the master of N parallel
    processes. When called without parameter, run as non master
    process. Options are mutually exclusive. See below for available
    options.
 
OPTIONS
    -t Run tests. Add -v flag for doctest verbose output.
 
    -h Show this page
 
 
This process is designed to be part of an arbitrary long ring
of processes working together in parallel to discover prime numbers
in sequence.
 
The ring is designed to work as a series of N worker processes and
a master connected to each other using pipes. The workers form a
string of processes and the master closes the ring between the
first and last process of the worker string.
 
A simple protocol is used to allow the collaboration on the ring.
Each process reads messages on its standard input, does the necessary
processing and emits messages for the next process on the ring on its
standard output.
 
The protocol is formed of the following types of messages:
- J;  : Token
- ?n; : Is n a prime?
- Pn; : n is a prime
- Nn; : n is not a prime
 
Each process maintains its own list of primes, that is not
supposed to overlap with the list of the other processes.
 
The token is used to tell which process is going to add the next
discovered prime to its own list. Once a process that holds the
token has received a new prime (Pn message) to update its list,
it passes the token on to the next process on the ring.
 
When a process receives an undecided message (?n message), the
following can happen:
- n is found to be a multiple of a known prime in its list. A
nonprime message (Nn message) can be sent out to the next
process on the ring;
- n is not found to be a multiple of a prime in its list. The
message is forwarded unchanged on the ring.
 
When a process receives a prime (message Pn), either it has
the token and it has to save the new prime in its list, or
does not have the token and it must not save the pime in its
list. In both cases it has to forward the prime message on
the ring, but in the case it had the token, it must emit a
token message right AFTER forwarding the prime message
(otherwise the next process on the ring will save the new
prime too).
 
'''
