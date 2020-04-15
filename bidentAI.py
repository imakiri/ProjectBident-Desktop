import operator

import pytesseract

# import cv2
# from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


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
        if self.kwargs['hint']:
            return f'{self.name}: {tmp} \n{self.kwargs["hint"]}'
        else:
            return f'{self.name}: {tmp}'


class Area:
    
    def __init__(self):
        self.imr = None
        self.templates = {
            'Default': {
                'imgSize': (0, 0),
                'topLeft': (0, 0),
                'bottomRight': (0, 0),
                'mod': ((0, 0), (0, 0))
            },
            'test': {
                'imgSize': (1920, 1080),
                'topLeft': (144, 36),
                'bottomRight': (720, 480)
            }
        }
    
    def addTemplate(self, name: str, refImgSize: tuple, topLeft: tuple, bottomRight: tuple):
        """
        :type refImgSize, topLeft, bottomRight: tuple(x, y) from top-left to bottom-right
        :param name: Template's name.
        :param refImgSize: Reference image size.
        :param topLeft: Top-left point of the box.
        :param bottomRight: Bottom-right point of the box.
        """
        if self.templates[name] is not None:
            raise RWDError('Already exist', name)
        
        self.templates[name] = {
            'imgSize': refImgSize,
            'topLeft': topLeft,
            'bottomRight': bottomRight
        }
    
    def delTemplate(self, name):
        try:
            del self.templates[name]
        except:
            raise RWDError('Doesn\'t exist', name)
    
    def setTemplateProperties(self, name: str, mod: list = [[0, 0], [0, 0]], rx: int = None, ry: int = None):
        """
        :param mod: (x=(a, b), y=(a, b)
        a:
            0: absolute positioning
            1: relative positioning
        b:
            0: to top\left side
            1: to bottom\right side
            2: to rPoint
        :param rx: X-coordinate of rPoint
        :param ry: Y-coordinate of rPoint
        """
        r = (rx, ry)
        b = list(map(
            operator.or_,
            list(map(lambda x: (x[1] != 2), mod)),
            list(map(lambda x, y: (x[1] == 2 and y is not None), mod, r))
        ))
        if not b[0]:
            raise RWDError('Additional argument required', 'rx')
        if not b[1]:
            raise RWDError('Additional argument required', 'ry')
        if type(name) is not str:
            raise RWDError('Incorrect argument type', 'name', type(name))
        
        self.templates[name].update({'mod': mod, 'rx': rx, 'ry': ry})
    
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
            self.templates[templateName]['mod']
        except:
            raise RWDError('Doesn\'t exist', templateName, 'mod',
                           hint='Properties haven\'t been set. Run .setTemplatePropreties to set them')
        
        box = [[], []]


A = Area()
try:
    # A.setTemplateProperties('sdfg', (2, 0))
    A.getBox((), 'test')
except Exception as e:
    print(e)
