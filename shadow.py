#!/usr/bin/python3
import base64;
import sys;

class Crafter:

    def __init__(self, jpg1, jpg2, w, h):
        self.jpg1 = jpg1
        self.jpg2 = jpg2
        self.w = w
        self.h = h

    def craft(self, out1, out2):
        size1 = len(self.jpg1) - 4 # we remove leading 0xffd8 and trailing 0xffd9
        size2 = len(self.jpg2) - 2 # we remove leading 0xffd8
        jmp1 = size1 + 10 + 4 # jump over file 1 from 0x234
        jmp2 = size2 # jump over file 2
        imgStart = 0x95
        imgEnd = 0x23e + size1 + 4 + size2

        out1.write(base64.b64decode(h1))
        out2.write(base64.b64decode(h2))

        duplicator = Duplicator([out1, out2])

        duplicator.write(jmp1.to_bytes(2, 'big'))
        duplicator.write(b'\0' * 8)
        duplicator.write(self.jpg1[2:-2])
        duplicator.write(b'\xff\xfe')
        duplicator.write(jmp2.to_bytes(2, 'big'))
        duplicator.write(self.jpg2[2:])

        # write PDF sections and auto-compute their xref index
        footer = Footer()
        footer.append(
"""endstream
endobj
""")
        footer.mark()
        footer.append(
"""2 0 obj
{w}
endobj
""".format(w=self.w))
        footer.mark()
        footer.append(
"""3 0 obj
{h}
endobj
""".format(h=self.h))
        footer.mark()
        footer.append(
"""4 0 obj
/XObject
endobj
""")
        footer.mark()
        footer.append(
"""5 0 obj
/Image
endobj
""")
        footer.mark()
        footer.append(
"""6 0 obj
/DCTDecode
endobj
""")
        footer.mark()
        footer.append(
"""7 0 obj
/DeviceRGB
endobj
""")
        footer.mark()
        footer.append(
"""8 0 obj
{length}
endobj
""".format(length=imgEnd-imgStart))
        footer.mark()
        footer.append(
"""9 0 obj
<<
  /Type /Catalog
  /Pages 10 0 R
>>
endobj
""")
        footer.mark()
        footer.append(
"""10 0 obj
<<
  /Type /Pages
  /Count 1
  /Kids [11 0 R]
>>
endobj
""")
        footer.mark()
        footer.append(
"""11 0 obj
<<
  /Type /Page
  /Parent 10 0 R
  /MediaBox [0 0 {w} {h}]
  /CropBox [0 0 {w} {h}]
  /Contents 12 0 R
  /Resources
  <<
    /XObject <</Im0 1 0 R>>
  >>
>>
endobj
""".format(w=self.w, h=self.h))
        footer.mark()
        footer.append(
"""12 0 obj
<</Length 38>>
stream
q
  {w:05d} 0 0 {h:05d} 0 0 cm
  /Im0 Do
Q
endstream
endobj
""".format(w=self.w, h=self.h))
        xrefPos = footer.position()
        footer.append(
"""xref
0 13 
0000000000 65535 f 
0000000017 00000 n 
""")

        for index in footer.indices:
            footer.append('{:010d} 00000 n \n'.format(imgEnd + index))

        footer.append(
"""trailer << /Root 9 0 R /Size 13>>

startxref
{xrefpos}
%%EOF
""".format(xrefpos=imgEnd+xrefPos))

        # write the footer to the file
        duplicator.write(bytes(footer.data, "UTF-8"));

class Footer:

    def __init__(self):
        self.data = ""
        self.indices = []

    def append(self, text):
        self.data += text

    def mark(self):
        self.indices.append(self.position())

    def position(self):
        return len(self.data)

class Duplicator:

    def __init__(self, outputs):
        self.outputs = outputs

    def write(self, *args):
        for output in self.outputs:
            output.write(*args)

def main():
    if len(sys.argv) < 5:
        sys.exit('Usage: %s <jpg1> <jpg2> <width> <height>'.format(sys.argv[0]))
    with open(sys.argv[1], 'rb') as file1, open(sys.argv[2], 'rb') as file2:
        w = int(sys.argv[3])
        h = int(sys.argv[4])
        crafter = Crafter(file1.read(), file2.read(), w, h)
        with open('shadow1.pdf', 'wb') as out1, open('shadow2.pdf', 'wb') as out2:
            crafter.craft(out1, out2)

h1 = """
JVBERi0xLjMKJeLjz9MKCgoxIDAgb2JqCjw8L1dpZHRoIDIgMCBSL0hlaWdodCAzIDAgUi9UeXBl
IDQgMCBSL1N1YnR5cGUgNSAwIFIvRmlsdGVyIDYgMCBSL0NvbG9yU3BhY2UgNyAwIFIvTGVuZ3Ro
IDggMCBSL0JpdHNQZXJDb21wb25lbnQgOD4+CnN0cmVhbQr/2P/+ACRTSEEtMSBpcyBkZWFkISEh
ISGFL+wJIzl1nDmxocY8TJfh//4Bf0bck6a2fgE7ApqqHbJWC0XKZ9aIx/hLjEx5H+ArPfYU+G2x
aQkBxWtFwVMK/t+3YDjpcnIv561yjw5JBOBGwjBXD+nUE5ir4S71vJQr4zVCpIAtmLXXDyozLsN/
rDUU503cDyzBqHTNDHgwWiFWZGEwl4lga9C/P5jNqARGKaEAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/+
"""

h2 = """
JVBERi0xLjMKJeLjz9MKCgoxIDAgb2JqCjw8L1dpZHRoIDIgMCBSL0hlaWdodCAzIDAgUi9UeXBl
IDQgMCBSL1N1YnR5cGUgNSAwIFIvRmlsdGVyIDYgMCBSL0NvbG9yU3BhY2UgNyAwIFIvTGVuZ3Ro
IDggMCBSL0JpdHNQZXJDb21wb25lbnQgOD4+CnN0cmVhbQr/2P/+ACRTSEEtMSBpcyBkZWFkISEh
ISGFL+wJIzl1nDmxocY8TJfh//4Bc0bckWa2fhGPApq2IbJWD/nKZ8yox/hbqEx5AwwrPeIY+G2z
qQkB1d9FwU8m/t+z3DjpasIv571yjw5FvOBG0jxXD+sUE5i7VS71oKgr4zH+pIA3uLXXHw4zLt+T
rDUA603cDezBqGR5DHgsdiFWYN0wl5HQa9CvP5jNpLxGKbEAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/+
"""

if __name__ == "__main__":
    main()
