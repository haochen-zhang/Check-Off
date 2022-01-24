#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[53]:


#!/usr/bin/env python
# coding: utf-8

# In[43]:


#!/usr/bin/env python
# coding: utf-8

# In[88]:
        
import doctest

"""6.009 Lab 10: Snek Is You Video Game"""
class board:
    
    def __init__(self,row,col):
        self.row=row
        self.col=col
        
        #a dictionary that maps names to objects
        self.graphics={"snek":[],"rock":[],"computer":[],"flag":[],"wall":[],"bug":[]}
        
        #a dictionary that maps locations to objects
        self.graphic_objs={}
        self.text_verbs={}
        self.text_conjs={}
        self.text_nouns={}
        self.text_ppts={}
        self.objs=[self.graphic_objs,self.text_verbs,self.text_conjs,self.text_nouns,self.text_ppts]
        self.player=[]
        self.rules=[]
        self.state="ongoing"
        
        
    def remove_player(self,obj):
        old_coord=obj.coord
        #remove from dictionary that maps category to objs
        self.graphics[obj.name].remove(obj)
        #remove from dictionary that maps coord to objs
        for dictionary in self.get_objects():
            if old_coord in dictionary:
                if obj in dictionary[old_coord]:
                    dictionary[old_coord].remove(obj)
                    if dictionary[old_coord]==[]:
                        del dictionary[old_coord]

        
    def move_object(self,obj,v):
        old_coord=obj.coord
        obj.coord=(obj.coord[0]+v[0],obj.coord[1]+v[1])
        for dictionary in self.get_objects():
            if old_coord in dictionary:
                if obj in dictionary[old_coord]:
                    #delete old coord from dictionary
                    dictionary[old_coord].remove(obj)
                    if dictionary[old_coord]==[]:
                        del dictionary[old_coord]
                    #add new coord to dictionary
                    if obj.coord not in dictionary:
                        dictionary[obj.coord]=[obj]
                    else:
                        dictionary[obj.coord].append(obj)
                        
                        
    def dump_helper(self):
        objects={}
        dict_lst=[self.graphic_objs,self.text_conjs,self.text_nouns,self.text_ppts,self.text_verbs]
        for dct in dict_lst:
            for loc in dct:
                if loc not in objects:
                    objects[loc]=dct[loc][:]
                else:
                    objects[loc]+=dct[loc][:]
        return objects
        
    def all_objects(self):
        objects={}
        objects.update(self.graphic_objs)
        objects.update(self.text_conjs)
        objects.update(self.text_nouns)
        objects.update(self.text_ppts)
        objects.update(self.text_verbs)
        return objects
        
        
    def get_players(self):
        if self.player==[]:
            return None    
        all_players=[]
        for players in self.player:
            all_players+=self.graphics[players]
        return all_players
    def get_objects(self):
        
        return self.objs
          
    def change_graphics(self,start,end,changed):
        start=start.lower()
        end=end.lower()
        name=end
        if self.graphics[start]==[]:
            return None
        if self.graphics[end]!=[]:
            ppts=self.graphics[end][0].ppt
        else:
            ppts=set()
            for rule in self.rules[0]:
                if rule[0].lower()==end:
                    ppts.add(rule[1].lower())
        lst=self.graphics[start][:]
        for obj in lst:
            if obj not in changed:
                obj.ppt=ppts
                obj.name=name
                self.graphics[start].remove(obj)
                self.graphics[end].append(obj)
                changed.append(obj)
        
        
    def reset_graphics(self):
        for category in self.graphics:
            for obj in self.graphics[category]:
                obj.reset_ppt()
                
    def update(self,graphic_objs,text_verbs,text_conjs,text_nouns,text_ppts):
        self.graphic_objs=graphic_objs
        self.text_verbs=text_verbs
        self.text_conjs=text_conjs
        self.text_nouns=text_nouns
        self.text_ppts=text_ppts  
        dicts=[self.graphic_objs,self.text_verbs,self.text_conjs,self.text_nouns,self.text_ppts]
        for dictionary in dicts:
            for loc in dictionary:
                for obj in dictionary[loc]:
                    if loc in self.objs:
                        self.objs[loc].append(obj)
                    else:
                        self.objs[loc]=[obj]
    def get_instances(self,category):
        category=category.lower()
        return self.graphics[category]
    def update_rules(self,rules):
        self.rules=rules
        
    def add_graphic(self,category,obj):
        self.graphics[category].append(obj)
        
    def set_player(self,category):
        newplayer=category.lower()
        self.player.append(newplayer)
        for obj in self.graphics[newplayer]:
            obj.isplayer=True

class obj:
    pass

class graphic_obj(obj):
    def __init__(self,name,coord):
        self.name=name
        self.isplayer=False
        self.ppt=set()
        self.coord=coord
    def reset_ppt(self):
        self.ppt=set()
    def set_ppt(self,ppt):
        ppt=ppt.lower()
        self.ppt.add(ppt)
        
        
class text_obj(obj):
    def __init__(self,name,coord):
        self.ppt={"push"}
        self.name=name
        self.coord=coord
class text_noun(text_obj):
    pass
