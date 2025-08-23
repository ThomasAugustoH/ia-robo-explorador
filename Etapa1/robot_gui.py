import tkinter as tk
import threading
import time
from random import randint
from robot import Robot


class RobotGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulação do Robô - Interface Gráfica")
        self.master.geometry("900x700")
        self.master.configure(bg='#f0f0f0')
        
        # Configuração do grid - exatamente como no seu runner.py
        self.rows, self.cols = 10, 10
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        
        # Posição inicial aleatória - como no seu código
        self.start_x = randint(0, self.cols - 1)
        self.start_y = randint(0, self.rows - 1)
        
        self.robot = Robot(self.grid, self.start_x, self.start_y)
        
        # Para rastrear o estado
        self.visited_cells = set()
        self.visited_cells.add((self.start_x, self.start_y))
        self.step_count = 0
        self.is_running = False
        self.speed = 500
        
        # Interceptar métodos do robô para capturar os movimentos
        self.setup_robot_hooks()
        
        self.setup_ui()
        self.update_display()
    
    def setup_robot_hooks(self):
        """Intercepta os métodos do robô para capturar cada movimento"""
        # Guarda os métodos originais
        self.original_move_forward = self.robot.move_forward
        self.original_rotate = self.robot.rotate
        
        # Substitui pelos métodos que capturam o estado
        def hooked_move_forward():
            result = self.original_move_forward()
            self.visited_cells.add(tuple(self.robot.position))
            self.step_count += 1
            self.master.after(0, self.update_display)  # Atualiza a UI
            if self.speed > 0:
                time.sleep(self.speed / 1000.0)  # Pausa baseada na velocidade
            return result
        
        def hooked_rotate():
            result = self.original_rotate()
            self.master.after(0, self.update_display)  # Atualiza a UI
            if self.speed > 0:
                time.sleep(self.speed / 1000.0)  # Pausa baseada na velocidade
            return result
        
        self.robot.move_forward = hooked_move_forward
        self.robot.rotate = hooked_rotate
    
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.master, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="Simulação do Robô - Posição Inicial Aleatória", 
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=(0, 10))
        
        # Label mostrando posição inicial
        self.initial_pos_label = tk.Label(
            main_frame,
            text=f"🎲 Posição inicial aleatória: ({self.start_x}, {self.start_y})",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2196F3'
        )
        self.initial_pos_label.pack(pady=(0, 10))
        
        # Frame do grid
        grid_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=2)
        grid_frame.pack(pady=5)
        
        # Criar o grid visual
        self.cells = {}
        for y in range(self.rows):
            for x in range(self.cols):
                cell = tk.Label(
                    grid_frame,
                    width=4,
                    height=2,
                    relief='solid',
                    bd=1,
                    bg='white',
                    font=('Arial', 10, 'bold')
                )
                # Inverter y para mostrar (0,0) no canto inferior esquerdo
                cell.grid(row=self.rows-1-y, column=x, padx=1, pady=1)
                self.cells[(x, y)] = cell
        
        # Frame de informações
        info_frame = tk.LabelFrame(
            main_frame, 
            text="Informações do Robô", 
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#333',
            padx=10,
            pady=10
        )
        info_frame.pack(pady=10, fill='x')
        
        # Labels de informação
        self.position_label = tk.Label(
            info_frame, 
            text=f"Posição: ({self.start_x}, {self.start_y})", 
            font=('Arial', 11),
            bg='#f0f0f0'
        )
        self.position_label.pack(anchor='w', pady=2)
        
        self.direction_label = tk.Label(
            info_frame, 
            text="Direção: Norte ↑", 
            font=('Arial', 11),
            bg='#f0f0f0'
        )
        self.direction_label.pack(anchor='w', pady=2)
        
        self.steps_label = tk.Label(
            info_frame, 
            text="Passos dados: 0", 
            font=('Arial', 11),
            bg='#f0f0f0'
        )
        self.steps_label.pack(anchor='w', pady=2)
        
        self.status_label = tk.Label(
            info_frame, 
            text="Status: Pronto para executar", 
            font=('Arial', 11),
            bg='#f0f0f0'
        )
        self.status_label.pack(anchor='w', pady=2)
        
        # Frame de controle de velocidade
        speed_frame = tk.Frame(main_frame, bg='#f0f0f0')
        speed_frame.pack(pady=5)
        
        tk.Label(
            speed_frame, 
            text="Velocidade (0 = máxima):", 
            font=('Arial', 10),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.speed_var = tk.IntVar(value=500)
        speed_scale = tk.Scale(
            speed_frame,
            from_=0,
            to=2000,
            orient='horizontal',
            variable=self.speed_var,
            command=self.update_speed,
            bg='#f0f0f0',
            length=200
        )
        speed_scale.pack(side='left', padx=10)
        
        self.speed_label = tk.Label(
            speed_frame, 
            text="500ms", 
            font=('Arial', 10),
            bg='#f0f0f0'
        )
        self.speed_label.pack(side='left')
        
        # Frame de botões
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=15, fill='x')
        
        button_container = tk.Frame(button_frame, bg='#f0f0f0')
        button_container.pack(expand=True)
        
        self.run_button = tk.Button(
            button_container,
            text="▶️ Executar",
            command=self.run_original_code,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            relief='raised',
            bd=2
        )
        self.run_button.pack(side='left', padx=5)
        
        self.reset_button = tk.Button(
            button_container,
            text="Nova Posição Aleatória",
            command=self.reset_simulation,
            bg='#2196F3',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            relief='raised',
            bd=2
        )
        self.reset_button.pack(side='left', padx=5)
        
        # Label de instruções
        instruction_label = tk.Label(
            main_frame,
            text="Clique em 'Executar' para rodar seu código com posição inicial aleatória!",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#666'
        )
        instruction_label.pack(pady=10)
    
    def update_speed(self, value):
        self.speed = int(value)
        if self.speed == 0:
            self.speed_label.config(text="máxima")
        else:
            self.speed_label.config(text=f"{self.speed}ms")
    
    def get_direction_info(self):
        directions = {
            1: ("Norte", "↑"),
            2: ("Leste", "→"), 
            3: ("Sul", "↓"),
            4: ("Oeste", "←")
        }
        if self.robot.direction in directions:
            return directions[self.robot.direction]
        return ("Finalizado", "✓")
    
    def update_display(self):
        # Limpar todas as células
        for cell in self.cells.values():
            cell.config(bg='white', text='', fg='black')
        
        # Marcar posição inicial com cor especial
        initial_pos = (self.start_x, self.start_y)
        if initial_pos in self.cells:
            self.cells[initial_pos].config(bg='#FFF9C4', text='🏁', fg='#F57F17')
        
        # Marcar células visitadas (exceto a inicial)
        for pos in self.visited_cells:
            if pos != initial_pos and pos in self.cells:
                self.cells[pos].config(bg='#E3F2FD')
        
        # Marcar posição atual do robô
        robot_pos = tuple(self.robot.position)
        if robot_pos in self.cells:
            direction_name, direction_symbol = self.get_direction_info()
            self.cells[robot_pos].config(
                bg='#4CAF50',
                text=direction_symbol,
                fg='white'
            )
        
        # Atualizar labels de informação
        self.position_label.config(text=f"Posição: {tuple(self.robot.position)}")
        
        direction_name, direction_symbol = self.get_direction_info()
        self.direction_label.config(text=f"Direção: {direction_name} {direction_symbol}")
        
        self.steps_label.config(text=f"Passos dados: {self.step_count}")
        
        # Atualizar status
        if self.robot.direction > 4:
            self.status_label.config(text="Status: Completado! Atingiu todas as paredes.")
        elif self.robot.can_move_forward():
            self.status_label.config(text="Status: Movendo para frente...")
        else:
            self.status_label.config(text="Status: Rotacionando...")
    
    def run_original_code(self):
        """Executa exatamente o código do seu runner.py atualizado em uma thread separada"""
        if self.is_running:
            return
        
        self.is_running = True
        self.run_button.config(state='disabled', text="🏃 Executando...")
        self.status_label.config(text="Status: Iniciando execução...")
        
        def execute_runner():
            try:
                # Print da posição inicial (como no seu código)
                print(f"Robô iniciando na posição aleatória: ({self.start_x}, {self.start_y})")
                
                # AQUI ESTÁ SEU DO runner.py EXATAMENTE COMO VOCÊ ESCREVEU:
                while self.robot.direction < 5:
                    while self.robot.can_move_forward():
                        self.robot.move_forward()  # Interceptado para mostrar na UI
                    self.robot.rotate()  # Interceptado para mostrar na UI
                
                # Print final (como no seu código)
                print("Hitted all four walls")
                
                # Quando terminar
                self.master.after(0, self.on_execution_finished)
                
            except Exception as e:
                print(f"Erro na execução: {e}")
                self.master.after(0, self.on_execution_finished)
        
        # Executa em thread separada para não travar a UI
        thread = threading.Thread(target=execute_runner)
        thread.daemon = True
        thread.start()
    
    def on_execution_finished(self):
        """Chamado quando a execução termina"""
        self.is_running = False
        self.run_button.config(state='normal', text="Concluído!")
        self.status_label.config(text="Status: Hitted all four walls!")
        
        # Depois de 2 segundos, volta o botão ao normal
        self.master.after(2000, lambda: self.run_button.config(text="▶️ Executar"))
    
    def reset_simulation(self):
        """Reinicia a simulação com nova posição aleatória"""
        if self.is_running:
            return
        
        # Gerar nova posição aleatória - exatamente como no seu código
        self.start_x = randint(0, self.cols - 1)
        self.start_y = randint(0, self.rows - 1)
        
        # Recriar exatamente como no runner.py
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.robot = Robot(self.grid, self.start_x, self.start_y)
        
        # Reinstalar os hooks
        self.setup_robot_hooks()
        
        self.step_count = 0
        self.visited_cells = set()
        self.visited_cells.add((self.start_x, self.start_y))
        
        # Atualizar UI
        self.initial_pos_label.config(text=f"Nova posição inicial aleatória: ({self.start_x}, {self.start_y})")
        self.position_label.config(text=f"Posição: ({self.start_x}, {self.start_y})")
        self.run_button.config(text="Executar", state='normal')
        self.update_display()
        
        print(f"Nova simulação - Posição inicial: ({self.start_x}, {self.start_y})")


def main():
    try:
        root = tk.Tk()
        app = RobotGUI(root)
        root.mainloop()
    except ImportError as e:
        print(f"Erro: Não foi possível importar 'robot.py'")
        print(f"Certifique-se de que o arquivo está na mesma pasta!")
        print(f"Detalhes: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()