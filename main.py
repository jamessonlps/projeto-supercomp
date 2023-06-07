import subprocess
import json
import numpy as np
import matplotlib.pyplot as plt
import os

class Knapsack():
  def __init__(self) -> None:
    self.fix_movie = 25     # Número de filmes no teste 1
    self.fix_category = 4   # Número de categorias no teste 2

    self.n_movies = np.arange(10, 31, 1) # array com número de filmes
    self.n_cats = np.arange(5, 26, 1)    # array com número de categorias

    self.results_t1_gulosa = None # resultados experimento t1 para gulosa
    self.results_t2_gulosa = None # resultados experimento t2 para gulosa

    self.results_t1_aleatoria = None # resultados experimento t1 para aleatória
    self.results_t2_aleatoria = None # resultados experimento t2 para aleatória

    self.results_t1_openmp = None # resultados experimento t1 para openmp
    self.results_t2_openmp = None # resultados experimento t2 para openmp


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
    # Gera resultados do teste 1 => Número de filmes é fixo
    list_files_t1 = os.listdir("./inputs/test1")
    i = 0
    for input_file in list_files_t1:
      with open(f"./inputs/test1/{input_file}") as file:
        proc = subprocess.run(
          ['./openmp', f'./outputs/openmp/test1/openmp-out-{i}.json'],
          input=file.read(),
          text=True,
          capture_output=True
        )
      with open(f"./outputs/logs/openmp-test1-{i}.txt", "w+") as file:
        file.write(proc.stdout)
      i += 1
    
    # Gera resultados do teste 2 => Número de categorias é fixo
    list_files_t2 = os.listdir("./inputs/test2")
    i = 0
    for input_file in list_files_t2:
      with open(f"./inputs/test2/{input_file}") as file:
        proc = subprocess.run(
          ['./openmp', f'./outputs/openmp/test2/openmp-out-{i}.json'],
          input=file.read(),
          text=True,
          capture_output=True
        )
      with open(f"./outputs/logs/openmp-test2-{i}.txt", "w+") as file:
        file.write(proc.stdout)
      i += 1


  def _get_results_openmp(self):
    self._generate_openmp_outputs()

    # Resultados para o teste 1
    files_json_openmp_t1 = os.listdir("./outputs/openmp/test1")
    results = {
      "exec_time": [], 
      "screen_time": [], 
      "num_movies": [], 
      "num_categories": [],
      "num_threads": []
    }
    for file in files_json_openmp_t1:
      with open(f"./outputs/openmp/test1/{file}", "r") as f:
        data = json.load(f)
        results["exec_time"].append(data["exec_time"] / 1000000)
        results["screen_time"].append(data["screen_time"])
        results["num_movies"].append(data["num_movies"])
        results["num_categories"].append(data["num_categories"])
        results["num_threads"].append(data["num_threads"])
    self.results_t1_openmp = results

    # Resultados para o teste 2
    files_json_openmp_t2 = os.listdir("./outputs/openmp/test2")
    results = {
      "exec_time": [], 
      "screen_time": [], 
      "num_movies": [], 
      "num_categories": [],
      "num_threads": []
    }
    for file in files_json_openmp_t2:
      with open(f"./outputs/openmp/test2/{file}", "r") as f:
        data = json.load(f)
        results["exec_time"].append(data["exec_time"] / 1000000)
        results["screen_time"].append(data["screen_time"])
        results["num_movies"].append(data["num_movies"])
        results["num_categories"].append(data["num_categories"])
        results["num_threads"].append(data["num_threads"])
    self.results_t2_openmp = results


  def plot_results(self, heuristic: str):
    results_t1, results_t2 = self._generate_outputs(heuristic=heuristic)
    
    fig = plt.figure(figsize=(12, 7))
    plt.scatter(results_t1["num_categories"], results_t1["exec_time"])
    plt.xlabel("Número de categorias")
    plt.ylabel("Tempo de execução do algoritmo [s]")
    plt.title(f"Número de filmes fixo: {self.fix_movie}")
    plt.grid(True)
    plt.savefig(f"./img/{heuristic}/{heuristic}-filmes-fixo.png")
    plt.clf()
    
    plt.scatter(results_t2["num_movies"], results_t2["exec_time"])
    plt.xlabel("Número de filmes")
    plt.ylabel("Tempo de execução do algoritmo [s]")
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
    self._get_results_openmp()

    plt.scatter(self.results_t1_openmp["num_categories"], self.results_t1_openmp["exec_time"], c="r", label="Aleatória")
    plt.xlabel("Número de categorias")
    plt.ylabel("Tempo de execução do algoritmo [s]")
    plt.title(f"Número de filmes fixo: {self.fix_movie}")
    plt.grid(True)
    plt.savefig("./img/openmp-filmes-fixo.png")
    plt.clf()

    plt.scatter(self.results_t2_openmp["num_movies"], self.results_t2_openmp["exec_time"], c="r", label="Aleatória")
    plt.xlabel("Número de filmes")
    plt.ylabel("Tempo de execução do algoritmo [s]")
    plt.title(f"Número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig("./img/openmp-categ-fixo.png")
    plt.clf()

    plt.scatter(self.results_t1_openmp["num_categories"], self.results_t1_openmp["screen_time"], c="r", label="Aleatória")
    plt.xlabel("Número de categorias")
    plt.ylabel("Tempo de tela [h]")
    plt.title(f"Número de filmes fixo: {self.fix_movie}")
    plt.grid(True)
    plt.savefig("./img/openmp-filmes-fixo-tela.png")
    plt.clf()

    plt.scatter(self.results_t2_openmp["num_movies"], self.results_t2_openmp["screen_time"], c="r", label="Aleatória")
    plt.xlabel("Número de filmes")
    plt.ylabel("Tempo de tela [h]")
    plt.title(f"Número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig("./img/openmp-categ-fixo-tela.png")
    plt.clf()

    plt.scatter(self.results_t1_openmp["num_categories"], self.results_t1_openmp["selected"], c="r", label="Aleatória")
    plt.xlabel("Número de categorias")
    plt.ylabel("Número de filmes selecionados")
    plt.title(f"Número de filmes fixo: {self.fix_movie}") 
    plt.grid(True)
    plt.savefig("./img/openmp-filmes-fixo-selecionados.png")
    plt.clf()

    plt.scatter(self.results_t2_openmp["num_movies"], self.results_t2_openmp["selected"], c="r", label="Aleatória")
    plt.xlabel("Número de filmes")
    plt.ylabel("Número de filmes selecionados")
    plt.title(f"Número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig("./img/openmp-categ-fixo-selecionados.png")
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

    plt.scatter(self.results_t1_aleatoria["num_categories"], self.results_t1_aleatoria["screen_time"], c="r", label="Aleatória")
    plt.scatter(self.results_t1_gulosa["num_categories"], self.results_t1_gulosa["screen_time"], c="g", label="Gulosa")
    plt.xlabel("Número de categorias")
    plt.ylabel("Tempo de tela [h]")
    plt.title(f"Comparação com número de filmes fixo: {self.fix_movie}")
    plt.legend()
    plt.grid(True)
    plt.savefig("./img/compara-filmes-fixo-tela.png")
    plt.clf()

    plt.scatter(self.results_t2_aleatoria["num_movies"], self.results_t2_aleatoria["screen_time"], c="r", label="Aleatória")
    plt.scatter(self.results_t2_gulosa["num_movies"], self.results_t2_gulosa["screen_time"], c="g", label="Gulosa")
    plt.xlabel("Número de filmes")
    plt.ylabel("Tempo de tela [h]")
    plt.title(f"Comparação com número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig("./img/compara-categ-fixo-tela.png")
    plt.clf()

    plt.scatter(self.results_t1_aleatoria["num_categories"], self.results_t1_aleatoria["selected"], c="r", label="Aleatória")
    plt.scatter(self.results_t1_gulosa["num_categories"], self.results_t1_gulosa["selected"], c="g", label="Gulosa")
    plt.xlabel("Número de categorias")
    plt.ylabel("Número de filmes selecionados")
    plt.title(f"Comparação com número de filmes fixo: {self.fix_movie}")
    plt.legend()
    plt.grid(True)
    plt.savefig("./img/compara-filmes-fixo-selecionados.png")
    plt.clf()

    plt.scatter(self.results_t2_aleatoria["num_movies"], self.results_t2_aleatoria["selected"], c="r", label="Aleatória")
    plt.scatter(self.results_t2_gulosa["num_movies"], self.results_t2_gulosa["selected"], c="g", label="Gulosa")
    plt.xlabel("Número de filmes")
    plt.ylabel("Número de filmes selecionados")
    plt.title(f"Comparação com número de categorias fixo: {self.fix_category}")
    plt.grid(True)
    plt.savefig("./img/compara-categ-fixo-selecionados.png")
    plt.clf()


  def run(self):
    # Descomente a linha abaixo para gerar novos inputs
    self.generate_input_files()

    # self.plot_results(heuristic="gulosa")
    # self.plot_results(heuristic="aleatoria")
    # self.plot_results_aleatoria()
    # self.plot_results_openmp()
    # self.plot_results_comparison()


if __name__ == "__main__":
  knapsack = Knapsack()
  knapsack.run()