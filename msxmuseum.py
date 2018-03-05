#!/usr/bin/python
import os
import pygame
import subprocess
import time
import platform
import logging

from games import gGameDescriptions
from game import Game
from joypad import *

logging.basicConfig(filename='log.log',level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(module)s | %(message)s')

# Globals
gJoystick = None
gScreen = None
gFontBig = None
gFontSmall = None
gGames = []

class Platform:
    Linux = 0
    Windows = 1
    RaspberryPi = 2

    @staticmethod
    def Get():
        if platform.system() == "Windows":
            return Platform.Windows
        if os.uname()[4].startswith("arm"):
            return Platform.RaspberryPi
        return Platform.Linux


    @staticmethod
    def GetExtension():
        if Platform.Get() == Platform.Linux:
            return ".linux"
        if Platform.Get() == Platform.Windows:
            return ".windows"
        return ".rpi"


def InitPygame():
    if Platform.Get() == Platform.RaspberryPi:
        os.system("clear")
    pygame.init()
    # Release the audio device so openmsx can have it.
    pygame.mixer.init()
    pygame.mixer.quit()

    pygame.joystick.init()

    global gJoystick
    gJoystick = None
    try:
        gJoystick = pygame.joystick.Joystick(0) # create a joystick instance
        gJoystick.init() # init instance
        logging.info('Enabled joystick: ' + j.get_name())
    except:
        logging.info('No joystick found')

    global gFontBig
    gFontBig = pygame.font.Font("fonts/MSX-WIDTH40.ttf", 24)

    global gFontSmall
    gFontSmall = pygame.font.Font("fonts/MSX-WIDTH40.ttf", 16)


def StartVideoMode(inMode):
    logging.debug("StartVideoMode %s" % inMode)
    global gScreen
    SCREENRECT = pygame.Rect(0, 0, 640, 480)
    bitdepth = 32
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, inMode, bitdepth)
    gScreen = pygame.display.set_mode(SCREENRECT.size, inMode, bestdepth)
    pygame.display.set_caption("MSX museum")
    pygame.mouse.set_visible(False)


def LoadGameData():
    global gGames
    gGames = []
    games_left = len(gGameDescriptions)
    max_txt = 'Loading, 999 games left'
    max_width, max_height = gFontSmall.size(max_txt)
    for gameDescription in gGameDescriptions:
        gScreen.fill((0, 0, 0))
        txt = 'Loading, %d games left' % games_left
        rendered_text = gFontSmall.render(txt, True, (255, 255, 255), (0, 0, 0))
        gScreen.blit(rendered_text, (gScreen.get_width() - max_width - 10, gScreen.get_height() - max_height - 10))
        pygame.display.flip()

        game = Game(gameDescription)
        if game.HasGameFile():
            gGames.append(game)
        games_left -= 1

    if len(gGames) == 0:
        ExitWithError("No games found.")
        
