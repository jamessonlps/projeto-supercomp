#include "functions.h"
#include <thrust/host_vector.h>
#include <thrust/device_vector.h>
#include <thrust/functional.h>

using namespace std;

struct unop {
  int num_movies;
  movie *movies;
  int *max_by_cat;

  unop(int _num_movies, movie *_movies, int *_max_by_cat) 
    : num_movies(_num_movies), movies(_movies), max_by_cat(_max_by_cat) {};

  __device__
  int operator() (int movies_combination) {   // movies_combination means the movies that are selected
    bool time_scheduled[24];                  // Store if a time slot is already scheduled
    vector<int> max_by_cat_copy = max_by_cat; // Store the maximum number of movies per category

    for (int t = 0; t < 24; t++) {
      time_scheduled[t] = false;
    }

    int num_movies_added = 0;

    for(int i = 0; i < num_movies; i++) {
      movie movie_i = movies[i];

      if (num_movies_added >= 24) return -1;
      
      if ((movies_combination & (1 << i)) && (max_by_cat_copy[movie_i.category - 1] > 0)) {
        if (movie_i.begin > movie_i.end) {
          // Check if required slots are available for start interval (begin -> 24)
          for (int t = movie_i.begin; t < 24; t++) {
            if (time_scheduled[t]) return -1;
          }
          // Check if required slots are available for end interval (0 -> end)
          for (int t = 0; t < movie_i.end; t++) {
            if (time_scheduled[t]) return -1;
          }

          // Add movie to slots (begin -> 24)
          for (int t = movie_i.begin; t < 24; t++) {
            time_scheduled[t] = true;
          }
          // Add movie to slots (0 -> end)
          for (int t = 0; t < movie_i.end; t++) {
            time_scheduled[t] = true;
          }

          num_movies_added++;
          max_by_cat_copy[movie_i.category - 1]--;
        }

        else {
          // Check if required slots are available for interval (begin -> end)
          for (int t = movie_i.begin; t < movie_i.end; t++) {
            if (time_scheduled[t]) return -1;
          }

          // Add movie to slots (begin -> end)
          for (int t = movie_i.begin; t < movie_i.end; t++) {
            time_scheduled[t] = true;
          }

          num_movies_added++;
          max_by_cat_copy[movie_i.category - 1]--;
        }
      }
    }

    return num_movies_added;
  }
}

/**
 * @brief Dynamic programming algorithm for GPU. How this works:
 * 
 * A vector with all movies is created (movies_gpu). 
 * 
 * Then, a vector with all possible movie combinations is created: movie_combinations_gpu.
 * This vector is filled with the number of movies that can be scheduled for each combination.
 * 
 * The number of movies that can be scheduled for each combination is calculated by the unary operator unop.
 * 
 * @param movies A vector with all movies
 * @param max_by_cat A map with the maximum number of movies per category
 * @param num_categories Number of categories
*/
void dynamic_program_gpu(vector<movie> &movies, map<int, int> &max_by_cat, int num_categories) {
  thrust::device_vector<movie> movies_gpu(movies.size());                   // num_movies
  thrust::device_vector<int> max_by_cat_gpu(num_categories);                // num_categories
  thrust::device_vector<int> movie_combinations_gpu(pow(movies.size(), 2)); // num_movies ^ 2
  thrust::couting_iterator<int> counter(0);                                 // num_movies ^ 2 (for movie_combinations_gpu)

  movies_gpu = movies;

  for (int i = 0; i < num_categories; i++) {
    max_by_cat_gpu[i] = max_by_cat[i + 1];
  }

  thrust::transform(
    counter,                                                                  // Start of input
    counter + pow(movies.size(), 2),                                          // End of input
    movie_combinations_gpu.begin(),                                           // Output
    unop(movies.size(), movies_gpu.data().get(), max_by_cat_gpu.data().get()) // Unary Operator
  );

  thrust::host_vector<int> movie_combinations_cpu(movie_combinations_gpu.size());
  thrust::copy(movie_combinations_gpu.begin(), movie_combinations_gpu.end(), movie_combinations_cpu.begin());

  int max_movies = 0;
  for (int i = 0; i < movie_combinations_cpu.size(); i++) {
    if (movie_combinations_cpu[i] > max_movies) {
      max_movies = movie_combinations_cpu[i];
    }
  }

  // get movies from best solution
  vector<movie> best_movies;


  cout << "Maximum number of movies: " << max_movies << endl;
}


int main(int argc, char *argv[]) {
  int num_movies;
  int num_categories;

  cin >> num_movies >> num_categories;

  vector<movie> movies(num_movies);
  map<int, int> max_by_category;

  fetch_categories(max_by_category, num_categories);
  fetch_movies(movies, num_movies);

  dynamic_program_gpu(movies, max_by_category, num_categories);

  return 0;
}