import random
from test_app.region_dicts import *
from test_app.models import *

class Room:
  def __init__(self, x = 0, y = 0, floor = 0, visited = 0):

    self.visited = visited
    self.n_to = None
    self.s_to = None
    self.e_to = None
    self.w_to = None
    self.u_to = None
    self.d_to = None
    self.x = x
    self.y = y
    self.floor = floor
    self.coords = [self.x,self.y,self.floor]
    self.id = f'{self.x}{self.y}{self.floor}'
    
    #placeholders
    self.description = ''
    self.region = 'in a castle'
    self.title = self.region + self.id

  

  
  def connect_rooms(self, connecting_room):
    entrance_dict = {(0,1,0): 'n_to', (0,-1,0): 's_to', (1,0,0): 'e_to', (-1,0,0): 'w_to', (0,0,1): 'u_to', (0,0,-1): 'd_to' }
    try:

      translation1 = (connecting_room.x - self.x, connecting_room.y - self.y, connecting_room.floor - self.floor)
      translation2 = (self.x - connecting_room.x, self.y - connecting_room.y, self.floor - connecting_room.floor) 
      
      setattr(self, entrance_dict[translation1], connecting_room)
      setattr(connecting_room, entrance_dict[translation2], self)
    except:
       return print("cannot connect these rooms")


  def update_exits(self):
    possible_directions = ['n_to','s_to', 'e_to',  'w_to',  'u_to',  'd_to']
    self.exits = {}
    for pd in possible_directions:
      if getattr(self, pd) is None:
        tf = False
      else:
        tf = True
      self.exits[pd] = tf


  def create_full_description(self):
    d_text = {'n_to' : 'north', 's_to' : 'south ', 'w_to' : 'west', 'e_to' : 'east',
                  'u_to': 'stairs up','d_to': 'stairs down'}
    
    cur_reg_dict = all_regions[self.region]
    sights = random.sample(cur_reg_dict['Sights'],2)
    smells = random.sample(cur_reg_dict['Smells'],2)
    sounds = random.sample(cur_reg_dict['Sounds'],2)
    feels = random.sample(cur_reg_dict['Touch'],2)
    paths = random.sample(cur_reg_dict['Paths'],4)
    hows = random.sample(cur_reg_dict['How'],4)

    self.update_exits()
    available_exits = [e for e in self.exits.keys() if self.exits[e] is not False]
    #print(available_exits)
    exit_text = ''
    counter = 0
    for t in available_exits:

      if t in ['n_to','s_to', 'e_to',  'w_to']:
        exit_text = exit_text + '  A' + paths[counter] + f' {hows[counter]} to the {d_text[t]}.'
      elif t=='u_to':
        exit_text = exit_text + '  A' +  random.choice(cur_reg_dict['Up']) + f' leads upwards.'
      elif t=='d_to':
        exit_text = exit_text + '  A' + random.choice(cur_reg_dict['Down']) + f' leads downwards.'
      counter += 1

    self.description = (f'''You are {self.region}.  You see {sights[0]} and 
                        {sights[1]}.  You can smell {smells[0]} and hear {sounds[0]}.
                          You feel {feels[0]}.  ''' + exit_text).replace('\n                        ','')


