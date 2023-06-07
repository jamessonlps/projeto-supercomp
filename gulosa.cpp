#include "functions.h"
#include <fstream>
#include <chrono>

using namespace std;

void gulosa(vector<movie> &solution, int &total_time, int &num_categories, int &num_movies)
{
  map<int, int> max_cat;            // Dicionário { "categoria": filmes_disponíveis }
  map<int, bool> times_available;   // Dicionário com horários disponíveis
  vector<movie> movies(num_movies); // Lista de filmes

  fetch_categories(max_cat, num_categories);
  fetch_movies(movies, num_movies);

  order_movies_by_end_ascending(movies);
  init_availability_list(times_available);

  movie last_selected = {0, 0, 0, 0};

  for (auto &movie : movies)
  {
    // Tempo máximo de 24h
    if (total_time >= 24)
    {
      return;
    }

    if (movie.begin >= last_selected.end && max_cat[movie.category] > 0 && has_time_available(times_available, movie))
    {
      solution.push_back(movie);
      update_availability_list(times_available, movie);

      max_cat[movie.category]--;
      total_time += movie.duration;
      last_selected = movie;
    }
  }
}

int main(int argc, char *argv[])
{
  // string file_name = argv[1];
  // json output_json;

  int total_time = 0; // tempo total dos filmes selecionados
  int exec_time = 0;  // tempo de execução do algoritmo
  int num_movies;     // Número total de filmes
  int num_categories; // Número total de categorias
  vector<movie> movies_selected;

  cin >> num_movies;
  cin >> num_categories;

  chrono::steady_clock::time_point start_exec = chrono::steady_clock::now();
  gulosa(movies_selected, total_time, num_categories, num_movies);
  chrono::steady_clock::time_point end_exec = chrono::steady_clock::now();

  exec_time = chrono::duration_cast<chrono::microseconds>(end_exec - start_exec).count();

  // Número de filmes
  cout << num_movies << endl;

  // Número de categorias
  cout << num_categories << endl;

  // Número de filmes selecionados
  cout << movies_selected.size() << endl;

  // Tempo de execução
  cout << exec_time << endl;

  // Tempo de tela
  cout << total_time << endl;

  return 0;
}