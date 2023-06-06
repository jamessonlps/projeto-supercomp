#include "functions.h"
#include <fstream>
#include <chrono>
#include <omp.h>
#include <bitset>
#include <nlohmann/json.hpp>

using namespace std;
using json = nlohmann::json;


struct movie_item {
  movie m;
  bitset<24> time_used;
};

struct exhaustive_return {
  bitset<64> solution;
  int screen_time;
};

void fill_movie_time_used(movie_item &movie_item) {
  for (int i = 0; i < 24; i++) {
    if (movie_item.m.begin < movie_item.m.end) {
      if (i >= movie_item.m.begin && i < movie_item.m.end)
        movie_item.time_used.set(i);
    } 
    else {
      if (i >= movie_item.m.begin || i < movie_item.m.end)
        movie_item.time_used.set(i);
    }
  }
}


vector<exhaustive_return> exhaustive(vector<movie_item> &mis, map<int, int> &max_by_cat, int num_movies, int num_threads) {
  long int max_solutions = min(pow(2, num_movies), pow(2, 62));

  vector<exhaustive_return> solutions;

  #pragma omp parallel
  {
    #pragma omp parallel for num_threads(num_threads)
    for (long int i = 0; i < max_solutions; i++) {
      map<int, int> max_by_cat_copy = max_by_cat;
      bitset<64> solution(i);
      bitset<24> time_available;
      int screen_time = 0;

      for (int j = 0; j < num_movies; j++) {
        if (solution[j] == 1) {
          bitset<24> is_addable = mis[j].time_used & time_available;

          if ((is_addable != 0) || (max_by_cat_copy[mis[j].m.category] == 0))
            continue;
          else {
            time_available = time_available | mis[j].time_used;
            max_by_cat_copy[mis[j].m.category] -= 1;
            screen_time += mis[j].m.duration;
          }
        }
      }
      
      #pragma omp critical
      {
        solutions.push_back({ solution, screen_time });
      }
    }
  }

  return solutions;
}


int main(int argc, char *argv[]) {
  // string filename = argv[1];
  // json output;

  int num_movies;
  int num_categories;
  int num_threads = 4;

  cin >> num_movies;
  cin >> num_categories;

  vector<movie> movies(num_movies);
  map<int, int> max_by_category;

  fetch_categories(max_by_category, num_categories);
  fetch_movies(movies, num_movies);

  vector<movie_item> movies_item;
  for (auto m : movies) {
    movie_item mi;
    mi.m = m;
    fill_movie_time_used(mi);
    movies_item.push_back(mi);
  }

  auto start_exec = chrono::high_resolution_clock::now();

  vector<exhaustive_return> solutions_response = exhaustive(
    movies_item, 
    max_by_category, 
    num_movies, 
    num_threads
  );

  auto end_exec = chrono::high_resolution_clock::now();
  int exec_time = chrono::duration_cast<chrono::milliseconds>(end_exec - start_exec).count();

  int max_solution = 0;
  int screen_time = 0;
  int num_solutions = solutions_response.size();

  // Obtem o indice do elemento com o maior numero de bits setados
  for (int i = 0; i < num_solutions; i++) {
    int count = solutions_response[i].solution.count();
    if (count > max_solution) {
      max_solution = count;
      screen_time = solutions_response[i].screen_time;
    }
  }

  cout << "Tempo de execução: " << exec_time << " ms" << endl;
  cout << "Tempo total de tela: " << screen_time << endl;
  cout << "Número de filmes: " << num_movies << endl;
  cout << "Número de threads: " << num_threads << endl;

  // output["exec_time"] = exec_time;
  // output["screen_time"] = screen_time;
  // output["num_movies"] = num_movies;
  // output["num_categories"] = num_categories;
  // output["num_threads"] = num_threads;

  // ofstream out(filename);
  // out << output.dump(2);
  // out.close();

  return 0;

}