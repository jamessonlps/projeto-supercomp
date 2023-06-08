#include "functions.h"
#include <fstream>
#include <chrono>
#include <omp.h>
#include <bitset>

using namespace std;

struct movie_item
{
  movie m;
  bitset<24> time_used;
};

struct exhaustive_return
{
  int total_movies;
  int screen_time;
};

void fill_movie_time_used(movie_item &movie_item)
{
  for (int i = 0; i < 24; i++)
  {
    if (movie_item.m.begin < movie_item.m.end)
    {
      if (i >= movie_item.m.begin && i < movie_item.m.end)
        movie_item.time_used.set(i);
    }
    else
    {
      if (i >= movie_item.m.begin || i < movie_item.m.end)
        movie_item.time_used.set(i);
    }
  }
}

exhaustive_return exhaustive(const vector<movie_item> &mis, vector<int> &max_by_cat, const int num_movies, const int num_threads, const int num_categories)
{
  unsigned long int max_solutions = pow(2, num_movies);

  int best_num_movies = 0;
  int best_screen_time = 0;

#pragma omp parallel
  {
#pragma omp parallel for shared(best_num_movies, best_screen_time)
    for (unsigned long int i = 0; i < max_solutions; i++)
    {
      vector<int> max_by_cat_used(num_categories, 0);

      bitset<31> solution(i);    // 31 bits (cada bit representa um filme)
      bitset<24> time_available; // 24 bits (cada bit representa um horário)

      int screen_time = 0;  // Tempo total de tela da solução
      int total_movies = 0; // Número total de filmes na solução

      // Percorremos cada bit da solução.
      for (int j = 0; j < num_movies; j++)
      {
        // Se o bit for 1, então o filme está na solução.
        if (solution[j] == 1)
        {
          // Verificamos se ainda há filmes disponíveis na categoria do filme.
          int category_id = mis[j].m.category - 1;
          if (max_by_cat_used[category_id] < max_by_cat[category_id])
          {
            // Verificamos se o filme pode ser adicionado na solução.
            bitset<24> is_addable = mis[j].time_used & time_available;

            // Se o filme não puder ser adicionado, ou se não houver
            // mais filmes disponíveis na categoria dele, então não adicionamos.
            if (is_addable.none())
            {
              time_available = time_available | mis[j].time_used;
              max_by_cat_used[category_id] += 1;
              screen_time += mis[j].m.duration;
              total_movies += 1;
            }
          }
        }
      }

#pragma omp critical
      {
        if (total_movies > best_num_movies)
        {
          best_num_movies = total_movies;
          best_screen_time = screen_time;
        }
      }
    }
  }

  exhaustive_return solution;

  solution.screen_time = best_screen_time;
  solution.total_movies = best_num_movies;

  return solution;
}

int main(int argc, char *argv[])
{
  int num_movies;
  int num_categories;
  int num_threads = atoi(argv[1]);

  omp_set_num_threads(num_threads);

  cin >> num_movies;
  cin >> num_categories;

  vector<movie> movies(num_movies);

  vector<int> max_by_category(num_categories);
  for (int i = 0; i < num_categories; i++)
  {
    int limit;
    cin >> limit;
    max_by_category[i] = limit;
  }

  // fetch_categories(max_by_category, num_categories);
  fetch_movies(movies, num_movies);

  vector<movie_item> movies_item;
  for (auto m : movies)
  {
    movie_item mi;
    mi.m = m;
    fill_movie_time_used(mi);
    movies_item.push_back(mi);
  }

  auto start_exec = chrono::high_resolution_clock::now();

  exhaustive_return solutions_response = exhaustive(
      movies_item,
      max_by_category,
      num_movies,
      num_threads,
      num_categories);

  auto end_exec = chrono::high_resolution_clock::now();
  auto exec_time = chrono::duration_cast<chrono::milliseconds>(end_exec - start_exec).count();

  // Número de filmes
  cout << num_movies << endl;

  // Número de categorias
  cout << num_categories << endl;

  // Número de threads
  cout << num_threads << endl;

  // Número de filmes selecionados
  cout << solutions_response.total_movies << endl;

  // Tempo de execução
  cout << exec_time << endl;

  // Tempo de tela
  cout << solutions_response.screen_time << endl;

  return 0;
}