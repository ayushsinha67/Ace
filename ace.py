#ACE"
VER = "1.2"
CREATOR = "Ayush Sinha"
YEAR = "2012"

#starting pressed key bug
#start with a mission screen
#change startin screen title FONT - "ACE"
#include the zeppelin
#include "after death" message

#	name for each level
#	user interface
# 	#engine sounds, 
#	first level
#		mission statements - reach and destroy enemy base - airship arrives at the end
#		storyline	
#   second level 
    #NIGHT BACKGROUND, THUNDER!!
        #include air alarm sound
        #destroy night time towers, bomber plane
        #destroy enemy bases
#    third level
        #warships, sea, harbour
#    different music for different level
    

#IMPORT
import simplegui
import math
import random

#==========================================================
#GLOBALS
#Canvas
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 680
CANVAS_LEVEL1_BACKGROUND = "AEC9E4"

#Timers
DIFFICULTY_RATE = 1.0
ANIMATION_TIMER = 50
GAME_SPEED_TIMER = 10

MAX_TURRET_FIRE_INTERVAL = 200
MAX_MESSERSCHMITT_FIRE_INTERVAL = 70
MAX_ZEPPELIN_FIRE_INTERVAL = 70

AI_MESSERSCHMITT_CREATE_MAX_INTERVAL = 400
AI_MESSERSCHMITT_CREATE_MIN_INTERVAL = 150
AI_ZEPPELIN_CREATE_MAX_INTERVAL = 1200
AI_ZEPPELIN_CREATE_MIN_INTERVAL = 800
AI_TURRET_CREATE_MAX_INTERVAL = 1000
AI_TURRET_CREATE_MIN_INTERVAL = 300
AI_TREE_CREATE_MAX_INTERVAL = 40
AI_TREE_CREATE_MIN_INTERVAL = 2

#Display
SCORE_X = CANVAS_WIDTH - 100
SCORE_Y = 30
SCORE_VAL_X = SCORE_X
SCORE_VAL_Y = 60
KILLS_X = SCORE_X - 100
KILLS_Y = 30
KILLS_VAL_X = KILLS_X
KILLS_VAL_Y = 60
LIFE_X = KILLS_X - 150
LIFE_Y = 30
LIFE_BAR_X = LIFE_X
LIFE_BAR_Y = 50
LIFE_BAR_LEN = 0
BOMB_DISP_X = LIFE_BAR_X - 70
BOMB_DISP_Y = LIFE_BAR_Y
BOMB_VAL_X = BOMB_DISP_X - 20
BOMB_VAL_Y = SCORE_Y

#Scoring and range
MESSERSCHMITT_SCORE_DESTROY = 10
ZEPPELIN_SCORE_DESTROY = 150
LEVEL1_ZEPPELIN_ENTRY_KILLS = 20
TURRET_SCORE_DESTROY = 50
CRASH_MARGIN = 10
BOMB_MAX = 10
ZEPPELIN_FIRING_ANGLE_ERROR = 20
TURRET_BULLET_DAMAGE_ADD = 15
TURRET_FIRING_ANGLE_ERROR = 20 #deg

#Spritesheet dimensions
turret_fire_ss_num = [16, 1]
explosion1_ss_num = [4, 4]
explosion2_ss_num = [16, 1]
explosion3_ss_num = [8, 5]
explosion4_ss_num = [8, 4]
smoke1_ss_num = [8, 5]

