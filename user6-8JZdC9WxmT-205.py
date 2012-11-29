#ACE"
VER = "1.0"
CREATOR = "Ayush Sinha"
YEAR = "2012"

#change score problem!
#enemy should evade bullets
#turret tip should follow plane ( even if not shooting )
#german fighters should shoot "at" the player  - timer
#turret should shoot bombs!! - timer
#include the zeppelin
#include "after death" message
#include reset button with playing instrucitions
#include air alarm sound
#limited no of bombs for the aircraft
#include levels  - change levels with points
#	first level messer... only - different trees
#    second level - add turrets with messer - different trees, NIGHT BACKGROUND, THUNDER!!
        #destroy night time towers
#    third level - include zeppelin
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
CANVAS_BACKGROUND = "AEC9E4"

#Timer
ANIMATION_TIMER = 50
GAME_SPEED_TIMER = 10
PLANE_AI_TIMER = 1000

#display
SCORE_WIDTH = CANVAS_WIDTH - 100
SCORE_HEIGHT = 30
SCORE_VAL_WIDTH = SCORE_WIDTH
SCORE_VAL_HEIGHT = 60
LIFE_WIDTH = CANVAS_WIDTH - 250
LIFE_HEIGHT = 30
LIFE_BAR_WIDTH = LIFE_WIDTH
LIFE_BAR_HEIGHT = 50

#PLANES 
CRASH_MARGIN = 10
ai_plane_ticker = 0
ai_plane_interval = 5
ai_turret_ticker = 0
ai_turret_interval = 10
ai_tree_ticker = 0
ai_tree_interval = 50

#menu
menu_background_size = [1000, 680]
menu_spitfire_center = [282, 504]
menu_thunderbolt_center = [709,498]
menu_select_range = 120

#turret
turret_radius = 20
turret_fire_size = [1024, 60]
turret_fire_ss_num = [ 16, 1 ]
turret_damage_rate =40

#thunderbolt
thunderbolt_size = [128, 54]
thunderbolt_vel = [0, 0]
thunderbolt_acc = [3, 1]
thunderbolt_ang_vel = 0
thunderbolt_ang_acc = 0.005
thunderbolt_orient = "right"
thunderbolt_bullet_colour = "Brown"
thunderbolt_bullet_size = 1
thunderbolt_bullet_length = 15
thunderbolt_bullet_speed = 10
thunderbolt_damage_rate = 10

#spitfire
spitfire_size = [128, 54]
spitfire_vel = [0, 0]
spitfire_acc = [3, 2]
spitfire_ang_vel = 0
spitfire_ang_acc = 0.005
spitfire_orient = "right"
spitfire_bullet_colour = "Blue"
spitfire_bullet_size = 1
spitfire_bullet_length = 15
spitfire_bullet_speed = 10
spitfire_damage_rate = 5

#messerschmitt
messerschmitt_size = [128, 45]
messerschmitt_vel = [-4, 0]
messerschmitt_acc = [3, 2]
messerschmitt_ang_vel = 0
messerschmitt_ang_acc = 0.02
messerschmitt_orient = "left"
messerschmitt_bullet_colour = "Black"
messerschmitt_bullet_size = 1
messerschmitt_bullet_length = 15
messerschmitt_bullet_speed = 10
messerschmitt_damage_rate = 20

#zepplin
zeppelin_size = [500, 300]
zeppelin_vel = [0, 0]
zeppelin_acc = [3, 2]
zeppelin_ang_vel = 0
zeppelin_ang_acc = 0.01
zeppelin_orient = "left"
zeppelin_bullet_colour = "Yellow"
zeppelin_bullet_size = 3
zeppelin_bullet_length = 20
zeppelin_bullet_speed = 10
zeppelin_damage_rate = 10

#bomb
bomb_size = [40, 15]

#tree
tree_size = [44,65]

#clouds
cloud_size = [1000, 752]
cloud_center = [cloud_size[0]/2, cloud_size[1]/2]

#explosion
explosion1_size = [256, 256 ]
explosion1_ss_num = [4, 4]
explosion2_size = [1024, 61]
explosion2_ss_num = [ 16, 1]
explosion3_size = [ 1024, 630 ]
explosion3_ss_num = [8, 5]

