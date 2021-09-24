import os
from pathlib import Path
import sys
import sqlite3
from sqlite3 import Error
from urllib.request import pathname2url
import numpy as np
#для попытки вывести динамическое время в заголовке формы
import re 
import time as time
from datetime import timedelta, datetime
import traceback
import threading
#------------------------------------------------------------------
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle
#LETTER
from reportlab.lib.pagesizes import  A4, letter, landscape 
from reportlab.lib import colors
#для рассылки
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
#------------------------------------------------------------------
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,  QInputDialog, QLineEdit, QFileDialog,QMessageBox,QDialog,QWidget,QMenu
from PyQt5.QtGui import *
from PyQt5.QtCore  import*

class Sql_Query(QDialog):
    global time_elemen,for_sec_signal,for_selec
    time_elemen=0
    for_selec=None
    for_sec_signal=None
    #не работает окно сообщения об ошибки 
    def openFileNameD(self):
        fileName=QtWidgets.QFileDialog.getOpenFileName()[0].replace('/','\\')
        global time_elemen
        time_elemen=time_elemen+1
        #if len(fileName)>0:
        return fileName
        
        
    # функция для проверки соеденения с бд и в ней будет вызов функции для выбора файла бд 
    def cheak_conection_with_db(self, adress_file, adress_of_data_base,rewritenum):
        try:
            dburi = 'file:{}?mode=rw'.format(pathname2url(adress_of_data_base))
            conn = sqlite3.connect(dburi, uri=True)
            if rewritenum==0:
                with open(adress_file, 'w'):
                    pass
                file= open(adress_file,'w')
                file.write(adress_of_data_base)
                file.close()
                return adress_of_data_base
            else:
                return adress_of_data_base
        except sqlite3.OperationalError:
            if time_elemen==0:
                adress_of_data_base =self.openFileNameD()
                rewritenum=0
            else:
                pass;
            if rewritenum==0:
                with open(adress_file, 'w'):
                    pass
                file= open(adress_file,'w')
                file.write(adress_of_data_base)
                file.close()
                return adress_of_data_base
            else:
                return adress_of_data_base 
    #функция которая отдает адрес бд  из файла на проверку конекта  в def cheak_conection_with_db и после в миксер запросов
    # adress_file -  адресс текстового файла , adress_of_data_base - адресс базы данных ,rewritenum - переменная для перезаписи адресса в бд 
    def adressmaker(self):
        adress_file=os.path.abspath('form.py')
        adress_file=adress_file.replace('form.py','')
        adress_file=adress_file+'myadress.txt'
        adress_of_data_base=''
        if os.path.isfile(adress_file) is True:
           file=open(adress_file,'r')
           adress_of_data_base=file.readline()
           file.close()
           ##################################################
           if not adress_of_data_base:
               if time_elemen==0:
                    adress_of_data_base=self.openFileNameD()
                    return self.cheak_conection_with_db(adress_file,adress_of_data_base,0)
               else:
                    pass;
           return self.cheak_conection_with_db(adress_file,adress_of_data_base,1)
        else:
            file=open(adress_file,'w')
            adress_of_data_base=adress_file.replace('myadress.txt','OB_DB.sqlite')
            adress_of_data_base=self.cheak_conection_with_db(adress_file,adress_of_data_base,1)
            file.write(adress_of_data_base)
            file.close()
            return adress_of_data_base
    def TABLE_ROWS_NAME(self):
        self.adressmaker()
        # MY_SQL_DATABASE_NAME='D:\Myproject\object_proect_for_Hotel\OB_DB.sqlite'
        #self.conect_to_base()
        conwithbase = sqlite3.connect(self.adressmaker())
        """установление курсора для начала работы запросов """
        cursor = conwithbase.cursor()
        result = cursor.execute(
        '''SELECT * from TABLE_ROWS_NAME''')
        b=result.fetchall()
        return (b)
        conwithbase.close()
    def ALL_SQL_AT_ONE(self,tipe_of_function,number_of_table,first_number,last_number):
        #номер индекса первого совпадения записи в большой таблице
        #element_zero_of_list=0
        #название таблицы
        #print(tipe_of_function,number_of_table,first_number,last_number)
        b=None
        element_table_name=''
        #массив содержаший названия полей 
        #first_number
        element_rows_name_of_list=[]
        #last_number
        element_of_data_for_rows=[]
        element_for_where_of_list=[]
        unikal_zero_index=0
        #первой и последний (ИНдекс)элемент выбранной таблицы в таблице  
        first_step=0
        last_step=0
        #сама готовая в будущем строка запроса 
        sql_string=''
        #великий список полей с названиями таблиц и полей в них 
        table_info=self.TABLE_ROWS_NAME()
        #---------------------------------------------------------------------
        #в этом цикле определяем границы вписенной таблицы
        for step_at_massive in range(0,len(table_info)):
            if table_info[step_at_massive][4]==number_of_table:     
                first_step=table_info[step_at_massive][0]
                break;
            else:
                pass;
        for i in range (first_step-1,len(table_info)):
                if table_info[i][4]==number_of_table:
                    if number_of_table==18 :
                        last_step=109
                        break;
                    else:
                        last_step=last_step+1
                else:
                   
                   last_step=table_info[i-1][0]
                  
                   break;
            #---------------------------------------------------------------------
            #название таблицы  вписываем её в переменную

        element_table_name=element_table_name+str(table_info[first_step-1][1])
        if tipe_of_function=='select':

            sql_string=sql_string+'select '

       
            #---------------------------------------------------------------------
            #ВНИМАНИЕ тут на том что эти числа вводятся разработчиком и по умолчанию они тут в пределах разумного и не проверяются на правильность первое меньше второго и тому подобное  
            #начинаем использовать переменные определяющие сколько полей нужно использовать
            # если обе равны '' то используются все поля
            # если вторая переменная равна '' то значит только одно поле
            # если первым является массив чисел из двух чисел выдастя интервал из этих двух чисел 
            # если указан массив из нескольки чисел и -1 то выдадутся только поля под теми числами в порядке возрастания   
            # если нужно условие с выводом всех полей то пишитется такое. first_number делается многомерным масивом где первый элемент пишитеться слово условие вторым * а во второй переменной last_number  сформировать два массива первый с полями для условия  второй с переменными для условия. Их размер долден быть одинаковым и расположение полей/переменных соответсвенным
            #если нужно условие с выводом конкретных полей то пишитется такое. first_number делается многомерным масивом где первый элемент пишитеться слово условие вторым массив с номерами полей для вывода(поля будут обрабатываться в порядке возрастания !!!) а во второй переменной last_number  сформировать два массива первый с полями для условия  второй с переменными для условия. Их размер долден быть одинаковым и расположение полей/переменных соответсвенным
            if first_number=='' and last_number=='':
                #for i in range(first_step,last_step):
                 #   element_rows_name_of_list.append(table_info[i][2])
                sql_string=sql_string+'* from '+element_table_name+' '
                conwithbase = sqlite3.connect(self.adressmaker())
                cursor = conwithbase.cursor()
                #print(sql_string)
                result = cursor.execute(sql_string)
                b=result.fetchall()
                return (b)
                conwithbase.close()
            
            elif type(first_number)==int and  last_number=='':
                for i in range(first_step-1,last_step):                    
                    if table_info[i][3]==first_number:        
                        element_rows_name_of_list.append(table_info[i][2])
                for i in range (0,len(element_rows_name_of_list)):
                    sql_string=sql_string+element_rows_name_of_list[i]
                sql_string=sql_string+' '+'from '+element_table_name+' '
                conwithbase = sqlite3.connect(self.adressmaker())
                cursor = conwithbase.cursor()
                #print(sql_string)
                result = cursor.execute(sql_string)
                b=result.fetchall()
                return (b)
                conwithbase.close()

            elif type(first_number)==list and last_number=='':

                for i in range(first_step-1,last_step):

                    if table_info[i][3]>=first_number[0] and table_info[i][3]<=first_number[1]:
                        element_rows_name_of_list.append(table_info[i][2])
               
                for i in range (0,len(element_rows_name_of_list)):
                    if i==0:
                        sql_string=sql_string+element_rows_name_of_list[i]
                    else:
                        sql_string=sql_string+','+element_rows_name_of_list[i]
                sql_string=sql_string+' '+'from '+element_table_name+' '
                conwithbase = sqlite3.connect(self.adressmaker())
                cursor = conwithbase.cursor()
                #print(sql_string)
                result = cursor.execute(sql_string)
                b=result.fetchall()
                return (b)
                conwithbase.close()

            elif type(first_number)==list and last_number==-1:
                
                for  i in range(first_step-1,last_step):
                    for q in range(0,len(first_number)):
                        if table_info[i][3]==first_number[q]:
                            element_rows_name_of_list.append(table_info[i][2])
               
                for i in range (0,len(element_rows_name_of_list)):
                    if i==0:
                        sql_string=sql_string+element_rows_name_of_list[i]
                    else:
                        sql_string=sql_string+' , '+element_rows_name_of_list[i]
                sql_string=sql_string+' '+'from '+element_table_name+' '
                conwithbase = sqlite3.connect(self.adressmaker())
                cursor = conwithbase.cursor()
                #print(sql_string)
                result = cursor.execute(sql_string)
                b=result.fetchall()
                return (b)
                conwithbase.close()
            #изменение на инсерт
            elif type(first_number)==list and first_number[0]=='WHERE' and first_number[1]=='*':
                # в строку запроса вписывается звездочка
                if last_number[0]==[]:
                    sql_string=sql_string+'* from '+element_table_name+' '
                else:
                        sql_string=sql_string+' '+first_number[1]+' '
                        #идет пробег по гранницам ранее указанной  таблице с полями и индексами
                        for  i in range(first_step-1,last_step):
                            #проверка указанного номера поля с номером поля из таблицы
                            for z in range(0,len(last_number[0])):
                                if table_info[i][3]==last_number[0][z]:
                                    #если номера совпали то происходит формирование списка с полями для условия . Обязательно количество полей для условия будет соответсвовать количеству переменных
                                    #element_for_where_of_list.append(table_info[i][2])
                                    element_rows_name_of_list.insert(unikal_zero_index,table_info[i][2])
                                    element_of_data_for_rows.insert(unikal_zero_index,last_number[1][z])
                            unikal_zero_index=unikal_zero_index+1
                        #пропись  названия таблицы 
                        #if element_table_name=="nesildi":
                        #    print('tut')
                        sql_string=sql_string+' '+'from '+element_table_name+' '
                        #пропись  начала условия
                        sql_string=sql_string+' '+first_number[0]+' '
                        #формирования запроса . длина прохода цикла равна количеству переменных в массиве с полями для условия или переменным для уловия из ВТОРОЙ переменной last_number
                        for i in range (0,len(last_number[0])):
                            #обязательное условие на случай только одного вхождения 
                            if i==0:
                                sql_string=sql_string+element_rows_name_of_list[i]+' = '+" '"+element_of_data_for_rows[i]+"' "
                            else:
                                sql_string=sql_string+'and '+element_rows_name_of_list[i]+' = '+' "'+element_of_data_for_rows[i]+'" '
                #print('kuku')
                #print(sql_string)
                conwithbase = sqlite3.connect(self.adressmaker())
                cursor = conwithbase.cursor()
                result = cursor.execute(sql_string)
                b=result.fetchall()
                return (b)
                conwithbase.close()
            #изменение на инсерт
            elif type(first_number)==list and first_number[0]=='WHERE' and type(first_number[1])==list:
                    #идет пробег по гранницам ранее указанной  таблице с полями и индексами
                    for  i in range(first_step-1,last_step):
                            #проверка указанного номера поля с номером поля из таблицы
                            for z in range(0,len(last_number[0])):
                                if table_info[i][3]==last_number[0][z]:
                                    #если номера совпали то происходит формирование списка с полями для условия . Обязательно количество полей для условия будет соответсвовать количеству переменных
                                    element_for_where_of_list.insert(unikal_zero_index,table_info[i][2])
                                    element_of_data_for_rows.insert(unikal_zero_index,last_number[1][z])
                            #формирования списка полей которые необходимо вывести при условии
                            for t in range(0,len(first_number[1])):
                                if table_info[i][3]==first_number[1][t]:
                                    element_rows_name_of_list.insert(unikal_zero_index,table_info[i][2])
                            unikal_zero_index=unikal_zero_index+1
                    # пропись этих полей после select  и перед from
                    for i in range(0,len(element_rows_name_of_list)):
                            if i==0:
                                sql_string=sql_string+element_rows_name_of_list[i]
                            else:
                                sql_string=sql_string+' , '+element_rows_name_of_list[i]
                    #пропись  названия таблицы 
                    if last_number[0]:
                        sql_string=sql_string+' from '+element_table_name+' '
                        if len(first_number)>=3:
                                sql_string=sql_string+' '+first_number[0]+' '
                                #формирования запроса . длина прохода цикла равна количеству переменных в массиве с полями для условия или переменным для уловия из ВТОРОЙ переменной last_number
                                for i in range (0,len(last_number[0])):
                                    #обязательное условие на случай только одного вхождения 
                                    if i==0:
                                        sql_string=sql_string+element_for_where_of_list[i]+' '+first_number[2] +' "'+ element_of_data_for_rows[i]+'%" '
                                    else:
                                        sql_string=sql_string+'and '+element_for_where_of_list[i]+' '+first_number[2] +' "'+ element_of_data_for_rows[i]+'%" '
                        else:
                                #пропись  начала условия
                                sql_string=sql_string+' '+first_number[0]+' '
                                #формирования запроса . длина прохода цикла равна количеству переменных в массиве с полями для условия или переменным для уловия из ВТОРОЙ переменной last_number
                                for i in range (0,len(last_number[0])):
                                    #обязательное условие на случай только одного вхождения 
                                    if i==0:
                                        sql_string=sql_string+element_for_where_of_list[i]+' = '+' "'+element_of_data_for_rows[i]+'" '
                                    else:
                                        sql_string=sql_string+'and '+element_for_where_of_list[i]+' = '+' "'+element_of_data_for_rows[i]+'" '
                    else:
                        sql_string=sql_string+' from '+element_table_name+' '
                    
                   #print(sql_string)
                    conwithbase = sqlite3.connect(self.adressmaker())
                    cursor = conwithbase.cursor()
                    result = cursor.execute(sql_string)
                    b=result.fetchall()
                    return (b)
                    conwithbase.close()
            #изменение на инсерт
            elif type(first_number)==list and first_number[0]=='WHERE' and first_number[1]=='like':
                if last_number[0]==[]:
                    sql_string=sql_string+'* from '+element_table_name+' '
                else:
                        #print('lastnum',last_number)
                        sql_string=sql_string+' * '
                        #идет пробег по гранницам ранее указанной  таблице с полями и индексами
                        for  i in range(first_step-1,last_step):
                            #проверка указанного номера поля с номером поля из таблицы
                            for z in range(0,len(last_number[0])):
                                if table_info[i][3]==last_number[0][z]:
                                    #если номера совпали то происходит формирование списка с полями для условия . Обязательно количество полей для условия будет соответсвовать количеству переменных
                                    #element_for_where_of_list.append(table_info[i][2])
                                    element_rows_name_of_list.insert(unikal_zero_index,table_info[i][2])
                                    element_of_data_for_rows.insert(unikal_zero_index,last_number[1][z])
                            unikal_zero_index=unikal_zero_index+1
                        #пропись  названия таблицы 
                        sql_string=sql_string+' '+'from '+element_table_name+' '
                        #пропись  начала условия
                        sql_string=sql_string+' '+first_number[0]+' '
                        #формирования запроса . длина прохода цикла равна количеству переменных в массиве с полями для условия или переменным для уловия из ВТОРОЙ переменной last_number
                        for i in range (0,len(last_number[0])):
                            #обязательное условие на случай только одного вхождения 
                            if i==0:
                                sql_string=sql_string+element_rows_name_of_list[i]+' '+first_number[1] +' "'+ element_of_data_for_rows[i]+'%" '
                            else:
                                sql_string=sql_string+'and '+element_rows_name_of_list[i]+' '+first_number[1] +' "'+ element_of_data_for_rows[i]+'%" '

                conwithbase = sqlite3.connect(self.adressmaker())
                cursor = conwithbase.cursor()
                #print(sql_string)
                result = cursor.execute(sql_string)
                b=result.fetchall()
                return (b)
                conwithbase.close()
            #----------------------------------------------------------------------
            # в этапе insert идет следующее распледеле переменных название функции, номер таблицы , !!!массив!!! с номерами полей и !!!!массив!!! с данными для ввода 
        elif tipe_of_function=='insert':
            sql_string=sql_string+'INSERT INTO '
            sql_string=sql_string+' '+element_table_name+'( '
            
            for i in range(first_step-1,last_step):
                 for q in range(0,len(first_number)):
                     if table_info[i][3]==first_number[q]:
                         element_rows_name_of_list.insert(unikal_zero_index,table_info[i][2])
                         element_of_data_for_rows.insert(unikal_zero_index,last_number[q])
                 unikal_zero_index=unikal_zero_index+1

            for i in range (0,len(element_rows_name_of_list)):
                    if i==0:
                        sql_string=sql_string+element_rows_name_of_list[i]
                    else:
                        sql_string=sql_string+','+element_rows_name_of_list[i]
            sql_string=sql_string+' ) VALUES ('
            for i in range(0,len(element_rows_name_of_list)):
                    if i==0:
                        #sql_string=sql_string+'{'+str(i)+'} '
                        sql_string=sql_string+'"'+'{'+str(0)+'['+str(i)+']'+'}'+'" '
                    else:
                        #sql_string=sql_string+',{'+str(i)+'}'
                        sql_string=sql_string+',"'+'{'+str(0)+'['+str(i)+']'+'}'+'"'
            sql_string=sql_string+')'
            sql_string=sql_string.format(element_of_data_for_rows)
            #print(sql_string)
            conwithbase = sqlite3.connect(self.adressmaker())
            cursor = conwithbase.cursor()
           # print(sql_string)
            cursor.execute(sql_string)
            conwithbase.commit()
            conwithbase.close()
            #в этапе удаления нужно уделить внимание по скольким полям будет удалятся записи 1му или более .  название функции, номер таблицы , !!!массив!!! с номерами полей и !!!!массив!!! с данными для удаления
        elif tipe_of_function=='delete':
            sql_string=sql_string+'DELETE FROM '
            sql_string=sql_string+' '+element_table_name+' WHERE '
            #формирует массив с списком полей для удаления
            for i in range(first_step-1,last_step):
                 for q in range(0,len(first_number)):
                     if table_info[i][3]==first_number[q]:
                         element_rows_name_of_list.insert(unikal_zero_index,table_info[i][2])
                         element_of_data_for_rows.insert(unikal_zero_index,last_number[q])
                 unikal_zero_index=unikal_zero_index+1
            if len(first_number)>1:
            #формирует строку для запроса 
                for i in range (0,len(element_rows_name_of_list)):
                        if i==0:
                            sql_string=sql_string+element_rows_name_of_list[i]+" = "
                            sql_string=sql_string+'"'+'{'+str(0)+'['+str(i)+']'+'}'+'"'
                        else:
                            sql_string=sql_string+' and '+element_rows_name_of_list[i]+" ="
                            sql_string=sql_string+'"'+'{'+str(0)+'['+str(i)+']'+'}'+'"'
            elif len(first_number)==1:
                for i in range (0,len(element_rows_name_of_list)):
                        if i==0:
                            sql_string=sql_string+element_rows_name_of_list[i]+" = "
                            sql_string=sql_string+'"'+'{'+str(0)+'['+str(i)+']'+'}'+'"'
            
            sql_string=sql_string.format(element_of_data_for_rows)
            #print(sql_string)
            conwithbase = sqlite3.connect(self.adressmaker())
            cursor = conwithbase.cursor()
            #print(sql_string)
            cursor.execute(sql_string)
            conwithbase.commit()
            #conwithbase.close()
            cursor.close()
        #в запросе UPDATE будет такой ход конем как двойной массив полями для обновления и переменными  [[],]  [[],]..  в первом подмассиве будут находится поля для условия where
        # а в основном поля для для условия SET ... во втором подмассие будут находится переменные для условия where  а в основном для условия SET 
        elif tipe_of_function=='update':
            temp_array=[]
            element_from_rows_for_where=[]
            element_from_variables_for_where=[]
            sql_string='UPDATE'+sql_string
            sql_string=sql_string+' '+element_table_name+' SET '
            if (type(first_number[0]) is list) and (type(last_number[0]) is list) and (type(first_number[1]) is list) and (type(last_number[1]) is list):
               # print('зашли сюда')
               # print('first_number before',first_number)
               # print('last_number before',last_number)
                temp_array=first_number[1]
                element_from_variables_for_where=last_number[1]
               # print('temp_array',temp_array)
                #print('element_from_variables_for_where',element_from_variables_for_where)
                first_number.remove(first_number[1])
                last_number.remove(last_number[1])
                #print('first_number after',first_number)
                #print('last_number after',last_number)

                for i in range(first_step-1,last_step):
                    for q in range(0,len(first_number[0])):
                        if table_info[i][3]==first_number[0][q]:
                            element_rows_name_of_list.insert(unikal_zero_index,table_info[i][2])
                            element_of_data_for_rows.insert(unikal_zero_index,last_number[0][q])
                    for z in range(0,len(temp_array)):
                        if table_info[i][3]==temp_array[z]:
                            element_from_rows_for_where.insert(unikal_zero_index,table_info[i][2])
                    unikal_zero_index=unikal_zero_index+1
                #print('element_rows_name_of_list for set',element_rows_name_of_list)
                #print('element_of_data_for_rows for set',element_of_data_for_rows)
                #print('element_from_rows_for_where',element_from_rows_for_where)
                if len(first_number[0])>1:
            #формирует строку для запроса 
                    for i in range (0,len(element_rows_name_of_list)):
                        if i==0:
                            
                            sql_string=sql_string+element_rows_name_of_list[i]+" = "
                            sql_string=sql_string+'"'+'{'+str(0)+'['+str(i)+']'+'}'+'"'
                            
                        else:
                            
                            sql_string=sql_string+' , '+element_rows_name_of_list[i]+" ="
                            sql_string=sql_string+'"'+'{'+str(0)+'['+str(i)+']'+'}'+'"'
                            
                elif len(first_number)==1:
                    for i in range (0,len(element_rows_name_of_list)):
                        if i==0:
                            
                            sql_string=sql_string+element_rows_name_of_list[i]+" = "
                            sql_string=sql_string+'"'+'{'+str(0)+'['+str(i)+']'+'}'+'"'
                        pass;
                sql_string=sql_string+' WHERE '
                #print('sql_string ',sql_string)
                if len(element_from_rows_for_where)>1:
            #формирует строку для запроса 
                    for i in range (0,len(element_from_rows_for_where)):
                        if i==0:
                            
                            sql_string=sql_string+element_from_rows_for_where[i]+" = "
                            sql_string=sql_string+'"'+'{'+str(1)+'['+str(i)+']'+'}'+'"'
                        else:
                            
                            sql_string=sql_string+' and '+element_from_rows_for_where[i]+" ="
                            sql_string=sql_string+'"'+'{'+str(1)+'['+str(i)+']'+'}'+'"'
                elif len(element_from_rows_for_where)==1:
                    for i in range (0,len(element_from_rows_for_where)):
                        if i==0:
                            sql_string=sql_string+element_from_rows_for_where[i]+" = "
                            sql_string=sql_string+'"'+'{'+str(1)+'['+str(i)+']'+'}'+'"'                            
            
            else:                 
                #print('не зашли ')
                pass;
            
            #print(sql_string)
            sql_string=sql_string.format(element_of_data_for_rows,element_from_variables_for_where)
            conwithbase = sqlite3.connect(self.adressmaker())
            cursor = conwithbase.cursor()
            #print(sql_string)
            cursor.execute(sql_string)
            conwithbase.commit()
            conwithbase.close()
        elif tipe_of_function=='else':
                sql_string=first_number
                conwithbase = sqlite3.connect(self.adressmaker())
                cursor = conwithbase.cursor()
                #print(sql_string)
                result = cursor.execute(sql_string)
                b=result.fetchall()
                #print(b)
                #if not b:
                #    pass;
                #else:
                return (b)
                conwithbase.close()
        elif tipe_of_function=='else_delete':
                sql_string=first_number
                conwithbase = sqlite3.connect(self.adressmaker())
                cursor = conwithbase.cursor()
                #print(sql_string)
                cursor.execute(sql_string)
                conwithbase.commit()
                cursor.close()
        #эти формы для запросов пока останутся так... в дальнейшем найдется куда они впишутся... основная их задача это проверка резулттатя полученного SQL запроса и подгонка его под необходимое .
        #.. возможно вормирование отдельного класса для этой задачи ... по аналогу класа  ALL_SQL_AT_ONE  либо же доработка текущего
   