#CLASSES         
#==========================================================
class UserInterface:
    def __init__(self):
        self.image_dict = {}
        self.button_dict = {}
        self.message_dict = {}
        self.mission_disp_ticker = 0
        self.mission_disp_interval = 500
       
    #UI state machine
    def update_state(self, game):
        if ( game.get_state() == "Menu") :
            frame.set_canvas_background("Black")
            sounds['menu_background_music'].play()
            self.button_dict['spitfire_sel_button'].show = True
            self.button_dict['thunderbolt_sel_button'].show = True
            self.image_dict['menu_back'].show = True
        elif ( game.get_state() == "End" ):
            self.message_dict['end_game'].show = True
        else:
            self.hide_all() 
    
    #create all objects
    def create_all(self):
        self.create_buttons()
        self.create_images()
        self.create_messages()
    
    #hide all
    def hide_all(self):
        #buttons
        for button in self.button_dict:
            self.button_dict[button].show = False
        for image in self.image_dict:
            self.image_dict[image].show = False
        for message in self.message_dict:
            self.message_dict[message].show = False
    
    #create images
    def create_images(self):
        self.image_dict['menu_back'] = ImageInfo(images['menu_background_image'], [CANVAS_WIDTH//2, CANVAS_HEIGHT//2] )
    
    #create buttons
    def create_buttons(self):
        self.button_dict['spitfire_sel_button'] = Button( 	images['spitfire_ui_button'],
                                                        sounds['menu_select_sound'], 
                                                        [300, 500],
                                                        "rectangle" )
        self.button_dict['thunderbolt_sel_button'] = Button(images['thunderbolt_ui_button'],
                                                        sounds['menu_select_sound'], 
                                                        [700, 500],
                                                        "rectangle" )
    
    #create messages
    def create_messages(self):
        self.message_dict['end_game'] = Message("An ACE never gives up...", [CANVAS_WIDTH//2 - 180, CANVAS_HEIGHT//2], 30, "Gray" )
    
    #draw all
    def draw(self,canvas):
        #images
        for image in self.image_dict:
            self.image_dict[image].draw(canvas)
        
        #buttons
        for button in self.button_dict:
            self.button_dict[button].draw(canvas)
        
        #messages
        for message in self.message_dict:
            self.message_dict[message].draw(canvas)
    
    #Mouse start Menu select
    def start_menu_select(self, pos, game):
        selected = False
        if self.button_dict['spitfire_sel_button'].clicked(pos):
            selected = True
            game.player_plane = Spitfire()
            
        elif self.button_dict['thunderbolt_sel_button'].clicked(pos) : 
            selected = True
            game.player_plane = Thunderbolt()
        
        if selected:
            game.set_state("Level_1")
            game.level_init("Level_1")
            sounds['menu_background_music'].rewind()

#==========================================================
class Message:
    #Initialize
    def __init__ (self, text, pos, size, colour):
        self.text = text
        self.size = size
        self.colour = colour
        self.pos = list(pos)
        self.show = False
    
    #draw
    def draw(self, canvas):
        if self.show:
             canvas.draw_text( self.text, self.pos, self.size, self.colour)
            
#==========================================================
class ImageInfo:
    #Initialize
    def __init__ (self, image, pos):
        self.image = image
        self.size = [self.image.get_width(), self.image.get_height()]
        self.center = [ self.size[0]//2, self.size[1]//2 ]
        self.pos = list(pos)
        self.show = False
    
    #draw
    def draw(self, canvas):
        if self.show:
             canvas.draw_image( self.image, self.center, self.size, self.pos, self.size )
                       
#==========================================================
class Button:
    #initialize
    def __init__ (self, image, sound, pos, shape ):
        self.image = image
        self.size = [self.image.get_width(), self.image.get_height()]
        self.center = [self.size[0]//2, self.size[1]//2]
        self.sound = sound
        self.shape = shape
        self.show = False
        self.pos = list(pos) #center point
    
    #draw button
    def draw(self, canvas ):
        if self.show:
            canvas.draw_image(	self.image, self.center, self.size, self.pos, self.size )
     
    #return clicked
    def clicked(self, click_pos ):
        if self.show:
            if self.shape == "rectangle":
                if ( (click_pos[0] < ( self.pos[0] + (self.size[0]//2) ) ) 
                        and (click_pos[0] > ( self.pos[0] - (self.size[0]//2) ) ) 
                        and (click_pos[1] < ( self.pos[1] + (self.size[1]//2) ) )
                        and (click_pos[1] > ( self.pos[1] - (self.size[1]//2) ) ) ):
                    self.sound.play()
                    return True
                else:
                    return False

#==========================================================
class Animation:
     #initialize
     def __init__ ( self, image, sound, ss_num ):
        self.image = image
        self.sound = sound
        self.size = [self.image.get_width(), self.image.get_height()]
        self.ss_num = list(ss_num)
        self.pos = [0, 0]
        self.frame_size = [ self.size[0]//( self.ss_num[0] ), self.size[1]//(self.ss_num[1] ) ] 
        self.current_center = [ (self.size[0]) - ( self.frame_size[0]//2 ) , 
                                (self.size[1]) - ( self.frame_size[1]//2 ) ]
        self.ss_index = [0, 0]
        self.animate_it = False
     
     #next image
     def next_image(self):
        if self.animate_it:
            self.current_center[0] += self.frame_size[0] 
            self.ss_index[0] += 1
            if ( self.ss_index[0] == self.ss_num[0] ):
                self.ss_index[0] = 0
                self.ss_index[1] += 1
                self.current_center[0] = self.frame_size[0] // 2
                self.current_center[1] += self.frame_size[1]
            if ( self.ss_index[1] == self.ss_num[1] ):
                self.ss_index[1] = 0
                self.current_center[1] = self.frame_size[1] // 2
            if( ( self.ss_index[0] == self.ss_num[0] - 1) and ( self.ss_index[1] == self.ss_num[1] - 1) ):
                self.current_center = [ (self.size[0]) - ( self.frame_size[0]//2 ) , 
                                        ( self.size[1]) - ( self.frame_size[1]//2 ) ]
                self.animate_it = False
                
     #start animation
     def animate(self, pos): 
        self.pos = list(pos)
        self.sound.rewind()
        self.current_center[0] = self.frame_size[0]//2
        self.current_center[1] = self.frame_size[1]//2
        self.ss_index = [0, 0]
        self.sound.play()
        self.animate_it = True
        
     #draw
     def draw(self, canvas, pos): 
        self.pos = list(pos)
        if self.animate_it:
            canvas.draw_image(self.image, self.current_center, self.frame_size, 
                          self.pos, self.frame_size, 0)
            
     #get animation state
     def get_state(self):
        return self.animate_it

#==========================================================
class Tree:
    #initialize
    def __init__(self, image, pos = CANVAS_WIDTH ):
        self.image = image
        self.size = [self.image.get_width(), self.image.get_height()]
        self.pos =  [ pos, CANVAS_HEIGHT - self.size[1]//2 ] 
        self.state = True
    
    #update state
    def update_state(self):
        if( self.pos[0] < 0 ):
            self.state = False

    #draw
    def draw(self, canvas):
        canvas.draw_image( self.image, [self.size[0]//2, self.size[1]//2], 
                              self.size, self.pos, self.size )
        
    #get state
    def get_state(self):
        return self.state

#==========================================================      
class GreenConifer(Tree):
    #Initialize
    def __init__(self, pos = CANVAS_WIDTH ):
        Tree.__init__(self, images['tree_green_image'], pos ) 

#==========================================================
class AuburnConifer(Tree):
    #Initialize
    def __init__(self, pos = CANVAS_WIDTH ):
        Tree.__init__(self, images['tree_auburn_image'], pos )
        
#==========================================================   
class Turret:
    #initialize
    def __init__(self, pos, radius = 20, damage_rate = 10 ):
        self.gun_anim = Animation( 		images['turret_fire_ss_image'], 
                                        sounds['turret_gun_sound'], 
                                        turret_fire_ss_num )
        
        self.damage_anim = Animation(	images['smoke1_ss_image'],
                                        sounds['no_sound'], 
                                        smoke1_ss_num )
        
        self.blow_anim = Animation( 	images['explosion3_ss_image'], 
                                        sounds['explosion3_sound'], 
                                        explosion3_ss_num )
        self.pos = pos
        self.radius = radius
        self.firing_angle = 90
        self.turret_len = 10
        self.turret_width = 10
        self.turret_colour = "Black"
        self.bullet_list = []
        self.bullet_speed = 37
        self.vert1 = [0,0]
        self.vert2 = [0,0]
        self.damage = 0
        self.damage_rate = damage_rate
        self.hits = 0
        self.damage = 0
        self.fire_ticker = 0
        self.fire_interval = random.randrange(0, MAX_TURRET_FIRE_INTERVAL )
        self.state = { 'Working':	True,
                       'Damage':	False,
                       'Explode':	False }
    
    #update fire timer
    def update_fire_timer(self, target ):
        self.fire_ticker += 1
        if( self.fire_ticker == self.fire_interval ):
            self.fire_ticker = 0
            self.fire_interval = random.randrange(0, MAX_TURRET_FIRE_INTERVAL )
            
            #fire at target
            v = [1, 1]
            v[0] = target[0] - self.pos
            v[1] = CANVAS_HEIGHT - target[1]
            angle = math.ceil( 180 / math.pi * math.atan2( v[1], v[0] ) )
            error = random.randrange(0, TURRET_FIRING_ANGLE_ERROR)
            self.fire( angle + error )
        
    #update state
    def update_state(self):
        if( (self.damage > 50) and (self.damage < 100) ):
            self.state['Damage'] = True 
        elif ( self.damage >= 100 ) and self.state['Working']:
            self.explode()
        elif ( self.state['Explode'] and ( not self.blow_anim.get_state() ) ):
                self.state['Explode'] = False
                
    #update position
    def update_pos(self):
        self.vert1[0] = self.pos + math.ceil( self.radius * math.cos( self.firing_angle * math.pi / 180 ) )
        self.vert1[1] = CANVAS_HEIGHT - math.ceil( self.radius * math.sin( self.firing_angle * math.pi / 180 ) )
        self.vert2[0] = self.vert1[0] + math.ceil( self.turret_len * math.cos( self.firing_angle * math.pi / 180 ) ) 
        self.vert2[1] = self.vert1[1] - math.ceil( self.turret_len * math.sin( self.firing_angle * math.pi / 180 ) ) 
        
        if( self.pos < 0 ):
            self.state['Working'] = False
    
    #draw
    def draw(self, canvas):
        #animate
        self.damage_anim.draw(canvas, self.vert1)
        self.gun_anim.draw(canvas, self.vert2)
        self.blow_anim.draw(canvas, self.vert1)
        
        if self.state['Working']:
            #draw turret
            canvas.draw_circle(( self.pos, CANVAS_HEIGHT), self.radius, 3, "White", "Gray")
            canvas.draw_line(self.vert1, self.vert2, self.turret_width, self.turret_colour)
            
            #animations
            if self.state['Damage'] and not self.damage_anim.get_state():
                self.damage_anim.animate(self.vert1)
                
        #update bullets
        remove = []
        for bullet in self.bullet_list:
            
            #blow bullet in the air
            if( bullet.pos[1] < random.randrange( 0, CANVAS_HEIGHT//3 ) ):
                bullet.blow_in_air()
            #update
            bullet.update_pos()
            bullet.update_state()
            bullet.draw(canvas)
            if ( bullet.get_state("destroy") ):
                remove.append(bullet)
        for bullet in remove:
            x = self.bullet_list.pop( self.bullet_list.index(bullet) )
            del x
    
    #animation timer update
    def anim_timer_update(self):
        self.gun_anim.next_image()
        self.damage_anim.next_image()
        self.blow_anim.next_image()
        for bullet in self.bullet_list:
            bullet.anim_timer_update()
    
    #fire 
    def fire(self, angle):
        if  self.state['Working']:
            self.firing_angle = angle
            self.gun_anim.animate(self.vert2)
            bullet_vel = [0, 0]
            bullet_vel[0] = math.ceil( self.bullet_speed * math.cos( self.firing_angle * math.pi / 180 ) )
            bullet_vel[1] = -math.ceil( self.bullet_speed * math.sin( self.firing_angle * math.pi / 180 ) )
            self.bullet_list.append( TurretBullet( 	self.vert2, bullet_vel, [0, 1]  ) )
    
    #cause self damage
    def cause_damage(self, item_type ): 
        if item_type == "bullet":
            self.damage += self.damage_rate
        elif item_type == "bomb":
            self.damage += 100	
        self.hits += 1
        
    #returns state
    def get_state(self, state_type):
        if state_type == "destroy":
            return not ( self.state['Working'] or self.state['Explode'] )
        elif state_type == "score":
            return (self.damage >= 100)
              
    # checks hits, removes hitting items and returns hit count
    def check_hit(self, ext_list, item_type ):
        remove = []
        hits = 0
        for ext in ext_list:
            if ( distance( ext.get_pos(), [self.pos, CANVAS_HEIGHT] ) <= ( self.radius + self.turret_len ) ):
                ext.explode()
                self.cause_damage(item_type)
                hits += 1
        return hits
    
    # explode
    def explode(self):
        self.blow_anim.animate(self.vert1)
        self.state['Explode'] = True
        self.state['Working'] = False
    
#==========================================================
class Bullet:
    #initialize
    def __init__(self, colour, size, length, pos, vel, acc, blow_anim ):
        self.colour = colour
        self.size = size
        self.length = length
        self.pos = list(pos)
        self.vert = [0, 0]
        self.vel = list(vel)
        self.acc = list(acc)
        self.blow_anim = blow_anim
        self.state = { 	'Flying' :	True,
                        'Explode':	False
                     }
    
    #update state
    def update_state(self):
        #check boundaries
        if self.state['Flying']:
            if ( self.pos[1] >= CANVAS_HEIGHT):
                self.explode()
            elif ( self.pos[1] < 0 ):
                self.state['Flying'] = False
            elif ( self.pos[0] > CANVAS_WIDTH ):
                self.state['Flying'] = False
            elif ( self.pos[0] < 0 ):
                self.state['Flying'] = False
               
        if ( self.state['Explode'] and ( not self.blow_anim.get_state() ) ):
                self.state['Explode'] = False
                
    #update position
    def update_pos(self):
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        if( self.vel[0] == 0 ):
           self.vert[0] = self.pos[0]
           self.vert[1] = self.pos[1] + self.length
        else:
            self.vert[0] = self.pos[0] + math.floor( self.length * ( math.cos( math.atan( self.vel[1] / self.vel[0] ) ) ) ) 
            self.vert[1] = self.pos[1] + math.floor( self.length * ( math.sin( math.atan( self.vel[1] / self.vel[0] ) ) ) )	
        
    #draw
    def draw(self,canvas):
        #draw elements
        self.blow_anim.draw(canvas, self.pos )
        
        #check state
        if ( self.state['Flying'] ):
            canvas.draw_line( self.pos, self.vert, self.size , self.colour )
    
    # get state
    def get_state(self, state_type):
        if state_type == "destroy" :
            return not ( self.state['Flying'] or self.state['Explode'] )
        else:
            return self.state[state_type]

    # animation timer update
    def anim_timer_update(self):
        self.blow_anim.next_image()
        
    #returns position
    def get_pos(self):
        return self.vert
    
    #explode
    def explode(self):
        self.blow_anim.animate(self.pos)
        self.state['Explode'] = True
        self.state['Flying'] = False

#==========================================================
class TurretBullet(Bullet):
    def __init__(	self,  
                    bullet_pos, 
                    bullet_vel, 
                    bullet_acc ):
        
        blow_anim = Animation(	images['explosion2_ss_image'], 
                                sounds['explosion2_sound'], 
                                explosion2_ss_num )
        Bullet.__init__(self,
                        "Brown", 
                        4, 
                        15,
                        bullet_pos,
                        bullet_vel, 
                        bullet_acc, 
                        blow_anim )
     
    #blow in air
    def blow_in_air(self):
        if not self.state['Explode']:
            self.explode()
        
#==========================================================
class FighterBullet(Bullet):
    def __init__(	self, 
                    bullet_colour, 
                    bullet_size, 
                    bullet_length, 
                    bullet_pos, 
                    bullet_vel, 
                    bullet_acc ):
        
        blow_anim = Animation(	images['explosion4_ss_image'], 
                                sounds['bullet_hit'], 
                                explosion4_ss_num )
        Bullet.__init__(self,
                        bullet_colour, 
                        bullet_size, 
                        bullet_length,
                        bullet_pos,
                        bullet_vel, 
                        bullet_acc, 
                        blow_anim ) 
 
#========================================================== 
class Bomb:
    #initialize 
    def __init__( self, image, pos, blow_anim ):
        self.image = image
        self.size = [self.image.get_width(), self.image.get_height() ]
        self.blow_anim = blow_anim
        self.pos = list(pos)
        self.vel = [0, 5 ]
        self.acc = [0, 0 ]
        self.state = { 	'Flying' :	True,
                        'Explode':	False
                     }
        
    #update state
    def update_state(self):
        #check boundaries
        if self.state['Flying']:
            if ( self.pos[1] > ( CANVAS_HEIGHT - (self.size[1]/2 ) - CRASH_MARGIN ) ):
                self.explode()
            elif ( self.pos[1] < (self.size[1]/2) ):
                self.state['Flying'] = False
            elif ( self.pos[0] > ( CANVAS_WIDTH - (self.size[0]/2 ) ) ):
                self.state['Flying'] = False
            elif ( self.pos[0] < ( self.size[0]/2) ):
                self.state['Flying'] = False
               
        if ( self.state['Explode'] and ( not self.blow_anim.get_state() ) ):
                self.state['Explode'] = False
           
    #update position
    def update_pos( self ):
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
            
    #draw fighter
    def draw(self, canvas): 
        #draw elements
        self.blow_anim.draw(canvas, self.pos )
        
        #check state
        if ( self.state['Flying'] ):         
            canvas.draw_image(self.image, [self.size[0]//2, self.size[1]//2], 
                              self.size, self.pos, self.size )
        
    # animation timer update
    def anim_timer_update(self):
        self.blow_anim.next_image()
        
    # get state
    def get_state(self, state_type):
        if state_type == "destroy" :
            return not ( self.state['Flying'] or self.state['Explode'] )
        else:
            return self.state[state_type]
    
    # get position
    def get_pos(self):
        return self.pos
    
    # explode
    def explode(self):
        self.blow_anim.animate(self.pos)
        self.state['Explode'] = True
        self.state['Flying'] = False
    
#========================================================== 
class FighterBomb(Bomb):
    def __init__(self, pos):
        blow_anim = Animation(		images['explosion2_ss_image'], 
                                    sounds['explosion2_sound'],  
                                    explosion2_ss_num )
        Bomb.__init__(self, images['bomb_image'], pos, blow_anim )
        
#==========================================================        
class Fighter: 
    #initialize 
    def __init__( 	self, 
                    image, 
                    engine_sound, gun_sound, 
                    pos, vel, acc, ang_vel, ang_acc, orient, rotation,
                    bullet_colour, bullet_size, bullet_length, bullet_speed, 
                    bullet_damage_rate ):
        
        self.image = image
        self.size = [self.image.get_width(), self.image.get_height() ]
        self.damage_anim = Animation(	images['smoke1_ss_image'],
                                        sounds['no_sound'], 
                                        smoke1_ss_num )
        
        self.blow_anim = Animation(		images['explosion1_ss_image'], 
                                        sounds['explosion1_sound'], 
                                        explosion1_ss_num )
        self.pos = list(pos)
        self.vel = list(vel)
        self.acc = list(acc)
        self.ang_vel = ang_vel
        self.ang_acc = ang_acc
        self.lift_factor = 10
        self.orient = orient 
        self.rotation = rotation
        self.engine_sound = engine_sound
        self.gun_sound = gun_sound
        self.bullet_list = []
        self.bomb_list = []
        self.bomb_num = BOMB_MAX
        self.bullet_colour = bullet_colour
        self.bullet_size = bullet_size
        self.bullet_length = bullet_length
        self.bullet_speed = bullet_speed
        self.damage = 0
        self.fire_ticker = 0
        self.fire_interval = random.randrange(0, 100 )
        self.bullet_damage_rate = bullet_damage_rate
        self.bomb_damage_rate = 100
        self.hits = 0
        self.hit_range = 50
        self.state = { 	'Flying' :	True,
                        'Damage' :	False,
                        'Explode':	False
                     }
    
    #update state
    def update_state(self):
        if( (self.damage > 50) and (self.damage < 100) ):
            self.state['Damage'] = True 
        elif ( ( self.damage >= 100 ) and self.state['Flying'] ):
            self.engine_sound.pause()
            self.explode()
        elif ( self.state['Explode'] and ( not self.blow_anim.get_state() ) ):
                self.state['Explode'] = False
        
    #check boundary
    def check_boundary(self):
        if self.state['Flying']:
            if ( self.pos[1] > ( CANVAS_HEIGHT - (self.size[1]/2 ) - CRASH_MARGIN ) ):
                self.engine_sound.pause()
                self.explode()
                self.pos[1] = CANVAS_HEIGHT - (self.size[1]/2 )
            if ( self.pos[1] < (self.size[1]/2) ):
                self.pos[1] = self.size[1]/2
            if ( self.pos[0] > ( CANVAS_WIDTH - (self.size[0]/2 ) ) ):
                self.pos[0] = CANVAS_WIDTH - (self.size[0]/2 )
            if ( self.pos[0] < ( self.size[0]//2 ) ):
                self.pos[0] = self.size[0]//2
           
    #update fighter position
    def update_pos( self ):
        #update position
        self.pos[0] += self.vel[0]
        if  self.orient == "right":
            self.pos[1] += self.vel[1] + math.ceil( self.lift_factor * math.sin( self.rotation ) )
        else:
            self.pos[1] += self.vel[1] - math.ceil( self.lift_factor * math.sin( self.rotation ) )
        self.rotation += self.ang_vel
            
    #draw fighter
    def draw(self, canvas): 
        #draw elements
        self.damage_anim.draw(canvas, self.pos )
        self.blow_anim.draw(canvas, self.pos )
       
        if ( self.state['Flying'] ):         
            #draw body
            canvas.draw_image(self.image, [self.size[0]//2, self.size[1]//2], 
                              self.size, self.pos, self.size, self.rotation)
            #play sounds
            self.engine_sound.set_volume(0.5)
            self.engine_sound.play()
            
            #animations
            if self.state['Damage']:
                if not self.damage_anim.get_state():
                    self.damage_anim.animate(self.pos)
        
        #draw/remove bullet
        remove = []
        for bullet in self.bullet_list:
            bullet.update_pos()
            bullet.update_state()
            bullet.draw(canvas)
            if ( bullet.get_state("destroy") ):
                remove.append( bullet )
        for bullet in remove:
            x = self.bullet_list.pop( self.bullet_list.index(bullet) )
            del x
            
        #draw/remove bomb
        remove = []
        for bomb in self.bomb_list:
            bomb.update_pos()
            bomb.update_state()
            bomb.draw(canvas)
            if ( bomb.get_state("destroy") ):
                remove.append(bomb)
        for bomb in remove:
            x = self.bomb_list.pop( self.bomb_list.index(bomb) )
            del x
        
    # down_key movement
    def key_down(self, key):
        if self.state['Flying']:
            self.engine_sound.set_volume(1)
            #movement
            if ( key == simplegui.KEY_MAP["left"] ):
                self.vel[0] -= self.acc[0]
            elif ( key == simplegui.KEY_MAP["right"] ) :
                self.vel[0] += self.acc[0]
            elif ( key == simplegui.KEY_MAP["up"] ) :
                self.vel[1] -= self.acc[1]
                if ( self.orient == "right" ):
                    self.ang_vel -= self.ang_acc
                else:
                    self.ang_vel += self.ang_acc
            elif ( key == simplegui.KEY_MAP["down"] ) :
                self.vel[1] += self.acc[1]
                if ( self.orient == "right" ):
                    self.ang_vel += self.ang_acc
                else:
                    self.ang_vel -= self.ang_acc
            
            #fire bullet
            elif ( key == simplegui.KEY_MAP["space"] ):
                self.fire_bullet()
            #fire bomb
            elif ( key == simplegui.KEY_MAP["b"] ) and ( self.bomb_num > 0 ):
                self.fire_bomb()
                self.bomb_num -= 1
    
    # up_key movement
    def key_up(self, key):
        if self.state['Flying']:
            self.engine_sound.set_volume(0.5)
            if ( key == simplegui.KEY_MAP["left"] ):
                self.vel[0] += self.acc[0]
            elif ( key == simplegui.KEY_MAP["right"] ) :
                self.vel[0] -= self.acc[0]
            elif ( key == simplegui.KEY_MAP["up"] ) :
                self.vel[1] += self.acc[1]
                if( self.orient == "right" ):
                    self.ang_vel += self.ang_acc
                else:
                    self.ang_vel -= self.ang_acc
            elif ( key == simplegui.KEY_MAP["down"] ) :
                self.vel[1] -= self.acc[1]
                if( self.orient == "right" ):
                    self.ang_vel -= self.ang_acc
                else:
                    self.ang_vel += self.ang_acc
        
    # animation timer update
    def anim_timer_update(self):
        self.damage_anim.next_image()
        self.blow_anim.next_image()
        
        for i in range( 0, len( self.bullet_list ) ):
            self.bullet_list[i].anim_timer_update()
            
        for i in range( 0, len( self.bomb_list ) ):
            self.bomb_list[i].anim_timer_update()
        
    # fire bullet
    def fire_bullet( self ):
        if self.state['Flying']:
            self.gun_sound.rewind()
            self.gun_sound.play()
            bullet_vel = [0,0]
            if ( self.orient == "right" ):
                bullet_vel[0] = math.ceil( self.bullet_speed * math.cos( self.rotation ) )
                bullet_vel[1] = math.ceil( self.bullet_speed * math.sin( self.rotation ) )
            else:
                bullet_vel[0] = -math.ceil( self.bullet_speed * math.cos( self.rotation ) )
                bullet_vel[1] = -math.ceil( self.bullet_speed * math.sin( self.rotation ) )
            
            self.bullet_list.append( FighterBullet( self.bullet_colour, 
                                                    self.bullet_size, 
                                                    self.bullet_length,
                                                    self.pos, 
                                                    bullet_vel, 
                                                    [0, 0] ) )    
    
    # fire bomb
    def fire_bomb( self ):
        if self.state['Flying']:
            bomb_vel = [0,0]
            bomb_vel[1] = 2
            if self.orient == "right":
                bomb_vel[0] = self.vel[0]
            self.bomb_list.append( FighterBomb( self.pos ) ) 
        
    # cause self damage
    def cause_damage(self, item_type ): 
        if item_type == "bullet":
            self.damage += self.bullet_damage_rate
        elif item_type == "turret_bullet":
            self.damage += self.bullet_damage_rate + TURRET_BULLET_DAMAGE_ADD
        elif item_type == "bomb":
            self.damage += self.bomb_damage_rate
        self.hits += 1
    
    # get flying state
    def get_state(self, state_type):
        if state_type == "destroy":
            return not ( self.state['Flying'] or self.state['Explode'] )
        elif state_type == "score":
            return ( self.damage >= 100 )
        else:
            return self.state[state_type]
    
    # checks hits, removes hitting items and returns hit count
    def check_hit(self, ext_list, item_type ):
        remove = []
        hits = 0
        for ext in ext_list:
            if ( ( distance( ext.get_pos(), self.pos ) < self.hit_range ) and ext.get_state('Flying') ):
                ext.explode()
                self.cause_damage(item_type)
                hits += 1
        return hits
    
    # check collision with plane
    def check_collision(self, ext_plane ):
        if ( ( distance( ext_plane.pos , self.pos )  < ( ext_plane.size[1] ) ) 
                and self.get_state('Flying') 
                and ext_plane.get_state('Flying') ):
            self.damage += 100
            self.engine_sound.pause()
            self.explode()
    
    # explode
    def explode(self):
        self.blow_anim.animate(self.pos)
        self.state['Explode'] = True
        self.state['Flying'] = False
    
    #update fire timer
    def update_fire_timer(self, max_interval ):
        self.fire_ticker += 1
        if( self.fire_ticker >= self.fire_interval ):
            self.fire_ticker = 0
            self.fire_interval = random.randrange(0, max_interval )
            self.fire_bullet()    

#========================================================== 
class Spitfire(Fighter):
    #Initialize
    def __init__(	self, 
                    pos = [100, CANVAS_HEIGHT//2], 
                    vel = [0, 0], 
                    acc = [3, 2], 
                    ang_vel = 0, 
                    ang_acc = 0.007 , 
                    orient = "right", 
                    rotation = 0	):
        
        Fighter.__init__( 	self,
                            images['spitfire_image'],  
                            sounds['spitfire_engine_sound'], 
                            sounds['spitfire_gun_sound'],
                            pos, 
                            vel, 
                            acc, 
                            ang_vel,
                            ang_acc,
                            orient,
                            rotation,
                            "Blue", 
                            1, 
                            15, 
                            10,
                            5	)
    
#========================================================== 
class Thunderbolt(Fighter):
    #Initialize
    def __init__(	self, 
                    pos = [100, CANVAS_HEIGHT//2], 
                    vel = [0, 0], 
                    acc = [3, 2], 
                    ang_vel = 0, 
                    ang_acc = 0.009 , 
                    orient = "right", 
                    rotation = 0	):
        
        Fighter.__init__( 	self,
                            images['thunderbolt_image'],  
                            sounds['thunderbolt_engine_sound'], 
                            sounds['thunderbolt_gun_sound'],
                            pos, 
                            vel, 
                            acc, 
                            ang_vel,
                            ang_acc,
                            orient,
                            rotation,
                            "Brown", 
                            1, 
                            15, 
                            10,
                            5	)

#========================================================== 
class Messerschmitt(Fighter):
    #Initialize
    def __init__(	self, 
                    pos = [CANVAS_WIDTH - 100, CANVAS_HEIGHT//2], 
                    vel = [-4, 0], 
                    acc = [3, 2], 
                    ang_vel = 0, 
                    ang_acc = 0.02 , 
                    orient = "left", 
                    rotation = 0	):
        
        Fighter.__init__( 	self,
                            images['messerschmitt_image'],  
                            sounds['messerschmitt_engine_sound'], 
                            sounds['messerschmitt_gun_sound'],
                            pos, 
                            vel, 
                            acc, 
                            ang_vel,
                            ang_acc,
                            orient,
                            rotation,
                            "Black", 
                            1, 
                            15, 
                            10,
                            20	)        
        
    #check boundary
    def check_boundary(self):
        if self.state['Flying']:
            if ( self.pos[1] > ( CANVAS_HEIGHT - (self.size[1]/2 ) - CRASH_MARGIN ) ):
                self.engine_sound.pause()
                self.explode()
                self.pos[1] = CANVAS_HEIGHT - (self.size[1]/2 )
            if ( self.pos[1] < (self.size[1]/2) ):
                self.pos[1] = self.size[1]/2
            if ( self.pos[0] > ( CANVAS_WIDTH - (self.size[0]/2 ) ) ):
                self.pos[0] = CANVAS_WIDTH - (self.size[0]/2 )
            if ( self.pos[0] < -1 * ( self.size[0]//2 ) ):
                self.state['Flying'] = False
        
#==========================================================
class Zeppelin(Fighter):
    #Initialize
    def __init__(	self, 
                    pos = [CANVAS_WIDTH - 100, CANVAS_HEIGHT//2], 
                    vel = [-1, 0], 
                    acc = [3, 2], 
                    ang_vel = 0, 
                    ang_acc = 0.02 , 
                    orient = "left", 
                    rotation = 0	):
        
        Fighter.__init__( 	self,
                            images['zeppelin_image'],  
                            sounds['zeppelin_engine_sound'], 
                            sounds['zeppelin_gun_sound'],
                            pos, 
                            vel, 
                            acc, 
                            ang_vel,
                            ang_acc,
                            orient,
                            rotation,
                            "Black", 
                            1, 
                            15, 
                            10,
                            5	)
        self.bullet_speed = 10
        self.bomb_damage_rate = 50
        self.hit_range = 150
    
    #check boundary
    def check_boundary(self):
        if self.state['Flying']:
            if ( self.pos[1] > ( CANVAS_HEIGHT - (self.size[1]/2 ) - CRASH_MARGIN ) ):
                self.engine_sound.pause()
                self.explode()
                self.pos[1] = CANVAS_HEIGHT - (self.size[1]/2 )
            if ( self.pos[1] < (self.size[1]/2) ):
                self.pos[1] = self.size[1]/2
            if ( self.pos[0] < -1 * ( self.size[0]//2 ) ):
                self.state['Flying'] = False
    
    # fire bullet
    def fire_bullet(self, target ):
        if self.state['Flying']:
            self.gun_sound.rewind()
            self.gun_sound.play()
            bullet_vel = [1, 1]
            X = self.pos[0] - target[0]
            Y = self.pos[1] - target[1] 
            angle = math.atan2(Y,X)
            error = math.radians(ZEPPELIN_FIRING_ANGLE_ERROR)
            angle += error
            bullet_vel[0] = -math.ceil( self.bullet_speed * math.cos(angle) ) 
            bullet_vel[1] = -math.ceil( self.bullet_speed * math.sin(angle) ) 
            pos = [self.pos[0], self.pos[1] + 60]
            self.bullet_list.append( FighterBullet( self.bullet_colour, 
                                                    self.bullet_size, 
                                                    self.bullet_length,
                                                    pos, 
                                                    bullet_vel, 
                                                    [0, 0] ) )    
    
    #update fire timer
    def update_fire_timer(self, target, max_interval ):
        self.fire_ticker += 1
        if( self.fire_ticker >= self.fire_interval ):
            self.fire_ticker = 0
            self.fire_interval = random.randrange(0, max_interval )
            self.fire_bullet(target)  
    
#==========================================================            
class Game:
    #Initialize
    def __init__(self):
        self.state = "Menu"
        self.score = 0
        self.kills = 0
        self.hits = 0
        self.background_music = sounds['background_music_level1']
        self.background_image = ImageInfo( images['cloud_image'], [CANVAS_WIDTH//2, CANVAS_HEIGHT//2] )
        self.player_plane = Spitfire()
        
        #LEVEL 1
        self.turret_list = []
        self.messerschmitt_list = []
        self.zeppelin_list = []
        self.tree_list = []
        
        #LEVEL 2
        nothing = 0
         
    #returns state
    def get_state(self):
        return self.state
    
    #set state
    def set_state(self, state_val):
        self.state = state_val
    
    #Game state machine
    def update_state(self, canvas, ai, ui ):
       
        #LEVELS
        if self.state is not "Menu":
            self.background_image.draw(canvas)
            self.show_status(canvas)
            
            #Update states
            self.level_update()
            
            #update enemy, elements
            self.enemy_update(canvas)
            self.element_update(canvas)
            
            #update player
            if not self.player_plane.get_state("destroy"):   
                self.background_music.play()
                self.player_plane_update(canvas)
            else:	
                self.end_game(canvas)
            
            #delete objects
            self.del_turret()
            self.del_messerschmitt()
            self.del_zeppelin()
            self.del_tree()
            
            #AI
            ai.new_messerschmitt(self)
            ai.new_zeppelin(self)
            ai.new_turret(self)
            ai.new_tree(self)
            ai.attack_player(self)
        
        #UI
        ui.update_state(game)
        ui.draw(canvas)
            
    #LEVEL Initializations
    def level_init(self, level):    
        if level == "Level_1":
            #background image
            frame.set_canvas_background(CANVAS_LEVEL1_BACKGROUND)
            self.background_image = ImageInfo( images['cloud_image'], [CANVAS_WIDTH//2, CANVAS_HEIGHT//2] )
            self.background_image.show = True
            
            #background music
            self.background_music = sounds['background_music_level1']
            
            # create random trees
            for i in range( 0 , random.randrange(0, 30 ) ):
                if random.randrange(1,3) == 1:
                    self.tree_list.append( GreenConifer( random.randrange(1, CANVAS_WIDTH, 10) ) )
                else:
                    self.tree_list.append( AuburnConifer( random.randrange(1, CANVAS_WIDTH, 10 ) ) )
    
    #LEVEL UPDATE
    def level_update(self):
        if (self.state == "Level_1") and (self.kills == LEVEL1_ZEPPELIN_ENTRY_KILLS ):
            self.state = "Level_1_zep"
    
    #PLAYER update
    def player_plane_update(self, canvas):
        self.player_plane.update_pos()
        self.player_plane.check_boundary()
        self.player_plane.update_state()
        self.player_plane.draw(canvas)
        
        if (self.state == "Level_1") or (self.state == "Level_1_zep") :
            for turret in self.turret_list:
                self.player_plane.check_hit( turret.bullet_list, "turret_bullet" )
            for messerschmitt in self.messerschmitt_list :
                self.player_plane.check_hit( messerschmitt.bullet_list, "bullet" )
                self.player_plane.check_collision( messerschmitt )
            for zeppelin in self.zeppelin_list :
                self.player_plane.check_hit( zeppelin.bullet_list, "bullet" )
                self.player_plane.check_collision( zeppelin )
    
    #ENEMY update
    def enemy_update(self, canvas):
        #turrets update
        for turret in self.turret_list:
            turret.update_pos()
            turret.update_state()
            turret.draw(canvas)
            bullet_hits = turret.check_hit( self.player_plane.bullet_list, "bullet")
            turret.check_hit( self.player_plane.bomb_list, "bomb")
            self.score += bullet_hits
       
        #messerchmitt update
        for messerschmitt in self.messerschmitt_list:
            messerschmitt.update_pos()
            messerschmitt.check_boundary()
            messerschmitt.update_state()
            messerschmitt.draw(canvas)
            bullet_hits = messerschmitt.check_hit( self.player_plane.bullet_list, "bullet" )
            messerschmitt.check_hit( self.player_plane.bomb_list, "bomb" )
            self.score += bullet_hits
        
        #zeppelin
        for zeppelin in self.zeppelin_list:
            zeppelin.update_pos()
            zeppelin.check_boundary()
            zeppelin.update_state()
            zeppelin.draw(canvas)
            bullet_hits = zeppelin.check_hit( self.player_plane.bullet_list, "bullet" )
            zeppelin.check_hit( self.player_plane.bomb_list, "bomb" )
            self.score += bullet_hits
    
    #ELEMENTS update
    def element_update(self, canvas):
        if (self.state == "Level_1") or (self.state == "Level_1_zep") or (self.state == "End"):
            for tree in self.tree_list:	#trees
                tree.update_state()
                tree.draw(canvas)
    
    #END Game
    def end_game(self, canvas):
        self.state = "End"
        self.background_music.pause()
        self.background_music.rewind()
        
    #Show gameplay status on the top right
    def show_status( self, canvas):
        #show_score on top
        canvas.draw_text( "SCORE", (SCORE_X, SCORE_Y), 15, "Blue")
        canvas.draw_text( str(self.score), (SCORE_VAL_X, SCORE_VAL_Y), 30, "Red")
        
        #show damage
        colour = "Red"
        canvas.draw_text( "LIFE", (LIFE_X , LIFE_Y), 15, "Blue")
        if self.player_plane.damage <= 50:
            colour = "Green"
        elif ( self.player_plane.damage > 50 ) and ( self.player_plane.damage < 70 ):
            colour = "Yellow"
        elif ( self.player_plane.damage >= 70 ) and ( self.player_plane.damage <= 100 ):
            colour = "Red"
        
        #show kills
        canvas.draw_text( "KILLS", (KILLS_X , KILLS_Y), 15, "Blue")
        canvas.draw_text( str(self.kills), (KILLS_VAL_X, KILLS_VAL_Y), 30, "Olive")
        
        #draw life bar
        if ( self.player_plane.damage <= 100 ):
            canvas.draw_line(	[LIFE_BAR_X, LIFE_BAR_Y], 
                                [LIFE_BAR_X + LIFE_BAR_LEN + (100 - self.player_plane.damage), LIFE_BAR_Y], 
                                12, colour )
            
        #show bombs available
        image_size = [ images['bomb_image'].get_width(), images['bomb_image'].get_height() ]
        image_center = [image_size[0]//2, image_size[1]//2 ]
        canvas.draw_image( images['bomb_image'], image_center, image_size, [BOMB_DISP_X, BOMB_DISP_Y], image_size )
        canvas.draw_text( str(self.player_plane.bomb_num), [BOMB_VAL_X, BOMB_VAL_Y], 20, "Red")
         
    #Move landscpae
    def move_landscape(self):
        #move turrets
        for turret in self.turret_list:
            turret.pos -= 2
        #move trees
        for tree in self.tree_list:
            tree.pos[0] -= 2
    
    #Add turret
    def create_turret(self, pos ):
        self.turret_list.append( Turret(pos) )
    
    #Delete turret
    def del_turret(self):
        remove = []
        for turret in self.turret_list:
            if turret.get_state("destroy"):
                remove.append( turret )
                if turret.get_state("score"):
                    self.score += TURRET_SCORE_DESTROY
                    self.kills += 1
        for turret in remove:
            x = self.turret_list.pop( self.turret_list.index(turret) )
            del x
          
    #Create messerschmitt
    def create_messerschmitt(self, pos):
        self.messerschmitt_list.append( Messerschmitt(  pos, 
                                                        vel = [-4, 0], 
                                                        acc = [3, 2], 
                                                        ang_vel = 0, 
                                                        ang_acc = 0.02 , 
                                                        orient = "left", 
                                                        rotation = 0) )
                     
    #Delete messerschmitt 
    def del_messerschmitt(self):
        remove = []
        for messerschmitt in self.messerschmitt_list:
            if messerschmitt.get_state("destroy"):
                remove.append( messerschmitt )
                if messerschmitt.get_state("score"):
                    self.score += MESSERSCHMITT_SCORE_DESTROY
                    self.kills += 1
        for messerschmitt in remove:
            x = self.messerschmitt_list.pop( self.messerschmitt_list.index(messerschmitt) )
            del x
    
    #Create zeppelin
    def create_zeppelin(self, pos):
        self.zeppelin_list.append( Zeppelin(pos) )
    
    #Delete zeppelin
    def del_zeppelin(self):
        remove = []
        for zeppelin in self.zeppelin_list:
            if zeppelin.get_state("destroy"):
                remove.append( zeppelin )
                if zeppelin.get_state("score"):
                    self.score += ZEPPELIN_SCORE_DESTROY
                    self.kills += 1
        for zeppelin in remove:
            x = self.zeppelin_list.pop( self.zeppelin_list.index(zeppelin) )
            del x
    
    #Add tree
    def create_tree(self, tree_type ):
        if tree_type == "green":
            self.tree_list.append( GreenConifer() )
        elif tree_type == "auburn":
            self.tree_list.append( AuburnConifer() )
            
    #Delete tree
    def del_tree(self):
        remove = []
        for tree in self.tree_list:
            if ( not tree.get_state() ):
                remove.append( tree )
        for tree in remove:
            x = self.tree_list.pop( self.tree_list.index(tree) )
            del x 
 
#==========================================================
class Ai():
    #initialize
    def __init__(self):
        self.tree_ticker = 0
        self.tree_interval = AI_TREE_CREATE_MAX_INTERVAL
        self.messerschmitt_ticker = 0
        self.messerschmitt_interval = AI_MESSERSCHMITT_CREATE_MAX_INTERVAL
        self.zeppelin_ticker = 0
        self.zeppelin_interval = AI_ZEPPELIN_CREATE_MAX_INTERVAL
        self.turret_ticker = 0
        self.turret_interval = AI_TURRET_CREATE_MAX_INTERVAL
    
    # update tickers
    def update_tickers(self):
        self.turret_ticker += 1
        self.tree_ticker += 1
        self.messerschmitt_ticker += 1
        self.zeppelin_ticker += 1
    
    #create new AI messerschmitt
    def new_messerschmitt(self, game):
        if game.get_state() == "Level_1":
            if ( self.messerschmitt_ticker >= self.messerschmitt_interval ) and game.player_plane.state['Flying']:
                
                pos = [0,0]
                pos[0] = CANVAS_WIDTH
                pos[1] = random.randrange(100, 501, 100)
                game.create_messerschmitt(pos)
                self.messerschmitt_ticker = 0
               
                maxim = AI_MESSERSCHMITT_CREATE_MAX_INTERVAL - math.ceil( game.score * DIFFICULTY_RATE )
                if( maxim < ( AI_MESSERSCHMITT_CREATE_MIN_INTERVAL + 50 ) ):
                    maxim = AI_MESSERSCHMITT_CREATE_MIN_INTERVAL + 50
                self.messerschmitt_interval = random.randrange( AI_MESSERSCHMITT_CREATE_MIN_INTERVAL,maxim, 50 )
    
    #AI create new zeppelin
    def new_zeppelin(self, game):
        if game.get_state() == "Level_1_zep" :
           
            if ( self.zeppelin_ticker >= self.zeppelin_interval ):
                pos = [0,0]
                pos[0] = CANVAS_WIDTH + 300
                pos[1] = random.randrange(100, 401, 100)
                game.create_zeppelin(pos)
                self.zeppelin_ticker = 0
                self.zeppelin_interval = random.randrange(  AI_ZEPPELIN_CREATE_MIN_INTERVAL, AI_ZEPPELIN_CREATE_MAX_INTERVAL, 100 )
    
    #AI create new turret
    def new_turret(self, game): 
        if self.turret_ticker >= self.turret_interval:
            game.create_turret(CANVAS_WIDTH)
            self.turret_ticker = 0
            
            maxim = AI_TURRET_CREATE_MAX_INTERVAL - math.ceil( game.score * DIFFICULTY_RATE )
            if( maxim < ( AI_TURRET_CREATE_MIN_INTERVAL + 50 ) ):
                maxim = AI_TURRET_CREATE_MIN_INTERVAL + 50
            self.turret_interval = random.randrange( AI_TURRET_CREATE_MIN_INTERVAL, maxim, 50 )
    
    #AI create tree
    def new_tree(self, game):
        if game.get_state() == "Level_1":
            if self.tree_ticker >= self.tree_interval:
                if random.randrange(1,3) == 1:
                    game.create_tree("green")
                else:
                    game.create_tree("auburn")
                self.tree_ticker = 0
                self.tree_interval = random.randrange( 	AI_TREE_CREATE_MIN_INTERVAL, 
                                                        AI_TREE_CREATE_MAX_INTERVAL )
    
    #AI chase player_plane
    def attack_player(self, game):
        #messerschmitts attacks player
        for attacker in game.messerschmitt_list:
            if( attacker.pos[0] > ( game.player_plane.pos[0] + (CANVAS_WIDTH//2) ) ):
                X = attacker.pos[0] - game.player_plane.pos[0]
                Y = attacker.pos[1] - game.player_plane.pos[1]
                attacker.rotation = math.atan2(Y,X)
            elif ( attacker.pos[1] > (CANVAS_HEIGHT - 180) ) or (attacker.pos[1] < 150 ):
                attacker.ang_vel = -( attacker.rotation / 10 )
    
#==========================================================
#EVENT HANDLERS
#---------------------------------------
#canvas handler
def draw(canvas): 
    global run_state, game, ai, ui
    
    if run_state == "loading":
        load(canvas)
    elif run_state == "loaded":
        init()
    elif run_state == "run":
        game.update_state(canvas, ai, ui)
    
#---------------------------------------
#down key handler
def down_key_handler(key):
    global game
    
    #player keys
    if game.get_state() != "Menu":
        game.player_plane.key_down(key)
 
    #reset
    if game.get_state() == "End":
        init()
        
#---------------------------------------   
#up key handler
def up_key_handler(key):
    global game
    if game.get_state() != "Menu":
        game.player_plane.key_up(key)
        
#---------------------------------------
#mouse click handler
def mouse_click_handler(pos):
    pos = list(pos)  
    #menu selection
    global game, ui 
    ui.start_menu_select(pos, game)
 
#---------------------------------------
#animation timer handler
def update_animation_timer():   
    #player
    game.player_plane.anim_timer_update()
    
    #turret
    for turret in game.turret_list:
        turret.anim_timer_update()
    
    #messerschmitt
    for messerschmitt in game.messerschmitt_list:
        messerschmitt.anim_timer_update()
    
    #zeppelin
    for zeppelin in game.zeppelin_list:
        zeppelin.anim_timer_update()

#---------------------------------------
#game speed timer handler
def update_game_speed_timer():    
    global game, ai
    
    if game.get_state() != "End":
 
        #update turret fire timers
        for turret in game.turret_list:
            turret.update_fire_timer( game.player_plane.pos )
        
        #update messerschmitt fire timers
        for messerschmitt in game.messerschmitt_list:
            messerschmitt.update_fire_timer( MAX_MESSERSCHMITT_FIRE_INTERVAL )
        
        #update zeppelin fire timers
        for zeppelin in game.zeppelin_list:
            zeppelin.update_fire_timer( game.player_plane.pos, MAX_ZEPPELIN_FIRE_INTERVAL )
        
        #update create timers
        ai.update_tickers()
        
    #move landscape left
    game.move_landscape()

#==========================================================
#GLOBAL FUNCTIONS
#calculate distance between two points
def distance( p, q ):
    return math.ceil( math.sqrt( ( ( p[0] - q[0] ) ** 2 ) + ( ( p[1] - q[1] ) ** 2 ) ) )

#---------------------------------------
#load game
def load(canvas):
    global run_state
    
    full = len(images)
    count = 0
    for image in images:
        if images[image].get_width() == 0:
            count += 1
    if count <= 1 :
        run_state = "loaded"
    add = math.ceil( ( (full - count) / full ) * 400 )
    canvas.draw_text("LOADING", (CANVAS_WIDTH//2 - 100, CANVAS_HEIGHT//2 - 50), 40, "White")
    canvas.draw_line( 	(CANVAS_WIDTH//2 - 200, CANVAS_HEIGHT//2), 
                        (CANVAS_WIDTH//2 - 200 + add, CANVAS_HEIGHT//2), 30, "Blue")
    
#---------------------------------------
#initialize game objects
def init():
    global game, ai, ui, run_state
    del game
    del ai
    del ui
    game = Game()
    ai = Ai()
    ui = UserInterface()
    ui.create_all()
    run_state = "run"
    
#==========================================================
#CREATE FRAME
frame = simplegui.create_frame("ACE", CANVAS_WIDTH, CANVAS_HEIGHT )

#==========================================================
#IMAGES
URL_BASE = "https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/images/V2/"
URL = { 
'menu_background_image'	:	"menu_background.jpg"
,'thunderbolt_image'	: 	"P47Thunderbolt.png"
,'spitfire_image' 		:	"spitfire.png"
,'messerschmitt_image'	:	"messerschmitt.png"
,'zeppelin_image'		:	"zeppelin.png"
,'cloud_image'			:	"background_level1.png" 
,'turret_fire_ss_image'	:	"turret_fire.png"
,'bomb_image'			:	"air_bombs.png"
,'tree_green_image'		:	"conifer_green.png"
,'tree_auburn_image'	:	"conifer_auburn.png"
,'explosion1_ss_image' 	:	"explosion1.png"
,'explosion2_ss_image' 	:	"explosion2.png"
,'explosion3_ss_image' 	:	"explosion3.png"
,'explosion4_ss_image'	:	"explosion4.png"
,'smoke1_ss_image' 		:	"smoke1.png"
,'thunderbolt_ui_button':	"thunderbolt_ui_button.png"
,'spitfire_ui_button'	:	"spitfire_ui_button.png"
,'no_image' 			:	""
}
    
#==========================================================
#SOUNDS
SOUND = {
'menu_background_music' 		:	"https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/HorrorPen%20-%20Dramatic%20Action_0.mp3"
,'background_music_level1' 		:	"https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/Wasteland%20Showdown_0.m4a"
,'menu_select_sound' 			:	"https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/UI/MENU%20A_Select.wav"
,'thunderbolt_engine_sound' 	:	"https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/Aircraft%20Twin%20Prop%20Warmup.mp3"
,'thunderbolt_gun_sound' 		:	"https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/thunderbolt_gun_sound.mp3"
,'spitfire_engine_sound' 		:	""
,'spitfire_gun_sound' 			:	"https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/spitfire_gun_sound.mp3"
,'messerschmitt_engine_sound' 	:	""
,'messerschmitt_gun_sound' 		:	"https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/messerschmitt_gun_sound.mp3"
,'zeppelin_engine_sound' 		:	""
,'zeppelin_gun_sound' 			:	""
,'turret_gun_sound' 			:	"https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/A_large_-Blocko-8333_hifi.mp3"
,'explosion1_sound' 			:	"https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/explosion1.mp3"
,'explosion2_sound' 			:	"https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/explosion2.mp3"
,'explosion3_sound' 			:	"https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/explosion2.mp3"
,'bullet_hit'					:	"https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/bullet_hit.wav"
,'no_sound' 					:	"" }

#==========================================================
#REGISTER EVENT HANDLERS
frame.set_canvas_background(CANVAS_LEVEL1_BACKGROUND)
frame.set_draw_handler(draw)
frame.set_keydown_handler(down_key_handler)
frame.set_keyup_handler(up_key_handler)
frame.set_mouseclick_handler(mouse_click_handler)

#==========================================================
#ADD LABELS
label_list = ["CONTROLS", 
              "-----------------",
              "Shoot : SPACE",
              "Drop Bomb  	: B",
              "Move 		: Arrow Keys" ]

label_obj = []
for label in label_list:
    label_obj.append( frame.add_label(label) )

#==========================================================
#TIMER
animation_timer = simplegui.create_timer( ANIMATION_TIMER, update_animation_timer )
game_speed_timer = simplegui.create_timer( GAME_SPEED_TIMER, update_game_speed_timer )

#==========================================================
#LOAD
#load sounds
sounds = {}
for i in SOUND:
    sounds[i] = simplegui.load_sound( SOUND[i] )

#load images
images = {}
for i in URL:
    images[i] = simplegui.load_image( URL_BASE + URL[i] )

#load objects
run_state = "loading"
game = Game()
ai = Ai()
ui = UserInterface()
ui.create_all()

#start timers
animation_timer.start()
game_speed_timer.start()

#start frame
frame.start()
