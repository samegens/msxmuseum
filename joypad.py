import pygame


# Values for Joypad2:
# left: value -1, axis 0
# right: 1, 0
# up: -1, 1
# down 1, 1
# triangle: 0
# circle: 1
# X: 2
# square: 3
# select: 8
# start: 9

class Joypad:
    kNone = 0

    kTriangleDown = 1
    kTriangleUp = 2
    kCircleDown = 3
    kCircleUp = 4
    kXDown = 5
    kXUp = 6
    kSquareDown = 7
    kSquareUp = 8

    kLeftDown = 9
    kLeftUp = 10
    kRightDown = 11
    kRightUp = 12
    kUpDown = 13
    kUpUp = 14
    kDownDown = 15
    kDownUp = 16

    kSelectDown = 17
    kSelectUp = 18
    kStartDown = 19
    kStartUp = 20

    sEventNameMap = {
        kNone: 'None',

        kTriangleDown: 'Triangle down',
        kTriangleUp: 'Triangle up',
        kCircleDown: 'Circle down',
        kCircleUp: 'Circle up',
        kXDown: 'X down',
        kXUp: 'X up',
        kSquareDown: 'Square down',
        kSquareUp: 'Square up',

        kLeftDown: 'Left down',
        kLeftUp: 'Left up',
        kRightDown: 'Right down',
        kRightUp: 'Right up',
        kUpDown: 'Up down',
        kUpUp: 'Up up',
        kDownDown: 'Down down',
        kDownUp: 'Down up',

        kSelectDown: 'Select down',
        kSelectUp: 'Select up',
        kStartDown: 'Start down',
        kStartUp: 'Start up'
    }


def GetJoypadEventName(inJoypadEvent):
    return Joypad.sEventNameMap[inJoypadEvent]


def TranslateEvent(inEvent):
    if inEvent.type == pygame.JOYBUTTONDOWN:
        button = inEvent.dict['button']
        if button in [0, 1, 2, 3, 8, 9]:
            return button * 2 + 1
        else:
            return Joypad.kNone

    if inEvent.type == pygame.JOYBUTTONUP:
        button = inEvent.dict['button']
        if button in [0, 1, 2, 3, 8, 9]:
            return button * 2 + 2
        else:
            return Joypad.kNone

    if inEvent.type == pygame.JOYAXISMOTION:
        value = inEvent.dict['value']
        axis = inEvent.dict['axis']
        if axis == 0:
            if value < -0.5:
                return Joypad.kLeftDown
            if value > 0.5:
                return Joypad.kRightDown
        if axis == 1:
            if value < -0.5:
                return Joypad.kUpDown
            if value > 0.5:
                return Joypad.kDownDown

    return Joypad.kNone
    

