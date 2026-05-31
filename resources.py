from pygame import image, mixer

def get_sprite(name):
    return image.load("assets/sprites/"+name+".png").convert_alpha();

def get_image(name):
    return image.load("assets/images/"+name+".png").convert();

def get_sound(name):
    return mixer.Sound("assets/sounds/"+name+".mp3");