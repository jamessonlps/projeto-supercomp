#ifndef FUNCTIONS_H_
#define FUNCTIONS_H_

#include <iostream>
#include <vector>
#include <map>
#include <cassert>
#include <algorithm>
#include <random>

using namespace std;

struct movie
{
  int id;
  int begin;
  int end;
  int category;
  int duration;
};

/**
 * @brief Preenche o dicionário com categorias e máximo de filmes
 * @param categories Dicionário que mapeia categoria e seu máximo de filmes
 * @param num_categories Total de categorias
 */
void fetch_categories(map<int, int> &categories, int num_categories);

/**
 * @brief Populates the movie vector with the input data.
 * @param movies Movies vector
 * @param num_movies Number of movies to be inserted
 */
void fetch_movies(vector<movie> &movies, int num_movies);

/**
 * @brief Ordena os filmes por horário de término
 * @param movies Vetor de filmes
 */
void order_movies_by_end_ascending(vector<movie> &movies);

/**
 * @brief Verifica se há vaga de horário para o filme selecionado
 * @param times_avaliable Lista de horários disponíveis
 * @param m Filme selecionado
 * @return true se há tempo disponível, false caso contrário
 */
bool has_time_available(map<int, bool> &times_avaliable, movie m);

/**
 * @brief Atualiza horários disponíveis
 * @param times_avaliable Dicionário de horários disponíveis
 * @param m Filme inserido
 */
void update_availability_list(map<int, bool> &times_avaliable, movie m);

/**
 * @brief Inicializa horários disponíveis
 * @param times_avaliable Dicionário de horários disponíveis
 */
void init_availability_list(map<int, bool> &times_avaliable);

#endif // FUNCTIONS_H_