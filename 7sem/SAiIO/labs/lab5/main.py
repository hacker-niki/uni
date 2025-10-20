import sys

INF = -sys.maxsize - 1

def topological_sort_dfs(graph):
    visited = {v: 0 for v in graph}
    sorted_vertices = []
    
    def dfs(u):
        visited[u] = 1
        
        for v, _ in graph[u]:
            if visited[v] == 0:
                dfs(v)
            elif visited[v] == 1:
                raise ValueError("Граф содержит контур и не является DAG.")
        
        visited[u] = 2
        sorted_vertices.append(u)
        
    for v in graph:
        if visited[v] == 0:
            dfs(v)
            
    return sorted_vertices[::-1]

def longest_path_dag(graph, start_node, end_node):
    try:
        topo_sorted_vertices = topological_sort_dfs(graph)
    except ValueError as e:
        return str(e), []
    
    # OPT[v] - максимальная длина пути от s до v
    # X[v] - предшествующая вершина на наидлиннейшем пути до v
    OPT = {v: INF for v in graph}
    X = {v: None for v in graph}
    
    # Максимальная длина пути от s до s равна 0
    OPT[start_node] = 0
    
    # прямой ход
    for u in topo_sorted_vertices:
        
        if OPT[u] == INF:
            continue
            
        for v, weight in graph[u]:
            
            # OPT(v) = max_{u} (OPT(u) + l(u, v))
            new_length = OPT[u] + weight
            
            if new_length > OPT[v]:
                OPT[v] = new_length
                X[v] = u
                
    max_length = OPT[end_node]
    if max_length == INF:
        return 0, f"Вершина {end_node} недостижима из {start_node}."
    
    # обратный ход
    path = []
    current = end_node
    
    while current is not None:
        path.append(current)
        if current == start_node:
            break
        current = X[current]
        
    if path[-1] != start_node:
         return max_length, f"Ошибка восстановления пути. Вершина {end_node} недостижима из {start_node}."
    
    path.reverse()
    
    return max_length, path

# Граф G = (V, A), где V = {A, B, C, D, E, F}
graph_example = {
    'A': [('B', 2), ('C', 5)],
    'B': [('D', 3), ('E', 1)],
    'C': [('D', 1), ('F', 6)],
    'D': [('F', 2)],
    'E': [('F', 3)],
    'F': []
}

start_node_example = 'A'
end_node_example = 'F'

max_len, path = longest_path_dag(graph_example, start_node_example, end_node_example)

print("Задача о наидлиннейшем пути в DAG")
print(f"Стартовая вершина (s): {start_node_example}")
print(f"Конечная вершина (t): {end_node_example}")
print("-" * 50)

if isinstance(path, str):
    print(f"Результат: {path}")
else:
    print(f"Максимальная длина (OPT({end_node_example})): {max_len}")
    print(f"Наидлиннейший путь: {' -> '.join(path)}")
