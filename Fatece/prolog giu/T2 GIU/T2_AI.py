import random

# A classe Board representa um tabuleiro de xadrez com 8 rainhas.
class Board:

    # O construtor da classe permite especificar a posição inicial das rainhas no tabuleiro.
    # Se nenhuma posição for especificada, posições aleatórias serão geradas.
    def __init__(self, positions=None):
        self.positions = positions if positions else self.random_positions()
        self.fitness = self.calculate_fitness()

    # Esta função gera uma lista de posições aleatórias para as rainhas.
    # random.randint(0, 7) é usado para gerar uma posição aleatória (entre 0 e 7) para cada uma das 8 rainhas.
    def random_positions(self):
        return [random.randint(0, 7) for _ in range(8)]

    # Esta função calcula a "aptidão" da configuração atual das rainhas, que é o número de ataques entre as rainhas.
    # Dois loops for são usados para comparar cada par de rainhas.
    # A função retorna o número total de ataques.
    def calculate_fitness(self):
        attacks = 0
        for i in range(8):
            for j in range(i + 1, 8):
                if self.positions[i] == self.positions[j] or \
                   abs(self.positions[i] - self.positions[j]) == j - i:
                    attacks += 1
        return attacks

    # Esta função converte as posições das rainhas para a notação de xadrez.
    def get_chess_notation(self):
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return [f"{columns[col]}{row + 1}" for col, row in enumerate(self.positions)]

# Esta função cria uma população inicial de tabuleiros.
def generate_initial_population(size):
    return [Board() for _ in range(size)]

# Esta função seleciona um tabuleiro da população usando um torneio.
def selection(population):
    tournament = random.sample(population, 5)
    return min(tournament, key=lambda board: board.fitness)

# Esta função realiza o cruzamento (crossover) entre dois tabuleiros (pais) para gerar dois novos tabuleiros (filhos).
def crossover(parent1, parent2):
    crossover_point = random.randint(1, 7)
    child1_positions = parent1.positions[:crossover_point] + parent2.positions[crossover_point:]
    child2_positions = parent2.positions[:crossover_point] + parent1.positions[crossover_point:]
    return Board(child1_positions), Board(child2_positions)

# Esta função realiza a mutação em um tabuleiro com uma determinada taxa de mutação.
def mutate(board, mutation_rate):
    if random.random() < mutation_rate:
        mutate_point = random.randint(0, 7)
        new_value = random.randint(0, 7)
        board.positions[mutate_point] = new_value
        board.fitness = board.calculate_fitness()

# Esta é a função principal que executa o algoritmo genético.
def genetic_algorithm(mutation_rate=0.1):
    # Gerar tamanho da população e número máximo de gerações aleatoriamente
    population_size = random.randint(50, 400)  # Exemplo de intervalo para a população
    max_generations = random.randint(500, 4000)  # Exemplo de intervalo para as gerações

    population = generate_initial_population(population_size)
    generation = 0
    best_solution = min(population, key=lambda board: board.fitness)

    while generation < max_generations:
        population = sorted(population, key=lambda board: board.fitness)
        if population[0].fitness == 0:
            best_solution = population[0]
            break
        
        new_population = []
        elite = population[:10]
        new_population.extend(elite)

        for _ in range((population_size - len(elite)) // 2):
            parent1 = selection(population)
            parent2 = selection(population)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.extend([child1, child2])
        
        population = new_population
        generation += 1

        current_best = min(population, key=lambda board: board.fitness)
        if current_best.fitness < best_solution.fitness:
            best_solution = current_best

    return best_solution, generation, population_size, max_generations

# Executar o algoritmo genético com parâmetros ajustáveis
solution, generations, population_size, max_generations = genetic_algorithm(mutation_rate=0.1)

# Exibir a solução
print("Solução encontrada:")
print("Posições das rainhas:", solution.get_chess_notation())
print("Número de gerações:", generations)
print("Tamanho da população:", population_size)
print("Máximo de gerações:", max_generations)
print("Fitness da solução:", solution.fitness)
