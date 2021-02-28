# Código exemplo do problema do quebra cabeça de N peças usando o algoritmo A*
# A Função heurística é a conhecida distância Manhattan entre a posição 
#  atual e a posição desejada para cada peça.
# Distância de Manhattan também conhecida como distância de quarteirão.

# D = |x1 – x2| + |y1 – y2|.

# Heurística => número de peças fora da posição desejada.

import random
import math
import time

_goal_state = [[1,2,3,4,5,6],
               [7,8,9,10,11,12],
               [13,14,15,16,17,18],
               [19,20,21,22,23,24],
               [25,26,27,28,29,30],
               [31,32,33,34,35,0]]
               

# -------------------------------------------------
def index(item, seq):
    """Função Auxiliar que retorna -1 para valor de índice não encontrado em uma seq"""
    if item in seq:
        return seq.index(item)
    else:
        return -1
        
        
# ------------------------------- Class do Quebra Cabeça
class NPuzzle:
    
    # -------------------------------------------------
    def __init__(self):
        # valor heurístico
        self._hval = 0
        # profundidade da busca no estado atual
        self._depth = 0
        # nó pai no caminho da pesquisa
        self._parent = None
        self.adj_matrix = []
        for i in range(6):
            self.adj_matrix.append(_goal_state[i][:])

    # -------------------------------------------------
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.adj_matrix == other.adj_matrix

    # -------------------------------------------------
    def __str__(self):
        res = ''
        for row in range(6):
            res += ' '.join(map(str, self.adj_matrix[row]))
            res += '\r\n'
        return res

    # -------------------------------------------------
    def _clone(self):
        p = NPuzzle()
        for i in range(6):
            p.adj_matrix[i] = self.adj_matrix[i][:]
        return p

    # -------------------------------------------------
    def _get_legal_moves(self):
        """Retorna a lista de tuplas com as quais o espaço livre pode ser trocado"""
        # pega a linha e coluna da peça vazia
        row, col = self.find(0)
        free = []
        
        # descobrir quais peças podem se mover para lá
        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < 5:
            free.append((row + 1, col))
        if col < 5:
            free.append((row, col + 1))

        return free

    # -------------------------------------------------
    def _generate_moves(self):
        free = self._get_legal_moves()
        zero = self.find(0)

        def swap_and_clone(a, b):
            p = self._clone()
            p.swap(a,b)
            p._depth = self._depth + 1
            p._parent = self
            return p

        return map(lambda pair: swap_and_clone(zero, pair), free)

    # -------------------------------------------------
    def _generate_solution_path(self, path):
        if self._parent == None:
            return path
        else:
            path.append(self)
            return self._parent._generate_solution_path(path)

    # -------------------------------------------------
    def solve(self, h):
        """Realiza a busca A* para o estado objetivo.
        h(puzzle) - função heuristica, retorna um inteiro
        """
        def is_solved(puzzle):
            return puzzle.adj_matrix == _goal_state

        openl = [self]
        closedl = []
        move_count = 0
        while len(openl) > 0:
            x = openl.pop(0)
            move_count += 1
            if (is_solved(x)):
                if len(closedl) > 0:
                    return x._generate_solution_path([]), move_count
                else:
                    return [x]

            succ = x._generate_moves()
            idx_open = idx_closed = -1
            for move in succ:
                
                # verifica se nós já foi visitado
                idx_open = index(move, openl)
                idx_closed = index(move, closedl)
                hval = h(move)
                
                # função de avaliação do jogo
                fval = hval + move._depth

                if idx_closed == -1 and idx_open == -1:
                    move._hval = hval
                    openl.append(move)
                elif idx_open > -1:
                    copy = openl[idx_open]
                    if fval < copy._hval + copy._depth:
                        # copiar os valores do movimento sobre os existentes
                        copy._hval = hval
                        copy._parent = move._parent
                        copy._depth = move._depth
                elif idx_closed > -1:
                    copy = closedl[idx_closed]
                    if fval < copy._hval + copy._depth:
                        move._hval = hval
                        closedl.remove(copy)
                        openl.append(move)

            closedl.append(x)
            openl = sorted(openl, key=lambda p: p._hval + p._depth)

        # se estado final não for encontrado, retorna falha
        return [], 0

    # -------------------------------------------------
    def shuffle(self, step_count):
        # Embaralha as peças
        for i in range(step_count):
            row, col = self.find(0)
            free = self._get_legal_moves()
            target = random.choice(free)
            self.swap((row, col), target)            
            row, col = target

    # -------------------------------------------------
    def find(self, value):
        # retorna a linha, coluna do valor especificado no gráfico
        if value < 0 or value > 36:
            raise Exception("valor fora da faixa")

        for row in range(6):
            for col in range(6):
                if self.adj_matrix[row][col] == value:
                    return row, col
    
    # -------------------------------------------------
    def peek(self, row, col):
        """retorna o valor na linha e coluna especificada"""
        return self.adj_matrix[row][col]

    # -------------------------------------------------
    def poke(self, row, col, value):
        """define um valor na linha e coluna especificada"""
        self.adj_matrix[row][col] = value

    # -------------------------------------------------
    def swap(self, pos_a, pos_b):
        """troca os valores nas coordenadas especificadas"""
        temp = self.peek(*pos_a)
        self.poke(pos_a[0], pos_a[1], self.peek(*pos_b))
        self.poke(pos_b[0], pos_b[1], temp)


# -------------------------------------------------
def heur(puzzle, item_total_calc, total_calc):
# Função Heurística genérica que fornece a posição atual e desejada para cada número e a função total.

#Parâmetros:
# puzzle - o quebra-cabeça
# item_total_calc - pega 6 parâmetros: linha e coluna atual, e linha e coluna alvo.
#
# Retorna: inteiro. A soma de item_total_calc sobre todas entradas e retorna um inteiro.
# Este é o valor da função heurística.
    t = 0
    for row in range(6):
        for col in range(6):
            val = puzzle.peek(row, col) - 1
            target_col = val % 6
            target_row = val / 6

            # account for 0 as blank
            if target_row < 0: 
                target_row = 5

            t += item_total_calc(row, target_row, col, target_col)

    return total_calc(t)

# Heurística distância de Manhattan que calcula o desempenho do algoritmo
def h_manhattan(puzzle):
    return heur(puzzle,
                lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                lambda t : t)

# Função sem uso de nenhuma heurística de avaliação do algoritmo
def h_default(puzzle):
    return 0

## ---------------------------
## Programa Principal N-Puzzle
## ---------------------------
def main():
    # Chama a função time para calcular o tempo de execução do algoritmo
    inicio = time.time()

    # Cria o tabuleiro a partir de sua classe
    p = NPuzzle()
    
    # Embaralha as peças e imprime tabuleiro
    p.shuffle(22)
    print(p)

    # Invoca o solver usando a distância Manhattan como heurística
    path, count = p.solve(h_manhattan)
    
    # Inverte lista de caminhos (ações)
    path.reverse()
    
    # Imprime a lista de ações
    for i in path: 
        print(i)
        print("")
        print("  | ")
        print("  | ")
        print(" \\\'/ \n")

    print("Resolvido com a Exploração por Distância de Manhattan:", count, "estados")

    # Invoca o solver sem uso da função de avaliação.
    path, count = p.solve(h_default)
    print("Resolvido sem uso da função de avaliação:", count, "estados.")

    # Calcula o tempo de execução do algoritmo
    fim = time.time()
    print('\nTempo de execução: %.2fs\n' % (fim-inicio))

if __name__ == "__main__":
    main()