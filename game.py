import os
import pygame
import subprocess
import logging
import platform


def ExitWithError(inMessage):
    logging.error(inMessage)
    exit(-1)


class Game:
    
    def __init__(self, inTuple):
        self.mName = inTuple[0]
        self.mMaker = inTuple[1]
        self.mYear = inTuple[2]

        games_base_dir = "games"
        if len(inTuple) > 3:
            directory = os.path.join(games_base_dir, inTuple[3])
        else:
            directory = os.path.join(games_base_dir, inTuple[0])

        self.mBoxShotPath = os.path.join(directory, "boxshot.jpg")
        self.mScreenShotPath = os.path.join(directory, "screenshot.png")

        game_path = os.path.join(directory, "game.rom")
        if os.path.exists(game_path):
            self.mRomPath = game_path
        game_path = os.path.join(directory, "game.zip")
        if os.path.exists(game_path):
            self.mRomPath = game_path
        game_path = os.path.join(directory, "game.dsk")
        if os.path.exists(game_path):
            self.mDiskPath = game_path
			
        if not self.mRomPath and not self.mDiskPath:
            logging.warning("Warning: could not find rom or disk for {0} in directory {1} (tried game.dsk, game.rom and game.zip)".format(self.mName, directory))

        if os.path.exists(self.mBoxShotPath):
            self.mBoxShotImage = LoadImage(self.mBoxShotPath)
        if os.path.exists(self.mScreenShotPath):
            self.mScreenShotImage = LoadImage(self.mScreenShotPath)


    def Draw(self, inSurface, inYOffset, inFontSmall, inFontBig):
        panel_width = inSurface.get_width() / 2
        panel_height = inSurface.get_height()
        if self.mBoxShotImage != None:
            x = (panel_width - self.mBoxShotImage.get_width()) / 2
            y = (panel_height - self.mBoxShotImage.get_height()) / 2
            inSurface.blit(self.mBoxShotImage, (x, y + inYOffset))

        if self.mScreenShotImage != None:
            x = panel_width + (panel_width - self.mScreenShotImage.get_width()) / 2
            y = (panel_height - self.mScreenShotImage.get_height()) / 2
            inSurface.blit(self.mScreenShotImage, (x, y + inYOffset))

        text_width, text_height = inFontBig.size(self.mName)
        rendered_text = inFontBig.render(self.mName, True, (255, 255, 255), (0, 0, 0))
        inSurface.blit(rendered_text, ((inSurface.get_width() - text_width) / 2, 30 + inYOffset))

        text = '%s - %d' % (self.mMaker, self.mYear)
        text_width, text_height = inFontSmall.size(text)
        rendered_text = inFontSmall.render(text, True, (255, 255, 255), (0, 0, 0))
        inSurface.blit(rendered_text, (inSurface.get_width() - text_width - 40, inSurface.get_height() - 40 + inYOffset))

        
    def HasGameFile(self):
        return self.mRomPath or self.mDiskPath

        
    def Launch(self, inScriptExtension):
        msxExe = 'openmsx'
        if platform.system() == "Windows":
            msxExe = "d:\\Dropbox\\portable_apps\\openmsx\\openmsx.exe"
			
        cmdline = [msxExe, "-script", "script" + inScriptExtension, "-machine", "Philips_NMS_8245"]
        if self.mRomPath:
            cmdline.extend(["-cart", self.mRomPath])
        else:
            cmdline.extend(["-diska", self.mDiskPath])
        directory, filename = os.path.split(self.mRomPath)
        translation_path = os.path.join(directory, 'translation.ips')
        if os.path.exists(translation_path):
            cmdline.extend(['-ips', translation_path])
        logging.info('Executing game: ' + ' '.join(cmdline))
        logging.info('Important openmsx keys:')
        logging.info('  PrtSc: make screenshot')
        logging.info('  Alt-F4: exit')
        logging.info('  Alt-F8: save state')
        logging.info('  Alt-F7: load state')
        fnull = open(os.devnull, "w")
        subprocess.call(cmdline, stdout = fnull, stderr = subprocess.STDOUT)


    mName = ''
    mMaker = ''
    mYear = 0
    mBoxShotPath = ''
    mBoxShotImage = None
    mScreenShotPath = ''
    mScreenShotImage = None
    mRomPath = ''
    mDiskPath = ''


def LoadImage(inPath):
    "loads an image, prepares it for play"
    try:
        surface = pygame.image.load(inPath)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(inPath, pygame.get_error()))

    return surface.convert()