#smoke
smoke1_size = [800, 510 ]
smoke1_ss_num = [8, 5]

#CLASSES 
#==========================================================
class Animation:
     #initialize
     def __init__ ( self, image, sound, size, ss_num ):
        self.image = image
        self.sound = sound
        self.size = list(size)
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
            self.sound.play()
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
    def __init__(self, image, size, pos):
        self.image = image
        self.pos = list(pos)
        self.size = list(size)
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
class Turret:
    #initialize
    def __init__(self, pos, radius, damage_rate):
        self.gun_anim = Animation( 		turret_fire_ss_image, 
                                        turret_gun_sound, 
                                        turret_fire_size, 
                                        turret_fire_ss_num )
        
        self.damage_anim = Animation(	smoke1_ss_image,
                                        no_sound, smoke1_size, 
                                        smoke1_ss_num )
        
        self.blow_anim = Animation( 	explosion3_ss_image, 
                                        explosion3_sound, 
                                        explosion3_size, 
                                        explosion3_ss_num )
        self.pos = pos
        self.radius = radius
        self.firing_angle = 90
        self.turret_len = 10
        self.turret_width = 10
        self.turret_colour = "Black"
        self.bullet_list = []
        self.bullet_colour = "Brown"
        self.bullet_size = 4
        self.bullet_length = 15
        self.bullet_speed = 38
        self.vert1 = [0,0]
        self.vert2 = [0,0]
        self.damage = 0
        self.damage_rate = damage_rate
        self.damage = 0
        self.state = { 'Working':	True,
                       'Damage':	False,
                       'Explode':	False }
       
    #update state
    def update_state(self):
        if( (self.damage > 50) and (self.damage < 100) ):
            self.state['Damage'] = True 
        elif ( self.damage >= 100 ) and self.state['Working']:
            self.blow_anim.animate(self.vert1)
            self.state['Explode'] = True
            self.state['Working'] = False
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
            if self.state['Damage']:
                if not self.damage_anim.get_state():
                    self.damage_anim.animate(self.vert1)
            
        #update bullets
        remove = []
        for i in range( 0, len(self.bullet_list) ):
            self.bullet_list[i].update_pos()
            self.bullet_list[i].draw(canvas)
            if ( self.bullet_list[i].out_of_range() ):
                remove.append( self.bullet_list[i] )
        for bullet in remove:
            x = self.bullet_list.pop( self.bullet_list.index(bullet) )
            del x
    
    #animation timer update
    def anim_timer_update(self):
        self.gun_anim.next_image()
        self.damage_anim.next_image()
        self.blow_anim.next_image()
    
    #fire 
    def fire(self, angle):
        self.firing_angle = angle
        self.gun_anim.animate(self.vert2)
        bullet_vel = [0, 0]
        bullet_vel[0] = math.ceil( self.bullet_speed * math.cos( self.firing_angle * math.pi / 180 ) )
        bullet_vel[1] = -math.ceil( self.bullet_speed * math.sin( self.firing_angle * math.pi / 180 ) )
        self.bullet_list.append( Bullet( self.bullet_colour, self.bullet_size, self.bullet_length,
                                 self.vert2, bullet_vel, [0, 1]  ) )
    
    #cause self damage
    def cause_damage(self, item_type ): 
        if item_type == "bullet":
            self.damage += self.damage_rate
        elif item_type == "bomb":
            self.damage += 100	
        
    #returns state
    def get_state(self):
        return ( self.state['Working'] or self.state['Explode'] )
    
    # check bullet hit
    def check_hit(self, ext_list, item_type ):
        remove = []
        for i in range( 0, len(ext_list) ):
            if ( distance( ext_list[i].get_pos(), [self.pos, CANVAS_HEIGHT] ) <= ( self.radius + self.turret_len ) ):
                remove.append( ext_list[i] )
        for item in remove:
            self.cause_damage(item_type)
            x = ext_list.pop( ext_list.index(item) )
            del x
            
