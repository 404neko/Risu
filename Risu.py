

import traceback
import io
import hashlib
import shutil
import os
import base64

from PIL import Image
from requests import session


class RisuExtension:

    def __init__(self):
        pass

    def can_handle(self, url):
        pass

    def handle(self, url):
        pass


class Risu:

    session = None
    path = 'risu'
    extensions = []
    cached = {}
    default_image = 'iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAIAAADTED8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB+0lEQVR42u3TQQ0AAAjEMED5SeeNBloJS9ZJCr4aCTAAGAAMAAYAA4ABwABgADAAGAAMAAYAA4ABwABgADAAGAAMAAYAA4ABwABgADAAGAAMAAYAA4ABwABgADAAGAAMAAYAA4ABwABgADAAGAAMAAYAA4ABwABgADAAGAAMgAHAAGAAMAAYAAwABgADgAHAAGAAMAAYAAwABgADgAHAAGAAMAAYAAwABgADgAHAAGAAMAAYAAwABgADgAHAAGAAMAAYAAwABgADgAHAAGAAMAAYAAwABgADgAHAAGAAMAAGAAOAAcAAYAAwABgADAAGAAOAAcAAYAAwABgADAAGAAOAAcAAYAAwABgADAAGAAOAAcAAYAAwABgADAAGAAOAAcAAYAAwABgADAAGAAOAAcAAYAAwABgADAAGAAOAATAAGAAMAAYAA4ABwABgADAAGAAMAAYAA4ABwABgADAAGAAMAAYAA4ABwABgADAAGAAMAAYAA4ABwABgADAAGAAMAAYAA4ABwABgADAAGAAMAAYAA4ABwABgADAAGAAMAAbAAGAAMAAYAAwABgADgAHAAGAAMAAYAAwABgADgAHAAGAAMAAYAAwABgADgAHAAGAAMAAYAAwABgADgAHAAGAAMAAYAAwABgADgAHAAGAAMAAYAAwABgADgAHgWu7LA4CJx71QAAAAAElFTkSuQmCC'

    def initialize_filesystem(self):
        for item in ['', 'image', 'thumbnail']
            try:
                os.mkdir(self.path + os.sep + item)
            except:
                pass
        for item in os.listdir(os.sep.join([path, image])):
            self.cached[item] = 0

    def on_fail(self):
        expected_path = os.sep.join([self.path, 'default'])
        if os.path.isfile():
            pass
        else:
            with open(expected_path, 'wb') as file_handle:
                file_handle.write(base64.encode(self.default_image))
        return expected_path

    def __init__(self, session=session(), path='risu', extensions=[]):
        self.session = session
        self.path = path
        self.extensions = extensions
    
    def get_hash(self, content):
        md5 = hashlib.md5()
        md5.update(content)
        return md5.hexdigest()

    def get_image(self, url):

        if url.startswith('file:///'): url = url[len('file:///'):]

        hash_ = self.get_hash(url)
        expected_path = os.sep.join([self.path, 'image', hash_])
        if hash_ in self.cached:
            return expected_path

        for plugin in self.plugins:
            if plugin.can_handle(url):
                content = plugin.handle(url)
                with open(expected_path, 'wb') as file_handle:
                    file_handle.write(content)

        if os.path.isfile(url):
            storage_path = expected_path
            shutil.copy2(url, storage_path)
            return storage_path

        if url[:7] in ['https:/', 'http://']:
            try:
                response = self.session.get(url)
                if response:
                    with open(expected_path, 'wb') as file_handle:
                        file_handle.write(response.content)
                    return expected_path
            except:
                return self.on_fail()

        # todo: base64

        return self.on_fail()
    
    def get_thumbnail(self, url, _size):

        if type(_size)==int:
            size = [_size, _size]
        else:
            size = _size

        if url.startswith('file:///'): url = url[len('file:///'):]
        hash_ = self.get_hash(url)
        expected_path = os.sep.join([self.path, 'thumbnail', hash_])

        if os.path.isfile(expected_path):
            return expected_path

        image_path = self.get_image(thumbnail)
        data = None
        with open(image_path, 'rb') as file_handle:
            data = file_handle.read()
        file_handle = io.BytesIO(data)
        file_handle.seek(0)
        image = Image.open(file_handle)
        image.thumbnail(size)
        image.save(expected_path)
        file_handle.close()
        return expected_path