#в класс ниже будут спихиваться все технические функции
##################################################
class Global_funck_of_Nothing(QWidget):
    def only_number(self,somethink):

        somethink=''.join(filter(str.isdigit,somethink))
        #somethink= re.sub('\D','',somethink)
        #print(type(somethink))

        return somethink
    def number_and_points(somethink):
        somethink=re.sub('[^\d\.]', '', somethink)
        #print(somethink)
        return somethink
    def if_its_empty(self,somethink):
        if type(somethink)==list :
            if somethink==None or somethink=='' :
                somethink.append('   ')
        else:
            if somethink==None or somethink=='' :
                somethink='   '
        return somethink
    def big_check_funk(self,event,my_data,my_type_data,element_way):
        data_for_return=None
        control_mass=['SHOW DATABASES',
'SHOW TABLES',
'SHOW COLUMNS FROM',
'SHOW CREATE TABLE ',
'SHOW INDEX FROM',
'SHOW GRANTS FOR',
'SHOW VARIABLES',
'SHOW',
'PROCESSLIST',
'SHOW STATUS',
'SHOW TABLE STATUS','RENAME TABLE','TRUNCATE TABLE','DROP TABLE','AND','OR','TESLIM']
        time_array=[]
        def small_func(my_data,my_type_data):
            count_point=0
            count_double_point=0
            time_array=[]
            if my_type_data=='date_time':
                for i in my_data:
                    if i=='.':
                        count_point=count_point+1
                    if i==':':
                        count_double_point=count_double_point+1
                time_array.append(count_point)
                time_array.append(count_double_point)
            elif my_type_data=='0.0=+' or my_type_data=='0.0+/-':
                for i in my_data:
                    if i=='.':
                        count_point=count_point+1
                time_array.append(count_point)
            return time_array
        if my_data=='' or my_data==None or (type(my_data)==list and my_data==[]):
            pass;
        else:
            if my_type_data=='text':
                if all([data.isalpha() or data==' 'for data in my_data]):
                    data_for_return=my_data
                    return data_for_return
                else:
                    element_way.setStyleSheet("QLineEdit {background-color: red;}")
                    ret = QMessageBox.question(self, 'MessageBox' , 'Yanlis yazmisiniz! Yazma {} tipilazim'.format(my_type_data) , QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                    if ret == QMessageBox.Yes:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                    else:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                       element_way.setText('')
            elif my_type_data=='date_time':
                time_array=small_func(my_data,my_type_data)
                if all([(data.isdigit() or data==' ' or data=='.' or data==':') and (time_array[0]<=2 and time_array[1]<=2) for data in my_data]):
                    data_for_return=my_data
                    return data_for_return
                else:
                    element_way.setStyleSheet("QLineEdit {background-color: red;}")
                    ret = QMessageBox.question(self, 'MessageBox' , 'Yanlis yazmisiniz! Yazma {} tipilazim'.format(my_type_data) , QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                    if ret == QMessageBox.Yes:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                    else:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                       element_way.setText('')
            elif my_type_data=='date':
                time_array=small_func(my_data,my_type_data)
                if all([(data.isdigit()  or data=='.') and (time_array[0]<=2) for data in my_data]):
                    data_for_return=my_data
                    return data_for_return
                else:
                    element_way.setStyleSheet("QLineEdit {background-color: red;}")
                    ret = QMessageBox.question(self, 'MessageBox' , 'Yanlis yazmisiniz! Yazma {} tipilazim'.format(my_type_data) , QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                    if ret == QMessageBox.Yes:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                    else:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                       element_way.setText('')
            elif my_type_data=='number_text':
                if all([data.isdigit() or data==' ' or data.isalpha() for data in my_data]):
                    data_for_return=my_data
                    return data_for_return
                else:
                    element_way.setStyleSheet("QLineEdit {background-color: red;}")
                    ret = QMessageBox.question(self, 'MessageBox' , 'Yanlis yazmisiniz! Yazma {} tipilazim'.format(my_type_data) , QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                    if ret == QMessageBox.Yes:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                    else:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                       element_way.setText('')
            #положительный целое число без пробелов и точек 
            elif my_type_data=='0=+':

                if all([data.isdigit() for data in my_data]):
                    data_for_return=my_data
                    return data_for_return
                else:
                    element_way.setStyleSheet("QLineEdit {background-color: red;}")
                    ret = QMessageBox.question(self, 'MessageBox' , 'Yanlis yazmisiniz! Yazma {} tipilazim'.format(my_type_data) , QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                    if ret == QMessageBox.Yes:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                    else:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                       element_way.setText('')
            #положительный десятичное без пробелов
            elif my_type_data=='0.0=+':
                time_array=small_func(my_data,my_type_data)
                if all([(data.isdigit()  or data=='.') and time_array[0]<=1 for data in my_data]):
                    #print(type(my_data))
                    data_for_return=float(my_data)
                    return data_for_return
                else:
                    element_way.setStyleSheet("QLineEdit {background-color: red;}")
                    ret = QMessageBox.question(self, 'MessageBox' , 'Yanlis yazmisiniz! Yazma {} tipilazim'.format(my_type_data) , QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                    if ret == QMessageBox.Yes:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                    else:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                       element_way.setText('')
            #десятичное число без пробелов и точек
            elif my_type_data=='0.0+/-':
                time_array=small_func(my_data,my_type_data)
                if all([(data.isdigit() or data=='-' or data=='.')and time_array[0]<=1 for data in my_data]):
                    data_for_return=my_data
                    return data_for_return
                else:
                    element_way.setStyleSheet("QLineEdit {background-color: red;}")
                    ret = QMessageBox.question(self, 'MessageBox' , 'Yanlis yazmisiniz! Yazma {} tipilazim'.format(my_type_data) , QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                    if ret == QMessageBox.Yes:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                    else:
                       element_way.setStyleSheet("QLineEdit {background-color: white;}")
                       element_way.setText('')
                
           

class Ui_update_and_insert(object):
    global size_value
    #При создании событий и их модернизации не забыть подправить функцию в setupUi
    #Создание всех элементов окна ввода/редактирования данных в таблицах value_size - размер ячеек для ввода(переменная для условия) ,name_of_table - название таблицы
    def setupUi(self, update_and_insert,value_size,name_of_table):
        global size_value
        size_value=value_size
        #Массив  с размерами окна для отображения в начале на 1-2 ячейки в самомо конце на 10 
        size_array=[[320,100],[480,100],[480,100],[640,200],[800,200]]
        if not update_and_insert.objectName():
            update_and_insert.setObjectName(u"update_and_insert")
        if value_size==1 or value_size==2:
            update_and_insert.resize(*size_array[0])
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(update_and_insert.sizePolicy().hasHeightForWidth())
            update_and_insert.setSizePolicy(sizePolicy)
            update_and_insert.setMinimumSize(QtCore.QSize(*size_array[0]))
            update_and_insert.setMaximumSize(QtCore.QSize(*size_array[0]))
            update_and_insert.setBaseSize(QtCore.QSize(*size_array[0]))
        elif value_size==3:
            update_and_insert.resize(*size_array[1])
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(update_and_insert.sizePolicy().hasHeightForWidth())
            update_and_insert.setSizePolicy(sizePolicy)
            update_and_insert.setMinimumSize(QtCore.QSize(*size_array[1]))
            update_and_insert.setMaximumSize(QtCore.QSize(*size_array[1]))
            update_and_insert.setBaseSize(QtCore.QSize(*size_array[1]))
        elif value_size==4:
            update_and_insert.resize(*size_array[2])
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(update_and_insert.sizePolicy().hasHeightForWidth())
            update_and_insert.setSizePolicy(sizePolicy)
            update_and_insert.setMinimumSize(QtCore.QSize(*size_array[2]))
            update_and_insert.setMaximumSize(QtCore.QSize(*size_array[2]))
            update_and_insert.setBaseSize(QtCore.QSize(*size_array[2]))
        elif value_size==7:
            update_and_insert.resize(*size_array[3])
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(update_and_insert.sizePolicy().hasHeightForWidth())
            update_and_insert.setSizePolicy(sizePolicy)
            update_and_insert.setMinimumSize(QtCore.QSize(*size_array[3]))
            update_and_insert.setMaximumSize(QtCore.QSize(*size_array[3]))
            update_and_insert.setBaseSize(QtCore.QSize(*size_array[3]))
        else:
            update_and_insert.resize(*size_array[4])
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(update_and_insert.sizePolicy().hasHeightForWidth())
            update_and_insert.setSizePolicy(sizePolicy)
            update_and_insert.setMinimumSize(QtCore.QSize(*size_array[4]))
            update_and_insert.setMaximumSize(QtCore.QSize(*size_array[4]))
            update_and_insert.setBaseSize(QtCore.QSize(*size_array[4]))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(update_and_insert)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        
        self.horizontalLayout_3 =QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        
    
        if value_size==1 :
            self.lab1 = QtWidgets.QLabel(update_and_insert)
            self.lab1.setObjectName(u"lab1")
            self.lab1.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab1)

            self.Ent1 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent1.setObjectName(u"Ent1")
            self.horizontalLayout_4.addWidget(self.Ent1)
        elif value_size==2 :
            self.lab1 = QtWidgets.QLabel(update_and_insert)
            self.lab1.setObjectName(u"lab1")
            self.lab1.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab1)
            
            self.lab2 = QtWidgets.QLabel(update_and_insert)
            self.lab2.setObjectName(u"lab2")
            self.lab2.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab2)
          
            self.Ent1 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent1.setObjectName(u"Ent1")
            self.horizontalLayout_4.addWidget(self.Ent1)

            self.Ent2 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent2.setObjectName(u"Ent2")
            self.horizontalLayout_4.addWidget(self.Ent2)
        elif value_size==3 :
            self.lab1 = QtWidgets.QLabel(update_and_insert)
            self.lab1.setObjectName(u"lab1")
            self.lab1.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab1)

            self.lab2 = QtWidgets.QLabel(update_and_insert)
            self.lab2.setObjectName(u"lab2")
            self.lab2.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab2)

            self.lab3 = QtWidgets.QLabel(update_and_insert)
            self.lab3.setObjectName(u"lab3")
            self.lab3.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab3)
          
            self.Ent1 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent1.setObjectName(u"Ent1")
            self.horizontalLayout_4.addWidget(self.Ent1)

            self.Ent2 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent2.setObjectName(u"Ent2")
            self.horizontalLayout_4.addWidget(self.Ent2)

            self.Ent3 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent3.setObjectName(u"Ent3")
            self.horizontalLayout_4.addWidget(self.Ent3)
        elif value_size==4 :
            self.lab1 = QtWidgets.QLabel(update_and_insert)
            self.lab1.setObjectName(u"lab1")
            self.lab1.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab1)

            self.lab2 = QtWidgets.QLabel(update_and_insert)
            self.lab2.setObjectName(u"lab2")
            self.lab2.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab2)

            self.lab3 = QtWidgets.QLabel(update_and_insert)
            self.lab3.setObjectName(u"lab3")
            self.lab3.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab3)

            self.lab4 = QtWidgets.QLabel(update_and_insert)
            self.lab4.setObjectName(u"lab4")
            self.lab4.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab4)

            self.Ent1 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent1.setObjectName(u"Ent1")
            self.horizontalLayout_4.addWidget(self.Ent1)

            self.Ent2 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent2.setObjectName(u"Ent2")
            self.horizontalLayout_4.addWidget(self.Ent2)

            self.Ent3 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent3.setObjectName(u"Ent3")
            self.horizontalLayout_4.addWidget(self.Ent3)

            list_of_perm=[1,2,3,4,5]

            self.perm_cb = QtWidgets.QComboBox(update_and_insert)
            self.perm_cb.setObjectName(u"perm_cb")
            for per in list_of_perm:
                self.perm_cb.addItem(str(per))
            self.perm_cb.setMinimumSize(QtCore.QSize(100, 20))
            self.perm_cb.setMaximumSize(QtCore.QSize(100, 20))
            MYSQL=Sql_Query()
            per_chek=int(MYSQL.ALL_SQL_AT_ONE('select',3,4,'')[0][0])
            if per_chek<=1:
                self.perm_cb.setDisabled(False)
            elif per_chek>1:
                self.perm_cb.setDisabled(True)
            #self.Ent4 = QtWidgets.QLineEdit(update_and_insert)
            #self.Ent4.setObjectName(u"Ent4")
            
            self.horizontalLayout_4.addWidget(self.perm_cb)
        elif value_size==7:
            self.lab1 = QtWidgets.QLabel(update_and_insert)
            self.lab1.setObjectName(u"lab1")
            self.lab1.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab1)

            self.lab2 = QtWidgets.QLabel(update_and_insert)
            self.lab2.setObjectName(u"lab2")
            self.lab2.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab2)

            self.lab3 = QtWidgets.QLabel(update_and_insert)
            self.lab3.setObjectName(u"lab3")
            self.lab3.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab3)

            self.lab4 = QtWidgets.QLabel(update_and_insert)
            self.lab4.setObjectName(u"lab4")
            self.lab4.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab4)

            self.lab5 = QtWidgets.QLabel(update_and_insert)
            self.lab5.setObjectName(u"lab5")
            self.lab5.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab5)

            self.lab6 = QtWidgets.QLabel(update_and_insert)
            self.lab6.setObjectName(u"lab6")
            self.lab6.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_3.addWidget(self.lab6)

            self.lab7 = QtWidgets.QLabel(update_and_insert)
            self.lab7.setObjectName(u"lab7")
            self.lab7.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_3.addWidget(self.lab7)

            self.Ent1 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent1.setObjectName(u"Ent1")
            self.horizontalLayout_4.addWidget(self.Ent1)

            self.Ent2 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent2.setObjectName(u"Ent2")
            self.horizontalLayout_4.addWidget(self.Ent2)

            self.Ent3 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent3.setObjectName(u"Ent3")
            self.horizontalLayout_4.addWidget(self.Ent3)

            self.Ent4 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent4.setObjectName(u"Ent4")
            self.horizontalLayout_4.addWidget(self.Ent4)

            self.Ent5 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent5.setObjectName(u"Ent5")
            self.horizontalLayout_4.addWidget(self.Ent5)

            self.Ent6 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent6.setObjectName(u"Ent6")
            self.horizontalLayout_2.addWidget(self.Ent6)

            self.Ent7 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent7.setObjectName(u"Ent7")
            self.horizontalLayout_2.addWidget(self.Ent7)
        else: 
            self.lab1 = QtWidgets.QLabel(update_and_insert)
            self.lab1.setObjectName(u"lab1")
            self.lab1.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab1)

            self.lab2 = QtWidgets.QLabel(update_and_insert)
            self.lab2.setObjectName(u"lab2")
            self.lab2.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab2)

            self.lab3 = QtWidgets.QLabel(update_and_insert)
            self.lab3.setObjectName(u"lab3")
            self.lab3.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab3)

            self.lab4 = QtWidgets.QLabel(update_and_insert)
            self.lab4.setObjectName(u"lab4")
            self.lab4.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab4)

            self.lab5 = QtWidgets.QLabel(update_and_insert)
            self.lab5.setObjectName(u"lab5")
            self.lab5.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_5.addWidget(self.lab5)

            self.lab6 = QtWidgets.QLabel(update_and_insert)
            self.lab6.setObjectName(u"lab6")
            self.lab6.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_3.addWidget(self.lab6)

            self.lab7 = QtWidgets.QLabel(update_and_insert)
            self.lab7.setObjectName(u"lab7")
            self.lab7.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_3.addWidget(self.lab7)

            self.lab8 = QtWidgets.QLabel(update_and_insert)
            self.lab8.setObjectName(u"lab8")
            self.lab8.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_3.addWidget(self.lab8)

            self.lab9 = QtWidgets.QLabel(update_and_insert)
            self.lab9.setObjectName(u"lab9")
            self.lab9.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_3.addWidget(self.lab9)

            self.lab10 = QtWidgets.QLabel(update_and_insert)
            self.lab10.setObjectName(u"lab10")
            self.lab10.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout_3.addWidget(self.lab10)

            self.Ent1 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent1.setObjectName(u"Ent1")
            self.horizontalLayout_4.addWidget(self.Ent1)

            self.Ent2 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent2.setObjectName(u"Ent2")
            self.horizontalLayout_4.addWidget(self.Ent2)

            self.Ent3 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent3.setObjectName(u"Ent3")
            self.horizontalLayout_4.addWidget(self.Ent3)

            self.Ent4 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent4.setObjectName(u"Ent4")
            self.horizontalLayout_4.addWidget(self.Ent4)

            self.Ent5 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent5.setObjectName(u"Ent5")
            self.horizontalLayout_4.addWidget(self.Ent5)

            self.Ent6 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent6.setObjectName(u"Ent6")
            self.horizontalLayout_2.addWidget(self.Ent6)

            self.Ent7 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent7.setObjectName(u"Ent7")
            self.horizontalLayout_2.addWidget(self.Ent7)

            self.Ent8 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent8.setObjectName(u"Ent8")
            self.horizontalLayout_2.addWidget(self.Ent8)

            self.Ent9 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent9.setObjectName(u"Ent9")
            self.horizontalLayout_2.addWidget(self.Ent9)

            self.Ent10 = QtWidgets.QLineEdit(update_and_insert)
            self.Ent10.setObjectName(u"Ent10")
            self.horizontalLayout_2.addWidget(self.Ent10)

        self.ok_but = QtWidgets.QPushButton(update_and_insert)
        self.ok_but.setObjectName(u"ok_but")
        self.horizontalLayout.addWidget(self.ok_but)

        self.cancel_but = QtWidgets.QPushButton(update_and_insert)
        self.cancel_but.setObjectName(u"cancel_but")
        self.horizontalLayout.addWidget(self.cancel_but)

        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addLayout(self.verticalLayout)      
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(update_and_insert,value_size,name_of_table)
        self.my_events(update_and_insert,name_of_table)
        #if ifelem==0:
        #    self.update_funck(update_and_insert,value_size,name_of_table)
        #elif ifelem==1:
        #    self.insert_funck()
        QtCore.QMetaObject.connectSlotsByName(update_and_insert)
    #Создание названий для элементов value_size - размер ячеек для ввода(переменная для условия) ,name_of_table - название таблицы
    def retranslateUi(self, update_and_insert,value_size,name_of_table):
        #update_and_insert.setWindowTitle(QCoreApplication.translate("update_and_insert", u"update_and_insert", None))
        _translate = QtCore.QCoreApplication.translate
        ClasS_part=Sql_Query()
        if type(name_of_table)==list:
            if value_size==1:
                if name_of_table[1]=='MainSql':
                    time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table[1])
                   # print('time array',time_aray)
                    self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                else:
                    time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table[1])
                   # print('time array',time_aray)
                    self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[1]), None))

            elif value_size==2:
                if name_of_table=='MainSql':
                    time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table[1])
                    self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                    self.lab2.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                else:
                    time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table[1])
                    self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                    self.lab2.setText(_translate("update_and_insert", u"{}".format(time_aray[1]), None))
            elif value_size==3:
                time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table[1])
                self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                self.lab2.setText(_translate("update_and_insert", u"{}".format(time_aray[1]), None))
                self.lab3.setText(_translate("update_and_insert", u"{}".format(time_aray[2]), None))
            elif value_size==4:
                time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table[1])
                self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                self.lab2.setText(_translate("update_and_insert", u"{}".format(time_aray[1]), None))
                self.lab3.setText(_translate("update_and_insert", u"{}".format(time_aray[2]), None))
                self.lab4.setText(_translate("update_and_insert", u"{}".format(time_aray[3]), None))
            elif value_size==7:
                time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table[1])
                self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                self.lab2.setText(_translate("update_and_insert", u"{}".format(time_aray[1]), None))
                self.lab3.setText(_translate("update_and_insert", u"{}".format(time_aray[2]), None))
                self.lab4.setText(_translate("update_and_insert", u"{}".format(time_aray[3]), None))
                self.lab5.setText(_translate("update_and_insert", u"{}".format(time_aray[4]), None))
                self.lab6.setText(_translate("update_and_insert", u"{}".format(time_aray[5]), None))
                self.lab7.setText(_translate("update_and_insert", u"{}".format(time_aray[6]), None))            
            else:
                time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table[1])
                self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                self.lab2.setText(_translate("update_and_insert", u"{}".format(time_aray[1]), None))
                self.lab3.setText(_translate("update_and_insert", u"{}".format(time_aray[2]), None))
                self.lab4.setText(_translate("update_and_insert", u"{}".format(time_aray[3]), None))
                self.lab5.setText(_translate("update_and_insert", u"{}".format(time_aray[4]), None))
                self.lab6.setText(_translate("update_and_insert", u"{}".format(time_aray[5]), None))
                self.lab7.setText(_translate("update_and_insert", u"{}".format(time_aray[6]), None))
                self.lab8.setText(_translate("update_and_insert", u"{}".format(time_aray[7]), None))
                self.lab9.setText(_translate("update_and_insert", u"{}".format(time_aray[8]), None))
                self.lab10.setText(_translate("update_and_insert", u"{}".format(time_aray[9]), None))
        else:
            if value_size==1:
                if name_of_table[1]=='MainSql':
                    time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table)
                   # print('time array',time_aray)
                    self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                else:
                    time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table)
                   # print('time array',time_aray)
                    self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[1]), None))

            elif value_size==2:
                if name_of_table=='MainSql':
                    time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table)
                    self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                    self.lab2.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                else:
                    time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table)
                    self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                    self.lab2.setText(_translate("update_and_insert", u"{}".format(time_aray[1]), None))
            elif value_size==3:
                time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table)
                self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                self.lab2.setText(_translate("update_and_insert", u"{}".format(time_aray[1]), None))
                self.lab3.setText(_translate("update_and_insert", u"{}".format(time_aray[2]), None))
            elif value_size==4:
                time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table)
                self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                self.lab2.setText(_translate("update_and_insert", u"{}".format(time_aray[1]), None))
                self.lab3.setText(_translate("update_and_insert", u"{}".format(time_aray[2]), None))
                self.lab4.setText(_translate("update_and_insert", u"{}".format(time_aray[3]), None))
            elif value_size==7:
                time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table)
                self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                self.lab2.setText(_translate("update_and_insert", u"{}".format(time_aray[1]), None))
                self.lab3.setText(_translate("update_and_insert", u"{}".format(time_aray[2]), None))
                self.lab4.setText(_translate("update_and_insert", u"{}".format(time_aray[3]), None))
                self.lab5.setText(_translate("update_and_insert", u"{}".format(time_aray[4]), None))
                self.lab6.setText(_translate("update_and_insert", u"{}".format(time_aray[5]), None))
                self.lab7.setText(_translate("update_and_insert", u"{}".format(time_aray[6]), None))            
            else:
                time_aray,count_of_rows=Ui_Hotel_Project.write_to_TB_W(self,ClasS_part,name_of_table)
                self.lab1.setText(_translate("update_and_insert", u"{}".format(time_aray[0]), None))
                self.lab2.setText(_translate("update_and_insert", u"{}".format(time_aray[1]), None))
                self.lab3.setText(_translate("update_and_insert", u"{}".format(time_aray[2]), None))
                self.lab4.setText(_translate("update_and_insert", u"{}".format(time_aray[3]), None))
                self.lab5.setText(_translate("update_and_insert", u"{}".format(time_aray[4]), None))
                self.lab6.setText(_translate("update_and_insert", u"{}".format(time_aray[5]), None))
                self.lab7.setText(_translate("update_and_insert", u"{}".format(time_aray[6]), None))
                self.lab8.setText(_translate("update_and_insert", u"{}".format(time_aray[7]), None))
                self.lab9.setText(_translate("update_and_insert", u"{}".format(time_aray[8]), None))
                self.lab10.setText(_translate("update_and_insert", u"{}".format(time_aray[9]), None))

        self.ok_but.setText(_translate("update_and_insert", u"OK", None))
        self.cancel_but.setText(_translate("update_and_insert", u"CANCEL", None))
    #Функция с событиями по нажатию на элементы формы 
    def my_events(self,update_and_insert,name_of_table):
        #print(name_of_table)
        global size_value
        value_size=size_value
        ControlPart= Global_funck_of_Nothing()
        MYSQ=Sql_Query()
        if type(name_of_table)==list:
                if name_of_table[1]=='nakitt' :
                    self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0=+',self.Ent1))
                elif name_of_table[1]=='MainSql':
                    pass;
                   #Сложная проверка на правильный скл запросс
                    #self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0=+',self.Ent1))
                #----------------------------------------Группа по две ячейки -----------------------------------------------------------------
                elif name_of_table[1]=='hamamwifi' :
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0=+',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'0=+',self.Ent2))
                elif name_of_table[1]=='giderler' :
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'text',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'0.0+/-',self.Ent2))
                elif name_of_table[1]=='admintablo' :
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0.0+/-',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'0.0+/-',self.Ent2))
                   #Сложная проверка на адресс  возможно в дальнейшем удалить или переделать ячейку 
                   #self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'0.0+/-',self.Ent2))
                elif name_of_table[1]=='SQLELECTRA' :
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'text',self.Ent2))
                   #self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0.0+/-',self.Ent1))
                   #Сложная проверка на адресс  возможно в дальнейшем удалить или переделать ячейку 
                   #self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'0.0+/-',self.Ent2))
                #---------------------------------------------------Группа на три ячейки----------------------------------------------------
                elif name_of_table[1]=='doviz':
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'text',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'0=+',self.Ent2))
                   self.Ent3.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent3.text(),'0.=+',self.Ent2))
                elif name_of_table[1]=='havludegisim':
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0=+',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'0=+',self.Ent2))
                   self.Ent3.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent3.text(),'0=+',self.Ent2))
                #-----------------------------------------------Группа четырех ----------------------------------------------------------
                elif name_of_table[1]=='teslim':
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'number_text',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'number_text',self.Ent2))
                   self.Ent3.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent3.text(),'number_text',self.Ent3))
                   #self.Ent4.setInputMask('0')
                   #self.Ent4.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent4.text(),'0=+',self.Ent1))
           
                #-----------------------------------------------Группа семи----------------------------------------------------------
                elif name_of_table[1]=='havlu':
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0=+',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'text',self.Ent2))
                   self.Ent3.setInputMask("00.00.0000")
                   self.Ent3.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent3.text(),'data',self.Ent3))
                   self.Ent4.setInputMask("00.00.0000")
                   self.Ent4.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent4.text(),'data',self.Ent4))
                   self.Ent5.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent5.text(),'0=+',self.Ent5))
                   self.Ent6.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent6.text(),'text',self.Ent6))
                   self.Ent7.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent7.text(),'text',self.Ent7))
           
                #-----------------------------------------------Группа десяти----------------------------------------------------------
                elif name_of_table[1]=='doublekey' or name_of_table[1]=='fitneskey':
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0=+',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'text',self.Ent2))
                   self.Ent3.setInputMask("00.00.0000")
                   self.Ent3.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent3.text(),'data',self.Ent3))
                   self.Ent4.setInputMask("00.00.0000")
                   self.Ent4.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent4.text(),'data',self.Ent4))
                   self.Ent5.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent5.text(),'0=+',self.Ent5))
                   self.Ent6.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent6.text(),'0=+',self.Ent6))
                   self.Ent7.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent7.text(),'0=+',self.Ent7))
                   self.Ent8.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent8.text(),'number_text',self.Ent8))
                   self.Ent9.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent9.text(),'text',self.Ent9))
                   self.Ent10.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent10.text(),'text',self.Ent10))
        else:
                if name_of_table=='nakitt' :
                    self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0=+',self.Ent1))
                elif name_of_table=='MainSql':
                    pass;
                   #Сложная проверка на правильный скл запросс
                    #self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0=+',self.Ent1))
                #----------------------------------------Группа по две ячейки -----------------------------------------------------------------
                elif name_of_table=='hamamwifi' :
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0=+',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'0=+',self.Ent2))
                elif name_of_table=='giderler' :
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'text',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'0.0+/-',self.Ent2))
                elif name_of_table=='admintablo' :
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0.0+/-',self.Ent1))
                   #Сложная проверка на адресс  возможно в дальнейшем удалить или переделать ячейку 
                   #self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'0.0+/-',self.Ent2))
                elif name_of_table=='SQLELECTRA' :
                    pass;
                   #self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0.0+/-',self.Ent1))
                   #Сложная проверка на адресс  возможно в дальнейшем удалить или переделать ячейку 
                   #self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'0.0+/-',self.Ent2))
                #---------------------------------------------------Группа на три ячейки----------------------------------------------------
                elif name_of_table=='doviz':
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'text',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'0=+',self.Ent2))
                   self.Ent3.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent3.text(),'0.=+',self.Ent2))
                elif name_of_table=='havludegisim':
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0=+',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'0=+',self.Ent2))
                   self.Ent3.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent3.text(),'0=+',self.Ent2))
                #-----------------------------------------------Группа четырех ----------------------------------------------------------
                elif name_of_table=='teslim':
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'number_text',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'number_text',self.Ent2))
                   self.Ent3.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent3.text(),'number_text',self.Ent3))
                   #self.Ent4.setInputMask('0')
                   #self.Ent4.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent4.text(),'0=+',self.Ent1))
           
                #-----------------------------------------------Группа семи----------------------------------------------------------
                elif name_of_table=='havlu':
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0=+',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'text',self.Ent2))
                   self.Ent3.setInputMask("00.00.0000")
                   self.Ent3.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent3.text(),'data',self.Ent3))
                   self.Ent4.setInputMask("00.00.0000")
                   self.Ent4.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent4.text(),'data',self.Ent4))
                   self.Ent5.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent5.text(),'0=+',self.Ent5))
                   self.Ent6.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent6.text(),'text',self.Ent6))
                   self.Ent7.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent7.text(),'text',self.Ent7))
           
                #-----------------------------------------------Группа десяти----------------------------------------------------------
                elif name_of_table=='doublekey' or name_of_table=='fitneskey':
                   self.Ent1.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent1.text(),'0=+',self.Ent1))
                   self.Ent2.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent2.text(),'text',self.Ent2))
                   self.Ent3.setInputMask("00.00.0000")
                   self.Ent3.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent3.text(),'data',self.Ent3))
                   self.Ent4.setInputMask("00.00.0000")
                   self.Ent4.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent4.text(),'data',self.Ent4))
                   self.Ent5.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent5.text(),'0=+',self.Ent5))
                   self.Ent6.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent6.text(),'0=+',self.Ent6))
                   self.Ent7.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent7.text(),'0=+',self.Ent7))
                   self.Ent8.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent8.text(),'number_text',self.Ent8))
                   self.Ent9.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent9.text(),'text',self.Ent9))
                   self.Ent10.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,self.Ent10.text(),'text',self.Ent10))
     #litle global fucnk ubpdate fuck отвечает за работу контекстного меню  
    def litle_global_funck(self,event,winpart,ifelem,value_size,name_of_table,som):
        if ifelem==0:
           # print('данные в распределяющей функциии',name_of_table[0].selectedItems()==[])
           # print('тип данных',type(name_of_table[0].selectedItems()==[]))
            #print(len(name_of_table[0].selectedItems()))
            if isinstance(None,type(name_of_table[0].selectedItems()))and len(name_of_table[0].selectedItems())==0:
                #print('Зашел по пустой строке в маленькой глобал функ ')
                #isinstance(None,type(name_of_table[0].selectedItems())):
                pass;
            else:
                self.update_funck(winpart,value_size,name_of_table,som)
        elif ifelem==1:
            self.insert_funck(winpart,value_size,name_of_table,som)
        elif ifelem==2:
            self.delete_funck(winpart,value_size,name_of_table,som)
        elif ifelem==3:
            self.delete_stil_one_data(winpart,value_size,name_of_table,som)
