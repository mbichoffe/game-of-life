import asyncio
import js
from js import document, console, initSVG, redraw, setInterval, clearInterval
from pyscript import when, Element
from game_of_life import GameOfLife
from patterns import Patterns

WIDTH = 60
HEIGHT = 40

# TO DO: add tooltips in html

def wrap_list(start_tag, values, end_tag):
    return start_tag + f"{end_tag}{start_tag}".join(values) + end_tag


def replace_element_text(el, text):
    if el.textContent:
        el.textContent = text
    else:
        el.innerText = text


def set_dropdown():
    selector_el = document.getElementById('pattern-options')
    options = Patterns.get_all_pattern_names()
    options.insert(0, 'random')
    options_el = wrap_list('<option>', options, '</option>')
    selector_el.insertAdjacentHTML('beforeend', options_el)


def update_gen_and_population():
    replace_element_text(document.getElementById('epoch'), f'generation: {game.t}')
    replace_element_text(document.getElementById('population'), f'population: {game.population}')


@when('input', selector='.range-selectors')
def on_range_update(event):
    label = event.srcElement.nextElementSibling
    label.innerText = event.srcElement.value
    if event.srcElement.id == 'generations':
        game.generations = int(event.srcElement.value)
    elif event.srcElement.id == 'delay':
        game.delay = int(event.srcElement.value)


@when('click', selector='#play')
def start_or_stop_game(event):
    # TO DO: add check to see if current generation is equal to game total generation, pop up warning
    if event.currentTarget.value == 'GO':
        pyscript.run_until_complete(start_game())
    else:
        stop_game()


@when('click', selector='#reset')
def reset_board(event):
    game.reset_game()
    redraw()


@when('click', selector='#clear')
def reset_board(event):
    game.clear_board()
    redraw()


@when('change', selector='#pattern-options')
def on_select_update(event):
    pattern = event.srcElement.value
    if pattern in Patterns.get_all_pattern_names():
        game.clear_board()
        game.add_pattern(pattern, 1, 1)
    elif pattern == 'random':
        game.create_random_grid()
    redraw()


async def start_game():
    game.playing = True
    document.getElementById('play').value = 'STOP'
    while game.t < game.generations and game.playing:
        game.apply_conways_rules()
        await asyncio.sleep(game.delay / 1000)
        update_gen_and_population()
        js.redraw()
    stop_game()


def stop_game():
    game.playing = False
    document.getElementById('play').value = 'GO'


def create_game():
    game_delay = int(document.getElementById('delay').value)
    game_generations = int(document.getElementById('generations').value)
    # TO DO: figure out cell size
    new_game = GameOfLife(WIDTH, HEIGHT, generations=game_generations, delay=game_delay)
    return new_game


game = create_game()
set_dropdown()
js.game_py = game
js.updateGenPop = update_gen_and_population
js.initSVG()

# TO DO: should probably make the patterns a property of the game so when it is selected, automatically changes the board