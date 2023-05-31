CXX = g++
CXXFLAGS = -Wall -O3 -g
CXXFLAGSGEN = -lboost_random

all: gulosa aleatorio gerador openmp

gulosa: functions.cpp gulosa.cpp
	$(CXX) $(CXXFLAGS) $^ -o $@

aleatorio: functions.cpp aleatorio.cpp
	$(CXX) $(CXXFLAGS) $^ -o $@

openmp: functions.cpp openmp.cpp
	$(CXX) $(CXXFLAGS) -fopenmp $^ -o $@

gerador: gerador.cpp
	$(CXX) $(CXXFLAGS) $(CXXFLAGSGEN) $^ -o $@

clean:
	rm -f gulosa aleatorio gerador openmp
