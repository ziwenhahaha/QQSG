
import zlib, os, struct

filelist = []

class FileVisitor:
    def __init__(self, startDir=os.curdir):
        self.startDir = startDir
    def run(self):
        for dirname, subdirnames, filenames in os.walk(self.startDir, True):
            for filename in filenames:
                self.visit_file(os.path.join(dirname, filename))
    def visit_file(self, pathname):
        filelist.append({'filename':pathname, 'size':0, 'zlib_size':0, 'offset':0, 'relative_filename': pathname.replace(os.path.normpath(self.startDir)+os.sep, '')})

def recode(source_dirname,out_filename):
    FileVisitor(source_dirname).run()
    total = len(filelist)
    fp = open(out_filename + '~', 'wb')
    fp.write('\x64\x00\x00\x00'.encode())
    fp.write(struct.pack('I', len(filelist)))
    fp.write(struct.pack('I', 0))
    fp.write(struct.pack('I', 0))
    offset = 16
    for index in range(total):
        item = filelist[index]
        item['offset'] = offset
        infile = open(item['filename'], 'rb')
        text = infile.read()
        infile.close()
        item['size'] = len(text)
        text = zlib.compress(text)
        item['zlib_size'] = len(text)
        fp.write(text)
        offset += item['zlib_size']
        print(u'已压缩文件 %d/%d' % (index + 1, total))
    filename_table_offset = offset
    for index in range(total):
        item = filelist[index]
        fp.write(struct.pack('H', len(item['relative_filename'])))
        fp.write(item['relative_filename'].encode())
        fp.write('\x01\x00\x00\x00'.encode())
        fp.write(struct.pack('I', item['offset']))
        fp.write(struct.pack('I', item['size']))
        fp.write(struct.pack('I', item['zlib_size']))
        offset += 2 + len(item['relative_filename']) + 16
        print(u'已输出路径 %d/%d' % (index+1, total))
    filename_table_len = offset - filename_table_offset
    fp.close()

    fp = open(out_filename + '~', 'rb')
    ret = open(out_filename, 'wb')

    fp.read(16)
    ret.write('\x64\x00\x00\x00'.encode())
    ret.write(struct.pack('I', len(filelist)))
    ret.write(struct.pack('I', filename_table_offset))
    ret.write(struct.pack('I', filename_table_len))

    copy_bytes = 16
    total_bytes = offset
    while True:
        text = fp.read(2**20)
        ret.write(text)
        copy_bytes += len(text)
        print(u'最后的拷贝 %d%%' % (copy_bytes * 100.0 / total_bytes))
        if not text:
            break
    fp.close()
    ret.close()
    os.remove(out_filename + '~')

if __name__ == "__main__":


    source_dirname = r"F:\QQSG\GameData_Modify\objects1\objects"
    out_filename = r"F:\QQSG\GameData_Recoding\objdects.pkg"
    recode()