class World:
  def __init__(self, x_dims = 10, y_dims = 10, floors = 2):

    self.x_dims = x_dims
    self.y_dims = y_dims
    self.floors = floors
    
    #make a grid of rooms populated with their respective co-ords
    #NOTE grid goes FLOOR, Y, X while COORDS goes X,Y,FLOOR
    self.grid = [None] * floors
    for f in range(floors):
      self.grid[f] = [None] * y_dims
      for i in range(y_dims):
        self.grid[f][i] = [None] * x_dims

    for f in range(floors):
      for i in range(y_dims):  #swap temp
        for j in range(x_dims):
          self.grid[f][i][j] = Room(j,i,f)
    
    #define some other useful attributes 
    #making grid for quick check of co_ords and neighbor translations
    self.check_grid = [[i,j] for i in range(x_dims) for j in range(y_dims)]
    self.neighbor_moves = [[1,0],[-1,0],[0,1],[0,-1]]
    


  def find_unvisited_neighbors(self,f=0):
    #first find neighbors
    current_neighbors = [[nm[0]+self.current_room.x, nm[1] + self.current_room.y] for nm in self.neighbor_moves]
    current_neighbors = [cn for cn in current_neighbors if cn in self.check_grid]
    self.current_unvisited_neighbors = [cn for cn in current_neighbors if self.grid[f][cn[1]][cn[0]].visited == 0]
    return self.current_unvisited_neighbors



  def make_path(self):
    """creates a maze for each floor using a recursive backtracker, 
    i.e. if every neighbor of the current room has been visited you pop the stack 
    to go back to the last room where there was an unvisited neighbor"""
    plot_list = []
    for f in range(self.floors):
      self.current_room = random.choice(random.choice(self.grid[f]))
      self.current_room.visited = 1

      self.total_unvisited = (self.x_dims * self.y_dims) - 1
      plot_list.append(self.current_room.coords)
      stack = [self.current_room]
      while self.total_unvisited != 0:
        old_room = self.current_room
        if self.find_unvisited_neighbors(f) != []:
          random_neighbor = random.choice(self.find_unvisited_neighbors(f))
          
          self.current_room = self.grid[f][random_neighbor[1]][random_neighbor[0]]
          plot_list.append(self.current_room.coords)
          if len(self.find_unvisited_neighbors(f)) >= 1:
            stack = [self.current_room] + stack
          self.current_room.connect_rooms(old_room)
          self.current_room.visited = 1
          self.total_unvisited -=1
          #print(self.total_unvisited)
        elif len(stack) !=0:
          #print('pop')
          #pop the stack
          self.current_room = stack[0]
          plot_list.append(self.current_room.coords)
          stack = stack[1:]
    return plot_list


  def print_rooms(self):
      '''
      Print the rooms in room_grid in ascii characters.
      '''
      for f in range(self.floors):
        # Add top border
        str = "# " * ((3 + self.x_dims * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid[f]) # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.x_dims * 5) // 2) + "\n"

        # Print string
        print(str)


  def create_regions(self,o = None,plot_list = []):
        """splits the map into regions using an origin point
            o is the origin point for the region split"""
        coords_to_region = {}
        if o is None:
          o = [self.x_dims // 2, self.y_dims // 2,  self.floors // 2]
        for f in range(self.floors):
          for i in range(self.y_dims):
            for j in range(self.x_dims):
              rc = self.grid[f][i][j]
              if rc.coords[0] >= o[0] and rc.coords[1] >= o[1] and rc.coords[2] >= o[2]:
                  rc.region = 'in a castle'
              if rc.coords[0] >= o[0] and rc.coords[1] >= o[1] and rc.coords[2] < o[2]:
                  rc.region = 'in a dungeon'
              if rc.coords[0] >= o[0] and rc.coords[1] < o[1] and rc.coords[2] >= o[2]:
                  rc.region = 'in a city'
              if rc.coords[0] >= o[0] and rc.coords[1] < o[1] and rc.coords[2] < o[2]:
                  rc.region = 'in the sewers'
              if rc.coords[0] < o[0] and rc.coords[1] < o[1] and rc.coords[2] >= o[2]:
                  rc.region = 'in a forest'
              if rc.coords[0] < o[0] and rc.coords[1] < o[1] and rc.coords[2] < o[2]:
                  rc.region = 'in an endless cave'
              if rc.coords[0] < o[0] and rc.coords[1] >= o[1] and rc.coords[2] >= o[2]:
                  rc.region = 'on a mountain'
              if rc.coords[0] < o[0] and rc.coords[1] >= o[1] and rc.coords[2] < o[2]:
                  rc.region = 'in an old abandoned mine'
              #coords_to_region[f'{j},{i},{f}'] = rc.region
        #return coords_to_region
    
  def populate_descriptions(self, o = None):
    ret = self.create_regions(o)
    for f in range(self.floors):
          for i in range(self.y_dims):
            for j in range(self.x_dims):
                self.grid[f][i][j].create_full_description()
    return ret

  def join_floors(self, stairwell = None):
    for f in range(self.floors-1):
      if stairwell is None:
        random_point = [random.choice(range(self.x_dims)), random.choice(range(self.x_dims))]
        self.grid[f][random_point[1]][random_point[0]].connect_rooms(self.grid[f+1][random_point[1]][random_point[0]])
      else:
        self.grid[f][stairwell[1]][stairwell[0]].connect_rooms(self.grid[f+1][stairwell[1]][stairwell[0]])


def pop_db(x_dims = 10, y_dims = 8, floors = 8, stairwell = [5,5]):
    my_world = World(x_dims,y_dims,floors)
    my_plot_list = my_world.make_path()
    my_world.join_floors(stairwell)
    my_world.populate_descriptions()
    


    for floor in my_world.grid:
        for row in floor:
            for r in row:
                temp_dict = {'n_to':0,'s_to':0,'e_to':0,'w_to':0,'u_to':0,'d_to':0}
                for d in temp_dict.keys():
                    if getattr(r, d) is None:
                        temp_dict[d] = None
                    else:
                        temp_dict[d] = getattr(r, d).coords
            
                r = Room_DB(id = r.id,
                            coords = r.coords,
                            description = r.description,
                            x = r.x,
                            y = r.y,
                            floor = r.floor,
                            n_to = temp_dict['n_to'],
                            s_to = temp_dict['s_to'],
                            e_to = temp_dict['e_to'],
                            w_to = temp_dict['w_to'],
                            u_to = temp_dict['u_to'],
                            d_to = temp_dict['d_to'],
                            region = r.region,
                            title = r.title)
                r.save()