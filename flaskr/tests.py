from BoardState import BoardState
import AlphaBeta
from Packager import *
from Oracle import decode
import mood

def test1():
    mood.set_mood("rational")
    json_blob = {'game': {'id': '2d0e4764-e273-4cbf-9967-18e8a370fdac', 'ruleset': {'name': 'standard', 'version': 'v1.0.17'}, 'timeout': 500}, 'turn': 55, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_XSSDH8MY7V4WjJhF6PmhBJHC', 'name': 'Robeworm', 'latency': '40', 'health': 86, 'body': [{'x': 4, 'y': 3}, {'x': 4, 'y': 4}, {'x': 5, 'y': 4}, {'x': 6, 'y': 4}], 'head': {'x': 4, 'y': 3}, 'length': 4, 'shout': ''}, {'id': 'gs_rbYT3DGrqfgwy8v6qQQ33prS', 'name': 'BattlePolar', 'latency': '102', 'health': 92, 'body': [{'x': 3, 'y': 4}, {'x': 2, 'y': 4}, {'x': 1, 'y': 4}, {'x': 1, 'y': 5}, {'x': 2, 'y': 5}, {'x': 3, 'y': 5}, {'x': 4, 'y': 5}, {'x': 5, 'y': 5}, {'x': 5, 'y': 6}, {'x': 6, 'y': 6}, {'x': 7, 'y': 6}, {'x': 7, 'y': 7}, {'x': 6, 'y': 7}], 'head': {'x': 3, 'y': 4}, 'length': 13, 'shout': ''}], 'food': [{'x': 9, 'y': 4}, {'x': 10, 'y': 1}, {'x': 2, 'y': 6}], 'hazards': []}, 'you': {'id': 'gs_XSSDH8MY7V4WjJhF6PmhBJHC', 'name': 'Robeworm', 'latency': '40', 'health': 86, 'body': [{'x': 4, 'y': 3}, {'x': 4, 'y': 4}, {'x': 5, 'y': 4}, {'x': 6, 'y': 4}], 'head': {'x': 4, 'y': 3}, 'length': 4, 'shout': ''}}
    state = from_json(json_blob)
    player = find_me(json_blob)
    move = AlphaBeta.decide_move(state, player, 2)
    assert decode(move) != "left"

def test2():
    mood.set_mood("rational")
    json_blob = {'game': {'id': 'd0350615-bfa4-4a20-a6d3-e274dd542fa8', 'ruleset': {'name': 'standard', 'version': 'v1.0.17'}, 'timeout': 500}, 'turn': 97, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_37fggR7hWy4Yt4YrXJ3WJdhP', 'name': 'Robeworm', 'latency': '58', 'health': 3, 'body': [{'x': 2, 'y': 1}, {'x': 3, 'y': 1}, {'x': 4, 'y': 1}], 'head': {'x': 2, 'y': 1}, 'length': 3, 'shout': ''}, {'id': 'gs_WWPJKCJVddHQYx33wB46CrG8', 'name': 'spaceworm', 'latency': '398', 'health': 85, 'body': [{'x': 5, 'y': 2}, {'x': 6, 'y': 2}, {'x': 6, 'y': 3}, {'x': 5, 'y': 3}, {'x': 4, 'y': 3}, {'x': 4, 'y': 4}, {'x': 5, 'y': 4}, {'x': 5, 'y': 5}, {'x': 5, 'y': 6}, {'x': 5, 'y': 7}], 'head': {'x': 5, 'y': 2}, 'length': 10, 'shout': ''}], 'food': [{'x': 0, 'y': 10}, {'x': 1, 'y': 1}, {'x': 9, 'y': 1}, {'x': 1, 'y': 8}, {'x': 10, 'y': 2}, {'x': 0, 'y': 7}, {'x': 9, 'y': 8}], 'hazards': []}, 'you': {'id': 'gs_37fggR7hWy4Yt4YrXJ3WJdhP', 'name': 'Robeworm', 'latency': '58', 'health': 3, 'body': [{'x': 2, 'y': 1}, {'x': 3, 'y': 1}, {'x': 4, 'y': 1}], 'head': {'x': 2, 'y': 1}, 'length': 3, 'shout': ''}}
    state = from_json(json_blob)
    player = find_me(json_blob)
    move = AlphaBeta.decide_move(state, player, 2)

def test3():
    mood.set_mood("rational")
    json_blob = {'game': {'id': '7cf9c520-e960-47a9-b2df-ce93e8f89f15', 'ruleset': {'name': 'standard', 'version': 'v1.0.17'}, 'timeout': 500}, 'turn': 69, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_Sf9S7JpgFmwBvdVSqB4HYVdM', 'name': 'spaceworm', 'latency': '367', 'health': 83, 'body': [{'x': 3, 'y': 2}, {'x': 3, 'y': 3}, {'x': 4, 'y': 3}, {'x': 4, 'y': 4}, {'x': 4, 'y': 5}, {'x': 5, 'y': 5}, {'x': 5, 'y': 4}, {'x': 6, 'y': 4}, {'x': 7, 'y': 4}], 'head': {'x': 3, 'y': 2}, 'length': 9, 'shout': ''}, {'id': 'gs_wVFMCpThYg3gRqS6cCdY9MTD', 'name': 'Robeworm', 'latency': '73', 'health': 31, 'body': [{'x': 6, 'y': 3}, {'x': 7, 'y': 3}, {'x': 7, 'y': 2}], 'head': {'x': 6, 'y': 3}, 'length': 3, 'shout': ''}], 'food': [{'x': 6, 'y': 10}, {'x': 2, 'y': 10}, {'x': 0, 'y': 10}, {'x': 10, 'y': 3}], 'hazards': []}, 'you': {'id': 'gs_wVFMCpThYg3gRqS6cCdY9MTD', 'name': 'Robeworm', 'latency': '73', 'health': 31, 'body': [{'x': 6, 'y': 3}, {'x': 7, 'y': 3}, {'x': 7, 'y': 2}], 'head': {'x': 6, 'y': 3}, 'length': 3, 'shout': ''}}
    state = from_json(json_blob)
    player = find_me(json_blob)
    move = AlphaBeta.decide_move(state, player, 2)
    assert decode(move) == "down"



if __name__ == "__main__":
    # test1()
    # test2()
    test3()