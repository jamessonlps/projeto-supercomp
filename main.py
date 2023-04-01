import subprocess
import json
import numpy as np
import matplotlib.pyplot as plt
import os

class Knapsack():
  def __init__(self) -> None:
    self.fix_movie = 100    # Número de filmes no teste 1
    self.fix_category = 20  # Número de categorias no teste 2
    
    self.n_movies = np.arange(20, 1020, 20) # array com número de filmes
    self.n_cats = np.arange(2, 30, 1) # array com número de categorias

    self.results_t1_gulosa = None # resultados experimento t1 para gulosa
    self.results_t2_gulosa = None # resultados experimento t2 para gulosa

    self.results_t1_aleatoria = None # resultados experimento t1 para aleatória
    self.results_t2_aleatoria = None # resultados experimento t2 para aleatória


  def generate_input_files(self) -> None:
    """
    Gera os arquivos de input para as heurísticas dos testes 1 e 2
    """
    
    # Gera arquivos do teste 1 => Número de filmes é fixo
    for cat in self.n_cats:
      subprocess.run(
        ['./gerador', f"{self.fix_movie}", f"{cat}", f"./inputs/test1/input-{cat}-categories.txt"], 
        capture_output=True
      )
    
    # Gera arquivos do teste 2 => Número de categorias é fixo
    for mov in self.n_movies:
      subprocess.run(
        ['./gerador', f"{mov}", f"{self.fix_category}", f"./inputs/test2/input-{mov}-movies.txt"], 
        capture_output=True
      )
    print("Arquivos de input gerados!")


  def _generate_gulosa_outputs(self):
    """
    Executa a heurística gulosa para cada input. São gerados 2
    outputs: 1 json com as informações principais que são usadas
    para plotar os gráficos e um arquivo de texto para análise.
    """
    # Gera resultados do teste 1 => Número de filmes é fixo
    list_files_t1 = os.listdir("./inputs/test1")
    i = 0
    for input_file in list_files_t1:
      with open(f"./inputs/test1/{input_file}") as file:
        proc = subprocess.run(
          ['./gulosa', f'./outputs/gulosa/test1/gulosa-out-{i}.json'],
          input=file.read(),
          text=True,
          capture_output=True
        )
      with open(f"./outputs/logs/gulosa-test1-{i}.txt", "w+") as file:
        file.write(proc.stdout)
      i += 1
    
    # Gera resultados do teste 2 => Número de categorias é fixo
    list_files_t2 = os.listdir("./inputs/test2")
    i = 0
    for input_file in list_files_t2:
      with open(f"./inputs/test2/{input_file}") as file:
        proc = subprocess.run(
          ['./gulosa', f'./outputs/gulosa/test2/gulosa-out-{i}.json'],
          input=file.read(),
          text=True,
          capture_output=True
        )
      with open(f"./outputs/logs/gulosa-test2-{i}.txt", "w+") as file:
        file.write(proc.stdout)
      i += 1
    print(f"Executados {i} arquivos de input para heurística gulosa")


  def _generate_aleatoria_outputs(self):
    # Gera resultados do teste 1 => Número de filmes é fixo
    list_files_t1 = os.listdir("./inputs/test1")
    i = 0
    for input_file in list_files_t1:
      with open(f"./inputs/test1/{input_file}") as file:
        proc = subprocess.run(
          ['./aleatorio', f'./outputs/aleatoria/test1/aleatoria-out-{i}.json'],
          input=file.read(),
          text=True,
          capture_output=True
        )
      with open(f"./outputs/logs/aleatoria-test1-{i}.txt", "w+") as file:
        file.write(proc.stdout)
      i += 1
    
    # Gera resultados do teste 2 => Número de categorias é fixo
    list_files_t2 = os.listdir("./inputs/test2")
    i = 0
    for input_file in list_files_t2:
      with open(f"./inputs/test2/{input_file}") as file:
        proc = subprocess.run(
          ['./aleatorio', f'./outputs/aleatoria/test2/aleatoria-out-{i}.json'],
          input=file.read(),
          text=True,
          capture_output=True
        )
      with open(f"./outputs/logs/aleatoria-test2-{i}.txt", "w+") as file:
        file.write(proc.stdout)
      i += 1


  def _get_results_gulosa(self):
    self._generate_gulosa_outputs()

    # Resultados para o teste 1
    files_json_gulosa_t1 = os.listdir("./outputs/gulosa/test1")
    results = {
      "exec_time": [], 
      "screen_time": [], 
      "num_movies": [], 
      "num_categories": []
    }
    for file in files_json_gulosa_t1:
      with open(f"./outputs/gulosa/test1/{file}", "r") as f:
        data = json.load(f)
        results["exec_time"].append(data["exec_time"] / 1000000)
        results["screen_time"].append(data["screen_time"])
        results["num_movies"].append(data["num_movies"])
        results["num_categories"].append(data["num_categories"])
    self.results_t1_gulosa = results

    # Resultados para o teste 2
    files_json_gulosa_t2 = os.listdir("./outputs/gulosa/test2")
    results = {
      "exec_time": [], 
      "screen_time": [], 
      "num_movies": [], 
      "num_categories": []
    }
    for file in files_json_gulosa_t2:
      with open(f"./outputs/gulosa/test2/{file}", "r") as f:
        data = json.load(f)
        results["exec_time"].append(data["exec_time"] / 1000000)
        results["screen_time"].append(data["screen_time"])
        results["num_movies"].append(data["num_movies"])
        results["num_categories"].append(data["num_categories"])
    self.results_t2_gulosa = results


  def _get_results_aleatoria(self):
    self._generate_aleatoria_outputs()

    # Resultados para o teste 1
    files_json_aleatoria_t1 = os.listdir("./outputs/aleatoria/test1")
    results = {
      "exec_time": [], 
      "screen_time": [], 
      "num_movies": [], 
      "num_categories": []
    }
    for file in files_json_aleatoria_t1:
      with open(f"./outputs/aleatoria/test1/{file}", "r") as f:
        data = json.load(f)
        results["exec_time"].append(data["exec_time"] / 1000000)
        results["screen_time"].append(data["screen_time"])
        results["num_movies"].append(data["num_movies"])
        results["num_categories"].append(data["num_categories"])
    self.results_t1_aleatoria = results

    # Resultados para o teste 2
    files_json_aleatoria_t2 = os.listdir("./outputs/aleatoria/test2")
    results = {
      "exec_time": [], 
      "screen_time": [], 
      "num_movies": [], 
      "num_categories": []
    }
    for file in files_json_aleatoria_t2:
      with open(f"./outputs/aleatoria/test2/{file}", "r") as f:
        data = json.load(f)
        results["exec_time"].append(data["exec_time"] / 1000000)
        results["screen_time"].append(data["screen_time"])
        results["num_movies"].append(data["num_movies"])
        results["num_categories"].append(data["num_categories"])
    self.results_t2_aleatoria = results


  def plot_results_gulosa(self):
    self._get_results_gulosa()
    
    fig = plt.figure(figsize=(12, 7))
    plt.scatter(self.results_t1_gulosa["num_categories"], self.results_t1_gulosa["exec_time"])
    plt.xlabel("Número de categorias")
    plt.ylabel("Tempo de execução do algoritmo [s]")
    plt.title(f"Número de filmes fixo: {self.fix_movie}")
    plt.grid(True)
    plt.savefig("./img/gulosa-filmes-fixo.png")
    plt.clf()
    
    plt.scatter(self.results_t2_gulosa["num_movies"], self.results_t2_gulosa["exec_time"])
    plt.xlabel("Número de filmes")
    plt.ylabel("Tempo de execução do algoritmo [s]")
    plt.title(f"Número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig("./img/gulosa-categ-fixo.png")
    plt.clf()


  def plot_results_aleatoria(self):
    self._get_results_aleatoria()
    
    plt.scatter(self.results_t1_aleatoria["num_categories"], self.results_t1_aleatoria["exec_time"])
    plt.xlabel("Número de categorias")
    plt.ylabel("Tempo de execução do algoritmo [s]")
    plt.title(f"Número de filmes fixo: {self.fix_movie}")
    plt.grid(True)
    plt.savefig("./img/aleatoria-filmes-fixo.png")
    plt.clf()
    
    plt.scatter(self.results_t2_aleatoria["num_movies"], self.results_t2_aleatoria["exec_time"])
    plt.xlabel("Número de filmes")
    plt.ylabel("Tempo de execução do algoritmo [s]")
    plt.title(f"Número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig("./img/aleatoria-categ-fixo.png")
    plt.clf()
  

  def plot_results_comparison(self):
    plt.scatter(self.results_t1_aleatoria["num_categories"], self.results_t1_aleatoria["exec_time"], c="r", label="Aleatória")
    plt.scatter(self.results_t1_gulosa["num_categories"], self.results_t1_gulosa["exec_time"], c="g", label="Gulosa")
    plt.xlabel("Número de categorias")
    plt.ylabel("Tempo de execução do algoritmo [s]")
    plt.title(f"Comparação com número de filmes fixo: {self.fix_movie}")
    plt.legend()
    plt.grid(True)
    plt.savefig("./img/compara-filmes-fixo.png")
    plt.clf()

    plt.scatter(self.results_t2_aleatoria["num_movies"], self.results_t2_aleatoria["exec_time"], c="r", label="Aleatória")
    plt.scatter(self.results_t2_gulosa["num_movies"], self.results_t2_gulosa["exec_time"], c="g", label="Gulosa")
    plt.xlabel("Número de filmes")
    plt.ylabel("Tempo de execução do algoritmo [s]")
    plt.title(f"Comparação com número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig("./img/compara-categ-fixo.png")
    plt.clf()


  def run(self):
    # self.generate_input_files()

    self.plot_results_gulosa()
    self.plot_results_aleatoria()
    self.plot_results_comparison()


if __name__ == "__main__":
  knapsack = Knapsack()
  knapsack.run()