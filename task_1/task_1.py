# На треугольном игровом поле расположена круглая мишень. Площадь треугольника в 3 раза больше площади круга. 
# Какова вероятность попасть в мишень при случайном броске?

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
import numpy as np

def triangular_darts(size):
    circle_radius = 4
    circle_area = np.pi * circle_radius**2
    
    triangle_area = 3 * circle_area
    
    side_length = np.sqrt((4 * triangle_area) / np.sqrt(3))
    height = (side_length * np.sqrt(3)) / 2
    
    triangle_points = [
        [0, 0],
        [side_length, 0],
        [side_length/2, height]
    ]
    
    circle_center = [side_length/2, height/3]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    triangle = Polygon(triangle_points, fill=False, edgecolor='blue', linewidth=2)
    ax.add_patch(triangle)
    
    target = Circle(circle_center, circle_radius, facecolor='red', alpha=0.5)
    ax.add_patch(target)
    
    points_inside_triangle = 0
    max_points = size * 2  
    
    X = np.random.uniform(0, side_length, max_points)
    Y = np.random.uniform(0, height, max_points)
    
    def point_in_triangle(point, triangle):
        x, y = point
        x1, y1 = triangle[0]
        x2, y2 = triangle[1]
        x3, y3 = triangle[2]
        
        denominator = (y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3)
        a = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / denominator
        b = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / denominator
        c = 1 - a - b
        
        return a >= 0 and b >= 0 and c >= 0
    
    valid_points = []
    for i in range(max_points):
        if point_in_triangle([X[i], Y[i]], triangle_points):
            valid_points.append([X[i], Y[i]])
            if len(valid_points) >= size:
                break
    
    valid_points = np.array(valid_points)
    X_valid = valid_points[:, 0]
    Y_valid = valid_points[:, 1]
    
    distances = (X_valid - circle_center[0])**2 + (Y_valid - circle_center[1])**2
    inside_circle = distances <= circle_radius**2
    

    plt.scatter(X_valid[inside_circle], Y_valid[inside_circle], 
                marker='o', c='green', s=30, alpha=0.7, label='Попадание в мишень')
    plt.scatter(X_valid[~inside_circle], Y_valid[~inside_circle], 
                marker='o', c='black', s=30, alpha=0.5, label='Промах')
    
    plt.xlim(-1, side_length + 1)
    plt.ylim(-1, height + 1)
    plt.gca().set_aspect('equal')
    plt.title(f'Метание дротиков в треугольное поле (n={size})')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    experimental_prob = np.sum(inside_circle) / size
    theoretical_prob = circle_area / triangle_area
    
    print('=' * 50)
    print('РЕЗУЛЬТАТЫ ЭКСПЕРИМЕНТА:')
    print('=' * 50)
    print(f'Всего бросков: {size}')
    print(f'Попаданий в мишень: {np.sum(inside_circle)}')
    print(f'Экспериментальная вероятность: {experimental_prob:.4f} ({experimental_prob*100:.2f}%)')
    print(f'Теоретическая вероятность: {theoretical_prob:.4f} ({theoretical_prob*100:.2f}%)')
    print(f'Площадь круга (мишени): {circle_area:.2f}')
    print(f'Площадь треугольника (поля): {triangle_area:.2f}')
    print(f'Отношение площадей: 1:{triangle_area/circle_area:.1f}')

triangular_darts(1000)