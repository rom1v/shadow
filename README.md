_SHAdow_ generates, from two JPEG images, two different PDF files having the
same SHA-1 sum.

## Usage

    ./shadow.py <img1> <img2> <width> <height>

For example :

    ./shadow.py sun.jpg water.jpg 640 480

This generates `shadow1.pdf` and `shadow2.pdf` in the current folder.

## Sample

Two images are provided :

    ./shadow.py tux.jpg troll.jpg 200 200

## Constraints

The input images must have the same size, and their files must be smaller than
64K.

## More

I wrote a blog article, in French:
[SHAdow](http://blog.rom1v.com/2017/03/shadow/).
