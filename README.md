# thermoprint
Simple script for printing to receipt paper using an escpos thermal printer

### usage

`python3 thermoprint.py "words go here"`

The input string will be split up into words using spaces.
Formatted sections begin and end with keywords prefixed with + and -.
For instance, `+em` and `-em` begin and end an emphasis section.
Formatted sections can be of the following types:
* `em` (emphasis: invert colors)
* `big` (double font size)
* `center` (alignment)
* `right` (alignment)
* `qr` (QR code)
Where `qr` is special: no other keywords are processed between `+qr` and `-qr`.
Additionally, `qr` may be concatenated with colon-separated keyword parameters:
* `ec` (error correction level: int)
* `size` (pixel size: int)
* `center` (alignment: bool)
So that a properly formatted QR section may look like `+qr:ec=1:size=7:center=False ... -qr`

