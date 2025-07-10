# thermoprint
Simple script for printing using a POS-5890 thermal receipt printer

### usage

`python3 thermoprint.py "words go here"`

A `DeviceNotFoundError` probably indicates inadequate permissions.

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

### thermonotif

A tweak to take input from the standard input instead of the argument vector.
This makes the script suitable for announcing notifications from [calcurse](https://github.com/lfos/calcurse).
This can be achieved by setting calcurse's `notification.command` variable to something like:
`calcurse --next | python3 /path/to/thermonotif.py`
given suitable permissions.

### checklist

A script to render the `calcurse` todo list as a checklist for printing with `thermonotif.py`.
Usage: `calcurse -t | python3 checklist.py | python3 thermonotif.py` (given appropriate permissions).