def ShowStartScreen():
    global gScreen

    gScreen.fill((0, 0, 0))
    pygame.display.flip()

    text_width, max_height = gFontSmall.size("MSX museum")
    start_y = 60
    line_space = 2
    line_height = max_height + line_space

    rendered_text = gFontSmall.render("MSX museum", True, (255, 255, 255), (0, 0, 0))
    gScreen.blit(rendered_text, ((gScreen.get_width() - text_width) / 2, 20))

    line = 0

    print("Use up-arrow/down-arrow to select game.")
    rendered_text = gFontSmall.render("Use up-arrow/down-arrow to select a game.", True, (255, 255, 255), (0, 0, 0))
    gScreen.blit(rendered_text, (10, start_y + line * line_height))
    line += 1

    print("Press a letter to cycle through games starting with that letter.")
    rendered_text = gFontSmall.render("Press a letter to cycle through games starting", True, (255, 255, 255), (0, 0, 0))
    gScreen.blit(rendered_text, (10, start_y + line * line_height))
    line += 1

    rendered_text = gFontSmall.render("    with that letter.", True, (255, 255, 255), (0, 0, 0))
    gScreen.blit(rendered_text, (10, start_y + line * line_height))
    line += 1

    print("Use SPACE/ENTER on keyboard or X on controller to start the selected game.")
    rendered_text = gFontSmall.render("Use SPACE/ENTER on keyboard or X on controller", True, (255, 255, 255), (0, 0, 0))
    gScreen.blit(rendered_text, (10, start_y + line * line_height))
    line += 1

    rendered_text = gFontSmall.render("    to start the selected game.", True, (255, 255, 255), (0, 0, 0))
    gScreen.blit(rendered_text, (10, start_y + line * line_height))
    line += 1

    print("Press Alt+F4 or SELECT in game to return to the game menu.")
    rendered_text = gFontSmall.render("Press Alt+F4 or SELECT in game to return to the", True, (255, 255, 255), (0, 0, 0))
    gScreen.blit(rendered_text, (10, start_y + line * line_height))
    line += 1

    rendered_text = gFontSmall.render("    game menu.", True, (255, 255, 255), (0, 0, 0))
    gScreen.blit(rendered_text, (10, start_y + line * line_height))
    line += 1

    text = "Press any button to continue."
    text_width, max_height = gFontSmall.size(text)
    rendered_text = gFontSmall.render(text, True, (255, 255, 255), (0, 0, 0))
    gScreen.blit(rendered_text, ((gScreen.get_width() - text_width) / 2, gScreen.get_height() - max_height - 10))
    line += 1

    pygame.display.flip()
    
    while True:
        e = pygame.event.wait()
        if e.type == pygame.KEYDOWN:
            break
    

def ExitWithError(inMessage):
    logging.error(inMessage)
    exit(-1)


def AnimateTransition(inOldGameIndex, inNewGameIndex, inDirection):
    global gFontSmall
    global gFontBig

    kNrSteps = 10
    screen_height = gScreen.get_height()
    step_size = screen_height / kNrSteps
    for step in range(0, kNrSteps):
        start_time = time.time()
        end_time = start_time + 1.0 / 60.0
        gScreen.fill((0, 0, 0))
        gGames[inOldGameIndex].Draw(gScreen, -inDirection * step * step_size, gFontSmall, gFontBig)
        gGames[inNewGameIndex].Draw(gScreen, -inDirection * step * step_size + inDirection * screen_height, gFontSmall, gFontBig)
        pygame.display.flip()
        milliseconds_to_wait = int((end_time - time.time()) * 1000)
        if milliseconds_to_wait > 0:
            pygame.time.wait(milliseconds_to_wait);


def FindNextGameStartingWith(inCharValue, inCurrentGameIndex):
    game_names = [game.mName for game in gGames]
    current_name = game_names[inCurrentGameIndex]
    games_with_startletter = [tuple[0] for tuple in gGameDescriptions if ord(tuple[0][0].lower()) == inCharValue]
    games_with_startletter.sort()
    if not games_with_startletter:
        return -1
    if current_name not in games_with_startletter:
        return game_names.index(games_with_startletter[0])
        
    index = games_with_startletter.index(current_name)
    new_index = (index + 1) % len(games_with_startletter)
    new_name = games_with_startletter[new_index]
    return game_names.index(new_name)


def FindPreviousGameStartingWith(inCharValue, inCurrentGameIndex):
    game_names = [game.mName for game in gGames]
    current_name = game_names[inCurrentGameIndex]
    games_with_startletter = [tuple[0] for tuple in gGameDescriptions if ord(tuple[0][0].lower()) == inCharValue]
    games_with_startletter.sort()
    if not games_with_startletter:
        return -1
    if current_name not in games_with_startletter:
        return game_names.index(games_with_startletter[0])
        
    index = games_with_startletter.index(current_name)
    new_index = (index - 1 + len(games_with_startletter)) % len(games_with_startletter)
    new_name = games_with_startletter[new_index]
    return game_names.index(new_name)


