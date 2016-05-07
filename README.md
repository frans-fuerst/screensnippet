# screensnippet
record cute little **gif**-screencasts using `byzanz` - and make selecting the
recorded area and running the command easy with `screensnippet`:

Record your workflow:

![CRV screencast](media/howto-bg.gif)


And post it online:

![CRV screencast](media/example-screencast.gif)

## Get & Install


    git clone https://github.com/frans-fuerst/screensnippet.git

Currently there's no installer - you can just run the python script:

    ./screensnippet/ssnippet

or alternatively you can place a symlink somewhere your `$PATH` environment variable points to, e.g.:

    cd ./screensnippet
    ln -s `pwd`/ssnippet ~/bin/

## Requirements


### `byzanz` (screensnippet is just a frontent)

    apt-get install byzanz
    or
    dnf install byzanz
  
### PyQt4 for your Python distribution

    dnf install python3-PyQt4   # on Fedora
    
