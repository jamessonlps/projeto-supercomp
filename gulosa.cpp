#include "functions.h"
#include <fstream>
#include <nlohmann/json.hpp>

using namespace std;
using json = nlohmann::json;

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
  string file_name = argv[1];
  json output_json;

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

  cout << "TEMPO DE EXECUÇÃO: " << exec_time << endl;
  cout << "TEMPO DE TELA: " << total_time << endl;
  cout << "FILMES SELECIONADOS: HEURÍSTICA GULOSA" << endl;

  for (auto &i : movies_selected)
  {
    cout << "ID: " << i.id << ", categoria: " << i.category << ", starts at: " << i.begin << ", ends at: " << i.end << ", duration: " << i.duration << endl;
  }

  output_json["exec_time"] = exec_time;
  output_json["screen_time"] = total_time;
  output_json["num_movies"] = num_movies;
  output_json["num_categories"] = num_categories;

  ofstream file(file_name);
  file << output_json.dump();
  file.close();

  return 0;
}