def Main():
    InitPygame()
    if Platform.Get() != Platform.RaspberryPi:
        StartVideoMode(pygame.RESIZABLE)
    else:
        StartVideoMode(pygame.FULLSCREEN)
    LoadGameData()
    ShowStartScreen()

    gCurrentGameIndex = 0
    while True:
        gScreen.fill((0, 0, 0))
        gGames[gCurrentGameIndex].Draw(gScreen, 0, gFontSmall, gFontBig)
        pygame.display.flip()
        
        e = pygame.event.wait()
        if e.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            break

        #txt = '%s: %s' % (pygame.event.event_name(e.type), e.dict)
        #print(txt)

        joypad_event = TranslateEvent(e)
        joypad_event_name = GetJoypadEventName(joypad_event)

        if joypad_event == Joypad.kUpDown or joypad_event == Joypad.kLeftDown or (e.type == pygame.KEYDOWN and (e.dict['key'] == pygame.K_UP or e.dict['key'] == pygame.K_LEFT)):
            # Go to previous game.
            old_game_index = gCurrentGameIndex
            gCurrentGameIndex = (gCurrentGameIndex - 1) % len(gGames)
            AnimateTransition(old_game_index, gCurrentGameIndex, -1)
        elif joypad_event == Joypad.kDownDown or joypad_event == Joypad.kRightDown or (e.type == pygame.KEYDOWN and (e.dict['key'] == pygame.K_DOWN or e.dict['key'] == pygame.K_RIGHT)):
            # Go to next game.
            old_game_index = gCurrentGameIndex
            gCurrentGameIndex = (gCurrentGameIndex + 1) % len(gGames)
            AnimateTransition(old_game_index, gCurrentGameIndex, 1)
        elif joypad_event == Joypad.kXDown  or (e.type == pygame.KEYDOWN and (e.dict['key'] == pygame.K_RETURN or e.dict['key'] == pygame.K_SPACE)):
            # Launch game.
            #if Platform.Get() == Platform.RaspberryPi:
            #    StartVideoMode(0)
            logging.debug("display.quit")
            pygame.display.quit()
            if Platform.Get() == Platform.RaspberryPi:
                os.system("clear")
            logging.debug("Launching game")
            gGames[gCurrentGameIndex].Launch(Platform.GetExtension())
            logging.debug("Game finished")
            #if Platform.Get() == Platform.RaspberryPi:
            logging.debug("display.init")
            pygame.display.init()
            logging.debug("after display.init")
            if Platform.Get() != Platform.RaspberryPi:
                StartVideoMode(pygame.RESIZABLE)
            else:
                StartVideoMode(pygame.FULLSCREEN)
            pygame.event.clear()
        elif e.type == pygame.KEYDOWN:
            char = e.dict['unicode']
            if char != None and len(char) > 0:
                ch = ord(char)
                if ch >= ord('a') and ch <= ord('z'):
                    new_game_index = FindNextGameStartingWith(ch, gCurrentGameIndex)
                    if new_game_index >= 0:
                        old_game_index = gCurrentGameIndex
                        gCurrentGameIndex = new_game_index
                        AnimateTransition(old_game_index, gCurrentGameIndex, 1)
                elif ch >= ord('A') and ch <= ord('Z'):
                    ch = ord(chr(ch).lower())
                    new_game_index = FindPreviousGameStartingWith(ch, gCurrentGameIndex)
                    if new_game_index >= 0:
                        old_game_index = gCurrentGameIndex
                        gCurrentGameIndex = new_game_index
                        AnimateTransition(old_game_index, gCurrentGameIndex, -1)

        gCurrentGameIndex = gCurrentGameIndex % len(gGames)

    logging.info("Exiting")

    
Main()
