import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


class RWError(Exception):
    
    def __init__(self, name, value=None):
        self.names = {
            'Already exist': 1
        }
        self.code = self.names[name]
        self.value = value
    
    def __str__(self):
        return (repr(self.name, self.value))


class Area:
    
    def __init__(self):
        self.imr = None
        self.templates = {
            'Default': ((0, 0), (0, 0), (0, 0))
        }
    
    def addTemplate(self, name, imgSize: tuple, topLeft: tuple, bottomRight: tuple):
        """
        :type imgSize, topLeft, bottomRight: tuple(x, y) from top-left to bottom-right
        :param name: Template's name.
        :param imgSize: Image size.
        :param topLeft: Top-left point of the box.
        :param bottomRight: Bottom-right point of the box.
        """
        if self.templates[name] is not None:
            raise RWError('Already exist', name)
        
        self.templates[name] = {
            'imgSize': imgSize,
            'topLeft': topLeft,
            'bottomRight': bottomRight}
    
    def setTemplateProperties(self, mod: tuple = None, rx: int = None, ry: int = None):
        """
        :param mod: (x, y)
        0: absolute positioning
        1: relative positioning
        2: relative to rPoint
        :param rx: X-coordinate of rPoint
        :param ry: Y-coordinate of rPoint
        """
        pass
