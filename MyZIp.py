# -*- coding: utf-8 -*-
import sys
import os
from os.path import isfile, isdir, join    #路徑檢視及操作os.path非常好用
from os import listdir    #os.listdir module
import zipfile    #f=zipfile.ZipFile(file, mode="r", compression=[ZIP_STORED], allowZip64=False)    壓縮2GB以上，請開64
import shutil    #刪除空資料夾及非空資料夾

"""列出資料夾所有檔案與目錄""" 
def print_list(input_path:str,print_list=None):

        if print_list == None:    #未return的list為None
                print_list = []
        """直接用get_files"""
        get_files(input_path,print_list)    #遍歷根目錄所有檔案路徑
        
        print("要執行的路徑共有以下清單:")
        print("---------------------------")
        """直接用get_files與ge差異"""
        for name in print_list:
                if isfile(name):
                        print("檔案:",name)
        #print("檔案共有:")
        #ge_list(input_path)
        print("---------------------------")

"""列出zip檔案底下所有檔案"""#以路径 Path = “E:\\data” 为例,需要保证以下几点：路径中间的斜杠一定是双斜杠 “ \\ ”data文件夹下不包含单独文件，保证全部是子文件夹。
def print_zip(input_path:str,print_list=None):
        if print_list == None:
                print_list = []
        if zipfile.is_zipfile(input_path):    #如函式前面註解所言,zip是檔案所以...無法用一般正常方法遍歷.須用這方法
                print("zip底下的檔案共有以下清單:")
                print("---------------------------")
                zp = zipfile.ZipFile(input_path,'r')
                for file in zp.namelist():
                        print("檔案:",file)
                print("---------------------------")

"""找出全部檔案路徑"""
def get_files(input_path:str,result:list):    #f(path,storge)
        #取得第一層檔案與子目錄名稱.
        files = listdir(input_path)
        
        for file in files:
                #產生keyin的路徑以下的絕對路徑
                fullpath = join(input_path,file)   #操作檔案需要絕對路徑.os.path.join(root_path,interable_E)做結合 or 用scandir()來迭代 的f'{dir}\\{file.name}'
                
                if os.path.isfile(fullpath):
                        result.append(fullpath)
                elif os.path.isdir(fullpath):
                        get_files(fullpath,result)    #連同儲存的list一起丟回函式遞迴

"""將get_files結果做產生器"""
def ge_list(input_path):
        li = []
        get_files(input_path,li)
        ge = iter(li)
        try:
                while True:
                        print(next(ge))    #是否有必要化成ge?
        except StopIteration:
                pass

"""確認放置路徑是否存在及創建"""
def check_path(input_path:str):
        if not os.path.exists(input_path):
                #壓縮目的路徑如存在就不跳except,否則創立路徑
                print("路徑為:",input_path,"不存在,將嘗試創立該資料夾路徑...")
                print("工作繼續進行中...")
                os.makedirs(input_path, exist_ok=True)    #try,except避免
        else:
                print("放置路徑確認存在,將繼續進行...")

"""輸入路徑做壓縮的函式"""
def zip_list(input_path:str,out_zip:str):

        """創立壓縮檔"""
        zp = zipfile.ZipFile(out_zip,'w')    #創立壓縮檔後,利用該物件的write將要壓縮的檔案寫入在該物件內.語法上同with zipfile.ZipFile(‘test.zip‘, mode=‘w‘) as zp:
        file_list = []
        get_files(input_path,file_list)

        """將檔案寫入壓縮檔"""
        for name in file_list:
                #ZIP_DEFLATED壓縮方式
                zp.write(name,os.path.basename(name),zipfile.ZIP_DEFLATED)
        zp.close()

"""輸入路徑做解壓縮"""
def unzip_list(input_path:str,output_path:str):
        
        zp = zipfile.ZipFile(input_path,'r')
        zp.extractall(output_path)    #解壓縮多個文件到指定路徑,如空值則默認解壓到python工作環境
        zp.close

