import csv

CSV_FILE = "more_data.csv"


def import_data_to_list(csv_file_path: str) -> list:
    """Import data from a csv into a list"""
    with open(csv_file_path, 'r', newline='') as file:
        reader = csv.reader(file, delimiter=",")
        data = list(reader)
    return data


def build_graph(edges: list) -> dict:
    """Generate graph from edges"""
    graph = {}
    for edge in edges:
        base, quote, price = edge
        price = float(price)
        if base not in graph:
            graph[base] = {quote: price}
        else:
            graph[base][quote] = price
        if quote not in graph:  # adding the reverse edge to make the graph undirected
            graph[quote] = {base: 1.0 / price}
        else:
            graph[quote][base] = 1.0 / price
    return graph


def get_price_from_path(end_coin: str, came_from: dict):
    """Compute final exchange rate from path"""
    current_coin, final_price, path = end_coin, 1, []
    while current_coin in came_from:
        path.append(current_coin)
        final_price *= came_from[current_coin][1]
        current_coin = came_from[current_coin][0]
    return final_price, path[::-1]


def bfs(start: str, end: str, graph: dict) -> tuple:
    """Breadth-first search"""
    came_from = {start: (None, 1)}  # initialize the path at the base currency with exchange rate 1
    queue = [start]
    open_set = {start}
    visited_set = set()

    while len(queue) > 0:
        current_coin = queue.pop(0)

        if current_coin == end:
            return get_price_from_path(current_coin, came_from)

        open_set.remove(current_coin)
        visited_set.add(current_coin)

        for neighbor, neighbor_price in graph[current_coin].items():

            if neighbor in visited_set:
                continue

            if neighbor not in open_set:
                queue.append(neighbor)
                open_set.add(neighbor)
                came_from[neighbor] = (current_coin, neighbor_price)  # record the node we came from along with the fx
    return 0, []


def get_price(base: str, quote: str, tickers: list) -> tuple:
    """
    Given a list of price tickers, find the price between two arbitrary assets
    - If there is a ticker of (base, quote, p), return p
    - If there is a ticker of (quote, base, p), return 1.0 / p
    - If there is no ticker of (base, quote, x) or (base, quote, x), but there are tickers like
        (base, mid, x) and (mid, quote, y), then return x * y
    - It is possible to take multiple hops to get the price. i.e. there are tickers like
        (base, mid1, x), (mid2, mid1, y), (mid2, quote, z), then return x * (1.0 / y) * z
    - If there are multiple paths from base to quote, should calculate with the path of the **LEAST** number of hops
    - If cannot find price between base and quote from tickers, return 0
    """

    graph = build_graph(tickers)
    if base not in graph:
        return 0, []
    return bfs(base, quote, graph)


if __name__ == "__main__":
    data = import_data_to_list(CSV_FILE)
    print(get_price("ETC", "EUR", data))
