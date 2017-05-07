import struct
from PIL import Image
 
def read_record_ETL8G(f):
    s = f.read(8199)
    r = struct.unpack('>2H8sI4B4H2B30x8128s11x', s)
    iF = Image.frombytes('F', (128, 127), r[14], 'bit', 4)
    iL = iF.convert('L')
    return r + (iL,)

shift_jis = []
jisx0208 = []
unicode3 = []
with open("JIS0208.TXT", "r") as f:
    for line in f:
        if line[0] == "#":
            pass
        else:
            sjis, jisx, unic, _ = line.strip().split("\t")
            shift_jis.append(int(sjis, 16))
            jisx0208.append(int(jisx, 16))
            unicode3.append(int(unic, 16))


def jis2uni(n):
    return unicode3[jisx0208.index(n)]
filename = 'ETL8G/ETL8G_01'
id_record = 16
 
with open(filename, 'r') as f:
    f.seek(id_record*8199)
    r = read_record_ETL8G(f)
 
print (r[0:-2], hex(r[1]), hex(jis2uni(r[1])))
print (r[14])
iE = Image.eval(r[-1], lambda x: 255-x*16)
fn = 'ETL8G_{:d}_{:s}.png'.format((r[0]-1)%20+1, hex(r[1])[-4:])
iE.save(fn, 'PNG')