#----функции контекстного меню и двойного щелчка--  -------------------------------------------------------------------------------------------------------
    def start_update_at_bd(self,event,winpart,name_of_table,dict_with_number_of_rows,temp_dict,value_size,som):
        global Hotel_parthT
        Hotel_parth=Hotel_parthT
        MYSQ=Sql_Query()
        new_dict=[]
         #----для записи в nesildi--------------------------------------
        sp_dict={
            15:[2,3,4,5,6,7],
            14:[2,3,4,5,8,9],
            13:[2,3,4,5,11,12,13],
            12:[2,3,4,5,21,22,23,24,25,26,27],
            11:[2,3,4,5,11,12],
            10:[2,3,4,5,16,22],
            9:[2,3,4,5,10,11,12,17,21,22,23,24,26,27],
            8:[2,3,4,5,18,19,20],
            7:[2,3,4,5,10,11,12,17,21,22,23,24,26,27],
            6:[2,3,4,5,14,15]
            }
        spec_name_dict={
            15:'Nakit para',
            14:'Avans ve Nakit',
            13:'Havlu Degisik',
            12:'Sahil Havlu',
            11:'Hamam WiFi',
            10:'Giderler',
            9:'Fitnes',
            8:'Doviz',
            7:'Yedek Anahtar',
            6:'Demir Para'
            }
        datanowT=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        name_from_now=MYSQ.ALL_SQL_AT_ONE('select',3,2,'')
        neyapti=['Sildi','Değişmiş','Yazdı']
        #----------------------------------------------------------
        #print('look',dict_with_number_of_rows)
        if value_size==1 :
                if name_of_table[1]=='MainSql':
                    new_dict.insert(0,winpart.Ent1.text())
                elif name_of_table[1]=='nakitt':
                    new_dict.insert(0,temp_dict[0])
                    new_dict.insert(1,winpart.Ent1.text())
                    
                else:
                    new_dict.insert(0,winpart.Ent1.text())
        elif value_size==2 :
                new_dict.insert(0,winpart.Ent1.text())
                new_dict.insert(1,winpart.Ent2.text())
        elif value_size==3:
                new_dict.insert(0,winpart.Ent1.text())
                new_dict.insert(1,winpart.Ent2.text())
                new_dict.insert(2,winpart.Ent3.text())
        elif value_size==4 :
                new_dict.insert(0,winpart.Ent1.text())
                new_dict.insert(1,winpart.Ent2.text())
                new_dict.insert(2,winpart.Ent3.text())
                new_dict.insert(3,winpart.perm_cb.currentText())
        elif value_size==7:
                new_dict.insert(0,winpart.Ent1.text())
                new_dict.insert(1,winpart.Ent2.text())
                new_dict.insert(2,winpart.Ent3.text())
                new_dict.insert(3,winpart.Ent4.text())
                new_dict.insert(4,winpart.Ent5.text())
                new_dict.insert(5,winpart.Ent6.text())
                new_dict.insert(6,winpart.Ent7.text())
        else: 
                new_dict.insert(0,winpart.Ent1.text())
                new_dict.insert(1,winpart.Ent2.text())
                new_dict.insert(2,winpart.Ent3.text())
                new_dict.insert(3,winpart.Ent4.text())
                new_dict.insert(4,winpart.Ent5.text())
                new_dict.insert(5,winpart.Ent6.text())
                new_dict.insert(6,winpart.Ent7.text())
                new_dict.insert(7,winpart.Ent8.text())
                new_dict.insert(8,winpart.Ent9.text())
                new_dict.insert(9,winpart.Ent10.text())
        
        if name_of_table[2]==10  and new_dict[0]=='':
            new_dict[0]=0
        elif  name_of_table[2]==15  and new_dict[1]=='':
            
            new_dict[1]=0
        elif (name_of_table[2]==8 ) and ((new_dict[1]=='' and new_dict[2]=='')or(new_dict[1]=='' and new_dict[2]!='')or(new_dict[1]!='' and new_dict[2]=='')):
            if new_dict[1]=='' and  new_dict[2]=='':
                new_dict[1]=0
                new_dict[2]=0
            elif new_dict[1]=='':
                new_dict[1]=0
            elif new_dict[2]=='':
                new_dict[2]=0

        elif (name_of_table[2]==11) and((new_dict[0]=='' and new_dict[1]=='')or(new_dict[0]=='' and new_dict[1]!='')or(new_dict[0]!='' and new_dict[1]=='')):
            if new_dict[0]=='' and  new_dict[1]=='':
                new_dict[0]=0
                new_dict[1]=0
            elif new_dict[0]=='':
                new_dict[0]=0
            elif new_dict[1]=='':
                new_dict[1]=0

        elif (name_of_table[2]==12) and((new_dict[0]=='' and new_dict[4]=='')or(new_dict[0]=='' and new_dict[4]!='')or(new_dict[0]!='' and new_dict[4]=='')):
            if new_dict[0]=='' and  new_dict[4]=='':
                new_dict[0]=0
                new_dict[4]=0
            elif new_dict[0]=='':
                new_dict[0]=0
            elif new_dict[4]=='':
                new_dict[4]=0


        elif (name_of_table[2]==13)and((new_dict[0]=='' and new_dict[1]==''and new_dict[2]=='')or
                                            (new_dict[0]=='' and new_dict[1]==''and new_dict[2]!='')or
                                             (new_dict[0]=='' and new_dict[1]!='' and new_dict[2]=='')or
                                             (new_dict[0]=='' and new_dict[1]!='' and new_dict[2]!='')or
                                             (new_dict[0]!='' and new_dict[2]=='' and new_dict[1]=='')or
                                             (new_dict[0]!='' and new_dict[1]=='' and new_dict[2]!='')or
                                             (new_dict[0]!='' and new_dict[1]!='' and new_dict[2]=='')
                                             ):
            if new_dict[0]=='' and new_dict[1]==''and new_dict[2]=='':
                    new_dict[0]=0
                    new_dict[1]=0
                    new_dict[2]=0
            elif new_dict[0]=='' and new_dict[1]==''and new_dict[2]!='':
                    new_dict[0]=0
                    new_dict[1]=0
            elif new_dict[0]=='' and new_dict[1]!='' and new_dict[2]=='':
                    new_dict[0]=0
                    new_dict[2]=0
            elif new_dict[0]=='' and new_dict[1]!='' and new_dict[2]!='':
                new_dict[0]=0
            elif new_dict[0]!='' and new_dict[1]=='' and new_dict[2]=='':
                    new_dict[1]=0
                    new_dict[2]=0
            elif new_dict[0]!='' and new_dict[1]=='' and new_dict[2]!='':
                    new_dict[1]=0
            elif new_dict[0]!='' and new_dict[1]!='' and new_dict[2]=='':
                    new_dict[2]=0
        elif(name_of_table[2]==7 or name_of_table[2]==9 )and ((new_dict[4]=='' and new_dict[5]=='' and new_dict[6]=='')or
                                                              
                                                              (new_dict[4]=='' and new_dict[5]=='' and new_dict[6]!='')or
                                                              (new_dict[4]=='' and new_dict[5]!='' and new_dict[6]=='')or
                                                              (new_dict[4]=='' and new_dict[5]!='' and new_dict[6]!='')or
                                                              
                                                              (new_dict[4]!='' and new_dict[5]=='' and new_dict[6]=='')or
                                                              (new_dict[4]!='' and new_dict[5]=='' and new_dict[6]!='')or
                                                              (new_dict[4]!='' and new_dict[5]!='' and new_dict[6]=='')):

            if  new_dict[4]=='' and new_dict[5]=='' and new_dict[6]=='':
                new_dict[4]=0
                new_dict[5]=0
                new_dict[6]=0
            elif new_dict[4]=='' and new_dict[5]=='' and new_dict[6]!='':
                new_dict[4]=0
                new_dict[5]=0
            elif new_dict[4]=='' and new_dict[5]!='' and new_dict[6]=='':
                new_dict[4]=0
                new_dict[6]=0
            elif new_dict[4]=='' and new_dict[5]!='' and new_dict[6]!='':
                new_dict[4]=0
            elif new_dict[4]!='' and new_dict[5]=='' and new_dict[6]=='':
                new_dict[5]=0
                new_dict[6]=0
            elif  new_dict[4]!='' and new_dict[5]=='' and new_dict[6]!='':
                new_dict[5]=0
            elif  new_dict[4]!='' and new_dict[5]!='' and new_dict[6]=='':
                new_dict[6]=0
        
        MYSQ.ALL_SQL_AT_ONE('update',name_of_table[2],[dict_with_number_of_rows,dict_with_number_of_rows],[new_dict,temp_dict])
        if name_of_table[1]=='admintablo':
           pass;
        elif name_of_table[1]=='SQLELECTRA':
            pass;
        elif name_of_table[1]=='MainSql':
            pass;
        else:
            try:
                MYSQ.ALL_SQL_AT_ONE('insert',16,sp_dict[name_of_table[2]],[datanowT,name_from_now[0][0],spec_name_dict[name_of_table[2]],neyapti[1],*temp_dict])
            except KeyError:
                pass;
        Ui_Hotel_Project().show_data(Hotel_parth,MYSQ,['refresh'])
        som.close() 
    def start_insert_at_bd(self,event,winpart,name_of_table,value_size,som):
        global Hotel_parthT
        Hotel_parth=Hotel_parthT
        MYSQ=Sql_Query()
        new_dict=[]
        dict_with_number_of_rows={
            10:[2,3],
            15:[2,3],
            8:[2,3,4],
            11:[2,3],
            13:[2,3,4],
            7:[2,3,4,5,6,7,8,9,10,11],
            9:[2,3,4,5,6,7,8,9,10,11],
            12:[2,3,4,5,6,7,8],
            18:[2,3,4,5],
            2:[2],
            4:[2,3],
            5:[2,3]}
         #----для записи в nesildi--------------------------------------
        sp_dict={
            15:[2,3,4,5,6,7],
            14:[2,3,4,5,8,9],
            13:[2,3,4,5,11,12,13],
            12:[2,3,4,5,21,22,23,24,25,26,27],
            11:[2,3,4,5,11,12],
            10:[2,3,4,5,16,22],
            9:[2,3,4,5,10,11,12,17,21,22,23,24,26,27],
            8:[2,3,4,5,18,19,20],
            7:[2,3,4,5,10,11,12,17,21,22,23,24,26,27],
            6:[2,3,4,5,14,15]
            }
        spec_name_dict={
            15:'Nakit para',
            14:'Avans ve Nakit',
            13:'Havlu Degisik',
            12:'Sahil Havlu',
            11:'Hamam WiFi',
            10:'Giderler',
            9:'Fitnes',
            8:'Doviz',
            7:'Yedek Anahtar',
            6:'Demir Para'
            }
        datanowT=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        name_from_now=MYSQ.ALL_SQL_AT_ONE('select',3,2,'')
        neyapti=['Sildi','Değişmiş','Yazdı']
        #----------------------------------------------------------
        if value_size==1 :
                if name_of_table[1]=='MainSql':
                    new_dict.insert(0,winpart.Ent1.text())
                else:
                    new_dict.insert(0,winpart.Ent1.text())
        elif value_size==2 :
                new_dict.insert(0,winpart.Ent1.text())
                new_dict.insert(1,winpart.Ent2.text())
        elif value_size==3:
                new_dict.insert(0,winpart.Ent1.text())
                new_dict.insert(1,winpart.Ent2.text())
                new_dict.insert(2,winpart.Ent3.text())
        elif value_size==4 :
                new_dict.insert(0,winpart.Ent1.text())
                new_dict.insert(1,winpart.Ent2.text())
                new_dict.insert(2,winpart.Ent3.text())
                new_dict.insert(3,winpart.perm_cb.currentText())
        elif value_size==7:
                new_dict.insert(0,winpart.Ent1.text())
                new_dict.insert(1,winpart.Ent2.text())
                new_dict.insert(2,winpart.Ent3.text())
                new_dict.insert(3,winpart.Ent4.text())
                new_dict.insert(4,winpart.Ent5.text())
                new_dict.insert(5,winpart.Ent6.text())
                new_dict.insert(6,winpart.Ent7.text())
        else: 
                #print('was here')
                new_dict.insert(0,winpart.Ent1.text())
                new_dict.insert(1,winpart.Ent2.text())
                new_dict.insert(2,winpart.Ent3.text())
                new_dict.insert(3,winpart.Ent4.text())
                new_dict.insert(4,winpart.Ent5.text())
                new_dict.insert(5,winpart.Ent6.text())
                new_dict.insert(6,winpart.Ent7.text())
                new_dict.insert(7,winpart.Ent8.text())
                new_dict.insert(8,winpart.Ent9.text())
                new_dict.insert(9,winpart.Ent10.text())
        
        if (name_of_table[2]==10 or name_of_table[2]==15 ) and new_dict[1]=='':
            new_dict[1]=0
        elif (name_of_table[2]==8 ) and ((new_dict[1]=='' and new_dict[2]=='')or(new_dict[1]=='' and new_dict[2]!='')or(new_dict[1]!='' and new_dict[2]=='')):
            if new_dict[1]=='' and  new_dict[2]=='':
                new_dict[1]=0
                new_dict[2]=0
            elif new_dict[1]=='':
                new_dict[1]=0
            elif new_dict[2]=='':
                new_dict[2]=0

        elif (name_of_table[2]==11) and((new_dict[0]=='' and new_dict[1]=='')or(new_dict[0]=='' and new_dict[1]!='')or(new_dict[0]!='' and new_dict[1]=='')):
            if new_dict[0]=='' and  new_dict[1]=='':
                new_dict[0]=0
                new_dict[1]=0
            elif new_dict[0]=='':
                new_dict[0]=0
            elif new_dict[1]=='':
                new_dict[1]=0

        elif (name_of_table[2]==12) and((new_dict[0]=='' and new_dict[4]=='')or(new_dict[0]=='' and new_dict[4]!='')or(new_dict[0]!='' and new_dict[4]=='')):
            if new_dict[0]=='' and  new_dict[4]=='':
                new_dict[0]=0
                new_dict[4]=0
            elif new_dict[0]=='':
                new_dict[0]=0
            elif new_dict[4]=='':
                new_dict[4]=0


        elif (name_of_table[2]==13)and((new_dict[0]=='' and new_dict[1]==''and new_dict[2]=='')or
                                            (new_dict[0]=='' and new_dict[1]==''and new_dict[2]!='')or
                                             (new_dict[0]=='' and new_dict[1]!='' and new_dict[2]=='')or
                                             (new_dict[0]=='' and new_dict[1]!='' and new_dict[2]!='')or
                                             (new_dict[0]!='' and new_dict[2]=='' and new_dict[1]=='')or
                                             (new_dict[0]!='' and new_dict[1]=='' and new_dict[2]!='')or
                                             (new_dict[0]!='' and new_dict[1]!='' and new_dict[2]=='')
                                             ):
            if new_dict[0]=='' and new_dict[1]==''and new_dict[2]=='':
                    new_dict[0]=0
                    new_dict[1]=0
                    new_dict[2]=0
            elif new_dict[0]=='' and new_dict[1]==''and new_dict[2]!='':
                    new_dict[0]=0
                    new_dict[1]=0
            elif new_dict[0]=='' and new_dict[1]!='' and new_dict[2]=='':
                    new_dict[0]=0
                    new_dict[2]=0
            elif new_dict[0]=='' and new_dict[1]!='' and new_dict[2]!='':
                new_dict[0]=0
            elif new_dict[0]!='' and new_dict[1]=='' and new_dict[2]=='':
                    new_dict[1]=0
                    new_dict[2]=0
            elif new_dict[0]!='' and new_dict[1]=='' and new_dict[2]!='':
                    new_dict[1]=0
            elif new_dict[0]!='' and new_dict[1]!='' and new_dict[2]=='':
                    new_dict[2]=0
        elif(name_of_table[2]==7 or name_of_table[2]==9 )and ((new_dict[4]=='' and new_dict[5]=='' and new_dict[6]=='')or
                                                              
                                                              (new_dict[4]=='' and new_dict[5]=='' and new_dict[6]!='')or
                                                              (new_dict[4]=='' and new_dict[5]!='' and new_dict[6]=='')or
                                                              (new_dict[4]=='' and new_dict[5]!='' and new_dict[6]!='')or
                                                              
                                                              (new_dict[4]!='' and new_dict[5]=='' and new_dict[6]=='')or
                                                              (new_dict[4]!='' and new_dict[5]=='' and new_dict[6]!='')or
                                                              (new_dict[4]!='' and new_dict[5]!='' and new_dict[6]=='')):

            if  new_dict[4]=='' and new_dict[5]=='' and new_dict[6]=='':
                new_dict[4]=0
                new_dict[5]=0
                new_dict[6]=0
            elif new_dict[4]=='' and new_dict[5]=='' and new_dict[6]!='':
                new_dict[4]=0
                new_dict[5]=0
            elif new_dict[4]=='' and new_dict[5]!='' and new_dict[6]=='':
                new_dict[4]=0
                new_dict[6]=0
            elif new_dict[4]=='' and new_dict[5]!='' and new_dict[6]!='':
                new_dict[4]=0
            elif new_dict[4]!='' and new_dict[5]=='' and new_dict[6]=='':
                new_dict[5]=0
                new_dict[6]=0
            elif  new_dict[4]!='' and new_dict[5]=='' and new_dict[6]!='':
                new_dict[5]=0
            elif  new_dict[4]!='' and new_dict[5]!='' and new_dict[6]=='':
                new_dict[6]=0
        MYSQ.ALL_SQL_AT_ONE('insert',name_of_table[2],dict_with_number_of_rows[name_of_table[2]],new_dict)
        if name_of_table[1]=='admintablo':
           pass;
        elif name_of_table[1]=='SQLELECTRA':
            pass;
        elif name_of_table[1]=='MainSql':
            pass;
        else:
            MYSQ.ALL_SQL_AT_ONE('insert',16,sp_dict[name_of_table[2]],[datanowT,name_from_now[0][0],spec_name_dict[name_of_table[2]],neyapti[2],*new_dict])
        Ui_Hotel_Project().show_data(Hotel_parth,MYSQ,['refresh'])
        som.close() 
    def start_delete_at_bd(self,name_of_table,dict_with_number_of_rows,temp_dict,som):
        global Hotel_parthT
        Hotel_parth=Hotel_parthT
        MYSQ=Sql_Query()
        count_row=int(Global_funck_of_Nothing().only_number(str(MYSQ.ALL_SQL_AT_ONE('else',6,'Select count(*) from {}'.format(name_of_table[1]),''))))
        #----для записи в nesildi--------------------------------------
        sp_dict={
            15:[2,3,4,5,6,7],
            14:[2,3,4,5,8,9],
            13:[2,3,4,5,11,12,13],
            12:[2,3,4,5,21,22,23,24,25,26,27],
            11:[2,3,4,5,11,12],
            10:[2,3,4,5,16,22],
            9:[2,3,4,5,10,11,12,17,21,22,23,24,26,27],
            8:[2,3,4,5,18,19,20],
            7:[2,3,4,5,10,11,12,17,21,22,23,24,26,27],
            6:[2,3,4,5,14,15]
            }
        spec_name_dict={
            15:'Nakit para',
            14:'Avans ve Nakit',
            13:'Havlu Degisik',
            12:'Sahil Havlu',
            11:'Hamam WiFi',
            10:'Giderler',
            9:'Fitnes',
            8:'Doviz',
            7:'Yedek Anahtar',
            6:'Demir Para'
            }
        datanowT=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        name_from_now=MYSQ.ALL_SQL_AT_ONE('select',3,2,'')
        neyapti=['Sildi','Değişmiş','Yazdı']
        #----------------------------------------------------------
        if count_row==1:
            last_row=MYSQ.ALL_SQL_AT_ONE('select',name_of_table[2],'','')
            if name_of_table[1]=='giderler':
                #присвоение в доп переменную копии строки без индекса в формате turple
                 temp_dict=list(last_row[0][1::])
                 #переделка turple в  list 
                 last_row=list(last_row[0][1::])
                 #присвоение значения по умолчанию
                 for i in range(0,len(last_row)): 
                    if i ==1:
                     last_row[i]=0
                    else:
                        last_row[i]=''
                 MYSQ.ALL_SQL_AT_ONE('update',name_of_table[2],[dict_with_number_of_rows,dict_with_number_of_rows],[last_row,temp_dict])
                 MYSQ.ALL_SQL_AT_ONE('insert',16,sp_dict[name_of_table[2]],[datanowT,name_from_now[0][0],spec_name_dict[name_of_table[2]],neyapti[0],*temp_dict])
            elif name_of_table[1]=='doviz':
                 #присвоение в доп переменную копии строки без индекса в формате turple
                 temp_dict=list(last_row[0][1::])
                 #переделка turple в  list 
                 last_row=list(last_row[0][1::])
                 #присвоение значения по умолчанию 
                 for i in range(0,len(last_row)): 
                    if i ==1 or i==2:
                     last_row[i]=0
                    else:
                        last_row[i]=''
                 MYSQ.ALL_SQL_AT_ONE('update',name_of_table[2],[dict_with_number_of_rows,dict_with_number_of_rows],[last_row,temp_dict])
                 MYSQ.ALL_SQL_AT_ONE('insert',16,sp_dict[name_of_table[2]],[datanowT,name_from_now[0][0],spec_name_dict[name_of_table[2]],neyapti[0],*temp_dict])
            elif name_of_table[1]=='doublekey' or name_of_table[1]=='fitneskey':
                #присвоение в доп переменную копии строки без индекса в формате turple
                 temp_dict=list(last_row[0][1::])
                 #переделка turple в  list 
                 last_row=list(last_row[0][1::])
                 #присвоение значения по умолчанию 
                 for i in range(0,len(last_row)): 
                    if i ==4 or i==5 or i==6:
                     last_row[i]=0
                    else:
                        last_row[i]=''
                 MYSQ.ALL_SQL_AT_ONE('update',name_of_table[2],[dict_with_number_of_rows,dict_with_number_of_rows],[last_row,temp_dict])
                 MYSQ.ALL_SQL_AT_ONE('insert',16,sp_dict[name_of_table[2]],[datanowT,name_from_now[0][0],spec_name_dict[name_of_table[2]],neyapti[0],*temp_dict])
            elif name_of_table[1]=='havlu':
                #присвоение в доп переменную копии строки без индекса в формате turple
                 temp_dict=list(last_row[0][1::])
                 #переделка turple в  list 
                 last_row=list(last_row[0][1::])
                 #присвоение значения по умолчанию 
                 for i in range(0,len(last_row)): 
                    if i ==4:
                     last_row[i]=0
                    else:
                        last_row[i]=''
                 MYSQ.ALL_SQL_AT_ONE('update',name_of_table[2],[dict_with_number_of_rows,dict_with_number_of_rows],[last_row,temp_dict])
                 MYSQ.ALL_SQL_AT_ONE('insert',name_of_table[2],sp_dict[name_of_table[2]],[datanowT,name_from_now[0],spec_name_dict[name_of_table[2]],neyapti[0],*temp_dict])
            else:
                MYSQ.ALL_SQL_AT_ONE('delete',name_of_table[2],dict_with_number_of_rows,temp_dict)
                MYSQ.ALL_SQL_AT_ONE('insert',16,sp_dict[name_of_table[2]],[datanowT,name_from_now[0][0],spec_name_dict[name_of_table[2]],neyapti[0],*temp_dict])
        else:
            MYSQ.ALL_SQL_AT_ONE('delete',name_of_table[2],dict_with_number_of_rows,temp_dict)
            if name_of_table[1]=='admintablo':
                pass;
            elif name_of_table[1]=='SQLELECTRA':
                pass;
            elif name_of_table[1]=='MainSql':
                pass;
            else:
                MYSQ.ALL_SQL_AT_ONE('insert',16,sp_dict[name_of_table[2]],[datanowT,name_from_now[0][0],spec_name_dict[name_of_table[2]],neyapti[0],*temp_dict])
        
        Ui_Hotel_Project().show_data(Hotel_parth,MYSQ,['refresh'])
        som.close()
    def start_delete_stil_one_data(self,event,winpart,name_of_table,som):
        #print('name_of_table',name_of_table)
        global Hotel_parthT
        Hotel_parth=Hotel_parthT
        MYSQ=Sql_Query()
        new_dict=[]
        new_dict.insert(0,winpart.Ent1.text())
        MYSQ.ALL_SQL_AT_ONE('else_delete',name_of_table[2],'DELETE FROM {0} where time <   "{1}"'.format(name_of_table[1],new_dict[0]),'')
        Ui_Hotel_Project().show_data(Hotel_parth,MYSQ,['refresh'])
        som.close()
    def update_funck(self,winpart,value_size,name_of_table,som):
        dict_with_number_of_rows={
            10:[2,3],
            15:[2,3],
            8:[2,3,4],
            11:[2,3],
            13:[2,3,4],
            7:[2,3,4,5,6,7,8,9,10,11],
            9:[2,3,4,5,6,7,8,9,10,11],
            12:[2,3,4,5,6,7,8],
            18:[2,3,4,5],
            2:[2],
            4:[2,3],
            5:[2,3]}
        temp_dict=[]
        if name_of_table[0].selectedItems()==[]:
            #print('Зашел по пустой строке в функции апдата ')
        #isinstance(None,type(name_of_table[0].selectedItems())):
            pass;
        else:
           # print('Зашел по полной строке ')
            table_data=name_of_table[0].selectedItems()
            #print(len(table_data))
        
            if value_size==1 :
                if name_of_table[1]=='MainSql':
                    temp_dict.insert(0,table_data[0].text())
                    winpart.Ent1.setText(table_data[0].text())
                elif name_of_table[1]=='nakitt':
                    temp_dict.insert(0,table_data[0].text())
                    temp_dict.insert(1,table_data[1].text())
                else:
                    temp_dict.insert(0,table_data[1].text())
                    winpart.Ent1.setText(table_data[1].text())
            elif value_size==2 :
                temp_dict.insert(0,table_data[0].text())
                temp_dict.insert(1,table_data[1].text())
                winpart.Ent1.setText(table_data[0].text())
                winpart.Ent2.setText(table_data[1].text())
            elif value_size==3 :
                temp_dict.insert(0,table_data[0].text())
                temp_dict.insert(1,table_data[1].text())
                temp_dict.insert(2,table_data[2].text())
                winpart.Ent1.setText(table_data[0].text())
                winpart.Ent2.setText(table_data[1].text())
                winpart.Ent3.setText(table_data[2].text())
            elif value_size==4 :
                temp_dict.insert(0,table_data[0].text())
                temp_dict.insert(1,table_data[1].text())
                temp_dict.insert(2,table_data[2].text())
                temp_dict.insert(3,table_data[3].text())
                winpart.Ent1.setText(table_data[0].text())
                winpart.Ent2.setText(table_data[1].text())
                winpart.Ent3.setText(table_data[2].text())
                winpart.perm_cb.setCurrentText(table_data[3].text())
                #winpart.ok_but.clicked.connect(lambda test_time: self.start_update_at_bd(test_time,winpart,name_of_table,dict_with_number_of_rows[18],temp_dict,value_size,som))
                #winpart.Ent4.setText(table_data[3].text())
            elif value_size==7:
                temp_dict.insert(0,table_data[0].text())
                temp_dict.insert(1,table_data[1].text())
                temp_dict.insert(2,table_data[2].text())
                temp_dict.insert(3,table_data[3].text())
                temp_dict.insert(4,table_data[4].text())
                temp_dict.insert(5,table_data[5].text())
                temp_dict.insert(6,table_data[6].text())
                
                winpart.Ent1.setText(table_data[0].text())
                winpart.Ent2.setText(table_data[1].text())
                winpart.Ent3.setText(table_data[2].text())
                winpart.Ent4.setText(table_data[3].text())
                winpart.Ent5.setText(table_data[4].text())
                winpart.Ent6.setText(table_data[5].text())
                winpart.Ent7.setText(table_data[6].text())
                #winpart.ok_but.clicked.connect(lambda test_time: self.start_update_at_bd(test_time,winpart,name_of_table,dict_with_number_of_rows[12],temp_dict,value_size,som))
            else: 
                temp_dict.insert(0,table_data[0].text())
                temp_dict.insert(1,table_data[1].text())
                temp_dict.insert(2,table_data[2].text())
                temp_dict.insert(3,table_data[3].text())
                temp_dict.insert(4,table_data[4].text())
                temp_dict.insert(5,table_data[5].text())
                temp_dict.insert(6,table_data[6].text())
                temp_dict.insert(7,table_data[7].text())
                temp_dict.insert(8,table_data[8].text())
                temp_dict.insert(9,table_data[9].text())

                winpart.Ent1.setText(table_data[0].text())
                winpart.Ent2.setText(table_data[1].text())
                winpart.Ent3.setText(table_data[2].text())
                winpart.Ent4.setText(table_data[3].text())
                winpart.Ent5.setText(table_data[4].text())
                winpart.Ent6.setText(table_data[5].text())
                winpart.Ent7.setText(table_data[6].text())
                winpart.Ent8.setText(table_data[7].text())
                winpart.Ent9.setText(table_data[8].text())
                winpart.Ent10.setText(table_data[9].text())
                #dict_with_number_of_rows[7] can be also 9
            #try:
            winpart.ok_but.clicked.connect(lambda test_time: self.start_update_at_bd(test_time,winpart,name_of_table,dict_with_number_of_rows[name_of_table[2]],temp_dict,value_size,som))
            winpart.cancel_but.clicked.connect(som.close)
            #except 18 :
            #    pass;
    def insert_funck(self,winpart,value_size,name_of_table,som):
        winpart.ok_but.clicked.connect(lambda tes: self.start_insert_at_bd(tes,winpart,name_of_table,value_size,som))
        winpart.cancel_but.clicked.connect(som.close)
    def delete_funck(self,winpart,value_size,name_of_table,som):
        dict_with_number_of_rows={
            10:[2,3],
            15:[2,3],
            8:[2,3,4],
            11:[2,3],
            13:[2,3,4],
            7:[2,3,4,5,6,7,8,9,10,11],
            9:[2,3,4,5,6,7,8,9,10,11],
            12:[2,3,4,5,6,7,8],
            18:[2,3,4,5],
            2:[2],
            4:[2,3],
            5:[2,3]}
        temp_dict=[]
        if name_of_table[0].selectedItems()==[]:
            #print('Зашел по пустой строке в функции апдата ')
        #isinstance(None,type(name_of_table[0].selectedItems())):
            pass;
        else:
           # print('Зашел по полной строке ')
            table_data=name_of_table[0].selectedItems()
            #print(len(table_data))
        
            if value_size==1 :
                if name_of_table[1]=='MainSql':
                    temp_dict.insert(0,table_data[0].text())
                    
                else:
                    temp_dict.insert(0,table_data[1].text())
                    
            elif value_size==2 :
                temp_dict.insert(0,table_data[0].text())
                temp_dict.insert(1,table_data[1].text())

            elif value_size==3 :
                temp_dict.insert(0,table_data[0].text())
                temp_dict.insert(1,table_data[1].text())
                temp_dict.insert(2,table_data[2].text())

            elif value_size==4 :
                temp_dict.insert(0,table_data[0].text())
                temp_dict.insert(1,table_data[1].text())
                temp_dict.insert(2,table_data[2].text())
                temp_dict.insert(3,table_data[3].text())

            elif value_size==7:
                temp_dict.insert(0,table_data[0].text())
                temp_dict.insert(1,table_data[1].text())
                temp_dict.insert(2,table_data[2].text())
                temp_dict.insert(3,table_data[3].text())
                temp_dict.insert(4,table_data[4].text())
                temp_dict.insert(5,table_data[5].text())
                temp_dict.insert(6,table_data[6].text())

            else: 
                temp_dict.insert(0,table_data[0].text())
                temp_dict.insert(1,table_data[1].text())
                temp_dict.insert(2,table_data[2].text())
                temp_dict.insert(3,table_data[3].text())
                temp_dict.insert(4,table_data[4].text())
                temp_dict.insert(5,table_data[5].text())
                temp_dict.insert(6,table_data[6].text())
                temp_dict.insert(7,table_data[7].text())
                temp_dict.insert(8,table_data[8].text())
                temp_dict.insert(9,table_data[9].text())

            self.start_delete_at_bd(name_of_table,dict_with_number_of_rows[name_of_table[2]],temp_dict,som)
    def delete_stil_one_data(self,winpart,value_size,name_of_table,som):
        winpart.ok_but.clicked.connect(lambda tes: self.start_delete_stil_one_data(tes,winpart,name_of_table,som))
        winpart.cancel_but.clicked.connect(som.close)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
    def update_for_one_line_edit(self,result,number_table,number_row):
         global Hotel_parthT
         Hotel_parth=Hotel_parthT
         MYSQ=Sql_Query()
         temp_dict=[0.0,0.0]
         sp_dict={
            15:[2,3,4,5,6,7],
            14:[2,3,4,5,8,9],
            13:[2,3,4,5,11,12,13],
            12:[2,3,4,5,21,22,23,24,25,26,27],
            11:[2,3,4,5,11,12],
            10:[2,3,4,5,16,22],
            9:[2,3,4,5,10,11,12,17,21,22,23,24,26,27],
            8:[2,3,4,5,18,19,20],
            7:[2,3,4,5,10,11,12,17,21,22,23,24,26,27],
            6:[2,3,4,5,14,15]
            }
         spec_name_dict={
            15:'Nakit para',
            14:'Avans ve Nakit',
            13:'Havlu Degisik',
            12:'Sahil Havlu',
            11:'Hamam WiFi',
            10:'Giderler',
            9:'Fitnes',
            8:'Doviz',
            7:'Yedek Anahtar',
            6:'Demir Para'
            }
         datanowT=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
         name_from_now=MYSQ.ALL_SQL_AT_ONE('select',3,2,'')
         neyapti=['Sildi','Değişmiş','Yazdı']
         
         old_result=MYSQ.ALL_SQL_AT_ONE('select',number_table,number_row,'')
         old_result=list(old_result)
         if number_row==2:
             temp_dict[0]=old_result[0][0]
             temp_dict[1]=''
         elif number_row==3:
            temp_dict[0]=''
            temp_dict[1]=old_result[0][0]
         #print('OLD RESULT',old_result[0][0])
         if result=='' or result==None:
             result=0.0
         MYSQ.ALL_SQL_AT_ONE('update',number_table,[[number_row],[number_row]],[[result],[old_result[0][0]]])
         MYSQ.ALL_SQL_AT_ONE('insert',16,sp_dict[number_table],[datanowT,name_from_now[0][0],spec_name_dict[number_table],neyapti[1],*temp_dict])
         Ui_Hotel_Project().show_data(Hotel_parth,MYSQ,['refresh'])

