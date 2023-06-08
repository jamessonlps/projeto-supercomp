import subprocess
import json
import numpy as np
import matplotlib.pyplot as plt
import os

class Knapsack():
  def __init__(self) -> None:
    self.fix_movie = 21     # Número de filmes no teste 1
    self.fix_category = 4   # Número de categorias no teste 2
    self.fix_threads = 4    # Número de threads no teste 3

    self.n_movies = np.arange(10, 31, 1) # array com número de filmes
    self.n_cats = np.arange(3, 16, 1)    # array com número de categorias
    self.n_threads = np.arange(1, 9, 1)  # array com número de threads

    self.results_t1_gulosa = None # resultados experimento t1 para gulosa
    self.results_t2_gulosa = None # resultados experimento t2 para gulosa

    self.results_t1_aleatoria = None # resultados experimento t1 para aleatória
    self.results_t2_aleatoria = None # resultados experimento t2 para aleatória

    self.results_t1_openmp = None # resultados experimento t1 para openmp
    self.results_t2_openmp = None # resultados experimento t2 para openmp
    self.results_t3_openmp = None # resultados experimento t3 para openmp


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


  def _generate_outputs(self, heuristic: str):
    """
    Gera os arquivos de output para as heurísticas dos testes 1 e 2

    Args:
      heuristic (str): nome da heurística a ser executada

    Returns:
      output_dict_t1 (dict): dicionário com os resultados do teste 1
      output_dict_t2 (dict): dicionário com os resultados do teste 2
    """

    # Gera resultados do teste 1 => Número de filmes é fixo
    list_files_t1 = os.listdir("./inputs/test1")
    
    output_dict_t1 = {
      "num_movies": [],
      "num_categories": [],
      "num_movies_selected": [],
      "exec_time": [],
      "screen_time": []
    }
    
    i = 0
    for input_file in list_files_t1:
      with open(f"./inputs/test1/{input_file}") as file:
        proc = subprocess.run(
          [f'./{heuristic}'],
          input=file.read(),
          text=True,
          capture_output=True
        )
      i += 1
      output_list = [float(x) for x in proc.stdout.strip().split()]

      output_dict_t1["num_movies"].append(output_list[0])
      output_dict_t1["num_categories"].append(output_list[1])
      output_dict_t1["num_movies_selected"].append(output_list[2])
      output_dict_t1["exec_time"].append(output_list[3])
      output_dict_t1["screen_time"].append(output_list[4])

    self.results_t1_gulosa = output_dict_t1
    with open(f"./outputs/{heuristic}/{heuristic}-test1-out.json", "w+") as file:
      json.dump(output_dict_t1, file, indent=2)
    
    # Gera resultados do teste 2 => Número de categorias é fixo
    list_files_t2 = os.listdir("./inputs/test2")

    output_dict_t2 = {
      "num_movies": [],
      "num_categories": [],
      "num_movies_selected": [],
      "exec_time": [],
      "screen_time": []
    }

    i = 0
    for input_file in list_files_t2:
      with open(f"./inputs/test2/{input_file}") as file:
        proc = subprocess.run(
          [f'./{heuristic}'],
          input=file.read(),
          text=True,
          capture_output=True
        )
      i += 1
      output_list = [float(x) for x in proc.stdout.strip().split()]

      output_dict_t2["num_movies"].append(output_list[0])
      output_dict_t2["num_categories"].append(output_list[1])
      output_dict_t2["num_movies_selected"].append(output_list[2])
      output_dict_t2["exec_time"].append(output_list[3])
      output_dict_t2["screen_time"].append(output_list[4])

    self.results_t2_gulosa = output_dict_t2
    with open(f"./outputs/{heuristic}/{heuristic}-test2-out.json", "w+") as file:
      json.dump(output_dict_t2, file, indent=2)
    
    return output_dict_t1, output_dict_t2


  def _generate_openmp_outputs(self):
    """
    Gera os arquivos de output para a heurística do teste 1 com openmp
    """

    # Gera resultados do teste 1 => Número de filmes é fixo
    list_files_t1 = os.listdir("./inputs/test1")
    
    output_dict_t1 = {
      "num_movies": [],
      "num_categories": [],
      "num_threads": [],
      "num_movies_selected": [],
      "exec_time": [],
      "screen_time": [],
    }

    i = 0
    for input_file in list_files_t1:
      with open(f"./inputs/test1/{input_file}") as file:
        proc = subprocess.run(
          [f'./openmp', f"{self.fix_threads}"],
          input=file.read(),
          text=True,
          capture_output=True
        )
      i += 1
      output_list = [float(x) for x in proc.stdout.strip().split()]

      output_dict_t1["num_movies"].append(output_list[0])
      output_dict_t1["num_categories"].append(output_list[1])
      output_dict_t1["num_threads"].append(output_list[2])
      output_dict_t1["num_movies_selected"].append(output_list[3])
      output_dict_t1["exec_time"].append(output_list[4])
      output_dict_t1["screen_time"].append(output_list[5])

    self.results_t1_openmp = output_dict_t1
    with open(f"./outputs/openmp/openmp-test1-out.json", "w+") as file:
      json.dump(output_dict_t1, file, indent=2)
    
    # Gera resultados do teste 2 => Número de categorias é fixo
    list_files_t2 = os.listdir("./inputs/test2")

    output_dict_t2 = {
      "num_movies": [],
      "num_categories": [],
      "num_threads": [],
      "num_movies_selected": [],
      "exec_time": [],
      "screen_time": [],
    }

    i = 0
    for input_file in list_files_t2:
      with open(f"./inputs/test2/{input_file}") as file:
        proc = subprocess.run(
          [f'./openmp', f"{self.fix_threads}"],
          input=file.read(),
          text=True,
          capture_output=True
        )
      i += 1
      output_list = [float(x) for x in proc.stdout.strip().split()]

      output_dict_t2["num_movies"].append(output_list[0])
      output_dict_t2["num_categories"].append(output_list[1])
      output_dict_t2["num_threads"].append(output_list[2])
      output_dict_t2["num_movies_selected"].append(output_list[3])
      output_dict_t2["exec_time"].append(output_list[4])
      output_dict_t2["screen_time"].append(output_list[5])

    self.results_t2_openmp = output_dict_t2
    with open(f"./outputs/openmp/openmp-test2-out.json", "w+") as file:
      json.dump(output_dict_t2, file, indent=2)

    # Gera resultados do teste 3 => Varia-se número de threads
    output_dict_t3 = {
      "num_movies": [],
      "num_categories": [],
      "num_threads": [],
      "num_movies_selected": [],
      "exec_time": [],
      "screen_time": [],
    }

    for n in self.n_threads:
      with open(f"./inputs/test2/input-24-movies.txt") as file:
        proc = subprocess.run(
          [f'./openmp', f"{n}"],
          input=file.read(),
          text=True,
          capture_output=True
        )
      output_list = [float(x) for x in proc.stdout.strip().split()]

      output_dict_t3["num_movies"].append(output_list[0])
      output_dict_t3["num_categories"].append(output_list[1])
      output_dict_t3["num_threads"].append(output_list[2])
      output_dict_t3["num_movies_selected"].append(output_list[3])
      output_dict_t3["exec_time"].append(output_list[4])
      output_dict_t3["screen_time"].append(output_list[5])

    self.results_t3_openmp = output_dict_t3
    with open(f"./outputs/openmp/openmp-test3-out.json", "w+") as file:
      json.dump(output_dict_t3, file, indent=2)

    return output_dict_t1, output_dict_t2, output_dict_t3


  def plot_results(self, heuristic: str):
    # results_t1, results_t2 = self._generate_outputs(heuristic=heuristic)

    with open(f"./outputs/{heuristic}/{heuristic}-test1-out.json") as file:
      results_t1 = json.load(file)

    with open(f"./outputs/{heuristic}/{heuristic}-test2-out.json") as file:
      results_t2 = json.load(file)
    
    fig = plt.figure(figsize=(12, 7))
    plt.scatter(results_t1["num_categories"], results_t1["exec_time"])
    plt.xlabel("Número de categorias")
    plt.ylabel("Tempo de execução do algoritmo [ms]")
    plt.title(f"Número de filmes fixo: {self.fix_movie}")
    plt.grid(True)
    plt.savefig(f"./img/{heuristic}/{heuristic}-filmes-fixo.png")
    plt.clf()
    
    plt.scatter(results_t2["num_movies"], results_t2["exec_time"])
    plt.xlabel("Número de filmes")
    plt.ylabel("Tempo de execução do algoritmo [ms]")
    plt.title(f"Número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig(f"./img/{heuristic}/{heuristic}-categ-fixo.png")
    plt.clf()
    
    plt.scatter(results_t1["num_categories"], results_t1["screen_time"])
    plt.xlabel("Número de categorias")
    plt.ylabel("Tempo de tela [h]")
    plt.title(f"Número de filmes fixo: {self.fix_movie}")
    plt.grid(True)
    plt.savefig(f"./img/{heuristic}/{heuristic}-filmes-fixo-tela.png")
    plt.clf()
    
    plt.scatter(results_t2["num_movies"], results_t2["screen_time"])
    plt.xlabel("Número de filmes")
    plt.ylabel("Tempo de tela [h]")
    plt.title(f"Número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig(f"./img/{heuristic}/{heuristic}-categ-fixo-tela.png")
    plt.clf()

    plt.scatter(results_t1["num_categories"], results_t1["num_movies_selected"])
    plt.xlabel("Número de categorias")
    plt.ylabel("Número de filmes selecionados")
    plt.title(f"Número de filmes fixo: {self.fix_movie}")
    plt.grid(True)
    plt.savefig(f"./img/{heuristic}/{heuristic}-filmes-fixo-selecionados.png")
    plt.clf()
    
    plt.scatter(results_t2["num_movies"], results_t2["num_movies_selected"])
    plt.xlabel("Número de filmes")
    plt.ylabel("Número de filmes selecionados")
    plt.title(f"Número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig(f"./img/{heuristic}/{heuristic}-categ-fixo-selecionados.png")
    plt.clf()


  def plot_results_openmp(self):

    with open("./outputs/openmp/openmp-test1-out.json") as file:
      self.results_t1_openmp = json.load(file)
    
    with open("./outputs/openmp/openmp-test2-out.json") as file:
      self.results_t2_openmp = json.load(file)
    
    with open("./outputs/openmp/openmp-test3-out.json") as file:
      self.results_t3_openmp = json.load(file)

    plt.scatter(self.results_t1_openmp["num_categories"], self.results_t1_openmp["exec_time"])
    plt.xlabel("Número de categorias")
    plt.ylabel("Tempo de execução do algoritmo [ms]")
    plt.title(f"Número de filmes fixo: {self.fix_movie}")
    plt.grid(True)
    plt.savefig("./img/openmp/openmp-filmes-fixo.png")
    plt.clf()

    plt.scatter(self.results_t2_openmp["num_movies"], self.results_t2_openmp["exec_time"])
    plt.xlabel("Número de filmes")
    plt.ylabel("Tempo de execução do algoritmo [ms]")
    plt.title(f"Número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig("./img/openmp/openmp-categ-fixo.png")
    plt.clf()

    plt.scatter(self.results_t1_openmp["num_categories"], self.results_t1_openmp["screen_time"])
    plt.xlabel("Número de categorias")
    plt.ylabel("Tempo de tela [h]")
    plt.title(f"Número de filmes fixo: {self.fix_movie}")
    plt.grid(True)
    plt.savefig("./img/openmp/openmp-filmes-fixo-tela.png")
    plt.clf()

    plt.scatter(self.results_t2_openmp["num_movies"], self.results_t2_openmp["screen_time"])
    plt.xlabel("Número de filmes")
    plt.ylabel("Tempo de tela [h]")
    plt.title(f"Número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig("./img/openmp/openmp-categ-fixo-tela.png")
    plt.clf()

    plt.scatter(self.results_t1_openmp["num_categories"], self.results_t1_openmp["num_movies_selected"])
    plt.xlabel("Número de categorias")
    plt.ylabel("Número de filmes selecionados")
    plt.title(f"Número de filmes fixo: {self.fix_movie}") 
    plt.grid(True)
    plt.savefig("./img/openmp/openmp-filmes-fixo-selecionados.png")
    plt.clf()

    plt.scatter(self.results_t2_openmp["num_movies"], self.results_t2_openmp["num_movies_selected"])
    plt.xlabel("Número de filmes")
    plt.ylabel("Número de filmes selecionados")
    plt.title(f"Número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig("./img/openmp/openmp-categ-fixo-selecionados.png")
    plt.clf()

    plt.scatter(self.results_t3_openmp["num_threads"], self.results_t3_openmp["exec_time"])
    plt.xlabel("Número de threads")
    plt.ylabel("Tempo de execução do algoritmo [ms]")
    plt.title(f"Execução para {self.fix_movie} filmes e {self.fix_category} categorias")
    plt.grid(True)
    plt.savefig("./img/openmp/openmp-threads.png")
    plt.clf()


  def plot_results_comparison(self):
    results_t1_aleatoria = None
    results_t1_gulosa = None
    results_t1_openmp = None
    results_t1_gpu = None

    results_t2_aleatoria = None
    results_t2_gulosa = None
    results_t2_openmp = None
    results_t2_gpu = None

    # Testes 1
    with open("./outputs/aleatoria/aleatoria-test1-out.json", "r") as f:
      results_t1_aleatoria = json.load(f)

    with open("./outputs/gulosa/gulosa-test1-out.json", "r") as f:
      results_t1_gulosa = json.load(f)

    with open("./outputs/openmp/openmp-test1-out.json", "r") as f:
      results_t1_openmp = json.load(f)

    with open("./outputs/gpu/gpu-test1-out.json", "r") as f:
      results_t1_gpu = json.load(f)

    # Testes 2
    with open("./outputs/aleatoria/aleatoria-test2-out.json", "r") as f:
      results_t2_aleatoria = json.load(f)

    with open("./outputs/gulosa/gulosa-test2-out.json", "r") as f:
      results_t2_gulosa = json.load(f)
    
    with open("./outputs/openmp/openmp-test2-out.json", "r") as f:
      results_t2_openmp = json.load(f)
    
    with open("./outputs/gpu/gpu-test2-out.json", "r") as f:
      results_t2_gpu = json.load(f)
    
    # Gráfico 1 - Número de categorias vs Tempo de execução
    plt.scatter(results_t1_aleatoria["num_categories"], results_t1_aleatoria["exec_time"], c="r", label="Aleatória", alpha=0.5)
    plt.scatter(results_t1_gulosa["num_categories"], results_t1_gulosa["exec_time"], c="g", label="Gulosa", alpha=0.5)
    plt.scatter(results_t1_openmp["num_categories"], results_t1_openmp["exec_time"], c="b", label="OpenMP", alpha=0.5)
    plt.scatter(results_t1_gpu["num_categories"], results_t1_gpu["exec_time"], c="y", label="GPU", alpha=0.5)
    plt.xlabel("Número de categorias")
    plt.ylabel("Tempo de execução do algoritmo [ms]")
    plt.title(f"Comparação com número de filmes fixo: {self.fix_movie}")
    plt.legend()
    plt.grid(True)
    plt.savefig("./img/compara-filmes-fixo.png")
    plt.clf()

    # Gráfico 2 - Número de filmes vs Tempo de execução
    plt.scatter(results_t2_aleatoria["num_movies"], results_t2_aleatoria["exec_time"], c="r", label="Aleatória", alpha=0.5)
    plt.scatter(results_t2_gulosa["num_movies"], results_t2_gulosa["exec_time"], c="g", label="Gulosa", alpha=0.5)
    plt.scatter(results_t2_openmp["num_movies"], results_t2_openmp["exec_time"], c="b", label="OpenMP", alpha=0.5)
    plt.scatter(results_t2_gpu["num_movies"], results_t2_gpu["exec_time"], c="y", label="GPU", alpha=0.5)
    plt.xlabel("Número de filmes")
    plt.ylabel("Tempo de execução do algoritmo [ms]")
    plt.title(f"Comparação com número de categorias fixo: {self.fix_category}")
    plt.legend()
    plt.grid(True)
    plt.savefig("./img/compara-categ-fixo.png")
    plt.clf()

    # Gráfico 3 - Mesmo do 2 mas sem OPENMP porque distorce
    plt.scatter(results_t2_aleatoria["num_movies"], results_t2_aleatoria["exec_time"], c="r", label="Aleatória", alpha=0.5)
    plt.scatter(results_t2_gulosa["num_movies"], results_t2_gulosa["exec_time"], c="g", label="Gulosa", alpha=0.5)
    plt.scatter(results_t2_gpu["num_movies"], results_t2_gpu["exec_time"], c="y", label="GPU", alpha=0.5)
    plt.xlabel("Número de filmes")
    plt.ylabel("Tempo de execução do algoritmo [ms]")
    plt.title(f"Comparação com número de categorias fixo: {self.fix_category} - sem OPENMP")
    plt.legend()
    plt.grid(True)
    plt.savefig("./img/compara-categ-fixo-sem-openmp.png")
    plt.clf()

    # Gráfico 4 - Número de categorias vs Número de filmes selecionados
    plt.scatter(results_t1_aleatoria["num_categories"], results_t1_aleatoria["num_movies_selected"], c="r", label="Aleatória", alpha=0.7, edgecolors="black", s=50)
    plt.scatter(results_t1_gulosa["num_categories"], results_t1_gulosa["num_movies_selected"], c="g", label="Gulosa", alpha=0.7, edgecolors="black", s=100)
    plt.scatter(results_t1_openmp["num_categories"], results_t1_openmp["num_movies_selected"], c="b", label="OpenMP", alpha=0.7, edgecolors="black", s=150)
    plt.scatter(results_t1_gpu["num_categories"], results_t1_gpu["num_movies_selected"], c="y", label="GPU", alpha=0.7, edgecolors="black", s=200)
    plt.xlabel("Número de categorias")
    plt.ylabel("Número de filmes selecionados")
    plt.title(f"Número total de filmes: {self.fix_movie}")
    plt.legend()
    plt.grid(True)
    plt.savefig("./img/compara-filmes-selecionados.png")
    plt.clf()



  def run(self):
    # Descomente a linha abaixo para gerar novos inputs
    # self.generate_input_files()

    self.plot_results(heuristic="gulosa")
    self.plot_results(heuristic="aleatoria")
    # self.plot_results(heuristic="gpu")

    # self.plot_results_aleatoria()
    # self.plot_results_openmp()
    # self.plot_results_comparison()


if __name__ == "__main__":
  knapsack = Knapsack()
  knapsack.run()