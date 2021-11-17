import os
def seperateData():
    file_path = 'rawData.txt'
    current_path = os.path.dirname(__file__)
    file_loc = os.path.join(current_path, file_path)
    filetxt = open(file_loc, "r")
    data = filetxt.read()
    filetxt.close()
    
    data = data.split("\n")
    for i in range(len(data)): 
        data[i] = data[i].split()
        data[i] = data[i][1:5]
        print(data[i])
    
    f = open("24sets.txt", "w")
    text = ''
    for line in data:
        for num in line:
            text += num + ' '
        text += "\n"
        

    f.write(text)
    f.close()