class Ui_Hotel_Project(object):
    global Hotel_parthT
    #При создании событий и их модернизации не забыть подправить функцию в setupUi
    #Создание всех элементов на главном окне 
    def setupUi(self, Hotel_Project):
        Hotel_Project.setObjectName("Hotel_Project")
        Hotel_Project.setEnabled(True)
        Hotel_Project.resize(1211, 859)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Hotel_Project.sizePolicy().hasHeightForWidth())
        Hotel_Project.setSizePolicy(sizePolicy)
        Hotel_Project.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Hotel_Project)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget = QtWidgets.QTabWidget(Hotel_Project)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName("tabWidget")
#-------------------------------------------------------------------------------------------------------------------------------------------------
        self.KASA_PAGE = QtWidgets.QWidget()
        self.KASA_PAGE.setObjectName("KASA_PAGE")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.KASA_PAGE)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(1000, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.KASA_PAGE)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.AVANS_ENTER = QtWidgets.QLineEdit(self.KASA_PAGE)
        self.AVANS_ENTER.setMaximumSize(QtCore.QSize(115, 22))
        self.AVANS_ENTER.setObjectName("AVANS_ENTER")
        self.horizontalLayout.addWidget(self.AVANS_ENTER)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(1000, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label_8 = QtWidgets.QLabel(self.KASA_PAGE)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        
        self.NAKIT_ENTER = QtWidgets.QLineEdit(self.KASA_PAGE)
        self.NAKIT_ENTER.setMaximumSize(QtCore.QSize(115, 22))
        self.NAKIT_ENTER.setObjectName("NAKIT_ENTER")
        self.horizontalLayout_2.addWidget(self.NAKIT_ENTER)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_17.addLayout(self.verticalLayout)
        self.label_2 = QtWidgets.QLabel(self.KASA_PAGE)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_17.addWidget(self.label_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.KASA_PAGE)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        
        self.D_EURO_ENTER = QtWidgets.QLineEdit(self.KASA_PAGE)
        self.D_EURO_ENTER.setMaximumSize(QtCore.QSize(115, 22))
        self.D_EURO_ENTER.setObjectName("D_EURO_ENTER")
        self.horizontalLayout_3.addWidget(self.D_EURO_ENTER)
        spacerItem2 = QtWidgets.QSpacerItem(1000, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.KASA_PAGE)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        
        self.D_TL_ENTER = QtWidgets.QLineEdit(self.KASA_PAGE)
        self.D_TL_ENTER.setMaximumSize(QtCore.QSize(115, 22))
        self.D_TL_ENTER.setObjectName("D_TL_ENTER")
        self.horizontalLayout_4.addWidget(self.D_TL_ENTER)
        spacerItem3 = QtWidgets.QSpacerItem(1000, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_17.addLayout(self.verticalLayout_2)
        
        self.GIDERLER_TB_W = QtWidgets.QTableWidget(self.KASA_PAGE)
        self.GIDERLER_TB_W.setObjectName("GIDERLER_TB_W")
        self.GIDERLER_TB_W.setColumnCount(0)
        self.GIDERLER_TB_W.setRowCount(0)
        self.verticalLayout_17.addWidget(self.GIDERLER_TB_W)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.KASA_PAGE)
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
       
        self.DOVIZ_TB_W = QtWidgets.QTableWidget(self.KASA_PAGE)
        self.DOVIZ_TB_W.setObjectName("DOVIZ_TB_W")
        self.DOVIZ_TB_W.setColumnCount(0)
        self.DOVIZ_TB_W.setRowCount(0)
        self.verticalLayout_3.addWidget(self.DOVIZ_TB_W)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.KASA_PAGE)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        

        self.NAKIT_TB_W = QtWidgets.QTableWidget(self.KASA_PAGE)
        self.NAKIT_TB_W.setObjectName("NAKIT_TB_W")
        self.NAKIT_TB_W.setColumnCount(0)
        self.NAKIT_TB_W.setRowCount(0)
        self.verticalLayout_5.addWidget(self.NAKIT_TB_W)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.verticalLayout_17.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem5 = QtWidgets.QSpacerItem(1000, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.label_9 = QtWidgets.QLabel(self.KASA_PAGE)
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        

        self.FARK_ENTER = QtWidgets.QLineEdit(self.KASA_PAGE)
        self.FARK_ENTER.setMaximumSize(QtCore.QSize(217, 22))
        self.FARK_ENTER.setObjectName("FARK_ENTER")
        self.horizontalLayout_6.addWidget(self.FARK_ENTER)
        self.verticalLayout_17.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtWidgets.QLabel(self.KASA_PAGE)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        
        self.TESLIM_VERILDI_ENTER = QtWidgets.QLineEdit(self.KASA_PAGE)
        self.TESLIM_VERILDI_ENTER.setObjectName("TESLIM_VERILDI_ENTER")
        self.horizontalLayout_8.addWidget(self.TESLIM_VERILDI_ENTER)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_8)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_12 = QtWidgets.QLabel(self.KASA_PAGE)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_7.addWidget(self.label_12)
        
        self.TESLIM_ALDI_ENTER = QtWidgets.QLineEdit(self.KASA_PAGE)
        self.TESLIM_ALDI_ENTER.setObjectName("TESLIM_ALDI_ENTER")
        self.horizontalLayout_7.addWidget(self.TESLIM_ALDI_ENTER)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_7)
        self.verticalLayout_17.addLayout(self.horizontalLayout_9)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(-1, -1, -1, 100)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_11 = QtWidgets.QLabel(self.KASA_PAGE)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_11.addWidget(self.label_11)
        
        self.HAVLU_DEGISIM_ENTER = QtWidgets.QTableWidget(self.KASA_PAGE)
        self.HAVLU_DEGISIM_ENTER.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HAVLU_DEGISIM_ENTER.sizePolicy().hasHeightForWidth())
        self.HAVLU_DEGISIM_ENTER.setSizePolicy(sizePolicy)
        self.HAVLU_DEGISIM_ENTER.setMaximumSize(QtCore.QSize(360, 60))
        self.HAVLU_DEGISIM_ENTER.setBaseSize(QtCore.QSize(360, 60))
        self.HAVLU_DEGISIM_ENTER.setObjectName("HAVLU_DEGISIM_ENTER")
        self.HAVLU_DEGISIM_ENTER.setColumnCount(0)
        self.HAVLU_DEGISIM_ENTER.setRowCount(0)
        self.horizontalLayout_11.addWidget(self.HAVLU_DEGISIM_ENTER)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem7)
        self.verticalLayout_6.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_10 = QtWidgets.QLabel(self.KASA_PAGE)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_10.addWidget(self.label_10)
        
        self.HAMAM_WIFI_ENTER = QtWidgets.QTableWidget(self.KASA_PAGE)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HAMAM_WIFI_ENTER.sizePolicy().hasHeightForWidth())
        self.HAMAM_WIFI_ENTER.setSizePolicy(sizePolicy)
        self.HAMAM_WIFI_ENTER.setMaximumSize(QtCore.QSize(360, 60))
        self.HAMAM_WIFI_ENTER.setBaseSize(QtCore.QSize(360, 60))
        self.HAMAM_WIFI_ENTER.setObjectName("HAMAM_WIFI_ENTER")
        self.HAMAM_WIFI_ENTER.setColumnCount(0)
        self.HAMAM_WIFI_ENTER.setRowCount(0)
        self.horizontalLayout_10.addWidget(self.HAMAM_WIFI_ENTER)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem8)
        self.verticalLayout_6.addLayout(self.horizontalLayout_10)
        self.verticalLayout_17.addLayout(self.verticalLayout_6)
        self.tabWidget.addTab(self.KASA_PAGE, "")
#--------------------------------------------------------------------------------------------------------------------------------        
        self.YEDEK_ANAHTAR_PAGE = QtWidgets.QWidget()
        self.YEDEK_ANAHTAR_PAGE.setObjectName("YEDEK_ANAHTAR_PAGE")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.YEDEK_ANAHTAR_PAGE)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        
        self.Y_FILTER_OD_NUM_ENTER = QtWidgets.QLineEdit(self.YEDEK_ANAHTAR_PAGE)
        self.Y_FILTER_OD_NUM_ENTER.setObjectName("Y_FILTER_OD_NUM_ENTER")
        self.horizontalLayout_12.addWidget(self.Y_FILTER_OD_NUM_ENTER)
        
        self.Y_FILETR_ISI_ENTER = QtWidgets.QLineEdit(self.YEDEK_ANAHTAR_PAGE)
        self.Y_FILETR_ISI_ENTER.setObjectName("Y_FILETR_ISI_ENTER")
        self.horizontalLayout_12.addWidget(self.Y_FILETR_ISI_ENTER)
        
        self.Y_FILTER_GIR_TAR_ENTER = QtWidgets.QLineEdit(self.YEDEK_ANAHTAR_PAGE)
        self.Y_FILTER_GIR_TAR_ENTER.setObjectName("Y_FILTER_GIR_TAR_ENTER")
        self.horizontalLayout_12.addWidget(self.Y_FILTER_GIR_TAR_ENTER)
        
        self.Y_FILTER_CIK_TAR_ENTER = QtWidgets.QLineEdit(self.YEDEK_ANAHTAR_PAGE)
        self.Y_FILTER_CIK_TAR_ENTER.setObjectName("Y_FILTER_CIK_TAR_ENTER")
        self.horizontalLayout_12.addWidget(self.Y_FILTER_CIK_TAR_ENTER)
        
        self.Y_FILTER_USD_ENTER = QtWidgets.QLineEdit(self.YEDEK_ANAHTAR_PAGE)
        self.Y_FILTER_USD_ENTER.setObjectName("Y_FILTER_USD_ENTER")
        self.horizontalLayout_12.addWidget(self.Y_FILTER_USD_ENTER)
        
        self.Y_FILTER_EURO_ENTER = QtWidgets.QLineEdit(self.YEDEK_ANAHTAR_PAGE)
        self.Y_FILTER_EURO_ENTER.setObjectName("Y_FILTER_EURO_ENTER")
        self.horizontalLayout_12.addWidget(self.Y_FILTER_EURO_ENTER)
        
        self.Y_FILTER_RUBLE_ENTER = QtWidgets.QLineEdit(self.YEDEK_ANAHTAR_PAGE)
        self.Y_FILTER_RUBLE_ENTER.setObjectName("Y_FILTER_RUBLE_ENTER")
        self.horizontalLayout_12.addWidget(self.Y_FILTER_RUBLE_ENTER)
        
        self.Y_FILTER_BAS_PAR_ENTER = QtWidgets.QLineEdit(self.YEDEK_ANAHTAR_PAGE)
        self.Y_FILTER_BAS_PAR_ENTER.setObjectName("Y_FILTER_BAS_PAR_ENTER")
        self.horizontalLayout_12.addWidget(self.Y_FILTER_BAS_PAR_ENTER)
        
        self.Y_FILTER_KIM_VER_ENTER = QtWidgets.QLineEdit(self.YEDEK_ANAHTAR_PAGE)
        self.Y_FILTER_KIM_VER_ENTER.setObjectName("Y_FILTER_KIM_VER_ENTER")
        self.horizontalLayout_12.addWidget(self.Y_FILTER_KIM_VER_ENTER)
        
        self.Y_FILTER_KIM_YAZ_ENTER = QtWidgets.QLineEdit(self.YEDEK_ANAHTAR_PAGE)
        self.Y_FILTER_KIM_YAZ_ENTER.setObjectName("Y_FILTER_KIM_YAZ_ENTER")
        self.horizontalLayout_12.addWidget(self.Y_FILTER_KIM_YAZ_ENTER)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        
        self.YEDEK_ANAHTAR_TB_W = QtWidgets.QTableWidget(self.YEDEK_ANAHTAR_PAGE)
        self.YEDEK_ANAHTAR_TB_W.setMinimumSize(QtCore.QSize(0, 0))
        self.YEDEK_ANAHTAR_TB_W.setObjectName("YEDEK_ANAHTAR_TB_W")
        self.YEDEK_ANAHTAR_TB_W.setColumnCount(0)
        self.YEDEK_ANAHTAR_TB_W.setRowCount(0)
        self.verticalLayout_8.addWidget(self.YEDEK_ANAHTAR_TB_W)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        
        self.label_13 = QtWidgets.QLabel(self.YEDEK_ANAHTAR_PAGE)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_13.addWidget(self.label_13)
        
        self.Y_TOTAL_DOLLAR_ENTER = QtWidgets.QLineEdit(self.YEDEK_ANAHTAR_PAGE)
        self.Y_TOTAL_DOLLAR_ENTER.setObjectName("Y_TOTAL_DOLLAR_ENTER")
        self.horizontalLayout_13.addWidget(self.Y_TOTAL_DOLLAR_ENTER)
        self.horizontalLayout_16.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        
        self.Y_TOTAL_EURO_ENTER = QtWidgets.QLineEdit(self.YEDEK_ANAHTAR_PAGE)
        self.Y_TOTAL_EURO_ENTER.setObjectName("Y_TOTAL_EURO_ENTER")
        self.horizontalLayout_14.addWidget(self.Y_TOTAL_EURO_ENTER)
        self.horizontalLayout_16.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        
        self.Y_TOTAL_RUBLE_ENTER = QtWidgets.QLineEdit(self.YEDEK_ANAHTAR_PAGE)
        self.Y_TOTAL_RUBLE_ENTER.setObjectName("Y_TOTAL_RUBLE_ENTER")
        self.horizontalLayout_15.addWidget(self.Y_TOTAL_RUBLE_ENTER)
        self.horizontalLayout_16.addLayout(self.horizontalLayout_15)
        self.verticalLayout_8.addLayout(self.horizontalLayout_16)
        self.verticalLayout_9.addLayout(self.verticalLayout_8)
        self.tabWidget.addTab(self.YEDEK_ANAHTAR_PAGE, "")
#---------------------------------------------------------------------------------------------        
        self.FITNES_ANAHTAR_PAGE = QtWidgets.QWidget()
        self.FITNES_ANAHTAR_PAGE.setObjectName("FITNES_ANAHTAR_PAGE")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.FITNES_ANAHTAR_PAGE)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        
        self.F_FILTER_OD_NUM_ENTER = QtWidgets.QLineEdit(self.FITNES_ANAHTAR_PAGE)
        self.F_FILTER_OD_NUM_ENTER.setObjectName("F_FILTER_OD_NUM_ENTER")
        self.horizontalLayout_17.addWidget(self.F_FILTER_OD_NUM_ENTER)
        
        self.F_FILETR_ISI_ENTER = QtWidgets.QLineEdit(self.FITNES_ANAHTAR_PAGE)
        self.F_FILETR_ISI_ENTER.setObjectName("F_FILETR_ISI_ENTER")
        self.horizontalLayout_17.addWidget(self.F_FILETR_ISI_ENTER)
        
        self.F_FILTER_GIR_TAR_ENTER = QtWidgets.QLineEdit(self.FITNES_ANAHTAR_PAGE)
        self.F_FILTER_GIR_TAR_ENTER.setObjectName("F_FILTER_GIR_TAR_ENTER")
        self.horizontalLayout_17.addWidget(self.F_FILTER_GIR_TAR_ENTER)
        
        self.F_FILTER_CIK_TAR_ENTER = QtWidgets.QLineEdit(self.FITNES_ANAHTAR_PAGE)
        self.F_FILTER_CIK_TAR_ENTER.setObjectName("F_FILTER_CIK_TAR_ENTER")
        self.horizontalLayout_17.addWidget(self.F_FILTER_CIK_TAR_ENTER)
        
        self.F_FILTER_USD_ENTER = QtWidgets.QLineEdit(self.FITNES_ANAHTAR_PAGE)
        self.F_FILTER_USD_ENTER.setObjectName("F_FILTER_USD_ENTER")
        self.horizontalLayout_17.addWidget(self.F_FILTER_USD_ENTER)
        
        self.F_FILTER_EURO_ENTER = QtWidgets.QLineEdit(self.FITNES_ANAHTAR_PAGE)
        self.F_FILTER_EURO_ENTER.setObjectName("F_FILTER_EURO_ENTER")
        self.horizontalLayout_17.addWidget(self.F_FILTER_EURO_ENTER)
        
        self.F_FILTER_RUBLE_ENTER = QtWidgets.QLineEdit(self.FITNES_ANAHTAR_PAGE)
        self.F_FILTER_RUBLE_ENTER.setObjectName("F_FILTER_RUBLE_ENTER")
        self.horizontalLayout_17.addWidget(self.F_FILTER_RUBLE_ENTER)
        
        self.F_FILTER_BAS_PAR_ENTER = QtWidgets.QLineEdit(self.FITNES_ANAHTAR_PAGE)
        self.F_FILTER_BAS_PAR_ENTER.setObjectName("F_FILTER_BAS_PAR_ENTER")
        self.horizontalLayout_17.addWidget(self.F_FILTER_BAS_PAR_ENTER)
        
        self.F_FILTER_KIM_VER_ENTER = QtWidgets.QLineEdit(self.FITNES_ANAHTAR_PAGE)
        self.F_FILTER_KIM_VER_ENTER.setObjectName("F_FILTER_KIM_VER_ENTER")
        self.horizontalLayout_17.addWidget(self.F_FILTER_KIM_VER_ENTER)
        
        self.F_FILTER_KIM_YAZ_ENTER = QtWidgets.QLineEdit(self.FITNES_ANAHTAR_PAGE)
        self.F_FILTER_KIM_YAZ_ENTER.setObjectName("F_FILTER_KIM_YAZ_ENTER")
        self.horizontalLayout_17.addWidget(self.F_FILTER_KIM_YAZ_ENTER)
        self.verticalLayout_10.addLayout(self.horizontalLayout_17)
        
        self.FITNES_ANAHTAR_TB_W = QtWidgets.QTableWidget(self.FITNES_ANAHTAR_PAGE)
        self.FITNES_ANAHTAR_TB_W.setObjectName("FITNES_ANAHTAR_TB_W")
        self.FITNES_ANAHTAR_TB_W.setColumnCount(0)
        self.FITNES_ANAHTAR_TB_W.setRowCount(0)
        self.verticalLayout_10.addWidget(self.FITNES_ANAHTAR_TB_W)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_16 = QtWidgets.QLabel(self.FITNES_ANAHTAR_PAGE)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_18.addWidget(self.label_16)
        
        self.F_TOTAL_DOLLAR_ENTER = QtWidgets.QLineEdit(self.FITNES_ANAHTAR_PAGE)
        self.F_TOTAL_DOLLAR_ENTER.setObjectName("F_TOTAL_DOLLAR_ENTER")
        self.horizontalLayout_18.addWidget(self.F_TOTAL_DOLLAR_ENTER)
        self.horizontalLayout_21.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        
        self.F_TOTAL_EURO_ENTER = QtWidgets.QLineEdit(self.FITNES_ANAHTAR_PAGE)
        self.F_TOTAL_EURO_ENTER.setObjectName("F_TOTAL_EURO_ENTER")
        self.horizontalLayout_19.addWidget(self.F_TOTAL_EURO_ENTER)
        self.horizontalLayout_21.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        
        self.F_TOTAL_RUBLE_ENTER = QtWidgets.QLineEdit(self.FITNES_ANAHTAR_PAGE)
        self.F_TOTAL_RUBLE_ENTER.setObjectName("F_TOTAL_RUBLE_ENTER")
        self.horizontalLayout_20.addWidget(self.F_TOTAL_RUBLE_ENTER)
        self.horizontalLayout_21.addLayout(self.horizontalLayout_20)
        self.verticalLayout_10.addLayout(self.horizontalLayout_21)
        self.verticalLayout_11.addLayout(self.verticalLayout_10)
        self.tabWidget.addTab(self.FITNES_ANAHTAR_PAGE, "")
#--------------------------------------------------------------------------------------------------------        
        self.HAVLU_PAGE = QtWidgets.QWidget()
        self.HAVLU_PAGE.setObjectName("HAVLU_PAGE")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.HAVLU_PAGE)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        
        self.H_FILTER_OD_NUM_ENTER = QtWidgets.QLineEdit(self.HAVLU_PAGE)
        self.H_FILTER_OD_NUM_ENTER.setObjectName("H_FILTER_OD_NUM_ENTER")
        self.horizontalLayout_22.addWidget(self.H_FILTER_OD_NUM_ENTER)
        
        self.H_FILETR_ISI_ENTER = QtWidgets.QLineEdit(self.HAVLU_PAGE)
        self.H_FILETR_ISI_ENTER.setObjectName("H_FILETR_ISI_ENTER")
        self.horizontalLayout_22.addWidget(self.H_FILETR_ISI_ENTER)
        
        self.H_FILTER_GIR_TAR_ENTER = QtWidgets.QLineEdit(self.HAVLU_PAGE)
        self.H_FILTER_GIR_TAR_ENTER.setObjectName("H_FILTER_GIR_TAR_ENTER")
        self.horizontalLayout_22.addWidget(self.H_FILTER_GIR_TAR_ENTER)
        
        self.H_FILTER_CIK_TAR_ENTER = QtWidgets.QLineEdit(self.HAVLU_PAGE)
        self.H_FILTER_CIK_TAR_ENTER.setObjectName("H_FILTER_CIK_TAR_ENTER")
        self.horizontalLayout_22.addWidget(self.H_FILTER_CIK_TAR_ENTER)
        
        self.H_FILTER_K_HAV_ENTER = QtWidgets.QLineEdit(self.HAVLU_PAGE)
        self.H_FILTER_K_HAV_ENTER.setObjectName("H_FILTER_K_HAV_ENTER")
        self.horizontalLayout_22.addWidget(self.H_FILTER_K_HAV_ENTER)
        
        self.H_FILTER_KIM_VER_ENTER = QtWidgets.QLineEdit(self.HAVLU_PAGE)
        self.H_FILTER_KIM_VER_ENTER.setObjectName("H_FILTER_KIM_VER_ENTER")
        self.horizontalLayout_22.addWidget(self.H_FILTER_KIM_VER_ENTER)
        
        self.H_FILTER_KIM_YAZ_ENTER = QtWidgets.QLineEdit(self.HAVLU_PAGE)
        self.H_FILTER_KIM_YAZ_ENTER.setObjectName("H_FILTER_KIM_YAZ_ENTER")
        self.horizontalLayout_22.addWidget(self.H_FILTER_KIM_YAZ_ENTER)
        self.verticalLayout_12.addLayout(self.horizontalLayout_22)
        
        self.HAVLU_TB_W = QtWidgets.QTableWidget(self.HAVLU_PAGE)
        self.HAVLU_TB_W.setObjectName("HAVLU_TB_W")
        self.HAVLU_TB_W.setColumnCount(0)
        self.HAVLU_TB_W.setRowCount(0)
        self.verticalLayout_12.addWidget(self.HAVLU_TB_W)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_23.addItem(spacerItem9)
        self.label_14 = QtWidgets.QLabel(self.HAVLU_PAGE)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_23.addWidget(self.label_14)
        
        self.H_TOTAL_HAVLU_ENTER = QtWidgets.QLineEdit(self.HAVLU_PAGE)
        self.H_TOTAL_HAVLU_ENTER.setObjectName("H_TOTAL_HAVLU_ENTER")
        self.horizontalLayout_23.addWidget(self.H_TOTAL_HAVLU_ENTER)
        self.verticalLayout_12.addLayout(self.horizontalLayout_23)
        self.tabWidget.addTab(self.HAVLU_PAGE, "")