class text_ppt(text_obj):
    pass        
class text_verb(text_obj):
    pass
        
class text_conj(text_obj):
    pass
    
        
            





# NO ADDITIONAL IMPORTS!

# All words mentioned in lab. You can add words to these sets,
# but only these are guaranteed to have graphics.
NOUNS = {"SNEK", "FLAG", "ROCK", "WALL", "COMPUTER", "BUG"}
PROPERTIES = {"YOU", "WIN", "STOP", "PUSH", "DEFEAT", "PULL"}
WORDS = NOUNS | PROPERTIES | {"AND", "IS"}

# Maps a keyboard direction to a (delta_row, delta_column) vector.
direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, where UPPERCASE
    strings represent word objects and lowercase strings represent regular
    objects (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['snek'], []],
        [['SNEK'], ['IS'], ['YOU']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    
    num_rows=len(level_description)
    num_cols=len(level_description[0])
    game=board(num_rows,num_cols)
#initializing graphic&text objects
    graphic_objs={}
    text_verbs={}
    text_conjs={}
    text_nouns={}
    text_ppts={}
    for row in range(num_rows):
        for col in range(num_cols):
            if level_description[row][col]!=[]:
                for obj in level_description[row][col]:
                    if obj.islower():
                        if (row,col) not in game.graphic_objs:
                            new_obj=graphic_obj(obj,(row,col))
                            game.graphic_objs[(row,col)]=[new_obj]
                            game.add_graphic(obj,new_obj)
                        else:
                            new_obj=graphic_obj(obj,(row,col))
                            game.graphic_objs[(row,col)].append(new_obj)
                            game.add_graphic(obj,new_obj)
                            
                            
                    if obj.isupper():
                        if obj=="IS":
                            game.text_verbs[(row,col)]=[text_verb(obj,(row,col))]
                        elif obj=="AND":
                            game.text_conjs[(row,col)]=[text_conj(obj,(row,col))]
                        elif obj in NOUNS:
                            game.text_nouns[(row,col)]=[text_noun(obj,(row,col))]
                        elif obj in PROPERTIES:
                            game.text_ppts[(row,col)]=[text_ppt(obj,(row,col))]

    return game

def get_rules(game):
    text_verbs=game.text_verbs
    text_ppts=game.text_ppts
    text_nouns=game.text_nouns
    text_conjs=game.text_conjs
    noun_rules=[]
    ppt_rules=[]
    num_rows=game.row
    num_cols=game.col
    #rules in cols
    for row,col in text_verbs:
        if row>=1 and (row-1,col) in text_nouns:
                subjs=[text_nouns[(row-1,col)][0].name]
                nouns=[]
                ppts=[]
                brk=False
                if row+1<num_rows:
                    if (row+1,col) in text_nouns:
                        nouns.append(text_nouns[(row+1,col)][0].name)
                    elif (row+1,col) in text_ppts:
                        ppts.append(text_ppts[(row+1,col)][0].name)
                if ppts!=[] or nouns!=[]:
                    current=row-2
                    while current-1>=0 and (current,col) in text_conjs and (current-1,col) in text_nouns:
                        subjs.append(text_nouns[(current-1,col)][0].name)
                        current=current-2
                    current=row+2
                    while current+1<num_rows and (current,col) in text_conjs:
                        if (current+1,col) in text_ppts:
                            ppts.append(text_ppts[(current+1,col)][0].name)
                            current=current+2
                        elif (current+1,col) in text_nouns:
                            nouns.append(text_nouns[(current+1,col)][0].name)
                            current=current+2
                #pair each property with each object
                for subj in subjs:
                    for ppt in ppts:
                        ppt_rules.append((subj,ppt))
                    for noun in nouns:
                        noun_rules.append((subj,noun))
        #rules in rows
        if col>=1 and (row,col-1) in text_nouns:
                subjs=[text_nouns[(row,col-1)][0].name]
                nouns=[]
                ppts=[]
                if col+1<num_cols:
                    if (row,col+1) in text_nouns:
                        nouns.append(text_nouns[(row,col+1)][0].name)
                    elif (row,col+1) in text_ppts:
                        ppts.append(text_ppts[(row,col+1)][0].name)
                if nouns!=[] or ppts!=[]:
                    current=col-2
                    while current-1>=0 and (row,current) in text_conjs and (row,current-1) in text_nouns:
                        subjs.append(text_nouns[(row,current-1)][0].name)
                        current=current-2
                    current=col+2
                    while current+1<num_cols and (row,current) in text_conjs:
                        if (row,current+1) in text_ppts:
                            ppts.append(text_ppts[(row,current+1)][0].name)
                            current=current+2
                        elif (row,current+1) in text_nouns:
                            nouns.append(text_nouns[(row,current+1)][0].name)
                            current=current+2

                #pair each property with each object
                for subj in subjs:
                    for ppt in ppts:
                        ppt_rules.append((subj,ppt))
                    for noun in nouns:
                        noun_rules.append((subj,noun))
    game.update_rules([ppt_rules,noun_rules])
    
    return game

def apply_ppt_rules(game):
    #handling property rules
    ppt_rules=game.rules[0]
    #reset graphic objects' properties
    game.reset_graphics()
    # set properties according to property rules
    for tpl in ppt_rules:
        #treat "YOU" as a special form
        if tpl[1]=="YOU":
            game.set_player(tpl[0])
        else:
            for obj in game.get_instances(tpl[0]):
                obj.set_ppt(tpl[1])

def apply_noun_rules(game):
    #handling noun rules
    noun_rules=game.rules[1] 
    changed=[]
    for tpl in noun_rules:
        game.change_graphics(tpl[0],tpl[1],changed)
    return game

def step_game(game, direction):
    """
    Given a game representation (as returned from new_game), modify that game
    representation in-place according to one step of the game.  The user's
    input is given by direction, which is one of the following:
    {'up', 'down', 'left', 'right'}.

    step_game should return a Boolean: True if the game has been won after
    updating the state, and False otherwise.
    """
    game.player=[]
    get_rules(game)
    apply_ppt_rules(game)
    players=game.get_players()
    if players==None:
        return False
    objs=game.all_objects()
    pulled=set()
    for player in players:
        start=player.coord
        v=direction_vector[direction]
        end=(player.coord[0]+v[0],player.coord[1]+v[1])
        stop=end
        push_start=end
        push_end=(end[0]+v[0],end[1]+v[1])
        pull_end=start
        pull_start=(player.coord[0]-v[0],player.coord[1]-v[1])
        
        if not (0<=end[0]<=game.row-1 and 0<=end[1]<=game.col-1):
            continue
        chain=[player]
        blocked=False
        if end in objs:
            for obj in objs[end]:
                if "stop" in obj.ppt and ("push" not in obj.ppt):
                    blocked=True
                if isinstance(obj,text_obj) or ("push" in obj.ppt):
                    if (0<=end[0]+v[0]<=game.row-1 and 0<=end[1]+v[1]<=game.col-1):
                        chain.append(obj)
                    else:
                        blocked=True
                    push_start=(push_start[0]+v[0],push_start[1]+v[1])
                    while (push_start in objs):
                        for i,obj in enumerate(objs[push_start]):
                            if ("push" in objs[push_start][i].ppt): 
                                if(0<=push_start[0]+v[0]<=game.row-1 and 0<=push_start[1]+v[1]<=game.col-1):
                                    chain.append(objs[push_start][i])                          
                                else:
                                    blocked=True
                            elif "stop" in objs[push_start][i].ppt:
                                blocked=True
                                break
                        push_start=(push_start[0]+v[0],push_start[1]+v[1])
        
        if not blocked:
            for obj in chain:
                if obj not in pulled:
                    pull_start=(obj.coord[0]-v[0],obj.coord[1]-v[1])
                    game.move_object(obj,(v[0],v[1])) 
                    pulled.add(obj)
                    
                else:
                    continue
                while pull_start in objs:
                    lst=objs[pull_start][:]
                    blocked=False
                    for obj in lst:
                        if ("pull" in obj.ppt):
                            if (pull_start[0]+v[0],pull_start[1]+v[1]) in objs:
                                for item in objs[(pull_start[0]+v[0],pull_start[1]+v[1])]:
                                    if "stop" in item.ppt and "push" not in item.ppt:
                                        blocked=True
                                        break
                                    if "push" in item.ppt:
                                        if not blocked and item not in pulled:
                                            game.move_object(item,(v[0],v[1]))
                                            pulled.add(item)
                            if not blocked and obj not in pulled:
                                game.move_object(obj,(v[0],v[1]))
                                pulled.add(obj)
                        elif ("stop" in obj.ppt):
                            blocked=True
                    if blocked:
                        break
                    pull_start=(pull_start[0]-v[0],pull_start[1]-v[1])

    get_rules(game)
    apply_noun_rules(game)
    apply_ppt_rules(game)
    handle_defeat(game)

    return check_if_won(game)
            

def handle_defeat(game):
    players=game.get_players()
    objs=game.all_objects()
    
    for player in players:
        defeat=False
        name=player.name
        for obj in objs[player.coord]:
            if "defeat" in obj.ppt:
                defeat=True
        if defeat:
            remove_lst=[]
            for obj in objs[player.coord]:
                if obj.name==name:
                    remove_lst.append(obj)
            for obj in remove_lst:
                game.remove_player(obj)
                
                
def check_if_won(game):
    players=game.get_players()
    objs=game.all_objects()
    for player in players:
        #check all players if  they are at the same coord with some objs with the property WIN
        for obj in objs[player.coord]:
            if "win" in obj.ppt:
                return True
    return False

def dump_game(game):
    """
    Given a game representation (as returned from new_game), convert it back
    into a level description that would be a suitable input to new_game.

    This function is used by the GUI and tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    rows=game.row
    cols=game.col
    level_description=[]
    for row in range(rows):
        level_description.append([])
        for col in range(cols):
            level_description[row].append([])
    objs=game.dump_helper()
    for loc in objs:
        for obj in objs[loc]:
            level_description[loc[0]][loc[1]].append(obj.name)      
    return level_description