#==========================================================
class Bullet:
    #initialize
    def __init__(self, colour, size, length, p, vel, acc ):
        self.colour = colour
        self.size = size
        self.length = length
        self.p = list(p)
        self.vel = list(vel)
        self.acc = list(acc)
        self.vert = [0, 0]
      
    #update position
    def update_pos(self):
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]
        self.p[0] += self.vel[0]
        self.p[1] += self.vel[1]
        
        if( self.vel[0] == 0 ):
           self.vert[0] = self.p[0]
           self.vert[1] = self.p[1] + self.length
        else:
            self.vert[0] = self.p[0] + math.floor( self.length * ( math.cos( math.atan( self.vel[1] / self.vel[0] ) ) ) ) 
            self.vert[1] = self.p[1] + math.floor( self.length * ( math.sin( math.atan( self.vel[1] / self.vel[0] ) ) ) )	
        
    #draw
    def draw(self,canvas):
        canvas.draw_line( self.p, self.vert, self.size , self.colour )
     
    #check border
    def out_of_range(self):
        if( ( self.vert[0] < 0 ) or ( self.vert[0] > CANVAS_WIDTH ) ):
            return True
        elif( ( self.vert[1] < 0 ) or ( self.vert[1] > CANVAS_HEIGHT ) ):
            return True
        else:
            return False
     
    #returns position
    def get_pos(self):
        return self.vert

