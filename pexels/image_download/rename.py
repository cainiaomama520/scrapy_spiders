# -*- coding: utf-8 -*-

import os
import os.path
from optparse import OptionParser


class Rename:

    def get_options(self):

        usage = '%prog [option]'
        parser = OptionParser(usage=usage)
        parser.add_option('-p', '--path', metavar='PATH',
                          action='store', dest='path',
                          help="jpg files's path")
        options, args = parser.parse_args()
        return options

    def rename(self, options):

        if len(options.path) != 0:
            files = os.listdir(options.path)
            i = 0
            for file in files:
                 if file.endswith('.JPG') or file.endswith('.jpg'):
                     i = i + 1
                     os.rename(os.path.join(options.path,file), os.path.join(options.path,str(i) + '.jpg'))#注意os.rename用得是文件的绝对路径，否则会出错！
                 if file.endswith('.PNG') or file.endswith('.png'):
                     i = i + 1
                     os.rename(os.path.join(options.path,file), os.path.join(options.path,str(i) + '.png'))

def main():
    r1 = Rename()
    options = r1.get_options()
    r1.rename(options)


if __name__ == '__main__':
    main()
