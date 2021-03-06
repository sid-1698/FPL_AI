import pandas as pd 
import os

def write(data,path,filename,show=1):
    if os.path.isdir(path) == False:
        os.makedirs(path)
    Writer = pd.ExcelWriter(path/filename,engine='xlsxwriter')
    data.to_excel(Writer)
    Writer.save()
    if show != 0:
        print(show,str(filename)," - Succesfully Written in ",str(path))  

if __name__ == "__main__":
    pass