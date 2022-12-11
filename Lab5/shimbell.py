import numpy as np

if __name__ == "__main__":
    s = [0, 5, 2, 1, 1,  # Матрица в виде списка
         2, 0, 0, 2, 0,
         0, 4, 0, 0, 0,
         0, 1, 0, 0, 0,
         1, 2, 0, 0, 0]

    dimension = (5, 5)  # Размерность

    n = np.array(s, dtype='int64')  # Матрица в виде numpy массива
    matrix = n.reshape(dimension)  # Матрица в виде numpy матрицы. На нее всегда будем умножать
    result_matrix = matrix.copy()  # Результат перемножения

    for l in range(2, dimension[1]):
        new_mat = []  # Лист с минимальными значениями по каждой позиции
        for i in range(dimension[0]):
            zeros_i = result_matrix[i] == 0  # Выбираем строчку (вернее позиции с нулями)
            for j in range(dimension[0]):
                zeros_j = matrix[:, j] == 0  # Выбираем столбец (вернее позиции с нулями)
                temp_i = result_matrix[i].copy()  # Строчка для сложения
                temp_i[zeros_j] = 0  # Заменяем в ней нулевые позиции столбца

                temp_j = matrix[:, j].copy()  # Столбец для сложения
                temp_j[zeros_i] = 0  # Заменяем в нем нулевые позиции строчки

                sum = temp_i + temp_j  # Складываем
                min = 0
                for k in sum:  # Ищем минимум > 0, если такой есть
                    if k > 0:
                        if min == 0:
                            min = k
                        if k < min:
                            min = k
                new_mat.append(min)  # Добавляем в лист с минимальными значениями по каждой позиции
        n = np.array(new_mat, dtype='int64')  # Преобразуем в матрицу
        new_matrix = n.reshape(dimension)  # Матрица в виде numpy матрицы
        print(f"Пути длиной {l}: ", new_matrix, sep="\n")
        result_matrix = new_matrix  # Перезаписываем для повторного использования новой матрицы в цикле