#-----------------------------------------------------------------------------------------------------------------------        
        self.CONTROL_PANE_PAGE = QtWidgets.QWidget()
        self.CONTROL_PANE_PAGE.setObjectName("CONTROL_PANE_PAGE")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.CONTROL_PANE_PAGE)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")

        self.STANDART_CB = QtWidgets.QCheckBox(self.CONTROL_PANE_PAGE)
        self.STANDART_CB.setChecked(True)
        self.STANDART_CB.setAutoRepeat(True)
        self.STANDART_CB.setAutoExclusive(True)
        self.STANDART_CB.setTristate(False)
        self.STANDART_CB.setObjectName("STANDART_CB")
        self.horizontalLayout_25.addWidget(self.STANDART_CB)

        self.AVANS_VE_NAKIT_CB = QtWidgets.QCheckBox(self.CONTROL_PANE_PAGE)
        self.AVANS_VE_NAKIT_CB.setAutoExclusive(True)
        self.AVANS_VE_NAKIT_CB.setObjectName("AVANS_VE_NAKIT_CB")
        self.horizontalLayout_25.addWidget(self.AVANS_VE_NAKIT_CB)

        self.NAKIT_PARA_CB = QtWidgets.QCheckBox(self.CONTROL_PANE_PAGE)
        self.NAKIT_PARA_CB.setAutoExclusive(True)
        self.NAKIT_PARA_CB.setObjectName("NAKIT_PARA_CB")
        self.horizontalLayout_25.addWidget(self.NAKIT_PARA_CB)

        self.GIDERLER_CB = QtWidgets.QCheckBox(self.CONTROL_PANE_PAGE)
        self.GIDERLER_CB.setAutoExclusive(True)
        self.GIDERLER_CB.setObjectName("GIDERLER_CB")
        self.horizontalLayout_25.addWidget(self.GIDERLER_CB)

        self.DOVIZ_CB = QtWidgets.QCheckBox(self.CONTROL_PANE_PAGE)
        self.DOVIZ_CB.setAutoExclusive(True)
        self.DOVIZ_CB.setObjectName("DOVIZ_CB")
        self.horizontalLayout_25.addWidget(self.DOVIZ_CB)

        self.DEMIR_PARA_CB = QtWidgets.QCheckBox(self.CONTROL_PANE_PAGE)
        self.DEMIR_PARA_CB.setAutoExclusive(True)
        self.DEMIR_PARA_CB.setObjectName("DEMIR_PARA_CB")
        self.horizontalLayout_25.addWidget(self.DEMIR_PARA_CB)

        self.HAVLU_DEGISIK_CB = QtWidgets.QCheckBox(self.CONTROL_PANE_PAGE)
        self.HAVLU_DEGISIK_CB.setAutoExclusive(True)
        self.HAVLU_DEGISIK_CB.setObjectName("HAVLU_DEGISIK_CB")
        self.horizontalLayout_25.addWidget(self.HAVLU_DEGISIK_CB)

        self.HAMAM_WIFI_CB = QtWidgets.QCheckBox(self.CONTROL_PANE_PAGE)
        self.HAMAM_WIFI_CB.setAutoExclusive(True)
        self.HAMAM_WIFI_CB.setObjectName("HAMAM_WIFI_CB")
        self.horizontalLayout_25.addWidget(self.HAMAM_WIFI_CB)

        self.YEDEK_ANAHTAR_CB = QtWidgets.QCheckBox(self.CONTROL_PANE_PAGE)
        self.YEDEK_ANAHTAR_CB.setAutoExclusive(True)
        self.YEDEK_ANAHTAR_CB.setObjectName("YEDEK_ANAHTAR_CB")
        self.horizontalLayout_25.addWidget(self.YEDEK_ANAHTAR_CB)

        self.FITNES_CB = QtWidgets.QCheckBox(self.CONTROL_PANE_PAGE)
        self.FITNES_CB.setAutoExclusive(True)
        self.FITNES_CB.setObjectName("FITNES_CB")
        self.horizontalLayout_25.addWidget(self.FITNES_CB)

        self.HAVLU_CB = QtWidgets.QCheckBox(self.CONTROL_PANE_PAGE)
        self.HAVLU_CB.setAutoExclusive(True)
        self.HAVLU_CB.setObjectName("HAVLU_CB")
        self.horizontalLayout_25.addWidget(self.HAVLU_CB)

        self.ADMIN_CB = QtWidgets.QCheckBox(self.CONTROL_PANE_PAGE)
        self.ADMIN_CB.setAutoExclusive(True)
        self.ADMIN_CB.setObjectName("ADMIN_CB")
        self.horizontalLayout_25.addWidget(self.ADMIN_CB)
        self.ADMIN_CB.setVisible(False)

        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem10)
        self.verticalLayout_7.addLayout(self.horizontalLayout_25)
        self.scrollArea = QtWidgets.QScrollArea(self.CONTROL_PANE_PAGE)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1171, 364))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")

        self.FILTER_ZAM_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_ZAM_ENTER.setObjectName("FILTER_ZAM_ENTER")
        self.horizontalLayout_24.addWidget(self.FILTER_ZAM_ENTER)

        self.FILTER_IS_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_IS_ENTER.setObjectName("FILTER_IS_ENTER")
        self.horizontalLayout_24.addWidget(self.FILTER_IS_ENTER)

        self.FILTER_TAB_NAM_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_TAB_NAM_ENTER.setObjectName("FILTER_TAB_NAM_ENTER")
        self.horizontalLayout_24.addWidget(self.FILTER_TAB_NAM_ENTER)

        self.FILTER_NE_YAP_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_NE_YAP_ENTER.setObjectName("FILTER_NE_YAP_ENTER")
        self.FILTER_NE_YAP_ENTER.setVisible(False)
        self.horizontalLayout_24.addWidget(self.FILTER_NE_YAP_ENTER)

        self.FILTER_00_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_00_ENTER.setObjectName("FILTER_00_ENTER")
        self.FILTER_00_ENTER.setVisible(False)
        self.horizontalLayout_24.addWidget(self.FILTER_00_ENTER)

        self.FILTER_01_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_01_ENTER.setObjectName("FILTER_01_ENTER")
        self.FILTER_01_ENTER.setVisible(False)
        self.horizontalLayout_24.addWidget(self.FILTER_01_ENTER)

        self.FILTER_02_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_02_ENTER.setObjectName("FILTER_02_ENTER")
        self.FILTER_02_ENTER.setVisible(False)
        self.horizontalLayout_24.addWidget(self.FILTER_02_ENTER)

        self.FILTER_03_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_03_ENTER.setObjectName("FILTER_03_ENTER")
        self.FILTER_03_ENTER.setVisible(False)
        self.horizontalLayout_24.addWidget(self.FILTER_03_ENTER)

        self.FILTER_04_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_04_ENTER.setObjectName("FILTER_04_ENTER")
        self.FILTER_04_ENTER.setVisible(False)
        self.horizontalLayout_24.addWidget(self.FILTER_04_ENTER)

        self.FILTER_05_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_05_ENTER.setObjectName("FILTER_05_ENTER")
        self.FILTER_05_ENTER.setVisible(False)
        self.horizontalLayout_24.addWidget(self.FILTER_05_ENTER)

        self.FILTER_06_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_06_ENTER.setObjectName("FILTER_06_ENTER")
        self.FILTER_06_ENTER.setVisible(False)
        self.horizontalLayout_24.addWidget(self.FILTER_06_ENTER)

        self.FILTER_07_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_07_ENTER.setObjectName("FILTER_07_ENTER")
        self.FILTER_07_ENTER.setVisible(False)
        self.horizontalLayout_24.addWidget(self.FILTER_07_ENTER)

        self.FILTER_08_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_08_ENTER.setObjectName("FILTER_08_ENTER")
        self.FILTER_08_ENTER.setVisible(False)
        self.horizontalLayout_24.addWidget(self.FILTER_08_ENTER)

        self.FILTER_09_ENTER = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.FILTER_09_ENTER.setObjectName("FILTER_09_ENTER")
        self.FILTER_09_ENTER.setVisible(False)
        self.horizontalLayout_24.addWidget(self.FILTER_09_ENTER)
        self.verticalLayout_13.addLayout(self.horizontalLayout_24)
        
        self.NESILDI_TB_W = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.NESILDI_TB_W.setObjectName("NESILDI_TB_W")
        self.NESILDI_TB_W.setColumnCount(0)
        self.NESILDI_TB_W.setRowCount(0)
        self.verticalLayout_13.addWidget(self.NESILDI_TB_W)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_7.addWidget(self.scrollArea)
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        
        self.TESLIM_TB_W = QtWidgets.QTableWidget(self.CONTROL_PANE_PAGE)
        self.TESLIM_TB_W.setObjectName("TESLIM_TB_W")
        self.TESLIM_TB_W.setColumnCount(0)
        self.TESLIM_TB_W.setRowCount(0)
        self.horizontalLayout_28.addWidget(self.TESLIM_TB_W)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        
        self.FILTER_TIME_ENTER = QtWidgets.QLineEdit(self.CONTROL_PANE_PAGE)
        self.FILTER_TIME_ENTER.setObjectName("FILTER_TIME_ENTER")
        self.horizontalLayout_26.addWidget(self.FILTER_TIME_ENTER)
        
        self.FILTER_NAME_ENTER = QtWidgets.QLineEdit(self.CONTROL_PANE_PAGE)
        self.FILTER_NAME_ENTER.setObjectName("FILTER_NAME_ENTER")
        self.horizontalLayout_26.addWidget(self.FILTER_NAME_ENTER)
        
        self.FILTER_FARK_ENTER = QtWidgets.QLineEdit(self.CONTROL_PANE_PAGE)
        self.FILTER_FARK_ENTER.setObjectName("FILTER_FARK_ENTER")
        self.horizontalLayout_26.addWidget(self.FILTER_FARK_ENTER)
        self.verticalLayout_14.addLayout(self.horizontalLayout_26)
        
        self.ALLEXCHANGE_TB_W = QtWidgets.QTableWidget(self.CONTROL_PANE_PAGE)
        self.ALLEXCHANGE_TB_W.setObjectName("ALLEXCHANGE_TB_W")
        self.ALLEXCHANGE_TB_W.setColumnCount(0)
        self.ALLEXCHANGE_TB_W.setRowCount(0)
        self.verticalLayout_14.addWidget(self.ALLEXCHANGE_TB_W)
        self.horizontalLayout_28.addLayout(self.verticalLayout_14)
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        
        self.MAIN_SQL_TB_W = QtWidgets.QTableWidget(self.CONTROL_PANE_PAGE)
        self.MAIN_SQL_TB_W.setObjectName("MAIN_SQL_TB_W")
        self.MAIN_SQL_TB_W.setColumnCount(0)
        self.MAIN_SQL_TB_W.setRowCount(0)
        self.verticalLayout_15.addWidget(self.MAIN_SQL_TB_W)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        
        self.ADMINTABLO_TB_W = QtWidgets.QTableWidget(self.CONTROL_PANE_PAGE)
        self.ADMINTABLO_TB_W.setObjectName("ADMINTABLO_TB_W")
        self.ADMINTABLO_TB_W.setColumnCount(0)
        self.ADMINTABLO_TB_W.setRowCount(0)
        self.horizontalLayout_27.addWidget(self.ADMINTABLO_TB_W)
        
        self.SQLELECTRA_TB_W = QtWidgets.QTableWidget(self.CONTROL_PANE_PAGE)
        self.SQLELECTRA_TB_W.setObjectName("SQLELECTRA_TB_W")
        self.SQLELECTRA_TB_W.setColumnCount(0)
        self.SQLELECTRA_TB_W.setRowCount(0)
        self.horizontalLayout_27.addWidget(self.SQLELECTRA_TB_W)
        self.verticalLayout_15.addLayout(self.horizontalLayout_27)
        self.horizontalLayout_28.addLayout(self.verticalLayout_15)
        self.verticalLayout_7.addLayout(self.horizontalLayout_28)
        self.verticalLayout_16.addLayout(self.verticalLayout_7)
        self.tabWidget.addTab(self.CONTROL_PANE_PAGE, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        #----------------Контекстное меню--------------------------
        #ui->tableWidget->setSelectionBehavior(QAbstractItemView::SelectRows)
        self.KASA_PAGE.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.GIDERLER_TB_W.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.NAKIT_TB_W.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.DOVIZ_TB_W.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.HAMAM_WIFI_ENTER.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.HAVLU_DEGISIM_ENTER.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.YEDEK_ANAHTAR_TB_W.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.FITNES_ANAHTAR_TB_W.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.HAVLU_TB_W.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.NESILDI_TB_W.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TESLIM_TB_W.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.MAIN_SQL_TB_W.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.SQLELECTRA_TB_W.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) 
        #self.ADMINTABLO_TB_W.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ALLEXCHANGE_TB_W.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #   настройка выбора столбцов  
        self.GIDERLER_TB_W.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.NAKIT_TB_W.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.DOVIZ_TB_W.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.HAMAM_WIFI_ENTER.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.HAVLU_DEGISIM_ENTER.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.YEDEK_ANAHTAR_TB_W.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.FITNES_ANAHTAR_TB_W.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.HAVLU_TB_W.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.NESILDI_TB_W.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.TESLIM_TB_W.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.MAIN_SQL_TB_W.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.SQLELECTRA_TB_W.setSelectionBehavior(QtWidgets.QTableView.SelectRows) 
        self.ADMINTABLO_TB_W.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.ALLEXCHANGE_TB_W.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        #настройка выбора строк в таблицах 
        self.GIDERLER_TB_W.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.NAKIT_TB_W.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.DOVIZ_TB_W.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.HAMAM_WIFI_ENTER.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.HAVLU_DEGISIM_ENTER.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.YEDEK_ANAHTAR_TB_W.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.FITNES_ANAHTAR_TB_W.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.HAVLU_TB_W.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.NESILDI_TB_W.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.TESLIM_TB_W.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.MAIN_SQL_TB_W.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.SQLELECTRA_TB_W.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection) 
        self.ADMINTABLO_TB_W.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ALLEXCHANGE_TB_W.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
#--------------------------------------------------------------------------------------------------------------
        self.permision_mixer(Hotel_Project)
        
       # self.my_events( Hotel_Project)
