# pdf-injection

Installation
```
git clone https://github.com/kaanatmacaa/pdf-injection.git
```

Usage
```
python3 xss-pdf.py -h
python3 xss-pdf.py 
python3 xss-pdf.py -u http://burpsuite12345.oastify.com
python3 xss-pdf.py -u http://burpsuite12345.oastify.com -sc "app.alert(2)"
python3 xss-pdf.py -o html
```

-o output: pdf, html, image
-u url: http://burpsuite12345.oastify.com
-sc: add additional script to PDF file


Open to new suggestions, please create an issue