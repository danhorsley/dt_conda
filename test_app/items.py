weapons = ['dagger', 'katana', 'knife', 'longsword', 'sabre', 'shortsword'
            'rapier', 'battle axe','club','flail','mace','quarterstaff','war hammer',
            'yo-yo','frisbee', 'boomerang']

wearables = ['robe', 'gloves', 'ring', 'amulet', 'necklace', 'boots', 'belt', 'cloak',
                'shirt','jeans', 't-shirt', 'sneakers']

skill = ['speed','strength','power', 'skill', 'invisibility','persuasion',
            'thought','nothing in particular', 'who knows what', 'mystery', 'destiny']

nouns = weapons + wearables


import random
class item:
  def __init__(self, name=None, item_room = None, owner = None):
    self.name = name
    self.item_room = item_room
    self.owner = owner 

class item_set:
  def __init__(self):
    self.item_dict = {}
    
  def gen_item(self):
    my_string = f'{random.choice(nouns)} of {random.choice(skill)}'
    self.item_dict[len(self.item_dict.keys())] = item(my_string)