#--------------------------------------------------------------------------------------------------------------
        self.retranslateUi(Hotel_Project)
        self.tabWidget.setCurrentIndex(0)
        
        QtCore.QMetaObject.connectSlotsByName(Hotel_Project)
    def permision_mixer(self,Hotel_Project):
        #----------------------------------------------------------------------------------------------------
        time_elem=Sql_Query()
        permision_user=time_elem.ALL_SQL_AT_ONE('select',3,4,'')
        #Система работы будет дурная . Идет обращение к таблице Now где береться уровень доступа 
        #После от него идет отрисовка данных, страниц, и функционал 
        #уровней будет 6 от  0 до 5 
        #0-1 полный доступ только 1й не знает о 0м 
        # 2 имеет не полный доступ только к панеле admin
        #3  доступ к полным 4 панелям 
        #4 не полный доступ к 4 панелям 
        #5 ограниченный доступ к панелям второй ключь фитнес и полотенца 
        #----------------------------------------------------------------------------------------------------
        if permision_user[0][0]=='5':
            #может просмотреть и распичатать данные с вкладок фитнес ключь полотенце
            self.tabWidget.removeTab(0)
            self.tabWidget.removeTab(3)
        elif permision_user[0][0]=='4':
            #может вносить и удалять данные с вкладок ключь полотенце фитнес
            self.tabWidget.removeTab(0)
            self.tabWidget.removeTab(3)
        elif permision_user[0][0]=='3':
            #может делать кассу и вносить -удалять данные с вкладок каса ключь  полотенце
            self.tabWidget.removeTab(4)
        elif permision_user[0][0]=='2':
            self.ADMINTABLO_TB_W.setVisible(False)
            self.SQLELECTRA_TB_W.setVisible(False)
            self.MAIN_SQL_TB_W.setVisible(False)
        elif permision_user[0][0]=='1':
            pass;
    #Создание имен которые отображаются на этих обьектах
    def retranslateUi(self, Hotel_Project):
        _translate = QtCore.QCoreApplication.translate
        #Hotel_Project.setWindowTitle(_translate("Hotel_Project", "KASA DEVIR TESLIM FORMU "+time.strftime("%d.%m.%Y %H:%M:%S")))
        self.label.setText(_translate("Hotel_Project", "AVANS"))
        self.label_8.setText(_translate("Hotel_Project", "NAKIT"))
        self.label_2.setText(_translate("Hotel_Project", "GIDERLER"))
        self.label_3.setText(_translate("Hotel_Project", "EURO"))
        self.label_4.setText(_translate("Hotel_Project", "    TL  "))
        self.label_6.setText(_translate("Hotel_Project", "DOVIZ"))
        self.label_5.setText(_translate("Hotel_Project", "NAKIT"))
        self.label_9.setText(_translate("Hotel_Project", "FARK"))
        self.label_7.setText(_translate("Hotel_Project", "TESLIIM VERILDI"))
        self.label_12.setText(_translate("Hotel_Project", "TESLIM ALDI"))
        self.label_11.setText(_translate("Hotel_Project", "HAVLU DEGISIM"))
        self.label_10.setText(_translate("Hotel_Project", "HAMAM WIFI    "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.KASA_PAGE), _translate("Hotel_Project", "KASA"))
        self.label_13.setText(_translate("Hotel_Project", "TOPLAM"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.YEDEK_ANAHTAR_PAGE), _translate("Hotel_Project", "YEDEK ANAHTAR"))
        self.label_16.setText(_translate("Hotel_Project", "TOPLAM"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.FITNES_ANAHTAR_PAGE), _translate("Hotel_Project", "FITNES ANAHTAR"))
        self.label_14.setText(_translate("Hotel_Project", "TOPLAM"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.HAVLU_PAGE), _translate("Hotel_Project", "HAVLU"))
        self.STANDART_CB.setText(_translate("Hotel_Project", "STANDART"))
        self.AVANS_VE_NAKIT_CB.setText(_translate("Hotel_Project", "AVANS VE NAKIT"))
        self.NAKIT_PARA_CB.setText(_translate("Hotel_Project", "NAKIT PARA"))
        self.GIDERLER_CB.setText(_translate("Hotel_Project", "GIDERLER"))
        self.DOVIZ_CB.setText(_translate("Hotel_Project", "DOVIZ"))
        self.DEMIR_PARA_CB.setText(_translate("Hotel_Project", "DEMIR PARA"))
        self.HAVLU_DEGISIK_CB.setText(_translate("Hotel_Project", "HAVLU DEGISIK"))
        self.HAMAM_WIFI_CB.setText(_translate("Hotel_Project", "HAMAM WIFI"))
        self.YEDEK_ANAHTAR_CB.setText(_translate("Hotel_Project", "YEDEK ANAHTAR"))
        self.FITNES_CB.setText(_translate("Hotel_Project", "FITNES"))
        self.HAVLU_CB.setText(_translate("Hotel_Project", "HAVLU"))
        self.ADMIN_CB.setText(_translate("Hotel_Project", "ADMIN"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CONTROL_PANE_PAGE), _translate("Hotel_Project", "CONTROL PANEL"))
    #---------------------------------------------------------------------------------------------------------------------------------------------------------
    #Рассылка на почту
    def send_my_report(self):
        global Hotel_parthT
        Hotel_parth=Hotel_parthT
        MYSQ=Sql_Query()
        fromaddr = "workeritman@gmail.com"
        my_email_adres=MYSQ.ALL_SQL_AT_ONE('select',4,2,'')[0][0]
        
        if not my_email_adres:
            pass
        else:
            # instance of MIMEMultipart
            msg = MIMEMultipart()
            
            self.print_funct(self, [Hotel_parth.KASA_PAGE,'Hotel_parth.KASA_PAGE',0,0],'to email')
            # open the file to be sent 
            filename = "tosend.pdf"
            # тут с адресом нужно что нибуть нахимичить
            attachment = open("tosend.pdf", "rb")
            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')
            # To change the payload into encoded form
            p.set_payload((attachment).read())
            # encode into base64
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            # attach the instance 'p' to instance 'msg'
            msg.attach(p)
            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
            # start TLS for security
            s.starttls()
            # Authentication
            s.login(fromaddr, '123worker123')
            # Converts the Multipart msg into a string
            text = msg.as_string()
            # sending the mail
            s.sendmail(fromaddr, my_email_adres, text)
            # terminating the session
            s.quit()
    #--------------------------функции подсчетов -------------------------------------------------------------------------------------------------------------
    def big_sum(self):
        global Hotel_parthT
        Hotel_parth=Hotel_parthT
        MYSQ=Sql_Query()
        base_result=MYSQ.ALL_SQL_AT_ONE('select',2,2,'')
        first_elem=MYSQ.ALL_SQL_AT_ONE('else',2,'{}'.format(base_result[0][0]),'')
        second_elem=MYSQ.ALL_SQL_AT_ONE('else',2,'{}'.format(base_result[1][0]),'')
        result=first_elem[0][0]-second_elem[0][0]
        
        Hotel_parth.FARK_ENTER.setDisabled(False)
        Hotel_parth.FARK_ENTER.setText(str(format(result,'.2f')))
        Hotel_parth.FARK_ENTER.setAlignment(QtCore.Qt.AlignCenter)
        Hotel_parth.FARK_ENTER.setDisabled(True)
        
    def small_sum(self):
        global Hotel_parthT
        Hotel_parth=Hotel_parthT
        MYSQ=Sql_Query()
        base_result_fitnes=MYSQ.ALL_SQL_AT_ONE('else',2,'SELECT sum(usd) ,sum(euro), sum(ruble) from fitneskey ','')
        base_result_second_key=MYSQ.ALL_SQL_AT_ONE('else',2,'SELECT sum(usd) ,sum(euro), sum(ruble) from doublekey ','')
        base_result_towel=MYSQ.ALL_SQL_AT_ONE('else',2,'SELECT sum(kachavlualindi) from havlu ','')

        Hotel_parth.Y_TOTAL_DOLLAR_ENTER.setDisabled(False)
        Hotel_parth.Y_TOTAL_EURO_ENTER.setDisabled(False)
        Hotel_parth.Y_TOTAL_RUBLE_ENTER.setDisabled(False)

        Hotel_parth.F_TOTAL_DOLLAR_ENTER.setDisabled(False)
        Hotel_parth.F_TOTAL_EURO_ENTER.setDisabled(False)
        Hotel_parth.F_TOTAL_RUBLE_ENTER.setDisabled(False)

        Hotel_parth.H_TOTAL_HAVLU_ENTER.setDisabled(False)
        #---------------------------------------------------
        Hotel_parth.Y_TOTAL_DOLLAR_ENTER.setText(str(format(base_result_second_key[0][0],'.2f')))
        Hotel_parth.Y_TOTAL_EURO_ENTER.setText(str(format(base_result_second_key[0][1],'.2f')))
        Hotel_parth.Y_TOTAL_RUBLE_ENTER.setText(str(format(base_result_second_key[0][2],'.2f')))

        Hotel_parth.F_TOTAL_DOLLAR_ENTER.setText(str(format(base_result_fitnes[0][0],'.2f')))
        Hotel_parth.F_TOTAL_EURO_ENTER.setText(str(format(base_result_fitnes[0][1],'.2f')))
        Hotel_parth.F_TOTAL_RUBLE_ENTER.setText(str(format(base_result_fitnes[0][2],'.2f')))

        Hotel_parth.H_TOTAL_HAVLU_ENTER.setText(str(format(base_result_towel[0][0])))
        #---------------------------------------------------
        Hotel_parth.Y_TOTAL_DOLLAR_ENTER.setAlignment(QtCore.Qt.AlignCenter)
        Hotel_parth.Y_TOTAL_EURO_ENTER.setAlignment(QtCore.Qt.AlignCenter)
        Hotel_parth.Y_TOTAL_RUBLE_ENTER.setAlignment(QtCore.Qt.AlignCenter)

        Hotel_parth.F_TOTAL_DOLLAR_ENTER.setAlignment(QtCore.Qt.AlignCenter)
        Hotel_parth.F_TOTAL_EURO_ENTER.setAlignment(QtCore.Qt.AlignCenter)
        Hotel_parth.F_TOTAL_RUBLE_ENTER.setAlignment(QtCore.Qt.AlignCenter)

        Hotel_parth.H_TOTAL_HAVLU_ENTER.setAlignment(QtCore.Qt.AlignCenter)
        #---------------------------------------------------
        Hotel_parth.Y_TOTAL_DOLLAR_ENTER.setDisabled(True)
        Hotel_parth.Y_TOTAL_EURO_ENTER.setDisabled(True)
        Hotel_parth.Y_TOTAL_RUBLE_ENTER.setDisabled(True)

        Hotel_parth.F_TOTAL_DOLLAR_ENTER.setDisabled(True)
        Hotel_parth.F_TOTAL_EURO_ENTER.setDisabled(True)
        Hotel_parth.F_TOTAL_RUBLE_ENTER.setDisabled(True)

        Hotel_parth.H_TOTAL_HAVLU_ENTER.setDisabled(True)
        
    def different_was_change(self):
        global Hotel_parthT
        Hotel_parth=Hotel_parthT
        MYSQ=Sql_Query()
        Hotel_parth.FARK_ENTER.setDisabled(False)
        result=Hotel_parth.FARK_ENTER.text()

        want_or_no=MYSQ.ALL_SQL_AT_ONE('select',4,3,'')[0][0]
        min_max=int(MYSQ.ALL_SQL_AT_ONE('select',5,3,'')[0][0])
        #---в дальнейшее для отправки пдф 
        if want_or_no=='yes':
            if min_max>0:
                if float(result)>min_max:
                   self.send_my_report()
                   if os.path.exists("tosend.pdf"):
                       os.remove("tosend.pdf")
                   else:
                        pass;
            elif min_max<0:
                if float(result)<min_max:
                   self.send_my_report()
                   if os.path.exists("tosend.pdf"):
                       os.remove("tosend.pdf")
                   else:
                        pass;
            else:
                pass;
        elif want_or_no=='no':
            pass;
        else:
            pass;

        
        Hotel_parth.FARK_ENTER.setDisabled(True)
        name_from_now=MYSQ.ALL_SQL_AT_ONE('select',3,2,'')[0][0]
        #print('name_from_now',name_from_now)
        datanowT=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        MYSQ.ALL_SQL_AT_ONE('insert',1,[2,3,4],[datanowT,name_from_now,result])
    #---------------------------------------------------------------------------------------------------------------------------------------------------------
    #Вспомогательная функция 1 к общему отображению данных
    #Создание двух переменных в которых хронятся название столбцов и количество строк в соответсвенной таблице вохможно позже перенести в соответвенный класс
    def write_to_TB_W(self,ClasS_part,table_name):
        arrive_name_of_count=None
        count_of_rows=None
        #print('table_name',table_name)
        #print(type(table_name))
        time_aray=[]
        double_time_array=[]
        id_dict={ 
                0:[2,3,4,5],
                1:[2,3,4,5,8,9],
                2:[2,3,4,5,6,7],
                3:[2,3,4,5,16,22],
                4:[2,3,4,5,18,19,20],
                5:[2,3,4,5,14,15],
                6:[2,3,4,5,11,12,13],
                7:[2,3,4,5,11,12],
                8:[2,3,4,5,21,22,23,24,10,11,12,17,26,27],
                9:[2,3,4,5,21,22,23,24,10,11,12,17,26,27],
                10:[2,3,4,5,21,22,23,24,25,26,27],
                11:[2,3,4,5,28,29]
                }
        
        if type(table_name)==list:
            arrive_name_of_count=ClasS_part.ALL_SQL_AT_ONE('else',6,'PRAGMA TABLE_INFO({})'.format(table_name[0]),'')
            for elem_of_mass in arrive_name_of_count:
                    time_aray.append(elem_of_mass[1])

            count_of_rows=int(Global_funck_of_Nothing().only_number(str(ClasS_part.ALL_SQL_AT_ONE('else',6,'Select count(*) from {}'.format(table_name[0]),''))))
            del time_aray[0]
            for i in range(0,len(id_dict[table_name[1]])):
                
                double_time_array.append(time_aray[id_dict[table_name[1]][i]-2])
            time_aray=double_time_array
        else:
            arrive_name_of_count=ClasS_part.ALL_SQL_AT_ONE('else',6,'PRAGMA TABLE_INFO({})'.format(table_name),'')

            for elem_of_mass in arrive_name_of_count:
                time_aray.append(elem_of_mass[1])

            count_of_rows=int(Global_funck_of_Nothing().only_number(str(ClasS_part.ALL_SQL_AT_ONE('else',6,'Select count(*) from {}'.format(table_name),''))))
            del time_aray[0]
        return time_aray,count_of_rows
    #selecet_mode= 'select', elem_part1='', elem_part2=''
    #Вспомогательная функция 2 к общему отображению данных
    #Запись данных во все таблицы /вспомогательная функция к Show_Data
    def write_data(self,ClasS_part,Name_TB_W,TB_ID,selecet_mode, elem_part1, elem_part2):
        permisionT=ClasS_part.ALL_SQL_AT_ONE('select',3,4,'')[0][0]
        name_dict={10:'giderler',8:'doviz',7:'doublekey',9:'fitneskey',12:'havlu'}
        
        #if TB_ID==10:
           # count_row=int(Global_funck_of_Nothing().only_number(str(ClasS_part.ALL_SQL_AT_ONE('else',TB_ID,'Select count(*) from {}'.format(name_dict[TB_ID]),''))))
        #    for row_number,row_data in enumerate(ClasS_part.ALL_SQL_AT_ONE(selecet_mode,TB_ID,elem_part1,elem_part2)):           
        #        for column_number,data in enumerate(row_data[1::]):
                    
        #            if data==0  and count_row==1:
        #                data=''
        #                Name_TB_W.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
        #            else:
        #                Name_TB_W.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
        #elif TB_ID==8:
        #    count_row=int(Global_funck_of_Nothing().only_number(str(ClasS_part.ALL_SQL_AT_ONE('else',TB_ID,'Select count(*) from {}'.format(name_dict[TB_ID]),''))))
        #    for row_number,row_data in enumerate(ClasS_part.ALL_SQL_AT_ONE(selecet_mode,TB_ID,elem_part1,elem_part2)):           
        #        for column_number,data in enumerate(row_data[1::]):
        #            
        #            if (column_number==1 or column_number==2 and data==0) and count_row==1:
        #                for column_num,data in enumerate(row_data):
        #                    data=''
        #                    Name_TB_W.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
        #            else:
        #                Name_TB_W.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
        #elif TB_ID==7:
        #    count_row=int(Global_funck_of_Nothing().only_number(str(ClasS_part.ALL_SQL_AT_ONE('else',TB_ID,'Select count(*) from {}'.format(name_dict[TB_ID]),''))))
        #    for row_number,row_data in enumerate(ClasS_part.ALL_SQL_AT_ONE(selecet_mode,TB_ID,elem_part1,elem_part2)):           
        #        for column_number,data in enumerate(row_data[1::]):
        #           
        #            if data==0 and count_row==1:
        #                data=''
        #                Name_TB_W.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
        #            else:
        #                Name_TB_W.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
        #elif TB_ID==9:
        #    count_row=int(Global_funck_of_Nothing().only_number(str(ClasS_part.ALL_SQL_AT_ONE('else',TB_ID,'Select count(*) from {}'.format(name_dict[TB_ID]),''))))
        #    for row_number,row_data in enumerate(ClasS_part.ALL_SQL_AT_ONE(selecet_mode,TB_ID,elem_part1,elem_part2)):           
        #        for column_number,data in enumerate(row_data[1::]):
        #            
        #            if data==0 and count_row==1:
        #                data=''
        #                Name_TB_W.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
        #            else:
        #                Name_TB_W.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
        #elif TB_ID==12:
        #    count_row=int(Global_funck_of_Nothing().only_number(str(ClasS_part.ALL_SQL_AT_ONE('else',TB_ID,'Select count(*) from {}'.format(name_dict[TB_ID]),''))))
        #    for row_number,row_data in enumerate(ClasS_part.ALL_SQL_AT_ONE(selecet_mode,TB_ID,elem_part1,elem_part2)):           
        #        for column_number,data in enumerate(row_data[1::]):
        #            
        #            if data==0 and count_row==1:
        #                data=''
        #                Name_TB_W.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
        #            else:
        #                Name_TB_W.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
        #else:
        if TB_ID==16:
                  for row_number,row_data in enumerate(ClasS_part.ALL_SQL_AT_ONE(selecet_mode,TB_ID,elem_part1,elem_part2)):           
                      for column_number,data in enumerate(row_data):
                          Name_TB_W.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))

        else:
                for row_number,row_data in enumerate(ClasS_part.ALL_SQL_AT_ONE(selecet_mode,TB_ID,elem_part1,elem_part2)):           
                    for column_number,data in enumerate(row_data[1::]):
                        Name_TB_W.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
    #Королева балла по отображению данных во всей проге /есть две вспомогательные функции сверху 
    def show_data(self,Hotel_parth,ClasS_part,array_of_names):
        global Hotel_parthT
        Hotel_parthT=Hotel_parth
        time_array_of_name_from_Now_table=None
        permisionT=ClasS_part.ALL_SQL_AT_ONE('select',3,4,'')[0][0]
        #Вывод данных с фильтрацией 
        if array_of_names[0]=='':
             id_dict={0:4,1:6,2:6,3:6,4:9,5:6,6:9,7:6,8:14,9:14,10:11,11:6}
             tablo_name_dict={0:'Standart',1:'Avans ve Nakit',2:'Nakit para', 3:'Giderler', 4:'Doviz',5:'Demir Para',6:'Havlu Degisik',7:'Hamam WiFi', 8:'Yedek Anahtar', 9:'Fitnes', 10:'Sahil Havlu',11:'Admin' }
             rows_name_dict={ 
                0:[2,3,4,5],
                1:[2,3,4,5,8,9],
                2:[2,3,4,5,6,7],
                3:[2,3,4,5,16,22],
                4:[2,3,4,5,18,19,20],
                5:[2,3,4,5,14,15],
                6:[2,3,4,5,11,12,13],
                7:[2,3,4,5,11,12],
                8:[2,3,4,5,10,11,12,17,21,22,23,24,26,27],
                9:[2,3,4,5,10,11,12,17,21,22,23,24,26,27],
                10:[2,3,4,5,21,22,23,24,25,26,27],
                11:[2,3,4,5,28,29]
                }
             midle_array=[] 
             uni_array=[[Hotel_parth.YEDEK_ANAHTAR_TB_W,'doublekey',7],
                       [Hotel_parth.FITNES_ANAHTAR_TB_W,'fitneskey',9],[Hotel_parth.HAVLU_TB_W,'havlu',12],
                       [Hotel_parth.ALLEXCHANGE_TB_W,'Allexchange',1],
                       [Hotel_parth.NESILDI_TB_W,'nesildi',16]]

             for part_of_array in uni_array:
                 if part_of_array[2]==array_of_names[2][2]:
                    
                    if part_of_array[2]==16:
                        midle_array.append(part_of_array[1])
                        midle_array.append(array_of_names[2][4])
                        array_of_namesT,count_of_rows=self.write_to_TB_W(ClasS_part,midle_array)
                    else:
                        array_of_namesT,count_of_rows=self.write_to_TB_W(ClasS_part,part_of_array[1])
                    time_array_of_name_from_Now_table=ClasS_part.ALL_SQL_AT_ONE('select',3,2,'')

                    #part_of_array[0].setRowCount(count_of_rows)
                    part_of_array[0].setColumnCount(len(array_of_namesT))
                    part_of_array[0].setHorizontalHeaderLabels(array_of_namesT)
                    part_of_array[0].verticalHeader().hide()
                    headers = part_of_array[0].horizontalHeader()

                    for i in range(0,len(array_of_namesT)):

                        headers.setSectionResizeMode(i,QtWidgets.QHeaderView.Stretch)

                    if  permisionT!='1' and permisionT!='0' and part_of_array[1]=='Allexchange':
                        array_of_names[2][0].append(3)
                        array_of_names[2][1].append(time_array_of_name_from_Now_table[0][0])

                        part_of_array[0].clearContents()
                        count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],array_of_names[1],[array_of_names[2][0],array_of_names[2][1]]))
                        part_of_array[0].setRowCount(count_of_rows)
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select',array_of_names[1],[array_of_names[2][0],array_of_names[2][1]])
                    elif  permisionT!='1' and permisionT!='0' and part_of_array[1]=='nesildi':
                        #print('Работа не под Кенаном')
                        #print('Начальные данные ',array_of_names)
                        #print('первое изменение данных')
                        #print('Добавление имени и номера соответсвенного поля в запрос на выборку ')
                        array_of_names[2][0].append(3)
                        array_of_names[2][1].append(time_array_of_name_from_Now_table[0][0])
                        #вставка переменных в массив 
                        #print('После первого изменения данные ',array_of_names)
                        #print('второе изменение данных')
                        #print('Вставка полей для конкретного вывода данных ')
                        array_of_names[1].insert(1,rows_name_dict[array_of_names[2][4]])
                        #print('Изменения способа сравнения в запросе ')
                        array_of_names[1].insert(2,' like ')
                        #print('После второго изменения данные ',array_of_names)
                        #print('третье возможное не большое изменение')
                        #print('Добавление конретной таблицы для поиска если не выбранная кнопка Standart')
                        if tablo_name_dict[array_of_names[2][4]]!='Standart':
                            array_of_names[2][0].append(4)
                            array_of_names[2][1].append(tablo_name_dict[array_of_names[2][4]])
                        else:
                            pass;
                        #print('После третьего изменения данные ',array_of_names)
                        #print('Очистка таблицы')
                        part_of_array[0].clearContents()
                        count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],array_of_names[1],[array_of_names[2][0],array_of_names[2][1]]))
                        part_of_array[0].setRowCount(count_of_rows)
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select',array_of_names[1],[array_of_names[2][0],array_of_names[2][1]])
                    elif (permisionT=='1' or permisionT=='0') and part_of_array[1]=='nesildi':
                            #print('--------------------Работа под логином Кенан -----------------------------------')
                            #print('Начальные  данные ',array_of_names)
                            #print('первое изменение данных')
                            #print('вставка полей для конкретного  вывода')
                            array_of_names[1].insert(1,rows_name_dict[array_of_names[2][4]])
                            #print('Изменение способа сравнение в запросе ')
                            array_of_names[1].insert(2,' like ')
                            #print('После первого изменения данные ',array_of_names)
                            #print('Второе изменение данных')
                            #print('Добавление конретной таблицы для поиска если не выбранная кнопка Standart')
                            if tablo_name_dict[array_of_names[2][4]]!='Standart':
                                array_of_names[2][0].append(4)
                                array_of_names[2][1].append(tablo_name_dict[array_of_names[2][4]])
                            else:
                                pass;
                            #print('После второго изменения данных')
                            #print('После вторго изменения данные ',array_of_names)
                            #print('Провека данных для условия where ')
                            part_of_array[0].clearContents()
                            count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],array_of_names[1],[array_of_names[2][0],array_of_names[2][1]]))
                            part_of_array[0].setRowCount(count_of_rows)
                            self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select',array_of_names[1],[array_of_names[2][0],array_of_names[2][1]])
                    else:
                        part_of_array[0].clearContents()
                        count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],array_of_names[1],[array_of_names[2][0],array_of_names[2][1]]))
                        part_of_array[0].setRowCount(count_of_rows)
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select',array_of_names[1],[array_of_names[2][0],array_of_names[2][1]])
        elif array_of_names[0]=='refresh':
            Hotel_parth.AVANS_ENTER.setText(str(ClasS_part.ALL_SQL_AT_ONE('select',14,2,'')[0][0]))
            Hotel_parth.NAKIT_ENTER.setText(str(ClasS_part.ALL_SQL_AT_ONE('select',14,3,'')[0][0]))
            Hotel_parth.D_EURO_ENTER.setText(Global_funck_of_Nothing().only_number(str(ClasS_part.ALL_SQL_AT_ONE('select',6,3,''))))
            Hotel_parth.D_TL_ENTER.setText(Global_funck_of_Nothing().only_number(str(ClasS_part.ALL_SQL_AT_ONE('select',6,2,''))))
            #Hotel_parth.TESLIM_VERILDI_ENTER.setText(array_of_names[2]+' '+array_of_names[3])
            #Hotel_parth.TESLIM_VERILDI_ENTER.setAlignment(QtCore.Qt.AlignCenter)
            #Hotel_parth.TESLIM_VERILDI_ENTER.setDisabled(True)
            #Hotel_parth.TESLIM_ALDI_ENTER.setText(array_of_names[0]+' '+array_of_names[1])
            #Hotel_parth.TESLIM_ALDI_ENTER.setAlignment(QtCore.Qt.AlignCenter)
            #Hotel_parth.TESLIM_ALDI_ENTER.setDisabled(True)
            uni_array=[[Hotel_parth.GIDERLER_TB_W,'giderler',10],[Hotel_parth.NAKIT_TB_W,'nakitt',15],
                       [Hotel_parth.DOVIZ_TB_W,'doviz',8],[Hotel_parth.HAMAM_WIFI_ENTER,'hamamwifi',11],
                       [Hotel_parth.HAVLU_DEGISIM_ENTER,'havludegisim',13],[Hotel_parth.YEDEK_ANAHTAR_TB_W,'doublekey',7],
                       [Hotel_parth.FITNES_ANAHTAR_TB_W,'fitneskey',9],[Hotel_parth.HAVLU_TB_W,'havlu',12],
                       [Hotel_parth.TESLIM_TB_W,'teslim',18],[Hotel_parth.ALLEXCHANGE_TB_W,'Allexchange',1],
                       [Hotel_parth.MAIN_SQL_TB_W,'MainSql',2],[Hotel_parth.SQLELECTRA_TB_W,'SQLELECTRA',4],
                       [Hotel_parth.ADMINTABLO_TB_W,'admintablo',5]]
            for part_of_array in uni_array:
                array_of_names,count_of_rows=self.write_to_TB_W(ClasS_part,part_of_array[1])
                part_of_array[0].setColumnCount(len(array_of_names))
                part_of_array[0].setHorizontalHeaderLabels(array_of_names)
                part_of_array[0].verticalHeader().hide()
                headers = part_of_array[0].horizontalHeader()
                for i in range(0,len(array_of_names)):
                    headers.setSectionResizeMode(i,QtWidgets.QHeaderView.Stretch)
                if  permisionT!='1' and permisionT!='0':
                    time_array_of_name_from_Now_table=ClasS_part.ALL_SQL_AT_ONE('select',3,2,'')
                    if part_of_array[1]=='nesildi':
                        #[1,29]
                        #print('tut',ClasS_part,part_of_array[0],part_of_array[2],'select',['WHERE','*'],[[3],[time_array_of_name_from_Now_table[0][0]]])
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select',['WHERE','*'],[[3],[time_array_of_name_from_Now_table[0][0]]])
                    if part_of_array[1]=='teslim':
                        #[1,5]
                        count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],['WHERE','*'],[[2,5],[time_array_of_name_from_Now_table[0][0],permisionT]]))
                        part_of_array[0].setRowCount(count_of_rows)
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select',['WHERE','*'],[[2,5],[time_array_of_name_from_Now_table[0][0],permisionT]])
                    elif part_of_array[1]=='Allexchange':
                        #[1,4]
                        count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],['WHERE','*'],[[3],[time_array_of_name_from_Now_table[0][0]]]))
                        part_of_array[0].setRowCount(count_of_rows)
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select',['WHERE','*'],[[3],[time_array_of_name_from_Now_table[0][0]]])
                    else:
                        count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],'',''))
                        part_of_array[0].setRowCount(count_of_rows)
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select','','')
                elif permisionT=='1':
                    if part_of_array[1]=='teslim':
                        count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('else',part_of_array[2],'select * from teslim where permision <> "0"',''))
                        part_of_array[0].setRowCount(count_of_rows)
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'else','select * from teslim where permision <> "0"','')
                    else:
                        count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],'',''))
                        part_of_array[0].setRowCount(count_of_rows)
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select','','')
                else:
                    count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],'',''))
                    part_of_array[0].setRowCount(count_of_rows)
                    self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select','','')
        #первое заполнение данных в tablewidget
        else:
            Hotel_parth.AVANS_ENTER.setText(str(ClasS_part.ALL_SQL_AT_ONE('select',14,2,'')[0][0]))
            Hotel_parth.NAKIT_ENTER.setText(str(ClasS_part.ALL_SQL_AT_ONE('select',14,3,'')[0][0]))
            Hotel_parth.D_EURO_ENTER.setText(Global_funck_of_Nothing().only_number(str(ClasS_part.ALL_SQL_AT_ONE('select',6,3,''))))
            Hotel_parth.D_TL_ENTER.setText(Global_funck_of_Nothing().only_number(str(ClasS_part.ALL_SQL_AT_ONE('select',6,2,''))))
            Hotel_parth.TESLIM_VERILDI_ENTER.setText(array_of_names[2]+' '+array_of_names[3])
            Hotel_parth.TESLIM_VERILDI_ENTER.setAlignment(QtCore.Qt.AlignCenter)
            Hotel_parth.TESLIM_VERILDI_ENTER.setDisabled(True)
            Hotel_parth.TESLIM_ALDI_ENTER.setText(array_of_names[0]+' '+array_of_names[1])
            Hotel_parth.TESLIM_ALDI_ENTER.setAlignment(QtCore.Qt.AlignCenter)
            Hotel_parth.TESLIM_ALDI_ENTER.setDisabled(True)
            uni_array=[[Hotel_parth.GIDERLER_TB_W,'giderler',10],[Hotel_parth.NAKIT_TB_W,'nakitt',15],
                       [Hotel_parth.DOVIZ_TB_W,'doviz',8],[Hotel_parth.HAMAM_WIFI_ENTER,'hamamwifi',11],
                       [Hotel_parth.HAVLU_DEGISIM_ENTER,'havludegisim',13],[Hotel_parth.YEDEK_ANAHTAR_TB_W,'doublekey',7],
                       [Hotel_parth.FITNES_ANAHTAR_TB_W,'fitneskey',9],[Hotel_parth.HAVLU_TB_W,'havlu',12],
                       [Hotel_parth.NESILDI_TB_W,'nesildi',16],[Hotel_parth.TESLIM_TB_W,'teslim',18],[Hotel_parth.ALLEXCHANGE_TB_W,'Allexchange',1],
                       [Hotel_parth.MAIN_SQL_TB_W,'MainSql',2],[Hotel_parth.SQLELECTRA_TB_W,'SQLELECTRA',4],
                       [Hotel_parth.ADMINTABLO_TB_W,'admintablo',5]]
            for part_of_array in uni_array:
                array_of_names,count_of_rows=self.write_to_TB_W(ClasS_part,part_of_array[1])
                part_of_array[0].setColumnCount(len(array_of_names))
                part_of_array[0].setHorizontalHeaderLabels(array_of_names)
                part_of_array[0].verticalHeader().hide()
                headers = part_of_array[0].horizontalHeader()
                for i in range(0,len(array_of_names)):
                    headers.setSectionResizeMode(i,QtWidgets.QHeaderView.Stretch)
                if  permisionT!='1' and permisionT!='0':
                    time_array_of_name_from_Now_table=ClasS_part.ALL_SQL_AT_ONE('select',3,2,'')
                    if part_of_array[1]=='nesildi':
                        #[1,29]
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select',['WHERE','*'],[[3],[time_array_of_name_from_Now_table[0][0]]])
                    if part_of_array[1]=='teslim':
                        #[1,5]
                        count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],['WHERE','*'],[[2,5],[time_array_of_name_from_Now_table[0][0],permisionT]]))
                        part_of_array[0].setRowCount(count_of_rows)
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select',['WHERE','*'],[[2,5],[time_array_of_name_from_Now_table[0][0],permisionT]])
                    elif part_of_array[1]=='Allexchange':
                        #[1,4]
                        count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],['WHERE','*'],[[3],[time_array_of_name_from_Now_table[0][0]]]))
                        part_of_array[0].setRowCount(count_of_rows)
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select',['WHERE','*'],[[3],[time_array_of_name_from_Now_table[0][0]]])
                    else:
                        count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],'',''))
                        part_of_array[0].setRowCount(count_of_rows)
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select','','')
                elif permisionT=='1':
                    if part_of_array[1]=='teslim':
                        count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('else',part_of_array[2],'select * from teslim where permision <> "0"',''))
                        part_of_array[0].setRowCount(count_of_rows)
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'else','select * from teslim where permision <> "0"','')
                    else:
                        count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],'',''))
                        part_of_array[0].setRowCount(count_of_rows)
                        self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select','','')
                else:
                    count_of_rows=len(ClasS_part.ALL_SQL_AT_ONE('select',part_of_array[2],'',''))
                    part_of_array[0].setRowCount(count_of_rows)
                    self.write_data(ClasS_part,part_of_array[0],part_of_array[2],'select','','')
        self.big_sum()
        self.small_sum()
    #--------------------------------------------------------------------------------------------------------------------------
    def get_data_from_qlineedits(self,tabid):
        global Hotel_parthT
        Hotel_parth=Hotel_parthT
        first_of_five_id=0
        emty_list_of_qlineEdits_data=[[],[],[],[],[]]
        list_of_filters=[[Hotel_parth.FILTER_TIME_ENTER,
                             Hotel_parth.FILTER_NAME_ENTER,
                             Hotel_parth.FILTER_FARK_ENTER],

                          [Hotel_parth.Y_FILTER_OD_NUM_ENTER,
                          Hotel_parth.Y_FILETR_ISI_ENTER,
                          Hotel_parth.Y_FILTER_GIR_TAR_ENTER,
                          Hotel_parth.Y_FILTER_CIK_TAR_ENTER,
                          Hotel_parth.Y_FILTER_USD_ENTER,
                          Hotel_parth.Y_FILTER_EURO_ENTER,
                          Hotel_parth.Y_FILTER_RUBLE_ENTER,
                          Hotel_parth.Y_FILTER_BAS_PAR_ENTER,
                          Hotel_parth.Y_FILTER_KIM_VER_ENTER,
                          Hotel_parth.Y_FILTER_KIM_YAZ_ENTER],

                          [Hotel_parth.F_FILTER_OD_NUM_ENTER,
                           Hotel_parth.F_FILETR_ISI_ENTER,
                           Hotel_parth.F_FILTER_GIR_TAR_ENTER,
                           Hotel_parth.F_FILTER_CIK_TAR_ENTER,
                           Hotel_parth.F_FILTER_USD_ENTER,
                           Hotel_parth.F_FILTER_EURO_ENTER,
                           Hotel_parth.F_FILTER_RUBLE_ENTER,
                           Hotel_parth.F_FILTER_BAS_PAR_ENTER,
                           Hotel_parth.F_FILTER_KIM_VER_ENTER,
                           Hotel_parth.F_FILTER_KIM_YAZ_ENTER],

                           [Hotel_parth.H_FILTER_OD_NUM_ENTER,
                            Hotel_parth.H_FILETR_ISI_ENTER,
                            Hotel_parth.H_FILTER_GIR_TAR_ENTER,
                            Hotel_parth.H_FILTER_CIK_TAR_ENTER,
                            Hotel_parth.H_FILTER_K_HAV_ENTER,
                            Hotel_parth.H_FILTER_KIM_VER_ENTER,
                            Hotel_parth.H_FILTER_KIM_YAZ_ENTER],

                            [Hotel_parth.FILTER_ZAM_ENTER,
                             Hotel_parth.FILTER_IS_ENTER,
                             Hotel_parth.FILTER_TAB_NAM_ENTER,
                             Hotel_parth.FILTER_NE_YAP_ENTER,
                             Hotel_parth.FILTER_00_ENTER,
                             Hotel_parth.FILTER_01_ENTER,
                             Hotel_parth.FILTER_02_ENTER,
                             Hotel_parth.FILTER_03_ENTER,
                             Hotel_parth.FILTER_04_ENTER,
                             Hotel_parth.FILTER_05_ENTER,
                             Hotel_parth.FILTER_06_ENTER,
                             Hotel_parth.FILTER_07_ENTER,
                             Hotel_parth.FILTER_08_ENTER,
                             Hotel_parth.FILTER_09_ENTER]]
        #проход по всем qlineedit для того что бы собрать значения в них и сформировать массив из этих данных 
        if tabid==4:
            for i in range(0,len(list_of_filters[0])):
                emty_list_of_qlineEdits_data[0].append(list_of_filters[0][i].text())
            for i in range(0,len(list_of_filters[4])):
                emty_list_of_qlineEdits_data[4].append(list_of_filters[4][i].text())
        else:
            for i in range(0,len(list_of_filters[tabid])):
                emty_list_of_qlineEdits_data[tabid].append(list_of_filters[tabid][i].text())
        return emty_list_of_qlineEdits_data
    
    def two_at_one_mix(self,event, signal_id, privet_elem, Hotel_parth):
        MYSQ=Sql_Query()
        list_of_filters=[self.FILTER_ZAM_ENTER,self.FILTER_IS_ENTER,self.FILTER_TAB_NAM_ENTER,
                         self.FILTER_NE_YAP_ENTER,self.FILTER_00_ENTER,self.FILTER_01_ENTER,
                         self.FILTER_02_ENTER,self.FILTER_03_ENTER,self.FILTER_04_ENTER,
                        self.FILTER_05_ENTER,self.FILTER_06_ENTER,self.FILTER_07_ENTER,self.FILTER_08_ENTER,self.FILTER_09_ENTER]
        id_dict={ 0:4, 1:6,  2:6,  3:6,    4:7, 5:6,  6:7, 7:6,  8:14, 9:14,  10:11, 11:6 }
        id_dic={ 
                0:[2,3,4,5],
                1:[2,3,4,5,8,9],
                2:[2,3,4,5,6,7],
                3:[2,3,4,5,16,22],
                4:[2,3,4,5,18,19,20],
                5:[2,3,4,5,14,15],
                6:[2,3,4,5,11,12,13],
                7:[2,3,4,5,11,12],
                8:[2,3,4,5,10,11,12,17,21,22,23,24,26,27],
                9:[2,3,4,5,10,11,12,17,21,22,23,24,26,27],
                10:[2,3,4,5,21,22,23,24,25,26,27],
                11:[2,3,4,5,28,29]
                }
        data_array=[]
        index_array=[]
        second_index_array=[]
        
        global for_sec_signal

        if signal_id==0:
                for i in range(0,id_dict[privet_elem]):
                        list_of_filters[i].setVisible(True)
                if id_dict[privet_elem]!=14:
                    for i in range(id_dict[privet_elem],len(list_of_filters)):
                        list_of_filters[i].setVisible(False)
                else:
                     pass;
                for_sec_signal=privet_elem
                self.show_data(Hotel_parth,MYSQ,['',['WHERE','*'],[[],[],16,id_dict[privet_elem],privet_elem]])
        elif signal_id==1:
            data_array=self.get_data_from_qlineedits(privet_elem)
            if privet_elem==4 :
                if (data_array[0][0]=='' and data_array[0][1]=='' and data_array[0][2]=='')and (data_array[4][0]=='' and data_array[4][1]=='' and data_array[4][2]=='' and data_array[4][3]=='' and data_array[4][4]=='' and data_array[4][5]==''and
                                       data_array[4][6]=='' and data_array[4][7]=='' and data_array[4][8]=='' and data_array[4][9]=='' and data_array[4][10]=='' and data_array[4][11]==''and
                                       data_array[4][12]=='' and data_array[4][13]==''):
                    self.show_data(Hotel_parth,MYSQ,['',['WHERE','*'],[[],[],16,id_dict[for_sec_signal],for_sec_signal]])
                    self.show_data(Hotel_parth,MYSQ,['',['WHERE','*'],[[],[],1]])
                elif (data_array[4][0]!='' or data_array[4][1]!='' or data_array[4][2]!='' or data_array[4][3]!='' or data_array[4][4]!='' or data_array[4][5]!=''or
                                       data_array[4][6]!='' or data_array[4][7]!='' or data_array[4][8]!='' or data_array[4][9]!='' or data_array[4][10]!='' or data_array[4][11]!=''or
                                       data_array[4][12]!='' or data_array[4][13]!='') and (data_array[0][0]=='' and data_array[0][1]=='' and data_array[0][2]==''):
                    for i in range(0,len(data_array[4])):
                        if data_array[4][i]:
                            index_array.append(id_dic[for_sec_signal][i])
                        else:
                            pass
                    data_array[4][:]=[item for item in data_array[4] if item !='']
                    self.show_data(Hotel_parth,MYSQ,['',['WHERE','like'],[index_array,data_array[4],16,id_dict[for_sec_signal],for_sec_signal]])
                    self.show_data(Hotel_parth,MYSQ,['',['WHERE','*'],[[],[],1]])
                elif (data_array[4][0]=='' and data_array[4][1]=='' and data_array[4][2]=='' and data_array[4][3]=='' and data_array[4][4]=='' and data_array[4][5]==''and
                                       data_array[4][6]=='' and data_array[4][7]=='' and data_array[4][8]=='' and data_array[4][9]=='' and data_array[4][10]=='' and data_array[4][11]==''and
                                       data_array[4][12]=='' and data_array[4][13]=='') and (data_array[0][0]!='' or data_array[0][1]!='' or data_array[0][2]!=''):
                    for i in range(0,len(data_array[0])):
                        if data_array[0][i]:
                            index_array.append(i+2)
                        else:
                            pass
                    data_array[0][:]=[item for item in data_array[0] if item !='']
                    self.show_data(Hotel_parth,MYSQ,['',['WHERE','like'],[index_array,data_array[0],1]])
                    self.show_data(Hotel_parth,MYSQ,['',['WHERE','*'],[[],[],16,id_dict[for_sec_signal],for_sec_signal]])
                elif (data_array[0][0]!='' or data_array[0][1]!='' or data_array[0][2]!='')and (data_array[4][0]!='' or data_array[4][1]!='' or data_array[4][2]!='' or data_array[4][3]!='' or data_array[4][4]!='' or data_array[4][5]!=''or
                                       data_array[4][6]!='' or data_array[4][7]!='' or data_array[4][8]!='' or data_array[4][9]!='' or data_array[4][10]!='' or data_array[4][11]!=''or
                                       data_array[4][12]!='' or data_array[4][13]!=''):
                    for i in range(0,len(data_array[4])):
                        if data_array[4][i]:
                            index_array.append(id_dic[for_sec_signal][i])
                        else:
                            pass
                    data_array[4][:]=[item for item in data_array[4] if item !='']
                    self.show_data(Hotel_parth,MYSQ,['',['WHERE','like'],[index_array,data_array[4],16,id_dict[for_sec_signal],for_sec_signal]])
                    #---------------------------------------------------------------------
                    for i in range(0,len(data_array[0])):
                        if data_array[0][i]:
                            second_index_array.append(i+2)
                        else:
                            pass
                    data_array[0][:]=[item for item in data_array[0] if item !='']
                    self.show_data(Hotel_parth,MYSQ,['',['WHERE','like'],[second_index_array,data_array[0],1]])
            else:
                # здесь отображаются таблицы с номерами 7 9 12 1-7я 2-9я 3-12я 
                list_of_tabindex={
                    1:7,
                    2:9,
                    3:12,
                    }
                for i in range(0,len(data_array[privet_elem])):
                        if data_array[privet_elem][i]:
                            index_array.append(i+2)
                        else:
                            pass
                data_array[privet_elem][:]=[item for item in data_array[privet_elem] if item !='']
                #=======================================================================================
                if  data_array[privet_elem] == []:
                    self.show_data(Hotel_parth,MYSQ,['',['WHERE','*'],[[],[],list_of_tabindex[privet_elem]]])
                else:
                    self.show_data(Hotel_parth,MYSQ,['',['WHERE','like'],[index_array,data_array[privet_elem],list_of_tabindex[privet_elem]]])
    #------------------------------------------------------------------------------------------------
    #функция с событиями фильтра на всех вкладках кроме каса
    def tabchage(self, event,Hotel_parth):
              tabid=self.tabWidget.currentIndex()
              if tabid ==1:
                  self.Y_FILTER_OD_NUM_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))  
                  self.Y_FILETR_ISI_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))  
                  self.Y_FILTER_GIR_TAR_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.Y_FILTER_CIK_TAR_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth)) 
                  self.Y_FILTER_USD_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth)) 
                  self.Y_FILTER_EURO_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.Y_FILTER_RUBLE_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth)) 
                  self.Y_FILTER_BAS_PAR_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.Y_FILTER_KIM_VER_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth)) 
                  self.Y_FILTER_KIM_YAZ_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.Y_TOTAL_DOLLAR_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.Y_TOTAL_EURO_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.Y_TOTAL_RUBLE_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
              elif tabid==2:
                  self.F_FILTER_OD_NUM_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.F_FILETR_ISI_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.F_FILTER_GIR_TAR_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.F_FILTER_CIK_TAR_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.F_FILTER_USD_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.F_FILTER_EURO_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth)) 
                  self.F_FILTER_RUBLE_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.F_FILTER_BAS_PAR_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.F_FILTER_KIM_VER_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.F_FILTER_KIM_YAZ_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.F_TOTAL_DOLLAR_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.F_TOTAL_EURO_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.F_TOTAL_RUBLE_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
              elif tabid ==3:
                  self.H_FILTER_OD_NUM_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.H_FILETR_ISI_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.H_FILTER_GIR_TAR_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.H_FILTER_CIK_TAR_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.H_FILTER_K_HAV_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.H_FILTER_KIM_VER_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.H_FILTER_KIM_YAZ_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.H_TOTAL_HAVLU_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
              elif tabid==4:
                  self.STANDART_CB.setChecked(True)
                  self.two_at_one_mix(self,0, 0, Hotel_parth)

                  self.FILTER_ZAM_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_IS_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_TAB_NAM_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_NE_YAP_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_00_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_01_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_02_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth)) 
                  self.FILTER_03_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_04_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_05_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_06_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_07_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_08_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_09_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))

                  self.FILTER_TIME_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_NAME_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
                  self.FILTER_FARK_ENTER.textChanged.connect(lambda time_test: self.two_at_one_mix(time_test,1,tabid,Hotel_parth))
    #Описание событий с этими элементами при нажатии 
    def my_events(self, Hotel_parth):
              ControlPart=Global_funck_of_Nothing()
              MYSQ=Sql_Query()
              uni_array=[
                   [Hotel_parth.GIDERLER_TB_W,'giderler',10,2],
                   [Hotel_parth.NAKIT_TB_W,'nakitt',15,1],
                   [Hotel_parth.DOVIZ_TB_W,'doviz',8,3],
                   [Hotel_parth.HAMAM_WIFI_ENTER,'hamamwifi',11,2],
                   [Hotel_parth.HAVLU_DEGISIM_ENTER,'havludegisim',13,3],
                   [Hotel_parth.YEDEK_ANAHTAR_TB_W,'doublekey',7,10],
                   [Hotel_parth.FITNES_ANAHTAR_TB_W,'fitneskey',9,10],
                   [Hotel_parth.HAVLU_TB_W,'havlu',12,7],
                   [Hotel_parth.NESILDI_TB_W,'nesildi',16,10],
                   [Hotel_parth.TESLIM_TB_W,'teslim',18,4],
                   [Hotel_parth.ALLEXCHANGE_TB_W,'Allexchange',1,3],
                   [Hotel_parth.MAIN_SQL_TB_W,'MainSql',2,2],
                   [Hotel_parth.SQLELECTRA_TB_W,'SQLELECTRA',4,2],
                   [Hotel_parth.ADMINTABLO_TB_W,'admintablo',5,2],
                   [Hotel_parth.KASA_PAGE,'Hotel_parth.KASA_PAGE',0,0]]
             
              #------------------------------------------Позже значение функции ControlPart передать в функцию Insert------------------------------------------------
                #Ui_update_and_insert.update_for_one_line_edit(self,result,number_table,numbrer_row) 14/2 14/3 6/2 6/3 
              Hotel_parth.AVANS_ENTER.textChanged.connect(lambda time_test: Ui_update_and_insert.update_for_one_line_edit(self,ControlPart.big_check_funk(time_test,Hotel_parth.AVANS_ENTER.text(),'0.0=+',Hotel_parth.AVANS_ENTER),14,2))
              #Hotel_parth.AVANS_ENTER.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,Hotel_parth.AVANS_ENTER.text(),'0.0=+',Hotel_parth.AVANS_ENTER))
              
              Hotel_parth.NAKIT_ENTER.textChanged.connect(lambda time_test: Ui_update_and_insert.update_for_one_line_edit(self,ControlPart.big_check_funk(time_test,Hotel_parth.NAKIT_ENTER.text(),'0.0=+',Hotel_parth.NAKIT_ENTER),14,3))
              #Hotel_parth.NAKIT_ENTER.textChanged.connect(lambda time_test: ControlPart.big_check_funk(time_test,Hotel_parth.NAKIT_ENTER.text(),'0.0=+',Hotel_parth.NAKIT_ENTER))
              
              #6/2 6/3
              Hotel_parth.D_TL_ENTER.textChanged.connect(lambda time_test: Ui_update_and_insert.update_for_one_line_edit(self,ControlPart.big_check_funk(time_test,Hotel_parth.D_TL_ENTER.text(),'0=+',Hotel_parth.D_TL_ENTER),6,2))
              Hotel_parth.D_EURO_ENTER.textChanged.connect(lambda time_test: Ui_update_and_insert.update_for_one_line_edit(self,ControlPart.big_check_funk(time_test,Hotel_parth.D_EURO_ENTER.text(),'0=+',Hotel_parth.D_EURO_ENTER),6,3))
              Hotel_parth.FARK_ENTER.textChanged.connect(self.different_was_change)
              #-------------------------------------------РАБОТА С ЭТИМ ----------------------------------------------------------
              Hotel_parth.tabWidget.currentChanged.connect(lambda time_test: self.tabchage(time_test,Hotel_parth))
              #----------------------------------------------------------------------------------------------------------------------
              Hotel_parth.STANDART_CB.clicked.connect(lambda checked, num=0: self.two_at_one_mix(checked,0, num, Hotel_parth))
              Hotel_parth.AVANS_VE_NAKIT_CB.clicked.connect(lambda checked, num=1: self.two_at_one_mix(checked,0, num, Hotel_parth))
              Hotel_parth.NAKIT_PARA_CB.clicked.connect(lambda checked, num=2: self.two_at_one_mix(checked,0, num, Hotel_parth))
              Hotel_parth.GIDERLER_CB.clicked.connect(lambda checked, num=3: self.two_at_one_mix(checked,0, num, Hotel_parth))
              Hotel_parth.DOVIZ_CB.clicked.connect(lambda checked, num=4: self.two_at_one_mix(checked,0, num, Hotel_parth))
              Hotel_parth.DEMIR_PARA_CB.clicked.connect(lambda checked, num=5: self.two_at_one_mix(checked,0, num, Hotel_parth))
              Hotel_parth.HAVLU_DEGISIK_CB.clicked.connect(lambda checked, num=6: self.two_at_one_mix(checked,0, num, Hotel_parth))
              Hotel_parth.HAMAM_WIFI_CB.clicked.connect(lambda checked, num=7: self.two_at_one_mix(checked,0, num, Hotel_parth))
              Hotel_parth.YEDEK_ANAHTAR_CB.clicked.connect(lambda checked, num=8: self.two_at_one_mix(checked,0, num, Hotel_parth))
              Hotel_parth.FITNES_CB.clicked.connect(lambda checked, num=9: self.two_at_one_mix(checked,0, num, Hotel_parth))
              Hotel_parth.HAVLU_CB.clicked.connect(lambda checked, num=10: self.two_at_one_mix(checked,0, num, Hotel_parth))
              Hotel_parth.ADMIN_CB.clicked.connect(lambda checked, num=11: self.two_at_one_mix(checked,0, num, Hotel_parth))
              #----------------------------------------------------------------------------------------------------------------------
              Hotel_parth.NAKIT_TB_W.clicked.connect(lambda time_test: self.select_row_fucnk(time_test,Hotel_parth.NAKIT_TB_W,uni_array[1][1]))
              Hotel_parth.GIDERLER_TB_W.clicked.connect(lambda time_test: self.select_row_fucnk(time_test,Hotel_parth.GIDERLER_TB_W,uni_array[0][1])) 
              Hotel_parth.DOVIZ_TB_W.clicked.connect(lambda time_test: self.select_row_fucnk(time_test,Hotel_parth.DOVIZ_TB_W,uni_array[2][1])) 
              Hotel_parth.HAMAM_WIFI_ENTER.clicked.connect(lambda time_test: self.select_row_fucnk(time_test,Hotel_parth.HAMAM_WIFI_ENTER,uni_array[3][1])) 
              Hotel_parth.HAVLU_DEGISIM_ENTER.clicked.connect(lambda time_test: self.select_row_fucnk(time_test, Hotel_parth.HAVLU_DEGISIM_ENTER,uni_array[4][1])) 
              Hotel_parth.YEDEK_ANAHTAR_TB_W.clicked.connect(lambda time_test: self.select_row_fucnk(time_test,Hotel_parth.YEDEK_ANAHTAR_TB_W,uni_array[5][1])) 
              Hotel_parth.FITNES_ANAHTAR_TB_W.clicked.connect(lambda time_test: self.select_row_fucnk(time_test,Hotel_parth.FITNES_ANAHTAR_TB_W,uni_array[6][1])) 
              Hotel_parth.HAVLU_TB_W.clicked.connect(lambda time_test: self.select_row_fucnk(time_test,Hotel_parth.HAVLU_TB_W,uni_array[7][1])) 
              Hotel_parth.NESILDI_TB_W.clicked.connect(lambda time_test: self.select_row_fucnk(time_test,Hotel_parth.NESILDI_TB_W,uni_array[8][1])) 
              Hotel_parth.TESLIM_TB_W.clicked.connect(lambda time_test: self.select_row_fucnk(time_test,Hotel_parth.TESLIM_TB_W,uni_array[9][1])) 
              Hotel_parth.MAIN_SQL_TB_W.clicked.connect(lambda time_test: self.select_row_fucnk(time_test,Hotel_parth.MAIN_SQL_TB_W,uni_array[11][1])) 
              Hotel_parth.SQLELECTRA_TB_W.clicked.connect(lambda time_test: self.select_row_fucnk(time_test,Hotel_parth.SQLELECTRA_TB_W,uni_array[12][1])) 
              Hotel_parth.ADMINTABLO_TB_W.clicked.connect(lambda time_test: self.select_row_fucnk(time_test,Hotel_parth.ADMINTABLO_TB_W,uni_array[13][1]))
              #---------------------------------------------Обновление записи в таблице------------------------------------------------------------------------
              Hotel_parth.GIDERLER_TB_W.doubleClicked.connect(lambda time_test: self.show_windows(time_test,0,2,uni_array[0])) 
              Hotel_parth.NAKIT_TB_W.doubleClicked.connect(lambda time_test: self.show_windows(time_test,0,1,uni_array[1]))
              Hotel_parth.DOVIZ_TB_W.doubleClicked.connect(lambda time_test: self.show_windows(time_test,0,3,uni_array[2])) 
              Hotel_parth.HAMAM_WIFI_ENTER.doubleClicked.connect(lambda time_test: self.show_windows(time_test,0,2,uni_array[3])) 
              Hotel_parth.HAVLU_DEGISIM_ENTER.doubleClicked.connect(lambda time_test: self.show_windows(time_test,0,3,uni_array[4])) 
              Hotel_parth.YEDEK_ANAHTAR_TB_W.doubleClicked.connect(lambda time_test: self.show_windows(time_test,0,10,uni_array[5])) 
              Hotel_parth.FITNES_ANAHTAR_TB_W.doubleClicked.connect(lambda time_test: self.show_windows(time_test,0,10,uni_array[6])) 
              Hotel_parth.HAVLU_TB_W.doubleClicked.connect(lambda time_test: self.show_windows(time_test,0,7,uni_array[7])) 
              #Hotel_parth.NESILDI_TB_W.doubleClicked.connect(lambda time_test: self.show_windows(time_test,0,10,uni_array[8])) 
              Hotel_parth.TESLIM_TB_W.doubleClicked.connect(lambda time_test: self.show_windows(time_test,0,4,uni_array[9])) 
              Hotel_parth.MAIN_SQL_TB_W.doubleClicked.connect(lambda time_test: self.show_windows(time_test,0,1,uni_array[11])) 
              Hotel_parth.SQLELECTRA_TB_W.doubleClicked.connect(lambda time_test: self.show_windows(time_test,0,2,uni_array[12])) 
              Hotel_parth.ADMINTABLO_TB_W.doubleClicked.connect(lambda time_test: self.show_windows(time_test,0,2,uni_array[13]))
              #---------------------------------------Вызов контекстного меню ---------------------------------------------------------------------
              Hotel_parth.KASA_PAGE.customContextMenuRequested.connect(lambda time_test :self.openMenu(time_test,uni_array[14]))
              Hotel_parth.ALLEXCHANGE_TB_W.customContextMenuRequested.connect(lambda time_test :self.openMenu(time_test,uni_array[10]))
              Hotel_parth.GIDERLER_TB_W.customContextMenuRequested.connect(lambda time_test :self.openMenu(time_test,uni_array[0]))
              Hotel_parth.DOVIZ_TB_W.customContextMenuRequested.connect(lambda time_test :self.openMenu(time_test,uni_array[2]))
              Hotel_parth.YEDEK_ANAHTAR_TB_W.customContextMenuRequested.connect(lambda time_test :self.openMenu(time_test,uni_array[5]))
              Hotel_parth.FITNES_ANAHTAR_TB_W.customContextMenuRequested.connect(lambda time_test :self.openMenu(time_test,uni_array[6]))
              Hotel_parth.HAVLU_TB_W.customContextMenuRequested.connect(lambda time_test :self.openMenu(time_test,uni_array[7]))
              Hotel_parth.NESILDI_TB_W.customContextMenuRequested.connect(lambda time_test :self.openMenu(time_test,uni_array[8]))
              Hotel_parth.TESLIM_TB_W.customContextMenuRequested.connect(lambda time_test :self.openMenu(time_test,uni_array[9]))
    #--------------------------прописываем работу контекстного меню --------------------------------------------------------------------------------
    def openMenu(self,event,data_array):
           # print(data_array)
            global Hotel_parthT
            Hotel_parth=Hotel_parthT
            MYSQ=Sql_Query()
            menu = QtWidgets.QMenu()
            print_this_list = QtWidgets.QAction('Yaz', menu)
            add_new_elem = QtWidgets.QAction('Yeni Aktar', menu)
            delete_elem = QtWidgets.QAction('Sil', menu)
            delete_stil_one_data = QtWidgets.QAction('Fazla Silmek', menu)
            permision_now=int(MYSQ.ALL_SQL_AT_ONE('select',3,4,'')[0][0])
            #print('permision_now',permision_now)
            uni_array=[
                   [Hotel_parth.GIDERLER_TB_W,'giderler',10,2],
  
                   [Hotel_parth.DOVIZ_TB_W,'doviz',8,3],
  
                   [Hotel_parth.YEDEK_ANAHTAR_TB_W,'doublekey',7,10],
                   [Hotel_parth.FITNES_ANAHTAR_TB_W,'fitneskey',9,10],
                   [Hotel_parth.HAVLU_TB_W,'havlu',12,7],
                   [Hotel_parth.NESILDI_TB_W,'nesildi',16,10],
                   [Hotel_parth.TESLIM_TB_W,'teslim',18,4],
                   [Hotel_parth.ALLEXCHANGE_TB_W,'Allexchange',1,3],

                   [Hotel_parth.KASA_PAGE,'Hotel_parth.KASA_PAGE',0,0]]
            for elem in uni_array:
                if data_array[1]==elem[1]:
                    if data_array[1]=='nesildi':
                        #print_this_list.triggered.connect(lambda i_test: self.print_funct(i_test,data_array))
                        #menu.addAction(print_this_list)
                        if permision_now==1 or permision_now==0:
                            delete_stil_one_data.triggered.connect(lambda i_test: self.delete_stil_one_data(i_test,3,1,data_array))
                            menu.addAction(delete_stil_one_data)
                    elif data_array[1]=='Hotel_parth.KASA_PAGE':
                        print_this_list.triggered.connect(lambda i_test: self.print_funct(i_test,data_array,'to print'))
                        menu.addAction(print_this_list)
                    elif data_array[1]=='Allexchange':
                        print_this_list.triggered.connect(lambda i_test: self.print_funct(i_test,data_array,'to print'))
                        menu.addAction(print_this_list)
                        if permision_now==1 or permision_now==0:
                            delete_stil_one_data.triggered.connect(lambda i_test: self.delete_stil_one_data(i_test,3,1,data_array))
                            menu.addAction(delete_stil_one_data)
                    elif data_array[1]=='doviz':
                        add_new_elem.triggered.connect(lambda i_test: self.add_new_elem_funct(i_test,1,data_array[3],data_array))
                        delete_elem.triggered.connect(lambda i_test: self.delete_elem_funct(i_test,2,data_array[3],data_array))
                        menu.addAction(add_new_elem)
                        menu.addAction(delete_elem)
                    elif data_array[1]=='teslim':
                        if permision_now==1 or permision_now==0:
                            add_new_elem.triggered.connect(lambda i_test: self.add_new_elem_funct(i_test,1,data_array[3],data_array))
                            delete_elem.triggered.connect(lambda i_test: self.delete_elem_funct(i_test,2,data_array[3],data_array))
                            menu.addAction(add_new_elem)
                            menu.addAction(delete_elem)

                    else:
                        print_this_list.triggered.connect(lambda i_test: self.print_funct(i_test,data_array,'to print'))

                        add_new_elem.triggered.connect(lambda i_test: self.add_new_elem_funct(i_test,1,data_array[3],data_array))
                        delete_elem.triggered.connect(lambda i_test: self.delete_elem_funct(i_test,2,data_array[3],data_array))
                        menu.addAction(print_this_list)
                        menu.addAction(add_new_elem)
                        menu.addAction(delete_elem)

            menu.exec_(QCursor.pos())

    #----------функции для контекстного меню----------------
    def print_funct(self,event, data_array,direct_text):
        global Hotel_parthT
        Hotel_parth=Hotel_parthT
        MYSQL=Sql_Query()
        if data_array[1]=='Hotel_parth.KASA_PAGE' and direct_text=='to email':
            filename = "tosend.pdf"
            #-----------------------------------------
            data = []
            # формирование таблицы заголовка
            data_now_table = Table([['', time.strftime("%d.%m.%Y %H:%M:%S")]], [210, 210])
            data_now_table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('BOX', (1, 0), (-1, -1), 2, colors.black),
            ])
            data_now_table.setStyle(data_now_table_style)
            perviy_zagolovok = Table([['KASA DEVIR TESLIM FORMU']], [420])
            perviy_zagolovok_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ])
            perviy_zagolovok.setStyle(perviy_zagolovok_style)
            kasaavans = Table([['', 'KASA AVANS', ' ', Hotel_parth.AVANS_ENTER.text()]], [105, 140, 70, 105])
            kasaavans_style = TableStyle([
                ('BOX', (3, 0), (-1, 0), 2, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ])
            kasaavans.setStyle(kasaavans_style)
            bignakitable = Table([['', 'NAKIT', '', Hotel_parth.NAKIT_ENTER.text()]], [170, 75, 70, 105])
            bignakitable_style = TableStyle([
                ('BOX', (3, 0), (-1, 0), 2, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, 0), 'LEFT'),
            ])
            bignakitable.setStyle(bignakitable_style)
            # формирование второй таблицы  гидер и наличие железных денег
            # деньги с рахода гидер
            vtoroy_zagolovok = Table([['GIDERLER']], [420])
            vtoroy_zagolovok.setStyle(perviy_zagolovok_style)
            demirevro_table = Table([['BOZUK EURO', '', '', Hotel_parth.D_EURO_ENTER.text()]], [105, 105, 105, 105])
            demirevro_table_style = TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
            ])
            demirevro_table.setStyle(demirevro_table_style)
            demirTL_table = Table([['BOZUK TL', '', '', Hotel_parth.D_TL_ENTER.text()]], [105, 105, 105, 105])
            demirTL_table_style = TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
            ])
            demirTL_table.setStyle(demirTL_table_style)
            #---------------------------часть для вставки в других таблицах------------------------------------------
            my_rows = Hotel_parth.GIDERLER_TB_W.rowCount()
            my_cols = Hotel_parth.GIDERLER_TB_W.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        #print(Hotel_parth.GIDERLER_TB_W.item(row,col).text())
                        tmp.append(Hotel_parth.GIDERLER_TB_W.item(row,col).text())
                    except:
                        tmp.append('')
                data.append(tmp)
            timelist = np.array(data).tolist()
            #----специальная часть для вставки выше -----------------
            if len(timelist)>=6:
                rows_count=str(MYSQL.ALL_SQL_AT_ONE('else',10,'SELECT count(*) FROM giderler','')[0][0])
                sum_of_money=str(MYSQL.ALL_SQL_AT_ONE('else',10,'SELECT sum(kacpara) from giderler','')[0][0])
                input_line='Kayitlari '+rows_count+' toplam'
                temp_array=[[input_line,'','',sum_of_money]]
                tgider = Table(temp_array, [105, 105, 105, 105])
                tgider_style = TableStyle([
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
                ])
            else:
                for i in (timelist):
                    i.insert(-1, '')
                    i.insert(-1, '')
                tgider = Table(timelist, [105, 105, 105, 105])
                tgider_style = TableStyle([
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
                ])
            tgider.setStyle(tgider_style)
            data = []
            # начало творения третьей группы  таблиц чуть позже поиграть с расположением- старые значение  86.6,86.6,86.6,86.6,86.6,86.6 \48, 70, 70, 72, 110, 100
            tretiy_zagolovok = Table([[ '','CINSI', 'DOVIZ', 'KUR', '', 'NAKIT']], [40, 70, 70, 72, 110, 100])
            tretiy_zagolovok_style = TableStyle([
                ('BOX', (1, 0), (3, 0), 2, colors.black),
                ('BOX', (-1, 0), (-1, -1), 2, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ])
            tretiy_zagolovok.setStyle(tretiy_zagolovok_style)
            #----------------------------------------------------------------------
            # деньги с обмена
            newdata = []
            newdata1 = []
            #-\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            my_rows = Hotel_parth.DOVIZ_TB_W.rowCount()
            my_cols = Hotel_parth.DOVIZ_TB_W.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        tmp.append(Hotel_parth.DOVIZ_TB_W.item(row,col).text())
                        #print(tmp)
                    except:
                        tmp.append('empty')
                newdata.append(tmp)
            #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            # наличные лиры в касе 
            my_rows = Hotel_parth.NAKIT_TB_W.rowCount()
            my_cols = Hotel_parth.NAKIT_TB_W.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        tmp.append(Hotel_parth.NAKIT_TB_W.item(row,col).text())
                    except:
                        tmp.append('empty')
                newdata1.append(tmp)
            newdatatime1 = np.array(newdata).tolist()
            newdatatime2 = np.array(newdata1).tolist()
            #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            doviz_table = Table(newdatatime1, [110, 70, 70, 70])
            nakit_table = Table(newdatatime2, [115, 100])
            nakit_table_style = TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ])
            doviz_table_style = TableStyle([
                
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ])
            doviz_table.setStyle(doviz_table_style)
            nakit_table.setStyle(nakit_table_style)
            emptyTable = Table([''], 10)
            combo_doviz_nakit = Table([[[doviz_table], [emptyTable], [nakit_table]]])
            #--------------------------------------------------------------------------------
            
            
            fark_table = Table([['', 'FARK', Hotel_parth.FARK_ENTER.text()]], [343, 73, 47])
            fark_table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('BOX', (2, 0), (2, 0), 2, colors.black),
            ])
            fark_table.setStyle(fark_table_style)
            # начало четвертой таблицы принял сдал 48,70,70,72,110,100 старое --66.6,173.2,43.3,43.3,173.2,43.3   463
            teslim_eden_alan_table = Table([['', 'TESLIM EDEN', 'SHIFT', '', 'TESLIM ALAN', 'SHIFT']],[125, 140, 47, 48, 140, 47])

            teslim_eden_alan_table_style = TableStyle([
                ('BOX', (1, 0), (1, 0), 2, colors.black),
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                ('BOX', (2, 0), (2, 0), 2, colors.black),
                ('BOX', (4, 0), (4, 0), 2, colors.black),
                ('ALIGN', (4, 0), (4, 0), 'CENTER'),
                ('ALIGN', (5, 0), (5, 0), 'CENTER'),
                ('BOX', (5, 0), (5, 0), 2, colors.black),
            ])
            teslim_eden_alan_table.setStyle(teslim_eden_alan_table_style)
            teslim_help_table1 = Table([['', Hotel_parth.TESLIM_VERILDI_ENTER.text(), '', Hotel_parth.TESLIM_ALDI_ENTER.text()]], [55, 265, 60, 300])
            teslim_help_table1_style = TableStyle([
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('ALIGN', (3, 0), (3, 0), 'LEFT'),
                ])
            teslim_help_table1.setStyle(teslim_help_table1_style)
            # 50,265,157.5,157.5
            teslim_help_table2 = Table([['', '........................', '', '........................']], [55, 265, 50, 265])
            teslim_help_table2_style = TableStyle([
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('ALIGN', (2, 0), (2, 0), 'RIGHT'),

            ])
            teslim_help_table2.setStyle(teslim_help_table2_style)
            # начало пятой таблицы компановки
            data = []
            my_rows = Hotel_parth.HAMAM_WIFI_ENTER.rowCount()
            my_cols = Hotel_parth.HAMAM_WIFI_ENTER.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        tmp.append(Hotel_parth.HAMAM_WIFI_ENTER.item(row,col).text())
                    except:
                        tmp.append('empty')
                data.append(tmp)
            
            hamamwifi_table = Table([['', 'HAMAM WIFI', '', data[0][0], data[0][1]]], [0, 80, 30, 40, 40])
            hamamwifi_table_style = TableStyle([
                ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
                ('ALIGN', (4, 0), (4, 0), 'RIGHT'), ])
            data = []
            my_rows = Hotel_parth.HAVLU_DEGISIM_ENTER.rowCount()
            my_cols = Hotel_parth.HAVLU_DEGISIM_ENTER.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        tmp.append(Hotel_parth.HAVLU_DEGISIM_ENTER.item(row,col).text())
                    except:
                        tmp.append('empty')
                data.append(tmp)
            havluchange_table = Table([['', 'HAVLU DEGISIM', data[0][0], data[0][1], data[0][2]]], [0, 80, 40, 30, 30])
            havluchange_table_style = TableStyle([
                ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
                ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
                ('ALIGN', (4, 0), (4, 0), 'RIGHT'), ])
            havluchange_table.setStyle(havluchange_table_style)
            # компановка таблиц для красивого оформления
            firstcombotable = Table([
                [data_now_table], [perviy_zagolovok], [kasaavans], [bignakitable] ])
            secondcombotable = Table([
                [vtoroy_zagolovok], [demirevro_table], [demirTL_table], [tgider] ])
            thirdcombotable = Table([
                [tretiy_zagolovok], [combo_doviz_nakit], [fark_table] ])
            fourthcombotable = Table([
                [teslim_eden_alan_table], [teslim_help_table1], [teslim_help_table2] ])
            fifthcombotable = Table([
               [hamamwifi_table], [havluchange_table], ])
            pdf = SimpleDocTemplate(filename, pagesize=A4)
            tablemas = []
            tablemas.append(firstcombotable)
            tablemas.append(secondcombotable)
            tablemas.append(thirdcombotable)
            tablemas.append(fourthcombotable)
            tablemas.append(fifthcombotable)
            pdf.build(tablemas)
            
        elif data_array[1]=='Hotel_parth.KASA_PAGE' and direct_text=='to print':
            filename = "Raport.pdf"
            #-----------------------------------------
            data = []
            # формирование таблицы заголовка
            data_now_table = Table([['', time.strftime("%d.%m.%Y %H:%M:%S")]], [210, 210])
            data_now_table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('BOX', (1, 0), (-1, -1), 2, colors.black),
            ])
            data_now_table.setStyle(data_now_table_style)
            perviy_zagolovok = Table([['KASA DEVIR TESLIM FORMU']], [420])
            perviy_zagolovok_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ])
            perviy_zagolovok.setStyle(perviy_zagolovok_style)
            kasaavans = Table([['', 'KASA AVANS', ' ', Hotel_parth.AVANS_ENTER.text()]], [105, 140, 70, 105])
            kasaavans_style = TableStyle([
                ('BOX', (3, 0), (-1, 0), 2, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ])
            kasaavans.setStyle(kasaavans_style)
            bignakitable = Table([['', 'NAKIT', '', Hotel_parth.NAKIT_ENTER.text()]], [170, 75, 70, 105])
            bignakitable_style = TableStyle([
                ('BOX', (3, 0), (-1, 0), 2, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, 0), 'LEFT'),
            ])
            bignakitable.setStyle(bignakitable_style)
            # формирование второй таблицы  гидер и наличие железных денег
            # деньги с рахода гидер
            vtoroy_zagolovok = Table([['GIDERLER']], [420])
            vtoroy_zagolovok.setStyle(perviy_zagolovok_style)
            demirevro_table = Table([['BOZUK EURO', '', '', Hotel_parth.D_EURO_ENTER.text()]], [105, 105, 105, 105])
            demirevro_table_style = TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
            ])
            demirevro_table.setStyle(demirevro_table_style)
            demirTL_table = Table([['BOZUK TL', '', '', Hotel_parth.D_TL_ENTER.text()]], [105, 105, 105, 105])
            demirTL_table_style = TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
            ])
            demirTL_table.setStyle(demirTL_table_style)
            #---------------------------часть для вставки в других таблицах------------------------------------------
            my_rows = Hotel_parth.GIDERLER_TB_W.rowCount()
            my_cols = Hotel_parth.GIDERLER_TB_W.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        #print(Hotel_parth.GIDERLER_TB_W.item(row,col).text())
                        tmp.append(Hotel_parth.GIDERLER_TB_W.item(row,col).text())
                    except:
                        tmp.append('')
                data.append(tmp)
            timelist = np.array(data).tolist()
            #----специальная часть для вставки выше -----------------
            if len(timelist)>=6:
                rows_count=str(MYSQL.ALL_SQL_AT_ONE('else',10,'SELECT count(*) FROM giderler','')[0][0])
                sum_of_money=str(MYSQL.ALL_SQL_AT_ONE('else',10,'SELECT sum(kacpara) from giderler','')[0][0])
                input_line='Kayitlari '+rows_count+' toplam'
                temp_array=[[input_line,'','',sum_of_money]]
                tgider = Table(temp_array, [105, 105, 105, 105])
                tgider_style = TableStyle([
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
                ])
            else:
                for i in (timelist):
                    i.insert(-1, '')
                    i.insert(-1, '')
                tgider = Table(timelist, [105, 105, 105, 105])
                tgider_style = TableStyle([
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
                ])
            tgider.setStyle(tgider_style)
            data = []
            # начало творения третьей группы  таблиц чуть позже поиграть с расположением- старые значение  86.6,86.6,86.6,86.6,86.6,86.6 \48, 70, 70, 72, 110, 100
            tretiy_zagolovok = Table([[ '','CINSI', 'DOVIZ', 'KUR', '', 'NAKIT']], [40, 70, 70, 72, 110, 100])
            tretiy_zagolovok_style = TableStyle([
                ('BOX', (1, 0), (3, 0), 2, colors.black),
                ('BOX', (-1, 0), (-1, -1), 2, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ])
            tretiy_zagolovok.setStyle(tretiy_zagolovok_style)
            #----------------------------------------------------------------------
            # деньги с обмена
            newdata = []
            newdata1 = []
            #-\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            my_rows = Hotel_parth.DOVIZ_TB_W.rowCount()
            my_cols = Hotel_parth.DOVIZ_TB_W.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        tmp.append(Hotel_parth.DOVIZ_TB_W.item(row,col).text())
                        #print(tmp)
                    except:
                        tmp.append('empty')
                newdata.append(tmp)
            #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            # наличные лиры в касе 
            my_rows = Hotel_parth.NAKIT_TB_W.rowCount()
            my_cols = Hotel_parth.NAKIT_TB_W.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        tmp.append(Hotel_parth.NAKIT_TB_W.item(row,col).text())
                    except:
                        tmp.append('empty')
                newdata1.append(tmp)
            newdatatime1 = np.array(newdata).tolist()
            newdatatime2 = np.array(newdata1).tolist()
            #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            doviz_table = Table(newdatatime1, [110, 70, 70, 70])
            nakit_table = Table(newdatatime2, [115, 100])
            nakit_table_style = TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ])
            doviz_table_style = TableStyle([
                
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ])
            doviz_table.setStyle(doviz_table_style)
            nakit_table.setStyle(nakit_table_style)
            emptyTable = Table([''], 10)
            combo_doviz_nakit = Table([[[doviz_table], [emptyTable], [nakit_table]]])
            #--------------------------------------------------------------------------------
            #farknow = zaprosspec()
            fark_table = Table([['', 'FARK', Hotel_parth.FARK_ENTER.text()]], [343, 73, 47])
            fark_table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('BOX', (2, 0), (2, 0), 2, colors.black),
            ])
            fark_table.setStyle(fark_table_style)
            # начало четвертой таблицы принял сдал 48,70,70,72,110,100 старое --66.6,173.2,43.3,43.3,173.2,43.3   463
            teslim_eden_alan_table = Table([['', 'TESLIM EDEN', 'SHIFT', '', 'TESLIM ALAN', 'SHIFT']],[125, 140, 47, 48, 140, 47])

            teslim_eden_alan_table_style = TableStyle([
                ('BOX', (1, 0), (1, 0), 2, colors.black),
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                ('BOX', (2, 0), (2, 0), 2, colors.black),
                ('BOX', (4, 0), (4, 0), 2, colors.black),
                ('ALIGN', (4, 0), (4, 0), 'CENTER'),
                ('ALIGN', (5, 0), (5, 0), 'CENTER'),
                ('BOX', (5, 0), (5, 0), 2, colors.black),
            ])
            teslim_eden_alan_table.setStyle(teslim_eden_alan_table_style)
            teslim_help_table1 = Table([['', Hotel_parth.TESLIM_VERILDI_ENTER.text(), '', Hotel_parth.TESLIM_ALDI_ENTER.text()]], [55, 265, 60, 300])
            teslim_help_table1_style = TableStyle([
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('ALIGN', (3, 0), (3, 0), 'LEFT'),
                ])
            teslim_help_table1.setStyle(teslim_help_table1_style)
            # 50,265,157.5,157.5
            teslim_help_table2 = Table([['', '........................', '', '........................']], [55, 265, 50, 265])
            teslim_help_table2_style = TableStyle([
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('ALIGN', (2, 0), (2, 0), 'RIGHT'),

            ])
            teslim_help_table2.setStyle(teslim_help_table2_style)
            # начало пятой таблицы компановки
            data = []
            my_rows = Hotel_parth.HAMAM_WIFI_ENTER.rowCount()
            my_cols = Hotel_parth.HAMAM_WIFI_ENTER.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        tmp.append(Hotel_parth.HAMAM_WIFI_ENTER.item(row,col).text())
                    except:
                        tmp.append('empty')
                data.append(tmp)
            #data.append(hamamwifitemp[0][1:3])

            hamamwifi_table = Table([['', 'HAMAM WIFI', '', data[0][0], data[0][1]]], [0, 80, 30, 40, 40])
            hamamwifi_table_style = TableStyle([
                ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
                ('ALIGN', (4, 0), (4, 0), 'RIGHT'), ])
            data = []
            my_rows = Hotel_parth.HAVLU_DEGISIM_ENTER.rowCount()
            my_cols = Hotel_parth.HAVLU_DEGISIM_ENTER.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        tmp.append(Hotel_parth.HAVLU_DEGISIM_ENTER.item(row,col).text())
                    except:
                        tmp.append('empty')
                data.append(tmp)
            havluchange_table = Table([['', 'HAVLU DEGISIM', data[0][0], data[0][1], data[0][2]]], [0, 80, 40, 30, 30])
            havluchange_table_style = TableStyle([
                ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
                ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
                ('ALIGN', (4, 0), (4, 0), 'RIGHT'), ])
            havluchange_table.setStyle(havluchange_table_style)
            # компановка таблиц для красивого оформления
            firstcombotable = Table([
                [data_now_table], [perviy_zagolovok], [kasaavans], [bignakitable] ])
            secondcombotable = Table([
                [vtoroy_zagolovok], [demirevro_table], [demirTL_table], [tgider] ])
            thirdcombotable = Table([
                [tretiy_zagolovok], [combo_doviz_nakit], [fark_table] ])
            fourthcombotable = Table([
                [teslim_eden_alan_table], [teslim_help_table1], [teslim_help_table2] ])
            fifthcombotable = Table([
               [hamamwifi_table], [havluchange_table], ])
            pdf = SimpleDocTemplate(filename, pagesize=A4)
            tablemas = []
            tablemas.append(firstcombotable)
            tablemas.append(secondcombotable)
            tablemas.append(thirdcombotable)
            tablemas.append(fourthcombotable)
            tablemas.append(fifthcombotable)
            pdf.build(tablemas)
            webbrowser.get('windows-default').open_new(filename)
        elif data_array[1]=='giderler':
            filename = "Giderler-Raport.pdf"
            #-----------------------------------------
            data = []
            # формирование таблицы заголовка
            data_now_table = Table([['', time.strftime("%d.%m.%Y %H:%M:%S")]], [210, 210])
            data_now_table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('BOX', (1, 0), (-1, -1), 2, colors.black),
            ])
            perviy_zagolovok_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ])
            data_now_table.setStyle(data_now_table_style)
          
            # формирование второй таблицы  гидер и наличие железных денег
            # деньги с рахода гидер
            vtoroy_zagolovok = Table([['GIDERLER']], [420])
            vtoroy_zagolovok.setStyle(perviy_zagolovok_style)
            demirevro_table = Table([['BOZUK EURO', '', '', Hotel_parth.D_EURO_ENTER.text()]], [105, 105, 105, 105])
            demirevro_table_style = TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
            ])
            demirevro_table.setStyle(demirevro_table_style)
            demirTL_table = Table([['BOZUK TL', '', '', Hotel_parth.D_TL_ENTER.text()]], [105, 105, 105, 105])
            demirTL_table_style = TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
            ])
            demirTL_table.setStyle(demirTL_table_style)
            #---------------------------часть для вставки в других таблицах------------------------------------------
            my_rows = Hotel_parth.GIDERLER_TB_W.rowCount()
            my_cols = Hotel_parth.GIDERLER_TB_W.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        #print(Hotel_parth.GIDERLER_TB_W.item(row,col).text())
                        tmp.append(Hotel_parth.GIDERLER_TB_W.item(row,col).text())
                    except:
                        tmp.append('')
                data.append(tmp)
            timelist = np.array(data).tolist()
            #----специальная часть для вставки выше -----------------
            for i in (timelist):
                    i.insert(-1, '')
                    i.insert(-1, '')
            tgider = Table(timelist, [105, 105, 105, 105])
            tgider_style = TableStyle([
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
                ])
            tgider.setStyle(tgider_style)
            
            # компановка таблиц для красивого оформления
            firstcombotable = Table([
                [data_now_table]])
            secondcombotable = Table([
                [vtoroy_zagolovok], [demirevro_table], [demirTL_table]])
            
            pdf = SimpleDocTemplate(filename, pagesize=A4)
            tablemas = []
            tablemas.append(firstcombotable)
            tablemas.append(secondcombotable)
            tablemas.append(tgider)
            pdf.build(tablemas)
            webbrowser.get('windows-default').open_new(filename)
        elif data_array[1]=='doublekey':
            filename = "Second-Key-Raport.pdf"
            #-----------------------------------------
            data = []
            # формирование таблицы заголовка
            data_now_table = Table([['', time.strftime("%d.%m.%Y %H:%M:%S")]], [545, 210])
            data_now_table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('BOX', (1, 0), (-1, -1), 2, colors.black),
            ])
            data_now_table.setStyle(data_now_table_style)
            perviy_zagolovok = Table([['IKINCI ANAHTARI']], [755])
            perviy_zagolovok_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ])
            perviy_zagolovok.setStyle(perviy_zagolovok_style)
            #---------------------------часть для вставки в других таблицах------------------------------------------
            my_rows = Hotel_parth.YEDEK_ANAHTAR_TB_W.rowCount()
            my_cols = Hotel_parth.YEDEK_ANAHTAR_TB_W.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        #print(Hotel_parth.GIDERLER_TB_W.item(row,col).text())
                        tmp.append(Hotel_parth.YEDEK_ANAHTAR_TB_W.item(row,col).text())
                    except:
                        tmp.append('')
                data.append(tmp)
            valible_list = np.array(data).tolist()
            #----специальная часть для вставки выше -----------------
            #for i in (timelist):
            #        i.insert(-1, '')
            #        i.insert(-1, '')
            #70, 70, 70, 70,70,70, 70, 70, 70,70,70
            name_of_columns = Table([['ODA NUMARASI','ADI','GIRIS TAR.','CIKIS TAR.','USD','EURO','RUBLE','BAS. PARA','KIM VERDI','KIM YAZDI']],[80, 75, 75, 75,75,75, 75, 75, 75, 75,75])
            name_of_columns_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (0, 0), 2, colors.black),
                ('BOX', (1, 0), (1, 0), 2, colors.black),
                ('BOX', (2, 0), (2, 0), 2, colors.black),
                ('BOX', (3, 0), (3, 0), 2, colors.black),
                ('BOX', (4, 0), (4, 0), 2, colors.black),
                ('BOX', (5, 0), (5, 0), 2, colors.black),
                ('BOX', (6, 0), (6, 0), 2, colors.black),
                ('BOX', (7, 0), (7, 0), 2, colors.black),
                ('BOX', (8, 0), (8, 0), 2, colors.black),
                ('BOX', (9, 0), (9, 0), 2, colors.black),
                ('BOX', (10, 0), (10, 0), 2, colors.black),
                ])
            name_of_columns.setStyle(name_of_columns_style)
            table_info = Table(valible_list, [80, 75, 75, 75,75,75, 75, 75, 75, 75,75])
            table_info_style = TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ])
            table_info.setStyle(table_info_style)
            toplam_table = Table([['TOPLAM',Hotel_parth.Y_TOTAL_DOLLAR_ENTER.text(),Hotel_parth.Y_TOTAL_EURO_ENTER.text(),Hotel_parth.Y_TOTAL_RUBLE_ENTER.text()]],[188.75,188.75,188.75,188.75])
            toplam_table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (0, 0), 2, colors.black),
                ('BOX', (1, 0), (1, 0), 2, colors.black),
                ('BOX', (2, 0), (2, 0), 2, colors.black),
                ('BOX', (3, 0), (3, 0), 2, colors.black),
                ])
            toplam_table.setStyle(toplam_table_style)
            data = []
           
            # компановка таблиц для красивого оформления
            firstcombotable = Table([
                [data_now_table], [perviy_zagolovok], [name_of_columns] ])
            #[ table_info],[toplam_table]
            pdf = SimpleDocTemplate(filename, pagesize=(landscape(letter))) 
            #LETTER)
            tablemas = []
            tablemas.append(firstcombotable)
            tablemas.append(table_info)
            tablemas.append(toplam_table)
            pdf.build(tablemas)
            webbrowser.get('windows-default').open_new(filename)
        elif data_array[1]=='fitneskey':
            filename = "Fitnes-Key-Raport.pdf"
            #-----------------------------------------
            data = []
            # формирование таблицы заголовка
            data_now_table = Table([['', time.strftime("%d.%m.%Y %H:%M:%S")]], [545, 210])
            data_now_table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('BOX', (1, 0), (-1, -1), 2, colors.black),
            ])
            data_now_table.setStyle(data_now_table_style)
            perviy_zagolovok = Table([['FITNES ANAHTARI']], [755])
            perviy_zagolovok_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ])
            perviy_zagolovok.setStyle(perviy_zagolovok_style)
            #---------------------------часть для вставки в других таблицах------------------------------------------
            my_rows = Hotel_parth.FITNES_ANAHTAR_TB_W.rowCount()
            my_cols = Hotel_parth.FITNES_ANAHTAR_TB_W.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        #print(Hotel_parth.GIDERLER_TB_W.item(row,col).text())
                        tmp.append(Hotel_parth.FITNES_ANAHTAR_TB_W.item(row,col).text())
                    except:
                        tmp.append('')
                data.append(tmp)
            valible_list = np.array(data).tolist()
            #----специальная часть для вставки выше -----------------
            #for i in (timelist):
            #        i.insert(-1, '')
            #        i.insert(-1, '')
            #70, 70, 70, 70,70,70, 70, 70, 70,70,70
            name_of_columns = Table([['ODA NUMARASI','ADI','GIRIS TAR.','CIKIS TAR.','USD','EURO','RUBLE','BAS. PARA','KIM VERDI','KIM YAZDI']],[80, 75, 75, 75,75,75, 75, 75, 75, 75,75])
            name_of_columns_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (0, 0), 2, colors.black),
                ('BOX', (1, 0), (1, 0), 2, colors.black),
                ('BOX', (2, 0), (2, 0), 2, colors.black),
                ('BOX', (3, 0), (3, 0), 2, colors.black),
                ('BOX', (4, 0), (4, 0), 2, colors.black),
                ('BOX', (5, 0), (5, 0), 2, colors.black),
                ('BOX', (6, 0), (6, 0), 2, colors.black),
                ('BOX', (7, 0), (7, 0), 2, colors.black),
                ('BOX', (8, 0), (8, 0), 2, colors.black),
                ('BOX', (9, 0), (9, 0), 2, colors.black),
                ('BOX', (10, 0), (10, 0), 2, colors.black),
                ])
            name_of_columns.setStyle(name_of_columns_style)
            table_info = Table(valible_list, [80, 75, 75, 75,75,75, 75, 75, 75, 75,75])
            table_info_style = TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ])
            table_info.setStyle(table_info_style)
            toplam_table = Table([['TOPLAM',Hotel_parth.F_TOTAL_DOLLAR_ENTER.text(),Hotel_parth.F_TOTAL_EURO_ENTER.text(),Hotel_parth.F_TOTAL_RUBLE_ENTER.text()]],[188.75,188.75,188.75,188.75])
            toplam_table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (0, 0), 2, colors.black),
                ('BOX', (1, 0), (1, 0), 2, colors.black),
                ('BOX', (2, 0), (2, 0), 2, colors.black),
                ('BOX', (3, 0), (3, 0), 2, colors.black),
                ])
            toplam_table.setStyle(toplam_table_style)
            data = []
           
            # компановка таблиц для красивого оформления
            firstcombotable = Table([
                [data_now_table], [perviy_zagolovok], [name_of_columns] ])
            #[ table_info],[toplam_table]
            pdf = SimpleDocTemplate(filename, pagesize=(landscape(letter))) 
            #LETTER)
            tablemas = []
            tablemas.append(firstcombotable)
            tablemas.append(table_info)
            tablemas.append(toplam_table)
            pdf.build(tablemas)
            webbrowser.get('windows-default').open_new(filename)
        elif data_array[1]=='havlu':
            filename = "Towels-Raport.pdf"
            #-----------------------------------------
            data = []
            # формирование таблицы заголовка
            data_now_table = Table([['', time.strftime("%d.%m.%Y %H:%M:%S")]], [545, 210])
            data_now_table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('BOX', (1, 0), (-1, -1), 2, colors.black),
            ])
            data_now_table.setStyle(data_now_table_style)
            perviy_zagolovok = Table([['HAVLU KARTI']], [755])
            perviy_zagolovok_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ])
            perviy_zagolovok.setStyle(perviy_zagolovok_style)
            #---------------------------часть для вставки в других таблицах------------------------------------------
            my_rows = Hotel_parth.HAVLU_TB_W.rowCount()
            my_cols = Hotel_parth.HAVLU_TB_W.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        #print(Hotel_parth.GIDERLER_TB_W.item(row,col).text())
                        tmp.append(Hotel_parth.HAVLU_TB_W.item(row,col).text())
                    except:
                        tmp.append('')
                data.append(tmp)
            valible_list = np.array(data).tolist()
            #----специальная часть для вставки выше -----------------
            #for i in (timelist):
            #        i.insert(-1, '')
            #        i.insert(-1, '')
            #70, 70, 70, 70,70,70, 70, 70, 70,70,70
            name_of_columns = Table([['ODA NUMARASI','ADI','GIRIS TAR.','CIKIS TAR.','KAC HAVLU','KIM VERDI','KIM YAZDI']],[107.85, 107.85, 107.85, 107.85, 107.85, 107.85, 107.85])
            name_of_columns_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (0, 0), 2, colors.black),
                ('BOX', (1, 0), (1, 0), 2, colors.black),
                ('BOX', (2, 0), (2, 0), 2, colors.black),
                ('BOX', (3, 0), (3, 0), 2, colors.black),
                ('BOX', (4, 0), (4, 0), 2, colors.black),
                ('BOX', (5, 0), (5, 0), 2, colors.black),
                ('BOX', (6, 0), (6, 0), 2, colors.black),
                
                ])
            name_of_columns.setStyle(name_of_columns_style)
            table_info = Table(valible_list, [107.85, 107.85, 107.85, 107.85, 107.85, 107.85, 107.85])
            table_info_style = TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ])
            table_info.setStyle(table_info_style)
            toplam_table = Table([['TOPLAM',Hotel_parth.H_TOTAL_HAVLU_ENTER.text()]],[377.5,377.5])
            toplam_table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (0, 0), 2, colors.black),
                ('BOX', (1, 0), (1, 0), 2, colors.black),
                
                ])
            toplam_table.setStyle(toplam_table_style)
            data = []
           
            # компановка таблиц для красивого оформления
            firstcombotable = Table([
                [data_now_table], [perviy_zagolovok], [name_of_columns] ])
            #[ table_info],[toplam_table]
            pdf = SimpleDocTemplate(filename, pagesize=(landscape(letter))) 
            #LETTER)
            tablemas = []
            tablemas.append(firstcombotable)
            tablemas.append(table_info)
            tablemas.append(toplam_table)
            pdf.build(tablemas)
            webbrowser.get('windows-default').open_new(filename)
        elif data_array[1]=='Allexchange':
            filename = "Allexchange-Raport.pdf"
            #-----------------------------------------
            data = []
            # формирование таблицы заголовка
            data_now_table = Table([['', time.strftime("%d.%m.%Y %H:%M:%S")]], [210, 210])
            data_now_table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('BOX', (1, 0), (-1, -1), 2, colors.black),
            ])
            data_now_table.setStyle(data_now_table_style)
            perviy_zagolovok = Table([['Allexchange']], [420])
            perviy_zagolovok_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ])
            perviy_zagolovok.setStyle(perviy_zagolovok_style)
            #---------------------------часть для вставки в других таблицах------------------------------------------
            my_rows = Hotel_parth.ALLEXCHANGE_TB_W.rowCount()
            my_cols = Hotel_parth.ALLEXCHANGE_TB_W.columnCount()
            for row in range(my_rows):
                tmp=[]
                for col in range(my_cols):
                    try:
                        #print(Hotel_parth.GIDERLER_TB_W.item(row,col).text())
                        tmp.append(Hotel_parth.ALLEXCHANGE_TB_W.item(row,col).text())
                    except:
                        tmp.append('')
                data.append(tmp)
            valible_list = np.array(data).tolist()
            #----специальная часть для вставки выше -----------------

            name_of_columns = Table([['SAAT','ADI','FARK']],[140, 140, 140])
            name_of_columns_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (0, 0), 2, colors.black),
                ('BOX', (1, 0), (1, 0), 2, colors.black),
                ('BOX', (2, 0), (2, 0), 2, colors.black),
                
                
                ])
            name_of_columns.setStyle(name_of_columns_style)
            table_info = Table(valible_list, [140,140,140])
            table_info_style = TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ])
            table_info.setStyle(table_info_style)
            
            data = []
           
            # компановка таблиц для красивого оформления
            #firstcombotable = Table([
            #    [data_now_table], [perviy_zagolovok], [name_of_columns] ])
            
            pdf = SimpleDocTemplate(filename, pagesize=A4) 
            #LETTER)
            tablemas = []
            #tablemas.append(firstcombotable)
            tablemas.append(data_now_table)
            tablemas.append(perviy_zagolovok)
            tablemas.append(name_of_columns)
            tablemas.append(table_info)
            pdf.build(tablemas)
            webbrowser.get('windows-default').open_new(filename)
        #elif data_array[1]=='nesildi':
        #    print('ne sildi')
    def add_new_elem_funct(self, event,ifelem, value,name_of_table):
        self.show_windows(event,ifelem, value,name_of_table)
    def delete_elem_funct(self, event,ifelem, value,name_of_table):
        self.show_windows(event,ifelem, value,name_of_table)
    def delete_stil_one_data(self,event,ifelem, value,name_of_table):
        self.show_windows(event,ifelem, value,name_of_table)
   
    #--------------------------------------------------------
    #--------функция для получения конкретных данных с таблицы помогает с выделением строки --------------------------------
    def select_row_fucnk(self,event,Part_TabelName,SomeArray):
        global for_selec
        
        MYSQ=Sql_Query()
        
        
        if  isinstance(None,type(Part_TabelName.currentItem())):
            #print('пропустила')
            pass;
        else:
            #print(Part_TabelName.currentItem())
            #gлучаем номер строки  после выделяем всю строку и в цикле проходим по выделенным элементам 
            row = Part_TabelName.currentItem().row()
            Part_TabelName.selectRow(row)
        if for_selec==None:
            for_selec = Part_TabelName
        elif Part_TabelName!=for_selec:
            try:
                for_selec.clearSelection()
                for_selec = Part_TabelName
            except RuntimeError:
                pass;
        else:
            pass;
    #---------------------Фукция по открытию окна ввода/редактирования записей value- количество ячеек ввода/вывода name_of_table-название таблицы с которой работаем
    def show_windows(self, event,ifelem, value,name_of_table):
        self.MYSQ=Sql_Query()
        #passs= self.password_edit.text()
        self.Hotel_Project = QtWidgets.QWidget()
        
        self.ui = Ui_update_and_insert()
        if ifelem==2:
            self.ui.litle_global_funck(event,self.ui,ifelem,value,name_of_table,self.Hotel_Project)
        else:
            self.ui.setupUi(self.Hotel_Project,value,name_of_table) 
            #self.ui.show_data(self.ui,MYSQ)
            #self,winpart,ifelem,value_size,name_of_table
            self.ui.litle_global_funck(event,self.ui,ifelem,value,name_of_table,self.Hotel_Project)
            #show_data(QtWidgets.QWidget(),MYSQ)
            self.Hotel_Project.show()

