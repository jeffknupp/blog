# Buffer Overflows Are Real Things That Actually Happen

For those who are just starting their career as engineers or may not have been exposed to a language requiring manual
memory management like C or C++, the term "buffer overflow" is like the McGuffin of security exploits. But buffer
overflows really happen! And they happen in real, well-tested, and well-reviewed code. But not every buffer overflow is
an attack vector for hackers. Most of the time, they're more benign and simply result in your program crashing or giving
garbage data. To a developer using a popular open source library, crashing and misbehaving is basically just as bad.

I recently ran into such an issue while working on a large infrastructural project that uses the [Parquet](https://parquet.apache.org) file format and
[Arrow](https://arrow.apache.org) in-memory data format (both are columnar). I uncovered a number of
issues/unimplemented features in Arrow and [parquet-cpp](https://github.com/apache/parquet-cpp) (the reference
implementation of Parquet has always been in Java. `parquet-cpp` ports this to C++ and makes it available to languages
that can interoperate with C/C++ libraries). More surprisingly (to me, at least), I encountered two issues in [Pandas](pandas.pydata.org), a library downloaded and used thousands of times a day with terrific test coverage and development practices.
