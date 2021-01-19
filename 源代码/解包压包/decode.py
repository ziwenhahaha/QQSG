# -*- coding: utf-8 -*-

import os, struct, zlib

def decode(pkgfilename,outdirname):
    pkgfile = open(pkgfilename, 'rb')
    pkgfile.read(4)
    filenums, = struct.unpack('I', pkgfile.read(4))
    filename_table_offset, = struct.unpack('I', pkgfile.read(4))
    filename_table_len, = struct.unpack('I', pkgfile.read(4))
    pkgfile.seek(filename_table_offset)
    for index in range(filenums):
        name_len, = struct.unpack('H', pkgfile.read(2))
        name = pkgfile.read(name_len)
        pkgfile.read(4)
        offset, = struct.unpack('I', pkgfile.read(4))
        size, = struct.unpack('I', pkgfile.read(4))
        zlib_size, = struct.unpack('I', pkgfile.read(4))
        current_pos = pkgfile.tell()
        pkgfile.seek(offset)
        text = pkgfile.read(zlib_size)
        text = zlib.decompress(text)
        pkgfile.seek(current_pos)
        # outfilename = os.path.join(outdirname, os.path.join(os.path.splitext(os.path.basename(pkgfilename))[0],
        #                                                     str(name, encoding="utf-8")))
        outfilename = os.path.join(outdirname, os.path.join(os.path.splitext(os.path.basename(pkgfilename))[0],
                                                                            str(name, encoding="gbk")))
        # print(u'进度 [%d/%d]: ' % (index + 1, filenums),
        #       os.path.join(os.path.splitext(os.path.basename(pkgfilename))[0], str(name, encoding="utf-8")))
        print(u'进度 [%d/%d]: ' % (index + 1, filenums),
              os.path.join(os.path.splitext(os.path.basename(pkgfilename))[0], str(name, encoding="gbk")))
        if not os.path.exists(os.path.dirname(outfilename)):
            os.makedirs(os.path.dirname(outfilename))
        open(outfilename, 'wb').write(text)

if __name__ == "__main__":
    pkgfilename = r"F:\QQSG\GameData_Pre\objects.pkg"
    outdirname = r"F:\QQSG\GameData_Modify\objects1"
    decode(pkgfilename,outdirname)

    # pkgfilename = r"F:\QQSG\GameData_Pre\objects2.pkg"
    # outdirname = r"F:\QQSG\GameData_Modify\objects2"
    # decode(pkgfilename,outdirname)
    #
    # pkgfilename = r"F:\QQSG\GameData_Pre\objects3.pkg"
    # outdirname = r"F:\QQSG\GameData_Modify\objects3"
    # decode(pkgfilename,outdirname)
    #
    # pkgfilename = r"F:\QQSG\GameData_Pre\objects4.pkg"
    # outdirname = r"F:\QQSG\GameData_Modify\objects4"
    # decode(pkgfilename,outdirname)