class Ui_autorisation_form(object):
    #При создании событий и их модернизации не забыть подправить функцию в setupUi
    #Создание элементов окна авторизации
    def setupUi(self, autorisation_form):
        if not autorisation_form.objectName():
            autorisation_form.setObjectName(u"autorisation_form")
        autorisation_form.resize(600, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(autorisation_form.sizePolicy().hasHeightForWidth())
        autorisation_form.setSizePolicy(sizePolicy)
        autorisation_form.setMinimumSize(QtCore.QSize(600, 300))
        autorisation_form.setMaximumSize(QtCore.QSize(600, 300))
        autorisation_form.setSizeIncrement(QtCore.QSize(600, 300))
        autorisation_form.setBaseSize(QtCore.QSize(600, 300))
        ##############################################################################
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(autorisation_form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        #############################################################################
        self.login_label = QtWidgets.QLabel(autorisation_form)
        self.login_label.setObjectName(u"login_label")
        self.login_label.setAlignment(QtCore.Qt.AlignCenter)
        #############################################################################
        self.login_cb = QtWidgets.QComboBox(autorisation_form)
        self.login_cb.setObjectName(u"login_cb")
        ############################################################################
        self.password_label = QtWidgets.QLabel(autorisation_form)
        self.password_label.setObjectName(u"password_label")
        sizePolicy1 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.password_label.sizePolicy().hasHeightForWidth())
        self.password_label.setSizePolicy(sizePolicy1)
        self.password_label.setMinimumSize(QtCore.QSize(286, 87))
        self.password_label.setMaximumSize(QtCore.QSize(286, 87))
        self.password_label.setAlignment(QtCore.Qt.AlignCenter)
        ################################################################################
        self.password_edit = QtWidgets.QLineEdit(autorisation_form)
        self.password_edit.setObjectName(u"password_edit")
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        ##################################################################################
        self.ok_button = QtWidgets.QPushButton(autorisation_form)
        self.ok_button.setObjectName(u"ok_button")
        self.cancel_button = QtWidgets.QPushButton(autorisation_form)
        self.cancel_button.setObjectName(u"cancel_button")
        ##################################################################################
        self.horizontalLayout.addWidget(self.login_label)
        self.horizontalLayout.addWidget(self.login_cb)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addWidget(self.password_label)
        self.horizontalLayout_2.addWidget(self.password_edit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addWidget(self.ok_button)
        self.horizontalLayout_3.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        ################################################################################
        self.retranslateUi(autorisation_form)
        self.my_events(autorisation_form)
        QtCore.QMetaObject.connectSlotsByName(autorisation_form)

    def show_data_at_cb(self,Class_part):
        #Какая то постная хуйня непонятно для чего с проверкой 
        only_time=Global_funck_of_Nothing()
        list_to_cb=only_time.if_its_empty(Class_part.ALL_SQL_AT_ONE('else',6,'SELECT name FROM teslim where permision <>0',''))
        if list_to_cb=='   ':
            self.login_cb.addItem('   ')
        else:
            for name in list_to_cb:
                self.login_cb.addItem(name[0])
    #Создание событий при нажатии на элементы окна авторизации
    def my_events(self,autorisation_form):
        self.password_edit.mousePressEvent=self.read_to_write
        self.ok_button.clicked.connect(self.show_windows)
        self.cancel_button.clicked.connect(self.close_wind)
    
    def read_to_write(self,autorisation_form):
        self.password_edit.setStyleSheet("QLineEdit {background-color: white;}")
        self.password_edit.setText('')
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
    def close_wind(self,autorisation_form):
         sys.exit(app.exec_())
    #Создание названий элементов которые отображаются в окне авторизации
    def retranslateUi(self, autorisation_form):
        _translate = QtCore.QCoreApplication.translate
        #autorisation_form.setWindowTitle(_translate("autorisation_form", u"autorisation_form", None))
        self.login_label.setText(_translate("autorisation_form", u"LOGIN", None))
        self.password_label.setText(_translate("autorisation_form", u"PASSWORD", None))
        self.ok_button.setText(_translate("autorisation_form", u"OK", None))
        self.cancel_button.setText(_translate("autorisation_form", u"CANCEL", None))
    #Отображение главного окна программы 
    def show_windows(self):
        MYSQ=Sql_Query()
        loginT=self.login_cb.currentText()
        passwordT=self.password_edit.text()
        temp_t=MYSQ.ALL_SQL_AT_ONE('select',18,['WHERE',[5,3]],[[2,4],[loginT,passwordT]])
        if not temp_t:
                self.password_edit.setStyleSheet("QLineEdit {background-color: red;}")
                self.password_edit.setEchoMode(QtWidgets.QLineEdit.Normal)
                self.password_edit.setText('YANLIS')
        else:
                shiftT,permisionT=temp_t[0][0],temp_t[0][1]
                #проверка таблицы сейчас (Now)
                temp_t=MYSQ.ALL_SQL_AT_ONE('select',3,[2,5],'')
                if not temp_t:
                    old_data=[['-','-']]
                    datanowT=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    MYSQ.ALL_SQL_AT_ONE('insert',3,[2,3,4,5],[loginT,shiftT,permisionT,datanowT])
                else:
                    data_old=datetime.strptime(temp_t[0][3],'%Y-%m-%d %H:%M:%S')
                    datanowT=datetime.now()
                    if datanowT>data_old:
                        old_data=MYSQ.ALL_SQL_AT_ONE('select',3,[2,3,-1],'')
                        MYSQ.ALL_SQL_AT_ONE('delete',3,[5],[temp_t[0][3]])
                        datanowT=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        MYSQ.ALL_SQL_AT_ONE('insert',3,[2,3,4,5],[loginT,shiftT,permisionT,datanowT])

                self.Hotel_Project = QtWidgets.QWidget()
                self.ui = Ui_Hotel_Project() 
                self.ui.setupUi(self.Hotel_Project) 
                self.ui.show_data(self.ui,MYSQ,[loginT,shiftT,old_data[0][0],old_data[0][1]])
                self.ui.my_events(self.ui)
                self.Hotel_Project.show()
                
       
#попытка с многоразовым запуском функции отрисовки заголовка формы
def every(delay, task):
  next_time = time.time() + delay
  while True:
    time.sleep(max(0, next_time - time.time()))
    try:
      task()
    except Exception:
      traceback.print_exc()
      # in production code you might want to have this instead of course:
      # logger.exception("Problem while executing repetitive task.")
    # skip tasks if we are behind schedule:
    next_time += (time.time() - next_time)
def time_at_label(Hotel_Project):
    
    _translate = QtCore.QCoreApplication.translate
    Hotel_Project.setWindowTitle(_translate("Hotel_Project", "KASA DEVIR TESLIM FORMU "+time.strftime("%d.%m.%Y %H:%M:%S")))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Hotel_Pro = QtWidgets.QWidget()
    Class_part=Sql_Query()
    aut = Ui_autorisation_form()

    aut.setupUi(Hotel_Pro)
    #заполнение полей данными 
    aut.show_data_at_cb(Class_part)
    #не работает как задуманно - заголовок с часами 
    #threading.Thread(target=lambda:every(5,time_at_label(Hotel_Project))).start()
    #показ 
    Hotel_Pro.show()
    
    sys.exit(app.exec_())
