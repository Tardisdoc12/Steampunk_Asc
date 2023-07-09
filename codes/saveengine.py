import globals

def fileExist(filename):
    try:
        file=open(filename,"x")
        file.close()
        return True
    except:
        return False

def CreateFile(filename):
    if fileExist(filename):
        file=open(filename,"w")
        file.write("Scientific\n")
        file.write("30 200\n")
        file.write("Scientific\n")
        file.write("0\n")
        file.write("Miner\n")
        file.write("0\n")
        file.write("Thief\n")
        file.write("0\n")
        file.write("Engeneer\n")
        file.write("0\n")
        file.close()

class SaveEngine:
    def __init__(self):
        self.filename="../Database/Save.txt"
        createFile(filename)

    def saveInformations(self):
        file=open(self.filename,"w")
        file.write(globals.archetype[0]+"\n") #Save le dernier archetype joué
        file.write(str(globals.position[0])+" "+str(globals.position[1])+"\n")
        #save the experience for each class!
        #creer une boucle sur le dico des classes de joueurs
        for classe in list(globals.classDico.classes.keys()):
            file.write(classe+"n")
            file.write(str(globals.XP[classe])+"\n")

    def ReadPrecedentSave(self):
        file=open(self.filename,"r")
        #on lit le dernier archetype jouer pour que dans la base il y ait une linéarité!
        globals.archetype=globals.classDico.classes[file.readline().strip()]
        #On lit la position dans la base et on va pouvoir la passer à globals.
        position=file.readline().strip().split()
        globals.position=(int(position[0]),int(position[1]))
        #on lit les points d'experience de chaque classe:
        for classe in globals.classDico.classes:
            classeTemp=file.readline().strip()
            globals.XP[classeTemp]=int(file.readline().strip())

if __name__ == "__main__":
    file=open("../Database/Test.txt","w")
    file.write("Ceci est un test.\n")
    file.close()
    file=open("../Database/Test.txt","r")
    var=file.readline().strip()
    file.close()
    print("la variable est :",var)
    stre="30 250\n"
    position=stre.strip().split()
    liste=(int(position[0]),int(position[1]))
    print(liste)
