#Software za komparaciju edi logova
#Usporedba da li isti pozivni znak u dva loga ima isti lokator 
#i provjera da li redni broj veze ima smisla u obziru na vrijeme veze.

import datetime

#funckcije 

def usporediQso(log1data,log2data):
    hasErrors = False
    if(log1data.r_locator == log2data.r_locator) == False:
        print("[",log1data.callsign,"] Lokator u (",log1data.filename,")logu -",log1data.r_locator,",redni broj veze",log1data.r_sent,"se ne poklapa sa lokatorom u (",log2data.filename,")logu -",log2data.r_locator,",redni broj veze",log2data.r_sent)
        hasErrors = True

    #te usporedi po vremenu i broju veze log1 na log2
    if (log1data.r_received > log2data.r_received) and (log1data.timedate < log2data.timedate) == True:
        print("[",log1data.callsign,"] Primljeni broj u (",log1data.filename,")logu -",log1data.r_received,"je veci od primljenoga broja -",log2data.r_received,"u (",log2data.filename,")logu iako je veza u logu 1 ranije odrzana")
        hasErrors = True
            
        #te usporedi po vremenu i broju veze log2 na log1
    if (log1data.r_received < log2data.r_received) and (log1data.timedate > log2data.timedate) == True:
        print("[",log1data.callsign,"] Primljeni broj u (",log1data.filename,") logu -",log2data.r_received,"je veci od primljenoga broja -",log1data.r_received,"u (",log2data.filename,")logu iako je veza u logu 2 ranije odrzana")
        hasErrors = True

    if(hasErrors): #odvoji greske za lakse citanje
        print(" ")
        return False
    return True

def ucitajEdi(filename):
    dest = {}
    try:

        with open(filename) as fp:  
            line = fp.readline()
            while line:
                line = fp.readline()  #za svaki red u edi fajlu
                if line.endswith(';;;;\n'): #ako zavrsava sa ;;;;(novi red)
                    line = line.split(";") # razdvoji qso redak sa ;

                    time = "20" + line[0]+line[1] #na datum dodaj 20 ispred
                    time = datetime.datetime.strptime(time, '%Y%m%d%H%M') #pretvori iz teksta u pravi format datuma
                    #izvuci sljedece podatke s obzirom na razmake
                    #qso callsign
                    callsign = line[2]
                    #poslani raport
                    rstsent = line[4]
                    r_sent = line[5]
                    #primljeni raport
                    rstreceived = line[6]
                    r_received = line[7]
                    r_locator = line[9]
                    #broj bodova
                    qrb = line[10]
                    #print(time,"|",callsign,"|",rstsent,"|",r_sent,"|",rstreceived,"|",r_received,"|",r_locator,"|",qrb)
                    data = qso(callsign,time,rstsent,r_sent,rstreceived,r_received,r_locator,qrb,filename)

                    # na kraju spremi u odredjeni spremnik
                    dest[callsign] = data

    except:
        print("Ne mogu otvoriti falj ",filename)
        quit()

    return dest



#classevi 
class edi: #ovaj jos nije implementiran
    def __init__(self,callsign,locator):
        self.callsign = callsign
        self.locator = locator

class qso:
    def __init__(self,callsign,timedate,rstsent,r_sent,rstreceived,r_received,r_locator,qrb,filename):
        self.callsign = str(callsign)
        self.timedate = str(timedate)
        self.rstsent = int(rstsent)
        self.r_sent = int(r_sent)
        self.rstreceived = int(rstreceived)
        self.r_received = int(r_received)
        self.r_locator = str(r_locator)
        self.qrb = str(qrb)
        self.filename = str(filename)
    #def __str__(self):
        #return(self.callsign)

nLogs = int(input("Unesi broj logova za crosscheck provjeru: "))
logs = []
for i in range(nLogs):
    filename = input("Unesi filename loga:")
    data = ucitajEdi(filename)
    logs.append(data)

print("")

brojGreski = 0
for log in logs:
    qsolist = log

    for qso in logs:
        qsolist2 = qso

        for callsign in qsolist2:
            veza1 = qsolist2[callsign]
            try:
                veza2 = qsolist[veza1.callsign]
                #print(veza1.callsign , veza2.callsign)
                ispravan = usporediQso(veza1,veza2)
                if ispravan == False:
                    brojGreski +=1
            except:
                pass




if brojGreski != 0:
    print("Pronadjeno je",brojGreski,"nepoklapanja u logovima")
else:
    print("Nepoklapanja nisu pronadjena")

input("Pritisni bilo koju tipku za izlaz ")
