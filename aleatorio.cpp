#include "functions.h"
#include <fstream>
#include <nlohmann/json.hpp>

using namespace std;
using json = nlohmann::json;

double prob = 0.25;

void aleatorio(vector<movie> &solution, int &total_time, int &num_categories, int &num_movies)
{
  map<int, int> max_cat;
  map<int, bool> times_available;
  vector<movie> movies(num_movies);

  fetch_categories(max_cat, num_categories);
  fetch_movies(movies, num_movies);

  order_movies_by_end_ascending(movies);
  init_availability_list(times_available);

  int seed = 10;
  default_random_engine engine(seed);
  uniform_real_distribution<double> distribution_real(0.0, 1.0);

  movie last_selected;

  for (int i = 0; i < num_movies; i++)
  {
    // Tempo total atingido
    if (total_time >= 24)
      return;

    double random_prob = distribution_real(engine);

    // Se P > 25%, escolhemos um filme ao acaso
    if (random_prob > prob)
    {
      uniform_int_distribution<int> distribution_int(i, num_movies - 1);
      int random_index = distribution_int(engine); // sorteia um índice

      // Se ainda há vaga por categoria e horário, adiciona
      if (max_cat[movies[random_index].category] > 0 && has_time_available(times_available, movies[random_index]))
      {
        solution.push_back(movies[random_index]);
        update_availability_list(times_available, movies[random_index]);

        max_cat[movies[random_index].category]--;
        total_time += movies[random_index].duration;
        last_selected = movies[random_index];
        i--;
      }
    }

    // Se P < 25%, prossegue com a heurística
    else
    {
      // Se há vaga na categoria e tempo, adiciona
      if (has_time_available(times_available, movies[i]) && max_cat[movies[i].category] > 0)
      {
        solution.push_back(movies[i]);
        update_availability_list(times_available, movies[i]);

        max_cat[movies[i].category]--;
        total_time += movies[i].duration;
        last_selected = movies[i];
      }
    }
  }
}

int main(int argc, char *argv[])
{
  string file_name = argv[1];
  json output_json;

  int num_movies;     // Número total de filmes
  int num_categories; // Número total de categorias
  int total_time = 0; // tempo total dos filmes selecionados
  int exec_time = 0;  // tempo de execução do algoritmo

  cin >> num_movies;
  cin >> num_categories;

  vector<movie> movies_selected;

  chrono::steady_clock::time_point start_exec = chrono::steady_clock::now();
  aleatorio(movies_selected, total_time, num_categories, num_movies);
  chrono::steady_clock::time_point end_exec = chrono::steady_clock::now();

  exec_time = chrono::duration_cast<chrono::microseconds>(end_exec - start_exec).count();

  cout << "TEMPO DE EXECUÇÃO: " << exec_time << endl;
  cout << "TEMPO DE TELA: " << total_time << endl;
  cout << "FILMES SELECIONADOS COM ALEATORIEDADE" << endl;

  for (auto &i : movies_selected)
  {
    cout << "ID: " << i.id << ", categoria: " << i.category << ", starts at: " << i.begin << ", ends at: " << i.end << endl;
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