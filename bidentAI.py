import math
import operator

import pytesseract

# import cv2
# from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


class Fixed():
    
    @classmethod
    def div(a, b):
        if a == 0 and b == 0:
            return 1
        else:
            return a / b


class RWDError(Exception):
    
    def __init__(self, name: str, *args, **kwargs):
        self.names = {
            'Already exist': 1,
            'Doesn\'t exist': 2,
            'Additional argument required': 3,
            'Incorrect argument type': 4
        }
        self.name = name
        self.code = self.names[name]
        self.args = list(args)
        self.kwargs = kwargs

    def __str__(self):
        tmp = '.'.join(map(str, self.args))
        try:
            return f'{self.name}: {tmp} \n{self.kwargs["hint"]}'
        except:
            return f'{self.name}: {tmp}'


class Area:
    
    def __init__(self):
        self.imr = None
        self.templates = {
            'Default': {
                'refImgSize': (0, 0),
                'topLeft': (0, 0),
                'bottomRight': (0, 0),
                'mode': ((0, 0), (0, 0))
            },
            'test': {
                'refImgSize': (1920, 1080),
                'topLeft': (144, 36),
                'bottomRight': (720, 480)
            }
        }

    def addTemplate(self, templateName: str, refImgSize: tuple, topLeft: tuple, bottomRight: tuple):
        """
        :type refImgSize, topLeft, bottomRight: tuple(x, y) from top-left to bottom-right
        :param name: Template's templateName.
        :param refImgSize: Reference image size.
        :param topLeft: Top-left point of the box.
        :param bottomRight: Bottom-right point of the box.
        """
        if self.templates[templateName] is not None:
            raise RWDError('Already exist', templateName)
    
        self.templates[templateName] = {
            'refImgSize': refImgSize,
            'topLeft': topLeft,
            'bottomRight': bottomRight
        }

    def delTemplate(self, templateName: str):
        try:
            del self.templates[templateName]
        except:
            raise RWDError('Doesn\'t exist', templateName)

    def setTemplateProperties(self, templateName: str, mode: tuple = ((0, 0), (0, 0)), rPoint: tuple = (None, None)):
        """
        :param mode: (x=(a, b), y=(a, b)
        a:
            0: absolute positioning
            1: relative positioning
        b:
            0: to the center
            1: to top\left side
            2: to bottom\right side
            3: to rPoint
        :param rx: X-coordinate of rPoint
        :param ry: Y-coordinate of rPoint
        """
        b = list(map(
            operator.or_,
            list(map(lambda x: (x[1] != 3), mode)),
            list(map(lambda x, y: (x[1] == 3 and y is not None), mode, rPoint))
        ))
        if not b[0]:
            raise RWDError('Additional argument required', 'rPoint', 'x')
        if not b[1]:
            raise RWDError('Additional argument required', 'rPoint', 'y')
        if type(templateName) is not str:
            raise RWDError('Incorrect argument type', 'templateName', type(templateName))
    
        self.templates[templateName].update({'mode': mode, 'rPoint': rPoint})

    def delTemplateProperties(self, templateName: str):
        try:
            del self.templates[templateName]['mode']
            del self.templates[templateName]['rPoint']
        except:
            raise RWDError('Doesn\'t exist', templateName, hint='There are no prorerties to delete')

    def getBox(self, imgSize: tuple, templateName: str) -> tuple:
        """
        Returns box for given imgSize and templateName
        :param imgSize: Given image size
        :param templateName: Given template
        :return box: (top-left point: (x, y), box size: (x, y))
        """
        try:
            self.templates[templateName]
        except:
            raise RWDError('Doesn\'t exist', templateName)
        try:
            self.templates[templateName]['mode']
        except:
            raise RWDError('Doesn\'t exist', templateName, 'mode',
                           hint='Properties haven\'t been set. Run .setTemplatePropreties to set them')
    
        topLeft = tuple(map(self._c,
                            imgSize,
                            self.templates[templateName]['topLeft'],
                            self.templates[templateName]['refImgSize'],
                            self.templates[templateName]['mode'],
                            self.templates[templateName]['rPoint']))
    
        bottomRight = tuple(map(self._c,
                                imgSize,
                                self.templates[templateName]['bottomRight'],
                                self.templates[templateName]['refImgSize'],
                                self.templates[templateName]['mode'],
                                self.templates[templateName]['rPoint']))
    
        return (topLeft, bottomRight)

    def _c(self, L: int, tX: int, tL: int, mode: tuple, rtX: int = None):
        k = L / tL
        if mode[1] == 0:
            _rtX = int(math.ceil(tL / 2))
            _rX = int(math.ceil(L / 2))
        elif mode[1] == 1:
            _rtX = 0
            _rX = 0
        elif mode[1] == 2:
            _rtX = tL
            _rX = L
        elif mode[1] == 3:
            _rtX = rtX
            _rX = int(k * rtX)
        else:
            raise RWDError('Incorrect argument type', 'mode', mode[1], hint='Can\' handle this mode')
    
        dtX = tX - _rtX
        if mode[0] == 0:
            return _rX + dtX
        elif mode[0] == 1:
            return _rX + k * dtX


A = Area()
try:
    # A.setTemplateProperties('test', [(0, 2), (0, 0)])
    # A.getBox((), 'test')
    pass
except Exception as e:
    print(e)
