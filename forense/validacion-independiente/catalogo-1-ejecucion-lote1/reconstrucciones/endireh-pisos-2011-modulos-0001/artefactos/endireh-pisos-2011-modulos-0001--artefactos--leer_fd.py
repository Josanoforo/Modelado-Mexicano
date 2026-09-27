"""Lector mínimo de celdas de texto BIFF8; no ejecuta fórmulas ni macros."""
import struct
import olefile

def records(data):
    p = 0
    while p + 4 <= len(data):
        tag, n = struct.unpack_from('<HH', data, p)
        yield p, tag, data[p+4:p+4+n]
        p += 4+n

class Chunks:
    def __init__(self, chunks): self.chunks, self.i, self.p = chunks, 0, 0
    def read(self, n):
        out = b''
        while n:
            if self.p == len(self.chunks[self.i]): self.i += 1; self.p = 0
            k = min(n, len(self.chunks[self.i])-self.p)
            out += self.chunks[self.i][self.p:self.p+k]; self.p += k; n -= k
        return out
    def chars(self, n, wide):
        out = ''
        while n:
            if self.p == len(self.chunks[self.i]):
                self.i += 1; self.p = 0; wide = self.read(1)[0] & 1
            k = min(n, (len(self.chunks[self.i])-self.p)//(1+wide))
            assert k > 0
            out += self.read(k*(1+wide)).decode('utf-16le' if wide else 'latin1')
            n -= k
        return out

def read_cells(path):
    with olefile.OleFileIO(path) as f: data = f.openstream('Workbook').read()
    rr = list(records(data)); strings = []; sheets = {}
    for i, (p, tag, b) in enumerate(rr):
        if tag == 0x85:
            offset = struct.unpack_from('<I', b)[0]; n, wide = b[6:8]
            sheets[offset] = b[8:8+n*(1+(wide&1))].decode('utf-16le' if wide&1 else 'latin1')
        if tag == 0xfc:
            chunks = [b[8:]]; j=i+1
            while j<len(rr) and rr[j][1]==0x3c: chunks.append(rr[j][2]); j+=1
            c=Chunks(chunks)
            for _ in range(struct.unpack_from('<I',b,4)[0]):
                n=struct.unpack('<H',c.read(2))[0]; flags=c.read(1)[0]
                rich=struct.unpack('<H',c.read(2))[0] if flags&8 else 0
                ext=struct.unpack('<I',c.read(4))[0] if flags&4 else 0
                strings.append(c.chars(n,flags&1)); c.read(4*rich+ext)
    sheet=''; out=[]
    for p,tag,b in rr:
        if p in sheets: sheet=sheets[p]
        if tag==0xfd:
            row,col,xf,idx=struct.unpack('<HHHI',b)
            out.append((sheet,row+1,col+1,strings[idx]))
    return out

if __name__=='__main__':
    import sys
    for row in read_cells(sys.argv[1]): print('\t'.join(map(str,row)))
