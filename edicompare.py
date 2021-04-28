# Software za komparaciju edi logova
# Usporedba da li isti pozivni znak u dva loga ima isti lokator
# i provjera da li rb = ima smisla u obziru na vrijeme veze.

import datetime

from colorama import Fore
from colorama import Style
from colorama import init

init(convert=True)


# funckcije

def ucitajEdi(filename, dest, dest2):
    try:

        with open(filename) as fp:
            line = fp.readline()
            while line:
                line = fp.readline()  # za svaki red u edi fajlu
                if line.endswith(';;;;\n'):  # ako zavrsava sa ;;;;(novi red)
                    line = line.split(";")  # razdvoji qso redak sa ;

                    time = "20" + line[0] + line[1]  # na datum dodaj 20 ispred
                    time = datetime.datetime.strptime(time, '%Y%m%d%H%M')  # pretvori iz teksta u pravi format datuma
                    # izvuci sljedece podatke s obzirom na razmake
                    # qso callsign
                    callsign = line[2]
                    # poslani raport
                    rstsent = line[4]
                    r_sent = line[5]
                    # primljeni raport
                    rstreceived = line[6]
                    r_received = line[7]
                    r_locator = line[9]
                    # broj bodova
                    qrb = line[10]
                    # print(time,"|",callsign,"|",rstsent,"|",r_sent,"|",rstreceived,"|",r_received,"|",r_locator,"|",qrb)
                    data = qso(callsign, time, rstsent, r_sent, rstreceived, r_received, r_locator, qrb)

                    # na kraju spremi u odredjeni spremnik
                    dest[callsign] = data
                    dest2[r_locator] = data

    except:
        print("Ne mogu otvoriti falj ", filename_edi_1)
        quit()


# classevi
class edi:  # ovaj jos nije implementiran
    def __init__(self, callsign, locator):
        self.callsign = callsign
        self.locator = locator


class qso:
    def __init__(self, callsign, timedate, rstsent, r_sent, rstreceived, r_received, r_locator, qrb):
        self.callsign = str(callsign)
        self.timedate = str(timedate)
        self.rstsent = int(rstsent)
        self.r_sent = int(r_sent)
        self.rstreceived = int(rstreceived)
        self.r_received = int(r_received)
        self.r_locator = str(r_locator)
        self.qrb = str(qrb)

    def __str__(self):
        return self.callsign


filename_edi_1 = input("Unesi filename prvoga edi loga: ")
filename_edi_2 = input("Unesi filename drugoga edi loga: ")

print("")

log1 = {}  # spremiste za prvi log, moguce korisiti SQL u buducnosti
log1byLoc = {}
ucitajEdi(filename_edi_1, log1, log1byLoc)

log2 = {}  # spremiste za drugi log, moguce korisitit SQL u buducnosti
log2byLoc = {}
ucitajEdi(filename_edi_2, log2, log2byLoc)

# napravi provjeru loga2 referencom u log1, provjeri lokatore
brojGreski = 0
brojUpozorenja = 0

for i in log1:
    # za svaki ppozivni znak u logu jedan

    try:
        hasErrors = False
        log1data = log1[i]
        log2data = log2[log1data.callsign]  # ako taj isti postoji u logu2 spremi ga u varijable,

        if not any(map(str.isdigit, log1data.callsign[:3])):
            # Ako prve tri znamenke pozivnoga znaka ne sadrze ni jedan broj
            int(log1data.callsign[:3])
            print(Fore.YELLOW + "[", log1data.r_locator, "]" + Style.RESET_ALL + "Pozivni znak u prvome logu -",
                  Fore.MAGENTA + log1data.callsign + Style.RESET_ALL, ",rb =", log1data.r_sent,
                  " ima za prve tri znamenke samo slova")
            brojUpozorenja += 1
            hasErrors = True

        # te usporedi po lokatoru
        if not (log1data.r_locator == log2data.r_locator):
            print(Fore.RED + "[", log1data.callsign, "]" + Style.RESET_ALL + "Lokator u prvome logu -",
                  Fore.MAGENTA + log1data.r_locator + Style.RESET_ALL, ",rb =", log1data.r_sent,
                  "se ne poklapa sa lokatorom u drugome logu -", Fore.MAGENTA + log2data.r_locator + Style.RESET_ALL,
                  ",rb =", log2data.r_sent)
            brojGreski += 1
            hasErrors = True

        # te usporedi po vremenu i broju veze log1 na log2
        if (log1data.r_received > log2data.r_received) and (log1data.timedate < log2data.timedate) == True:
            print(Fore.RED + "[", log1data.callsign, "]" + Style.RESET_ALL + "Primljeni broj u prvome logu",
                  Fore.MAGENTA + log1data.r_received + Style.RESET_ALL, "je veci od primljenoga broja -",
                  Fore.MAGENTA + log2data.r_received + Style.RESET_ALL,
                  "u drugome logu iako je veza u logu 1 ranije odrzana")
            brojGreski += 1
            hasErrors = True

        # te usporedi po vremenu i broju veze log2 na log1
        if (log1data.r_received < log2data.r_received) and (log1data.timedate > log2data.timedate) == True:
            print(Fore.RED + "[", log1data.callsign, "]" + Style.RESET_ALL + "Primljeni broj u drugome logu -",
                  Fore.MAGENTA + log2data.r_received + Style.RESET_ALL, "je veci od primljenoga broja -",
                  Fore.MAGENTA + log1data.r_received + Style.RESET_ALL,
                  "u prvome logu iako je veza u logu 2 ranije odrzana")
            brojGreski += 1
            hasErrors = True

        if hasErrors:  # odvoji greske za lakse citanje
            print(" ")
    except:
        pass

for i in log1byLoc:
    hasWarnings = False
    try:
        log1data = log1byLoc[i]
        log2data = log2byLoc[log1data.r_locator]

        if not (log1data.callsign == log2data.callsign):
            print(Fore.YELLOW + "[", log1data.r_locator, "]" + Style.RESET_ALL + "Pozivni znak u prvome logu -",
                  Fore.MAGENTA + log1data.callsign + Style.RESET_ALL, ",rb =", log1data.r_sent,
                  "se ne poklapa sa pozivnim znak u drugome logu -", Fore.MAGENTA + log2data.callsign + Style.RESET_ALL,
                  ",rb =", log2data.r_sent, "iako je lokator jednak")
            brojUpozorenja += 1
            hasWarnings = True

        if hasWarnings:  # odvoji greske za lakse citanje
            print(" ")
    except:
        pass

if brojGreski != 0:
    print(Fore.RED + "Pronadjeno je", brojGreski, "nepoklapanja u logovima" + Style.RESET_ALL)
if brojUpozorenja != 0:
    print(Fore.YELLOW + "Pronadjeno je", brojUpozorenja, "upozorenja u logovima" + Style.RESET_ALL)
if not brojGreski and not brojUpozorenja:
    print("Nepoklapanja nisu pronadjena")

input("Pritisni bilo koju tipku za izlaz ")
