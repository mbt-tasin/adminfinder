# Admin Finder
A Ultra-fast admin panel finding tool

## legal disclaimer:

Usage of Admin Panel Finder for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state, and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

## Usges:

For simple run

```bash
  python adminfinder.py -u https://example.com
```
Save the output
```bash
  python adminfinder.py -u https://example.com -o
```
You can use your own wordlist
```bash
  python adminfinder.py -u https://example.com -w wordlist.txt
```
I also add 5 second of interval after every 1000 request.If you continuously getting error try to adjust the parameters in adminfinder.py
```bash
  REQUESTS_PER_WAIT = 1000
  WAIT_TIME_SECONDS = 5
```
If you get error try to change your proxy server :)
