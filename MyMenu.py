from pygameMenuPro import *
from Tiles import Tiles
from MyGame import Game
Option.font.set_default_option(pygame.font.Font('AlphaWood.ttf', 50))
Option.font.set_default_title(pygame.font.SysFont('Plaguard-ZVnjx', 80))
Option.font.set_default_highlight(
    pygame.font.SysFont('Comic Sans MS', 50, bold=True))
Option.font.add_font('small_option_font', pygame.font.Font('AlphaWood.ttf', 25))
Option.font.add_font('small_title_font', pygame.font.SysFont('Plaguard-ZVnjx', 40))



def change_grid(option:Option):
    if(option.left in Option.input.last_checked_input):
        if(option.input_output > 2):
            option.input_output-=1
    elif(option.right in Option.input.last_checked_input):
        option.input_output +=1

def change_animation_speed(option: Option):
    if(K_LEFT in Option.input.last_checked_input):
        if(option.input_output > 1):
            option.input_output -= 1
    elif(K_RIGHT in Option.input.last_checked_input):
        if(option.input_output < 10):
            option.input_output += 1




def create_my_menu(surface, game, title_pos, main_loop):
    def start_game(game:Game):
        game.set_tiles(Tiles(game.tiles_rect.topleft, game.tiles_rect.size[0], grid_size_option.input_output))
        game.animation_speed = animation_speed_option.input_output/10
        main_menu.run_display = False
        main_loop()

    screen = surface
    start = Option('Start').add.select_listener(lambda _:start_game(game)).add.highlight()
    options = Option('Options').add.highlight().add.menu(screen, title_pos)
    credits = Option('Credits').add.highlight().add.menu(screen, title_pos)
    grid_size_option = Option('Grid Size: ')\
        .add.highlight()\
        .add.input(4)\
        .add.active_listener(change_grid)

    animation_speed_option = Option('Animation Speed: ')\
        .add.highlight()\
        .add.input(5)\
        .add.active_listener(change_animation_speed)

    options.set_options([
        grid_size_option,
        animation_speed_option
        ])
    main_menu = Option('2048').add.mouse_menu(screen, title_pos).set_options([
        start,
        options,
        credits
    ])
    return main_menu