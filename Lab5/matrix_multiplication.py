import numpy as np

if __name__ == "__main__":
    s = [1, 1, 0, 0,  # Матрица в виде списка
         0, 0, 1, 0,
         0, 0, 0, 0,
         0, 1, 1, 0]

    dimension = (4, 4)  # Размерность

    n = np.array(s, dtype='int64')  # Матрица в виде numpy массива
    matrix = n.reshape(dimension)  # Матрица в виде numpy матрицы
    zeros = np.zeros(dimension, dtype='int64')  # Нулевая матрица для сравнения
    result_matrix = matrix.copy()  # Матрица после перемножения, пока равна данной матрице
    pre_matrix = np.zeros(dimension, dtype='int64')  # Матрица до перемножения, пока равна 0 матрице
    eye = np.eye(dimension[0], dtype='int64')  # Матрица с диагональю из 1, чтоб потом прибавить
    reachability_matrix_disjunction = None  # Матрица достижимости с "дизъюнктивным сложением" и с единичной матрицей
    reachability_matrix_alg = None  # Матрица достижимости с "алгебраическим сложением сложением" без единичной матрицы
    matrixs = []  # Список матриц
    i = 0  # Итерации цикла

    # До тех пор, пока перемноженная матрица не равна 0 или не равна самой себе (цикл) или итерация не равна размерности
    while not (np.allclose(result_matrix, zeros) or np.allclose(result_matrix, pre_matrix) or i == dimension[0]):
        matrixs.append(result_matrix)  # Добавить перемноженную матрицу в массив матриц
        print(f'V{i + 1}:', result_matrix, sep='\n')
        pre_matrix = result_matrix.copy()  # Обновить предыдущую матрицу
        temp = np.matmul(result_matrix, matrix)  # Обновить перемноженную матрицу
        result_matrix = temp.copy()
        i += 1
        print('-----------------------------------')

    reachability_matrix_disjunction = matrixs[0].copy()  # Будем прибавлять дизъюнктивно к 1-ой матрице
    reachability_matrix_alg = sum(matrixs)  # Вычисление алгебраической суммы матриц

    for i in range(1, len(matrixs)):  # Прибавляем единички по маскам к 1-ой матрице
        mask = matrixs[i] != 0
        np.place(reachability_matrix_disjunction, mask, np.ones(dimension, dtype='int64')[mask])

    mask = eye != 0  # Прибавляем единички по главной диагонали
    np.place(reachability_matrix_disjunction, mask, np.ones(dimension, dtype='int64')[mask])

    print('Алгебраическое сложение:', reachability_matrix_alg, sep='\n')
    print('"Дизъюнктивное" сложение:', reachability_matrix_disjunction, sep='\n')

    transpose = reachability_matrix_disjunction.transpose()  # Транспонированная матрица достижимости
    strongly_connected_matrix = np.multiply(reachability_matrix_disjunction, transpose)  # Матрица сильной связности
    print('Матрица сильной связности:', strongly_connected_matrix, sep='\n')

    components = dict();  # Словарь с компонентами графа
    j = 0
    components_set = set()  # Множество с компонентами графа (чтоб исходную матрицу не изменять)
    for i in range(dimension[0]):  # Проходим по строкам матрицы
        k = np.where(strongly_connected_matrix[i] == 1)[0].tolist()  # Ищем единички
        if (set(k) - components_set) != set():  # Выбираем те единички, которых еще не было
            components[f"K{j + 1}"] = k  # Записываем их в словарь как компоненту
            j += 1
        components_set.update(k)  # И во множество, чтоб в следующих итерациях сравнивать
        # strongly_connected_matrix = np.delete(strongly_connected_matrix, k, 1)
        # strongly_connected_matrix = np.delete(strongly_connected_matrix, k, axis=0)
    print(components)
    print("Матрица смежности: ", matrixs[0], sep="\n")