#========================================================== 
class Bomb:
    #initialize 
    def __init__( self, image, size, pos):
        self.image = image
        self.size = list(size)
        self.sound = no_sound
        self.blow_anim = Animation(		explosion2_ss_image, 
                                        explosion2_sound, 
                                        explosion2_size, 
                                        explosion2_ss_num )
        self.pos = list(pos)
        self.vel = [0, 5 ]
        self.acc = [0, 0 ]
        self.state = { 	'Flying' :	True,
                        'Explode':	False
                     }
    #update state
    def update_state(self):
        self.sound.play()
        #check boundaries
        if self.state['Flying']:
            if ( self.pos[1] > ( CANVAS_HEIGHT - (self.size[1]/2 ) - CRASH_MARGIN ) ):
                self.sound.pause()
                self.blow_anim.animate(self.pos)
                self.state['Explode'] = True
                self.state['Flying'] = False
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
            #draw body
            canvas.draw_image(self.image, [self.size[0]//2, self.size[1]//2], 
                              self.size, self.pos, self.size)
        
    # animation timer update
    def anim_timer_update(self):
        self.blow_anim.next_image()
        
    # get flying state
    def get_state(self):
        return ( self.state['Flying'] or self.state['Explode'] )
    
    # get position
    def get_pos(self):
        return self.pos
    
#==========================================================        
class Fighter: 
    #initialize 
    def __init__( 	self, image, size, engine_sound, gun_sound, 
                    pos, vel, acc, ang_vel, ang_acc, orient,
                    bullet_colour, bullet_size, bullet_length, 
                    bullet_speed,
                    damage_rate ):
        
        self.image = image
        self.size = size
        self.damage_anim = Animation(	smoke1_ss_image,
                                        no_sound, smoke1_size, 
                                        smoke1_ss_num )
        
        self.blow_anim = Animation(		explosion1_ss_image, 
                                        explosion1_sound, 
                                        explosion1_size, 
                                        explosion1_ss_num )
        self.pos = list(pos)
        self.vel = list(vel)
        self.acc = list(acc)
        self.ang_vel = ang_vel
        self.ang_acc = ang_acc
        self.lift_factor = 10
        self.orient = orient 
        self.rotation = 0
        self.engine_sound = engine_sound
        self.gun_sound = gun_sound
        self.bullet_list = []
        self.bomb_list = []
        self.bullet_colour = bullet_colour
        self.bullet_size = bullet_size
        self.bullet_length = bullet_length
        self.bullet_speed = bullet_speed
        self.damage = 0
        self.damage_rate = damage_rate
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
            self.blow_anim.animate(self.pos)
            self.state['Explode'] = True
            self.state['Flying'] = False
        elif ( self.state['Explode'] and ( not self.blow_anim.get_state() ) ):
                self.state['Explode'] = False
           
    #update fighter position
    def update_pos( self ):
        #update position
        self.pos[0] += self.vel[0]
        if  self.orient == "right":
            self.pos[1] += self.vel[1] + math.ceil( self.lift_factor * math.sin( self.rotation ) )
        else:
            self.pos[1] += self.vel[1] - math.ceil( self.lift_factor * math.sin( self.rotation ) )
        self.rotation += self.ang_vel
        
        #check boundaries
        if self.state['Flying']:
            if ( self.pos[1] > ( CANVAS_HEIGHT - (self.size[1]/2 ) - CRASH_MARGIN ) ):
                self.blow_anim.animate(self.pos)
                self.engine_sound.pause()
                self.state['Flying'] = False
                self.state['Explode'] = True
                self.pos[1] = CANVAS_HEIGHT - (self.size[1]/2 )
            elif ( self.pos[1] < (self.size[1]/2) ):
                self.pos[1] = self.size[1]/2
            elif ( self.pos[0] > ( CANVAS_WIDTH - (self.size[0]/2 ) ) ):
                self.pos[0] = CANVAS_WIDTH - (self.size[0]/2 )
            elif ( self.pos[0] < -1 * ( self.size[1] ) ):
                self.pos[0] = self.size[1]
            
    #draw fighter
    def draw(self, canvas): 
        #draw elements
        self.damage_anim.draw(canvas, self.pos )
        self.blow_anim.draw(canvas, self.pos )
        
        #check state
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
        for i in range( 0, len(self.bullet_list) ):
            self.bullet_list[i].update_pos()
            self.bullet_list[i].draw(canvas)
            if ( self.bullet_list[i].out_of_range() ):
                remove.append( self.bullet_list[i] )
        for bullet in remove:
            x = self.bullet_list.pop( self.bullet_list.index(bullet) )
            del x
            
        #draw/remove bomb
        remove = []
        for i in range( 0, len(self.bomb_list) ):
            self.bomb_list[i].update_pos()
            self.bomb_list[i].update_state()
            self.bomb_list[i].draw(canvas)
            if ( not self.bomb_list[i].get_state() ):
                remove.append( self.bomb_list[i] )
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
            elif ( key == simplegui.KEY_MAP["b"] ):
                self.fire_bomb()
    
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
            self.bullet_list.append( Bullet( 	self.bullet_colour, self.bullet_size, self.bullet_length,
                                                self.pos, bullet_vel, [0, 0] ) )    
    
    # fire bomb
    def fire_bomb( self ):
        if self.state['Flying']:
            bomb_vel = [0,0]
            bomb_vel[1] = 2
            if self.orient == "right":
                bomb_vel[0] = self.vel[0]
            self.bomb_list.append( Bomb( bomb_image, bomb_size, self.pos, ) ) 
        
    # cause self damage
    def cause_damage(self, item_type ): 
        if item_type == "bullet":
            self.damage += self.damage_rate
        elif item_type == "bomb":
            self.damage += 100
    
    # get flying state
    def get_state(self):
        return ( self.state['Flying'] or self.state['Explode'] )
    
    # check hit
    def check_hit(self, ext_list, item_type ):
        remove = []
        for i in range( 0, len(ext_list) ):
            if ( distance( ext_list[i].get_pos(), self.pos ) < 50 ):
                remove.append( ext_list[i] )
        for item in remove:
            self.cause_damage(item_type)
            x = ext_list.pop( ext_list.index(item) )
            del x
    
    # check collision
    def check_collision(self, ext_plane ):
        if ( distance( ext_plane.pos , self.pos )  < self.size[1] ) and self.state['Flying'] and ext_plane.state['Flying']:
            self.engine_sound.pause()
            self.blow_anim.animate(self.pos)
            self.state['Explode'] = True
            self.state['Flying'] = False
            
#==========================================================            
class Game:
    #initialize
    def __init__(self):
        self.score = 0
        self.player_plane = Fighter(spitfire_image, 
                                    spitfire_size, 
                                    spitfire_engine_sound, 
                                    spitfire_gun_sound,
                                    [100, CANVAS_HEIGHT/2], 
                                    spitfire_vel, 
                                    spitfire_acc, 
                                    spitfire_ang_vel, 
                                    spitfire_ang_acc,
                                    spitfire_orient, 
                                    spitfire_bullet_colour, 
                                    spitfire_bullet_size, 
                                    spitfire_bullet_length, 
                                    spitfire_bullet_speed,
                                    spitfire_damage_rate )
        self.turret_list = []
        self.messerschmitt_list = []
        self.tree_list = []
        self.menu_state = True
        self.play_state = False
        self.score_state = False
    
    #mouse menu select
    def menu_select(self, pos):
        if self.menu_state:
            if( distance( pos, menu_spitfire_center ) < menu_select_range ) : 
                menu_select_sound.play()
                self.menu_state = False
                self.score_state = False
                self.play_state = True
                menu_background_music.rewind()
                menu_background_music.pause()
                self.player_plane = Fighter(spitfire_image, 
                                            spitfire_size, 
                                            spitfire_engine_sound, 
                                            spitfire_gun_sound,
                                            [100, CANVAS_HEIGHT/2], 
                                            spitfire_vel, 
                                            spitfire_acc, 
                                            spitfire_ang_vel,
                                            spitfire_ang_acc,
                                            spitfire_orient, 
                                            spitfire_bullet_colour, 
                                            spitfire_bullet_size, 
                                            spitfire_bullet_length, 
                                            spitfire_bullet_speed,
                                            spitfire_damage_rate )
          
            elif ( distance( pos, menu_thunderbolt_center ) < menu_select_range ) : 
                menu_select_sound.play()
                self.menu_state = False
                self.score_state = False
                self.play_state = True
                menu_background_music.rewind()
                menu_background_music.pause()
                self.player_plane = Fighter(thunderbolt_image, 
                                            thunderbolt_size,  
                                            thunderbolt_engine_sound, 
                                            thunderbolt_gun_sound, 
                                            [100, CANVAS_HEIGHT/2], 
                                            thunderbolt_vel, 
                                            thunderbolt_acc, 
                                            thunderbolt_ang_vel, 
                                            thunderbolt_ang_acc,
                                            thunderbolt_orient, 
                                            thunderbolt_bullet_colour, 
                                            thunderbolt_bullet_size, 
                                            thunderbolt_bullet_length, 
                                            thunderbolt_bullet_speed, 
                                            thunderbolt_damage_rate )
    
    #show score
    def show_score(self, canvas):
        pass
    
    #show status
    def show_status( self, canvas):
        #show_score on top
        canvas.draw_text( "SCORE", (SCORE_WIDTH , SCORE_HEIGHT), 15, "Blue")
        canvas.draw_text( str(self.score), (SCORE_VAL_WIDTH, SCORE_VAL_HEIGHT), 30, "Red")
        
        #show damage
        colour = "Red"
        canvas.draw_text( "LIFE", (LIFE_WIDTH , LIFE_HEIGHT), 15, "Blue")
        if self.player_plane.damage <= 50:
            colour = "Green"
        elif ( self.player_plane.damage > 50 ) and ( self.player_plane.damage < 70 ):
            colour = "Yellow"
        elif ( self.player_plane.damage >= 70 ) and ( self.player_plane.damage <= 100 ):
            colour = "Red"
        
        #draw life bar
        if ( self.player_plane.damage <= 100 ):
            canvas.draw_line(	[LIFE_BAR_WIDTH, LIFE_BAR_HEIGHT], 
                                [CANVAS_WIDTH - 150 - self.player_plane.damage, LIFE_BAR_HEIGHT], 
                                12, colour )
        
    #game reset
    def reset(self):
        #random turrets
        for i in range( 0, random.randrange(0,2) ):
            self.create_turret( random.randrange(10, CANVAS_WIDTH ) )
        
        #random trees
        for i in range( 0 , random.randrange(0, 30 ) ):
            self.create_tree( random.randrange(0, CANVAS_WIDTH ) )
    
    #add turret
    def create_turret(self, pos ):
        self.turret_list.append( Turret( pos, turret_radius, turret_damage_rate ) )
    
    #delete turret
    def del_turret(self):
        remove = []
        for i in range( 0, len( self.turret_list) ):
            if not self.turret_list[i].get_state():
                remove.append( self.turret_list[i] )
                self.score += 50
            elif ( self.turret_list[i].pos < 0 ):
                remove.append( self.turret_list[i] )
        for turret in remove:
            x = self.turret_list.pop( self.turret_list.index(turret) )
            del x
    
    #add messerchmitt
    def create_messerschmitt(self, pos ):
        self.messerschmitt_list.append( Fighter( 	messerschmitt_image, 
                                                    messerschmitt_size, 
                                                    messerschmitt_engine_sound, 
                                                    messerschmitt_gun_sound, 
                                                    pos, 
                                                    messerschmitt_vel, 
                                                    messerschmitt_acc, 
                                                    messerschmitt_ang_vel,
                                                    messerschmitt_ang_acc,
                                                    messerschmitt_orient, 
                                                    messerschmitt_bullet_colour, 
                                                    messerschmitt_bullet_size, 
                                                    messerschmitt_bullet_length, 
                                                    messerschmitt_bullet_speed ,
                                                    messerschmitt_damage_rate ) )
     
    #delete messerschmitt 
    def del_messerschmitt(self):
        remove = []
        for i in range( 0, len( self.messerschmitt_list) ):
            if ( not self.messerschmitt_list[i].get_state() ):
                remove.append( self.messerschmitt_list[i] )
                self.score += 10
            elif ( self.messerschmitt_list[i].pos[0] < self.messerschmitt_list[i].size[1] ): 
                remove.append( self.messerschmitt_list[i] )
        for messerschmitt in remove:
            x = self.messerschmitt_list.pop( self.messerschmitt_list.index(messerschmitt) )
            del x
    
    #add tree
    def create_tree(self, pos):
        self.tree_list.append( Tree( tree_image, tree_size, [pos, CANVAS_HEIGHT - tree_size[1]/2 ] ) )
    
    #delete tree
    def del_tree(self):
        remove = []
        for i in range( 0, len( self.tree_list) ):
            if ( not self.tree_list[i].get_state() ):
                remove.append( self.tree_list[i] )
        for tree in remove:
            x = self.tree_list.pop( self.tree_list.index(tree) )
            del x 
    
    #create AI messerschmitt
    def ai_create_messerschmitt(self):
        global ai_plane_interval, ai_plane_ticker
        if ai_plane_ticker >= ai_plane_interval:
            #create
            self.create_messerschmitt( [ CANVAS_WIDTH, random.randrange(100, 600, 100)] )
            ai_plane_ticker = 0
            ai_plane_interval = 5
            if self.score > 20:
                ai_plane_interval -= 1
            if self.score > 60:
                ai_plane_interval -= 1
    
    #create AI turret
    def ai_create_turret(self):
        global ai_turret_ticker, ai_turret_interval
        if ai_turret_ticker >= ai_turret_interval:
            self.create_turret(CANVAS_WIDTH)
            ai_turret_ticker = 0
            ai_turret_interval = random.randrange( 400, 700 )
    
    #create AI tree
    def ai_create_tree(self):
        global ai_tree_ticker, ai_tree_interval
        if ai_tree_ticker >= ai_tree_interval:
            self.create_tree(CANVAS_WIDTH)
            ai_tree_ticker = 0
            ai_tree_interval = random.randrange( 10, 80 )
        
    #move landscpae
    def move_landscape(self):
        #move turrets
        for i in range( 0, len( self.turret_list ) ):
            self.turret_list[i].pos -= 2
        #move trees
        for i in range( 0, len( self.tree_list ) ):
            self.tree_list[i].pos[0] -= 2
            
#==========================================================
#EVENT HANDLERS
#---------------------------------------
#canvas handler
def draw(canvas): 
    global game
    if ( game.menu_state ) :
        #background
        canvas.draw_image( menu_background_image, [ menu_background_size[0]/2,menu_background_size[1]/2 ], 
                           menu_background_size, [CANVAS_WIDTH/2, CANVAS_HEIGHT/2] , menu_background_size )
        menu_background_music.play()      
        
    elif ( game.play_state or game.score_state):
        #clouds
        canvas.draw_image(cloud_image, cloud_center, cloud_size, [CANVAS_WIDTH/2, CANVAS_HEIGHT/2] , cloud_size )
        #status
        game.show_status(canvas)
        
        #check if game is finished
        if not game.player_plane.get_state():
            game.play_state = False
            game.menu_state = False
            game.score_state = True
            game_background_music.pause()
            game_background_music.rewind()
        else:
            #player plane update
            game_background_music.play()
            game.player_plane.update_pos()
            game.player_plane.update_state()
            game.player_plane.draw(canvas)
            for i in range( 0, len( game.turret_list) ):
                game.player_plane.check_hit( game.turret_list[i].bullet_list, "bullet" )
            for i in range( 0, len( game.messerschmitt_list ) ):
                game.player_plane.check_hit( game.messerschmitt_list[i].bullet_list, "bullet" )
                game.player_plane.check_collision( game.messerschmitt_list[i] )
            
        #turrets update
        for i in range( 0, len( game.turret_list ) ):
            game.turret_list[i].update_pos()
            game.turret_list[i].update_state()
            game.turret_list[i].draw(canvas)
            game.turret_list[i].check_hit( game.player_plane.bullet_list, "bullet" )
            game.turret_list[i].check_hit( game.player_plane.bomb_list, "bomb" )
       
        #messerchmitt update
        for i in range( 0, len( game.messerschmitt_list ) ):
            game.messerschmitt_list[i].update_pos()
            game.messerschmitt_list[i].update_state()
            game.messerschmitt_list[i].draw(canvas)
            game.messerschmitt_list[i].check_hit( game.player_plane.bullet_list, "bullet" )
            game.messerschmitt_list[i].check_hit( game.player_plane.bomb_list, "bomb" )
            game.messerschmitt_list[i].check_collision( game.player_plane )
        
        #tree update
        for i in range( 0, len( game.tree_list ) ):
            game.tree_list[i].update_state()
            game.tree_list[i].draw(canvas)
            
        #create AI objects
        game.ai_create_messerschmitt()
        game.ai_create_turret()
        game.ai_create_tree()
        
        #delete objects
        game.del_turret()
        game.del_messerschmitt()
        game.del_tree()

#---------------------------------------
#down key handler
def down_key_handler(key):
    global game
    if game.play_state:
        #player
        game.player_plane.key_down(key)
 
    #reset
    elif game.score_state:
        del game
        game = Game()
        game.reset()
        
        
#---------------------------------------   
#up key handler
def up_key_handler(key):
    global game
    if game.play_state:
        #player
        game.player_plane.key_up(key)
        
#---------------------------------------
#mouse click handler
def mouse_click_handler(pos):
    pos = list(pos)  
    #menu selection
    global game
    game.menu_select(pos)
 
#---------------------------------------
#animation timer handler
def update_animation_timer():
    #player
    game.player_plane.anim_timer_update()
    
    #turret
    for i in range( 0, len( game.turret_list ) ):
        game.turret_list[i].anim_timer_update()
    
    #messerschmitt
    for i in range( 0, len( game.messerschmitt_list ) ):
        game.messerschmitt_list[i].anim_timer_update()
    
    #bullet

#---------------------------------------
#game speed timer handler
def update_game_move_timer():
    global game, ai_tree_ticker, ai_turret_ticker
    ai_turret_ticker += 1
    ai_tree_ticker += 1
    
    game.move_landscape()

#---------------------------------------
#AI plane creation timer
def update_game_plane_ai_timer():
    global ai_plane_ticker
    ai_plane_ticker += 1
    
#==========================================================
#HELPER FUNCTIONS
def distance( p, q ):
    return math.ceil( math.sqrt( ( ( p[0] - q[0] ) ** 2 ) + ( ( p[1] - q[1] ) ** 2 ) ) )

#==========================================================
#CREATE FRAME
frame = simplegui.create_frame("ACE", CANVAS_WIDTH, CANVAS_HEIGHT )

#==========================================================
#IMAGES
#menu
menu_background_image = simplegui.load_image("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/images/planesSpitfire1.png")

#planes
thunderbolt_image = simplegui.load_image("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/images/P47%20Thunderbolt.png")
spitfire_image = simplegui.load_image("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/images/spitfire1.png")
messerschmitt_image = simplegui.load_image("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/images/messerschmitt5.png")
zeppelin_image = simplegui.load_image("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/images/airship1.png")
cloud_image = simplegui.load_image("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/images/VolumetricCloudSample.png")

#turret
turret_fire_ss_image = simplegui.load_image("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/spritesheets/turret_fire.png")

#bomb
bomb_image = simplegui.load_image("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/images/air_bombs.png")

#tree
tree_image = simplegui.load_image("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/images/tree3_02.png")

#elements
explosion1_ss_image = simplegui.load_image("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/spritesheets/explosion1.png")
explosion2_ss_image = simplegui.load_image("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/spritesheets/explosion2.png")
explosion3_ss_image = simplegui.load_image("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/spritesheets/explosion3.png")
smoke1_ss_image = simplegui.load_image("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/spritesheets/smoke1.png")
no_image = simplegui.load_image("")

#==========================================================
#SOUNDS
#menu
menu_background_music = simplegui.load_sound("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/HorrorPen%20-%20Dramatic%20Action_0.mp3")
menu_select_sound = simplegui.load_sound("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/UI/MENU%20A_Select.wav")
game_background_music = simplegui.load_sound("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/Wasteland%20Showdown_0.ogg")

#planes
thunderbolt_engine_sound = simplegui.load_sound("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/Aircraft%20Twin%20Prop%20Warmup.mp3")
thunderbolt_gun_sound = simplegui.load_sound("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/thunderbolt_gun_sound.mp3")
spitfire_engine_sound = simplegui.load_sound("")
spitfire_gun_sound = simplegui.load_sound("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/spitfire_gun_sound.mp3")
messerschmitt_engine_sound = simplegui.load_sound("")
messerschmitt_gun_sound = simplegui.load_sound("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/messerschmitt_gun_sound.mp3")
zeppelin_engine_sound = simplegui.load_sound("")
zeppelin_gun_sound = simplegui.load_sound("")

#turrets
turret_gun_sound = simplegui.load_sound("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/A_large_-Blocko-8333_hifi.mp3")

#elements
explosion1_sound = simplegui.load_sound("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/explosion1.mp3")
explosion2_sound = simplegui.load_sound("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/explosion2.mp3")
explosion3_sound = simplegui.load_sound("https://dl.dropbox.com/u/20531919/Python%20Game%20Programming/sounds/explosion2.mp3")
no_sound = simplegui.load_sound("")

#==========================================================
#REGISTER EVENT HANDLERS
frame.set_canvas_background(CANVAS_BACKGROUND)
frame.set_draw_handler(draw)
frame.set_keydown_handler(down_key_handler)
frame.set_keyup_handler(up_key_handler)
frame.set_mouseclick_handler(mouse_click_handler)

#==========================================================
#TIMER
animation_timer = simplegui.create_timer( ANIMATION_TIMER, update_animation_timer )
game_move_timer = simplegui.create_timer( GAME_SPEED_TIMER, update_game_move_timer )
game_plane_ai_timer = simplegui.create_timer( PLANE_AI_TIMER, update_game_plane_ai_timer )


#==========================================================
#OBJECTS

#planes
zeppelin = Fighter( zeppelin_image, 
                    zeppelin_size, 
                    zeppelin_engine_sound, 
                    zeppelin_gun_sound, 
                    [700, 100], 
                    zeppelin_vel, 
                    zeppelin_acc, 
                    zeppelin_ang_vel,
                    zeppelin_ang_acc,
                    zeppelin_orient, 
                    zeppelin_bullet_colour, 
                    zeppelin_bullet_size,
                    zeppelin_bullet_length, 
                    zeppelin_bullet_speed,
                    zeppelin_damage_rate )

#Game
game = Game()
game.reset()

#==========================================================
#START
frame.start()
animation_timer.start()
game_move_timer.start()
game_plane_ai_timer.start()