"""使用者輸入選擇1:壓縮"""
def key1():

        keyin_path = ''     #使用者輸入欲壓縮路徑
        keyin_outputpath = ''    #使用者輸入壓縮檔欲輸出路徑
        
        """輸入資料防呆"""
        while True:
                keyin_path = input('請輸入要 壓縮的檔案或資料夾 絕對路徑:')
                #keyin_path = r"D:\\sample"   #測試用 input會自動加r'path'
                if os.path.exists(keyin_path):
                        break
                else:
                        print('要輸入的壓縮路徑錯誤或不存在,請重新輸入')
                        continue

        print("輸入要壓縮的路徑為:",keyin_path,end = '\n')
        print_list(keyin_path)

        """列出清單後確認防呆"""
        while True:
                choose = ''
                choose = input("是否要繼續壓縮?輸入Y/N\n").lower()
                if choose == 'y':
                        break
                #程式中止
                elif choose == 'n':
                        print("程式中止")
                        sys.exit()
                else:
                        print("輸入錯誤,請重新輸入")
                        continue

        keyin_outputpath = input('請接著輸入壓縮檔案後要放置的資料夾路徑:')
        #keyin_outputpath = r"D:\\test\test2\myzip"  #測試用 input會自動加r'path'
        check_path(keyin_outputpath)

        print("\n壓縮中...\n")
        zip_list(keyin_path,keyin_outputpath + '/work.zip')
        print("壓縮完成!")

        while True:
                del_choose = input("是否要刪除原資料夾?Y/N\n").lower()
                if del_choose == 'y':
                        del_dir(keyin_path)
                        break
                elif del_choose == 'n':
                        print("程式結束")
                        sys.exit()
                else:
                        print("輸入錯誤,請重新輸入")
                        continue

"""使用者輸入選擇2:解壓縮"""
def key2():

        keyin_path = ''     #使用者輸入欲解壓縮路徑
        keyin_outputpath = ''    #使用者輸入解壓縮欲輸出路徑
        
        while True:
                keyin_path = input('請輸入要 解壓縮的檔案或資料夾 絕對路徑:')
                #keyin_path = r"D:\\test\test2\myzip\work.zip"   #測試用
                if zipfile.is_zipfile(keyin_path):    #並非是zip檔
                        break
                else:
                        print('輸入的路徑不是壓縮檔或不存在,請重新輸入')
                        continue

        print("輸入要解壓縮的路徑為:",keyin_path,end = '\n')
        print_zip(keyin_path)

        while True:
                choose = ''
                choose = input("是否要繼續解壓縮?輸入Y/N\n").lower()
                if choose == 'y':
                        break
                elif choose == 'n':
                        print("程式中止")
                        sys.exit()
                else:
                        print("輸入錯誤,請重新輸入")
                        continue

        keyin_outputpath = input("請接著輸入 解壓縮 後要 放置 的路徑:")    #使用者輸入欲輸出路徑
        #keyin_outputpath = r"D:\finish"    #測試用
        check_path(keyin_outputpath)

        print("\n解壓縮中...\n")
        unzip_list(keyin_path,keyin_outputpath)
        print("解壓縮完成!")

        while True:
                del_choose = input("是否要刪除原zip檔?Y/N\n").lower()
                if del_choose == 'y':
                        del_file(keyin_path)
                        break
                elif del_choose == 'n':
                        print("程式結束")
                        sys.exit()
                else:
                        print("輸入錯誤,請重新輸入")
                        continue

"""刪除檔案"""
def del_file(file_name):
        if os.path.exists(file_name):
                os.remove(file_name)

"""刪除資料夾"""
def del_dir(dir_name):
        if os.path.exists(dir_name):
                shutil.rmtree(dir_name)    #os.rmdir(dir_name)    只能刪除空的資料夾

"""將程式結構清晰化"""
def main():
        while True:
                choose = input("請輸入使用功能:1.壓縮 2.解壓縮 3.離開\n")
                if choose == '1':
                        key1()
                elif choose == '2':
                        key2()
                elif choose == '3':
                        print("跳出程式")
                        sys.exit()
                else:
                        print("輸入錯誤,請重新輸入")
                        continue

"""主程式"""
if __name__ == '__main__':

        main()

       
