from room import Room
from player import Player
from world import World
from stack import Stack

import random
from ast import literal_eval


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []

# Visited is a dictionary of key=room.id, value=array of possible exits
visited = {}

# Array that keeps track of previous
reverse_path = Stack()

backtrack = {
    'n': 's',
    'e': 'w',
    's': 'n',
    'w': 'e'
}
 
curr_room = player.current_room
visited[curr_room.id] = curr_room.get_exits()

while len(visited) < len(room_graph):
    curr_room = player.current_room

    # If we are in a room we haven't checked yet, add it to the visited dictionary
    # with respective exits
    if curr_room.id not in visited:
        visited[curr_room.id] = curr_room.get_exits()
        previous_room = reverse_path.get_last()
        visited[curr_room.id].remove(previous_room)  

    # If the current room has no other exits, start backtracking
    if len(visited[curr_room.id]) == 0:
        previous_room = reverse_path.pop()
        traversal_path.append(previous_room)
        player.travel(previous_room)
    # Otherwise, continue checking rooms in DFT
    else:
        direction = visited[curr_room.id].pop()
        traversal_path.append(direction)
        reverse_path.push(backtrack[direction])
        player.travel(direction)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
