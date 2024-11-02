# Gioele Amendola
# 02/09/2024

import os, PyPDF2, textract

#IMMISSIONE DEI PARAMETRI
dirRoot: str = input("Inserisci la root directory: ")
string: str = input("Inserisci la stringa da cercare: ")

#FUNZIONI
def CercaStringaInFileName(file: str, string: str) -> bool:
    file = file.lower()
    string = string.lower()
    print(f"Cerco {string} in {file}")
    if string in file:
        print("Trovato\n")
        return True
    print("Non Trovato\n")
    return False

def CercaStringaInFileContent(file: str,string: str) -> bool:
    string = string.lower() 
    flag: bool = False
    print(f"Cerco {string} contenuto in {os.path.basename(file)}")
    _, ext= os.path.splitext(file)
    if ext == ".pdf":
        flag = CercaStringaInPdf(file, string)
    elif ext == ".doc" or ext == ".docx":
        flag = CercaStringaInDoc(file, string)
    else:
        try:
            with open(file, 'r') as f:
                line: str = f.readline()
                while line:
                    line = line.lower()
                    if string in line:
                        flag = True
                        break
                    line = f.readline()
        except:
            print(f"Errore: Path inesistente - {file}")
            flag = False
    if flag:
        print("Trovato\n")
        return True
    print("Non Trovato\n")
    return False

def CercaStringaInPdf(file: str, string: str) -> bool:
    obj = PyPDF2.PdfReader(file)
    nPages = len(obj.pages)
    for i in range(nPages):
        pageObj = obj.pages[i]
        text: str = pageObj.extract_text()
        text = text.lower()
        if string in text:
            return True
    return False

def CercaStringaInDoc(file: str, string: str) -> bool:
    # textract module
    # process function:
    # This is the core function used for extracting text.
    # It routes the filename to the appropriate parser and returns
    # the extracted text as a byte-string encoded with encoding.
    text: str = textract.process(file) 
    text = text.lower()
    if string.lower() in text:
        return True
    return False 


#NAVIGA NEL FILE SYSTEM
nFiles: int = 0
nContent: int = 0
foundIn: list[str] = []
for root, dirs, files in os.walk(dirRoot):
    print(f"Dir corrente {root} contenente {len(dirs)} subdir e {len(files)} files")
    for filename in files:
        flag: bool = CercaStringaInFileName(filename,string)
        if flag:
            foundIn.append(filename)
            nFiles += 1
        else:
            flag = CercaStringaInFileContent(os.path.join(root,filename), string)
            if flag:
                foundIn.append(filename)
                nContent += 1
print(f"\nLa stringa {string} è stata trovata come nome in {nFiles} file ed è contenuta in {nContent} file.")
while True:
    comand = input("\nVuoi vedere i file in cui è stato trovato? (y/n)") if foundIn else print("Nessun file trovato.")
    if comand in ["Y","y"]:
        print(f"File contenenti la stringa:\n{foundIn}")
        break
    elif comand in ["N","n"]:
        break
    else:
        print("Comando non riconosciuto. Riprova.")




