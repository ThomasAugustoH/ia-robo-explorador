from environment import Environment


def main():
    environment = Environment()
    total_passos, min_passos, max_passos, tentativas = 0, 999, 0, 1000

    for i in range(tentativas):
        passos = environment.run_simulation(10)
        print(passos)
        total_passos += passos
        min_passos = min(min_passos, passos)
        max_passos = max(max_passos, passos)
    
    print(f"Passos redundantes: {total_passos}. Mínimo: {min_passos}. Máximo: {max_passos}. Média: {total_passos / tentativas}")

if __name__ == "__main__":
    main()