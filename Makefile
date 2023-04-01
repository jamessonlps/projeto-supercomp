CXX = g++
CXXFLAGS = -Wall -O3 -g
CXXFLAGSGEN = -lboost_random

all: gulosa aleatorio gerador

gulosa: functions.cpp gulosa.cpp
	$(CXX) $(CXXFLAGS) $^ -o $@

aleatorio: functions.cpp aleatorio.cpp
	$(CXX) $(CXXFLAGS) $^ -o $@

gerador: gerador.cpp
	$(CXX) $(CXXFLAGS) $(CXXFLAGSGEN) $^ -o $@

clean:
	rm -f gulosa aleatorio gerador
