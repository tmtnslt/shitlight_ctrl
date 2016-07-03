#!/usr/bin/env python2.7
from __future__ import print_function
import time
import urwid
import shytlight_simulator as shytlight
from shitlight_patterns import shooting_star_cls
from shitlight_patterns import cross_cls 
from shitlight_patterns import raindrop_cls 
from shitlight_patterns import unicolor_cls 

pattern = shooting_star_cls.ShootingStarPattern()

in_splash_screen = False

def exit_on_q(key):
    if key in ('q', 'Q'):
        exit_program(None)
    elif key[0] != 'mouse press' and in_splash_screen == True:
        skip_splash(key)
    
def skip_splash(key):
    global in_splash_screen
    in_splash_screen = False
    show_menu()

def show_menu():
    shytlight.init_shitlight()
    loop.widget = top

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c[0])
        urwid.connect_signal(button, 'click', item_chosen, c[1])
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def menu_button(caption, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')

def item_chosen(button, choice):
    print(choice)
    response = urwid.Text([u'Running ', button.label, '\n'])
    done = menu_button('Ok', show_main_menu)
    top.pattern_menu(urwid.Filler(urwid.Pile([response, done])))

    # run pattern
    global pattern
    if pattern.is_alive():
        pattern.stop()
        shytlight.clear_buffer()
    
    pattern = choice()
    pattern.start()

def show_main_menu(button):
    
    top.main_menu(menu('Shitlight Patterns', choices))

def exit_program(button):
    if pattern.is_alive():
        pattern.stop()
    shytlight.clear_buffer()
    raise urwid.ExitMainLoop()


splash_palette = [
            ('banner', '', '', '', '#ffa', '#60d'),
            ('streak', '', '', '', 'g50', '#60a'),
            ('inside', '', '', '', 'g38', '#808'),
            ('outside', '', '', '', 'g27', '#a06'),
            ('bg', '', '', '', 'g7', '#d06'),]

placeholder = urwid.SolidFill()
loop = urwid.MainLoop(placeholder, splash_palette,
                          unhandled_input=exit_on_q)
loop.screen.set_terminal_properties(colors=256)
loop.widget = urwid.AttrMap(placeholder, 'bg')
loop.widget.original_widget = urwid.Filler(urwid.Pile([]))


## splash screen
div = urwid.Divider()
outside = urwid.AttrMap(div, 'outside')
inside = urwid.AttrMap(div, 'inside')
txt = urwid.Text(('banner', '  S H I T L I G H T  '), align='center')
streak = urwid.AttrMap(txt, 'streak')
txt2 = urwid.Text(('bg', 'press any key'), align='center')
pile = loop.widget.base_widget # .base_widget skips the decorations
for item in [outside, inside, streak, inside, outside, txt2]:
    pile.contents.append((item, pile.options()))

in_splash_screen = True


# menu screen
choices = [ ('Shooting Star', shooting_star_cls.ShootingStarPattern),
            ('Cross', cross_cls.CrossPattern),
            ('Unicolor', unicolor_cls.UnicolorPattern),
            ('Raindrop', raindrop_cls.RaindropPattern) ]


class PatternMenu(urwid.WidgetPlaceholder):
    def __init__(self, items):
        super(PatternMenu, self).__init__(urwid.SolidFill('S'))
        self.pattern = None

        self.main_menu(items)
        
    def main_menu(self, items):
        self.original_widget = urwid.Overlay(urwid.LineBox(items),
                  self.original_widget,
                  align='center',
                  valign='middle',
                  width=('relative', 80),
                  height=('relative', 80),
                  left=0,
                  right=3,
                  top=0,
                  bottom=2)

    def pattern_menu(self, items):
        self.original_widget = urwid.Overlay(urwid.LineBox(items),
                  self.original_widget,
                  align='center',
                  valign='middle',
                  width=('relative', 80),
                  height=('relative', 80),
                  min_width=24, min_height=8,
                  left=3,
                  right=0,
                  top=2,
                  bottom=0)

    def keypress(self, size, key):
        if key == 'esc' and self.pattern:
            self.original_widget = self.original_widget[0]
        else:
            return super(PatternMenu, self).keypress(size, key)

top = PatternMenu(menu('Shitlight Patterns', choices))

loop.run()




