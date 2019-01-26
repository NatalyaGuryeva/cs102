# -*- coding: utf-8 -*-
from api import get_friends
import time
import igraph
from igraph import Graph, plot
import config


def get_network(users_id, as_edgelist=True):
    t = 0
    users_ids = get_friends(users_id, 'bdate')
    edges = []
    matrix = [[0] * len(users_ids)] * len(users_ids)

    for user_1 in range(len(users_ids)):
        friends = get_friends(users_ids[user_1]['id'])
        t += 1
        for user_2 in range(user_1 + 1, len(users_ids)):
            if users_ids[user_2] in friends:
                matrix[user_2][user_1] = 1
                matrix[user_1][user_2] = 1
                if as_edgelist:
                    edges.append((user_1, user_2))
        if t == 3:
            time.sleep(1)
            t = 0

    if as_edgelist:
        return edges
    return matrix


def plot_graph(user_id):
    friends = get_friends(user_id, 'bdate')
    edges = get_network(user_id)
    vertices = [(i['first_name'] + ' ' + i['last_name']) for i in friends]

    graph = Graph(vertex_attrs={"label": vertices}, edges=edges, directed=False)

    N = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "edge_color": "gray",
        "layout": graf.layout_fruchterman_reingold(
            maxiter=100000,
            area=N ** 2,
            repulserad=N ** 2)
    }

    graph.simplify(multiple=True, loops=True)
    communities = graph.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    graph.vs['color'] = pal.get_many(clusters.membership)
    igraph.plot(graph, **visual_style)


if __name__ == '__main__':
    user_id = config.VK_CONFIG['user_id']
    plot_graph(user_id)
