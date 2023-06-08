// Geral
#include <iostream>
#include <omp.h>
#include <cmath>
#include <iomanip>
#include <cstdlib>
#include <algorithm>
#include <vector>
#include <string>
#include <chrono>
#include <random>
#include <map>
#include <bitset>

// Para thrust
#include <thrust/sort.h>
#include <thrust/reduce.h>
#include <thrust/device_vector.h>
#include <thrust/host_vector.h>
#include <thrust/transform.h>
#include <thrust/functional.h>
#include <thrust/random.h>
#include <thrust/generate.h>
#include <thrust/transform_reduce.h>
#include <thrust/iterator/counting_iterator.h>

using namespace std;

struct movie
{
  int id;
  int begin;
  int end;
  int category;
  int duration;
};

struct return_gpu
{
  int num_movies_selected;
  int screen_time;
};

void fetch_movies(vector<movie> &movies, int num_movies)
{
  for (int i = 0; i < num_movies; i++)
  {
    movie new_movie;

    new_movie.id = i;
    cin >> new_movie.begin;
    cin >> new_movie.end;
    cin >> new_movie.category;

    if (new_movie.end < new_movie.begin)
    {
      new_movie.duration = 24 - new_movie.begin + new_movie.end;
    }
    else
    {
      new_movie.duration = new_movie.end - new_movie.begin;
    }

    movies[i] = new_movie;
  }
}

struct customized_operator
{
  int num_movies;
  movie *movies;
  int *max_by_cat;
  int num_categories;

  customized_operator(
      int _num_movies,
      movie *_movies,
      int *_max_by_cat,
      int _num_categories)
      : num_movies(_num_movies),
        movies(_movies),
        max_by_cat(_max_by_cat),
        num_categories(_num_categories){};

  __device__ int operator()(const int &movies_combination_id) const
  { // movies_combination_id means the movies that are selected

    bool time_scheduled[24]; // Store if a time slot is already scheduled
    for (int t = 0; t < 24; t++)
    {
      time_scheduled[t] = false;
    }

    int max_by_cat_copy[26]; // Store the max_by_cat in a vector
    for (int i = 0; i < num_categories; i++)
    {
      max_by_cat_copy[i] = max_by_cat[i];
    }

    int num_movies_added = 0;

    for (int i = 0; i < num_movies; i++)
    {
      movie movie_i = movies[i];

      if (num_movies_added >= 24)
        return -1;

      if ((movies_combination_id & (1 << i)) && (max_by_cat_copy[movie_i.category - 1] > 0))
      {
        if (movie_i.begin > movie_i.end)
        {
          // Check if required slots are available for start interval (begin -> 24)
          for (int t = movie_i.begin; t < 24; t++)
          {
            if (time_scheduled[t])
              return -1;
          }
          // Check if required slots are available for end interval (0 -> end)
          for (int t = 0; t < movie_i.end; t++)
          {
            if (time_scheduled[t])
              return -1;
          }

          // Add movie to slots (begin -> 24)
          for (int t = movie_i.begin; t < 24; t++)
          {
            time_scheduled[t] = true;
          }
          // Add movie to slots (0 -> end)
          for (int t = 0; t < movie_i.end; t++)
          {
            time_scheduled[t] = true;
          }

          num_movies_added++;
          max_by_cat_copy[movie_i.category - 1]--;
        }

        else
        {
          // Check if required slots are available for interval (begin -> end)
          for (int t = movie_i.begin; t < movie_i.end; t++)
          {
            if (time_scheduled[t])
              return -1;
          }

          // Add movie to slots (begin -> end)
          for (int t = movie_i.begin; t < movie_i.end; t++)
          {
            time_scheduled[t] = true;
          }

          num_movies_added++;
          max_by_cat_copy[movie_i.category - 1]--;
        }
      }
    }

    return num_movies_added;
  }
};

/**
 * @brief Dynamic programming algorithm for GPU. How this works:
 *
 * A vector with all movies is created (movies_gpu).
 *
 * Then, a vector with all possible movie combinations is created: movie_combinations_gpu.
 * This vector is filled with the number of movies that can be scheduled for each combination.
 *
 * The number of movies that can be scheduled for each combination is calculated by the unary operator customized_operator.
 *
 * @param movies A vector with all movies
 * @param max_by_cat A map with the maximum number of movies per category
 * @param num_categories Number of categories
 * @param num_movies Number of movies
 */
void dynamic_program_gpu(vector<movie> &movies, vector<int> &max_by_cat, int num_categories, int num_movies, return_gpu &solution)
{
  unsigned long int num_combinations = pow(2, num_movies); // Number of possible combinations

  thrust::device_vector<movie> movies_gpu(movies);                     // Vector with all movies in GPU
  thrust::device_vector<int> max_by_cat_gpu(max_by_cat);               // Vector with max_by_cat in GPU
  thrust::device_vector<int> movie_combinations_gpu(num_combinations); // 2 ^ num_movies

  thrust::counting_iterator<int> counter(0); // 2 ^ num_movies (for movie_combinations_gpu)

  thrust::transform(
      counter,                        // Start of input
      counter + num_combinations,     // End of input
      movie_combinations_gpu.begin(), // Output
      customized_operator(
          num_movies,                                      // Number of movies
          thrust::raw_pointer_cast(movies_gpu.data()),     // Pointer to movies in GPU
          thrust::raw_pointer_cast(max_by_cat_gpu.data()), // Pointer to max_by_cat in GPU
          num_categories                                   // Number of categories
          )                                                // Unary Operator
  );

  // Find the maximum element in movie_combinations_gpu
  auto max_element_it = thrust::max_element(movie_combinations_gpu.begin(), movie_combinations_gpu.end());

  // Calculate the index of the maximum element
  int max_element_index = thrust::distance(movie_combinations_gpu.begin(), max_element_it);

  // Obtain the value of the maximum element (number of movies that can be scheduled)
  int max_element_value = *max_element_it;

  bitset<30> bitset(max_element_index);
  int screen_time = 0;

  for (int i = 0; i < num_movies; i++)
  {
    if (bitset[i])
    {
      screen_time += movies[i].duration;
    }
  }

  solution = {max_element_value, screen_time};
}

int main(int argc, char *argv[])
{
  int num_movies;
  int num_categories;

  cin >> num_movies >> num_categories;

  vector<movie> movies(num_movies);
  vector<int> max_by_category(num_categories);

  for (int i = 0; i < num_categories; i++)
  {
    int limit;
    cin >> limit;
    max_by_category[i] = limit;
  }

  fetch_movies(movies, num_movies);

  return_gpu solution;

  auto start_exec = chrono::high_resolution_clock::now();
  dynamic_program_gpu(movies, max_by_category, num_categories, num_movies, solution);
  auto end_exec = chrono::high_resolution_clock::now();
  auto exec_time = chrono::duration_cast<chrono::milliseconds>(end_exec - start_exec).count();

  // Print number of movies
  cout << num_movies << endl;

  // Print number of categories
  cout << num_categories << endl;

  // Print number of movies selected
  cout << solution.num_movies_selected << endl;

  // Print execution time
  cout << exec_time << endl;

  // Print screen time
  cout << solution.screen_time << endl;

  return 0;
}