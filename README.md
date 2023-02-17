# ipcheck
Extract the IP address from access logs such as Nginx and visualize the IP address of the access source

# What is ipcheck?
You can visualize reconnaissance threats by performing a heat map analysis.

It can be used as intelligence, such as checking the IP address from the exported CSV file and adding it to the firewall.

# Installation
- Operation confirmed with Python 3.9.4
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements

    ```
    $ cd ipcheck
    $ python3 -m pip install -r requirements.txt
    ```

# Usage

```
$ python3 src/main.py -h
usage: main.py [-h] [-b] -f F

optional arguments:
  -h, --help  show this help message and exit
  -b          batch mode
  -f F        file name to parse
```

## Normal mode
1. Specify the file name to be analyzed in the -f option and execute

    ```
    $ python3 src/main.py -f <accesslog>
    ```

## Batch mode
1. Execute the following command to export the Access Token obtained from ipinfo.io as an environment variable

    ```
    $ export access_token=xxxxxxxxxxxxxx
    ```

1. Specify the file name to be analyzed in the -f option and execute with -b

    ```
    $ python3 src/main.py -f <accesslog> -b
    ```

## Heatmap analysis
Open the generated heatmap.html in your browser.

# License
[MIT](https://choosealicense.com/licenses/mit/)
