#include "functions.h"

void fetch_categories(map<int, int> &categories, int num_categories)
{
  for (int i = 0; i < num_categories; i++)
  {
    int limit;
    cin >> limit;
    categories[i + 1] = limit;
  }
}

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

void order_movies_by_end_ascending(vector<movie> &movies)
{
  sort(movies.begin(), movies.end(), [](movie &a, movie &b)
       { return a.end < b.end; });
}

bool has_time_available(map<int, bool> &times_avaliable, movie m)
{
  // Quando o filme começa em um dia e termina em outro
  if (m.begin > m.end)
  {
    // Checa horários de begin até 23
    for (int i = m.begin; i <= 23; i++)
    {
      if (times_avaliable[i] == false)
      {
        return false;
      }
    }

    // Checa horários de 0 até end
    for (int j = 0; j <= m.end; j++)
    {
      if (j != m.end && times_avaliable[j] == false)
      {
        return false;
      }
    }
    return true;
  }

  for (int i = m.begin; i < m.end; i++)
  {
    if (times_avaliable[i] == false)
    {
      return false;
    }
  }
  return true;
}

void update_availability_list(map<int, bool> &times_avaliable, movie m)
{
  // Quando o filme começa em um dia e termina em outro
  if (m.begin > m.end)
  {
    // Preenche de m.begin até 23
    for (int i = m.begin; i < 24; i++)
    {
      times_avaliable[i] = false;
    }

    if (m.end > 0)
    {
      for (int i = 0; i < m.end; i++)
      {
        times_avaliable[i] = false;
      }
    }
  }

  for (int i = m.begin; i < m.end; i++)
  {
    times_avaliable[i] = false;
  }
}

void init_availability_list(map<int, bool> &times_avaliable)
{
  for (int i = 0; i < 24; i++)
  {
    times_avaliable[i] = true;
  }
}