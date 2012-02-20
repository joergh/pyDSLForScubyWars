# python DSL implementation for scubywars

## About

A straight forward DSL implementation in python for the ScubyWars server.  
See [ScubywarsKernel](https://github.com/SuperTux88/scubywars.kernel) for documentation etc.

## Usage

This simple program uses [PLY](http://www.dabeaz.com/ply/ply.html) to generate the parser.
The file tokendefs.py contains the tokenizer, parser.py contains the parser.

## Internals

The parser generates a python source file from the DSL source file. This python module is then executed.

See test.sb1 for a simple bot source in the DSL.


