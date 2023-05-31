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


vector<bitset<64>> exhaustive(vector<movie_item> &mis, map<int, int> &max_by_cat, int num_movies, int num_threads) {
  long int max_solutions = pow(2, num_movies);

  vector<bitset<64>> solutions;

  #pragma omp parallel
  {
    #pragma omp parallel for num_threads(num_threads)
    for (long int i = 0; i < max_solutions; i++) {
      map<int, int> max_by_cat_copy = max_by_cat;
      bitset<64> solution(i);
      bitset<24> time_available;

      for (int j = 0; j < num_movies; j++) {
        if (solution[j] == 1) {
          bitset<24> is_addable = mis[j].time_used & time_available;

          if (is_addable != 0)
            break;

          if (max_by_cat_copy[mis[j].m.category] == 0)
            break;

          time_available = time_available | mis[j].time_used;
          max_by_cat_copy[mis[j].m.category] -= 1;
        }

        if (j == num_movies - 1) {
          #pragma omp critical
          {
            solutions.push_back(solution);
          }
        }
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
  int num_threads = omp_get_max_threads();

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

  vector<bitset<64>> solutions = exhaustive(
    movies_item, 
    max_by_category, 
    num_movies, 
    num_threads
  );

  auto end_exec = chrono::high_resolution_clock::now();

  int exec_time = chrono::duration_cast<chrono::milliseconds>(end_exec - start_exec).count();

  int max_solution = 0;
  int max_solution_index = 0;
  int num_solutions = solutions.size();
  
  for (int i = 0; i < num_solutions; i++) {
    int count = solutions[i].count();
    if (count > max_solution) {
      max_solution = count;
      max_solution_index = i;
    }
  }

  vector<movie> best_solution;
  int duration_best_solution = 0;
  
  for (int i = 0; i < num_movies; i++) {
    if (solutions[max_solution_index][i] == 1) {
      best_solution.push_back(movies[i]);
      duration_best_solution += movies[i].duration;
    }
  }

  cout << "Tempo de execução: " << (double) exec_time / 1000 << " s" << endl;
  cout << "Tempo total de tela: " << duration_best_solution << endl;
  cout << "Filmes: " << endl;
  for (auto m : best_solution) {
    cout << m.id << endl;
  }

  // output["solution"] = solution;
  // output["max_solution"] = max_solution;

  // ofstream out(filename);
  // out << output.dump(2);
  // out.close();

  return 0;

}