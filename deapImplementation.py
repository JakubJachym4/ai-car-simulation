import random
import numpy as np
import pygame
from deap import base, creator, tools, algorithms

# Stałe
WIDTH = 1920
HEIGHT = 1080
CAR_SIZE_X = 60
CAR_SIZE_Y = 60
BORDER_COLOR = (255, 255, 255, 255)

# Klasyfikator dla osobników
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Reprezentacja genotypu: lista wag dla sieci neuronowej (prosta sieć z 5 wejściami i 3 wyjściami)
NUM_WEIGHTS = (5 + 1) * 3  # 5 wejść, 3 wyjścia, plus biasy
toolbox.register("attr_float", random.uniform, -1.0, 1.0)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=NUM_WEIGHTS)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Funkcja fitness: ocena sieci na podstawie przejechanej odległości
def evaluate(individual):
    weights = np.array(individual).reshape((5 + 1, 3))  # Przekształcenie na macierz wag
    car = Car(weights)
    return (car.simulate(),)  # Funkcja symulacji zwraca przejechaną odległość

# Operatory genetyczne
toolbox.register("mate", tools.cxTwoPoint)  # Krzyżowanie dwupunktowe
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.1)  # Mutacja Gaussa
toolbox.register("select", tools.selTournament, tournsize=3)  # Selekcja turniejowa
toolbox.register("evaluate", evaluate)

# Klasa Car z uproszczonym sterowaniem
class Car:
    def __init__(self, weights):
        self.weights = weights
        self.position = [830, 920]
        self.angle = 0
        self.speed = 20
        self.alive = True
        self.distance = 0

    def simulate(self):
        # Prosta symulacja ruchu pojazdu
        for _ in range(500):  # Maksymalna liczba kroków
            if not self.alive:
                break
            self.update()
        return self.distance

    def update(self):
        # Symulacja przesuwania pojazdu i sprawdzania kolizji
        self.distance += self.speed
        if self.distance > 1000:  # Zakładany limit odległości
            self.alive = False

# Główna funkcja ewolucji
def main():
    population = toolbox.population(n=50)  # Rozmiar populacji
    generations = 50  # Liczba generacji

    # Algorytm ewolucyjny DEAP
    result = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=generations, verbose=True)
    return result

if __name__ == "__main__":
    main()
