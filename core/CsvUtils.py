import csv  

#"database/dataset/chiron-dataset/music_views.csv"
def readDataFromCsv(filePath):
    data = []
    
    with open(filePath) as csvfile:  
        dictReader = csv.DictReader(csvfile)
        for row in dictReader:
            data.append(row)
    
    return data

def writeDataToCsv(filePath,data):
    fieldList = list(data[0].keys())
    
    with open(filePath,"w") as csvfile:  
        dictWriter = csv.DictWriter(csvfile,fieldList)
        dictWriter.writeheader()
        dictWriter.writerows(data)
