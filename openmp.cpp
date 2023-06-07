#include "functions.h"
#include <fstream>
#include <chrono>
#include <omp.h>
#include <bitset>

using namespace std;


struct movie_item {
  movie m;
  bitset<24> time_used;
};

struct exhaustive_return {
  int total_movies;
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
  unsigned long long max_solutions = pow(2, num_movies);

  vector<exhaustive_return> solutions;

  #pragma omp parallel
  {
    #pragma omp parallel for num_threads(num_threads) shared(max_solutions, solutions)
    for (unsigned long long i = 0; i < max_solutions; i++) {
      map<int, int> max_by_cat_copy = max_by_cat;
      bitset<35> solution(i);    // 35 bits (cada bit representa um filme)
      bitset<24> time_available; // 24 bits (cada bit representa um horário)
      
      int screen_time = 0;       // Tempo total de tela da solução
      int total_movies = 0;      // Número total de filmes na solução

      // Percorremos cada bit da solução.
      for (int j = 0; j < num_movies; j++) {
        // Se o bit for 1, então o filme está na solução.
        if (solution[j] == 1) {
          // Verificamos se o filme pode ser adicionado na solução.
          bitset<24> is_addable = mis[j].time_used & time_available;

          // Se o filme não puder ser adicionado, ou se não houver 
          // mais filmes disponíveis na categoria dele, então não adicionamos.
          if ((is_addable != 0) || (max_by_cat_copy[mis[j].m.category] == 0))
            continue;

          // Se o filme puder ser adicionado, então adicionamos.
          else {
            time_available = time_available | mis[j].time_used;
            max_by_cat_copy[mis[j].m.category] -= 1;
            screen_time += mis[j].m.duration;
            total_movies += 1;
          }
        }
      }

      // solutions.push_back({ solution, screen_time });
      
      #pragma omp critical
      {
        solutions.push_back({ total_movies, screen_time });
      }
    }
  }

  return solutions;
}


int main(int argc, char *argv[]) {
  int num_movies;
  int num_categories;
  int num_threads = atoi(argv[1]);

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
  auto exec_time = chrono::duration_cast<chrono::milliseconds>(end_exec - start_exec).count();

  // int max_solution = 0;
  // int screen_time = 0;
  // int num_solutions = solutions_response.size();

  // // Obtem o indice do elemento com o maior numero de bits setados
  // for (int i = 0; i < num_solutions; i++) {
  //   int count = solutions_response[i].solution.count();
  //   if (count > max_solution) {
  //     max_solution = count;
  //     screen_time = solutions_response[i].screen_time;
  //   }
  // }

  // Número de filmes
  cout << num_movies << endl;

  // // Número de categorias
  // cout << num_categories << endl;

  // // Número de threads
  // cout << num_threads << endl;

  // // Número de filmes selecionados
  // cout << max_solution << endl;

  // // Tempo de execução
  // cout << exec_time << endl;

  // // Tempo de tela
  // cout << screen_time << endl;

  return 0;

}