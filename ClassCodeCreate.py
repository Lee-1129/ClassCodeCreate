#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from xml.dom.minidom import parseString
import os

def getFile(path):
        ''' 获取指定目录下的所有指定后缀的文件名 '''
        File=""
        f_list = os.listdir(path)
         # print f_list
        for i in f_list:
             # os.path.splitext():分离文件名与扩展名
            if os.path.splitext(i)[1] == '.aquila':
                File = str(i)
                break
        return File


# 获取类的方法
def getClassOperations(e):
    # 获取类 e 的方法列表
    operationsList = e.getElementsByTagName("operations")
    operations = []
    i = 0
    while i < len(operationsList):
        operations.append(operationsList[i].getAttribute("name"))
        i = i + 1
    return operations


def getClassStructuralFeatures(e):
    # 获取类 c 的属性/继承关系列表
    structuralFeaturesList = e.getElementsByTagName("structuralFeatures")
    # 类c的继承类 如果有的话
    TargetNum = -1
    # 类 c 的属性
    AttributeList = []

    i = 0
    while i < len(structuralFeaturesList):
        # 获取一条structuralFeatures
        if structuralFeaturesList[i].getAttribute("xsi:type") == "Aquila:AqReference":
            # 先获取继承关系
            #TargetNum = getClassReference(structuralFeaturesList[i])
            pass
        elif structuralFeaturesList[i].getAttribute("xsi:type") == "Aquila:AqAttribute":
            # 获取属性值 添加到属性列表中
            AttributeList.append(structuralFeaturesList[i].getAttribute("name"))
        i = i + 1
    return AttributeList


# 封装一个类的信息
def getClassInfo(e,classnum):
    classinfo = []
    # 类名
    ClassName = e.getAttribute("name")
    classinfo.append(ClassName)
    # 定义类的继承关系
    # 类的编号 int
    classinfo.append(classnum)
    FatherClassNum = (e.getAttribute("superTypes"))
    if FatherClassNum=="":
        FatherClassNum = -1
    else:
        FatherClassNum=FatherClassNum[12:]
    classinfo.append(int(FatherClassNum))
    # classinfo.append(ClassName)
    # 获取类 c 的属性
    classinfo.append(getClassStructuralFeatures(e))
    # 获取类 c 的方法

    classinfo.append(getClassOperations(e))
    # 获取类 c 的友元
    FriendNum=[]
    FriendNumList = (e.getElementsByTagName("dependencies"))
    if FriendNumList!=[]:
        j = 0
        while j < len(FriendNumList):
            FriendNum.append(int(FriendNumList[j].getAttribute("target")[12:]))
            j = j+1
    else:
        pass
    classinfo.append(FriendNum)
    return classinfo


def createCode(classinfo):
    str1 = "class"
    str2 = "public"
    str3 = "private"
    str4 = "protected"
    str5 = "datatype"
    str6 = "friend"
    str7 = "void"
    code = ''

    i = 0
    # test = classinfo[0]
    while i < len(classinfo):
        temp = classinfo[i]
        codetemp = ""
        # 生成类名
        codetemp += str1 + " " + str(temp[0])
        if temp[2] == -1:
            pass
        else:
            # 获取父类的名字
            j = 0
            while j < len(classinfo):
                if classinfo[j][1] == temp[2]:
                    FatherName = classinfo[j][0]
                    codetemp += ": " + str2  + FatherName
                    break
                j = j + 1
            # public: A {
        codetemp+=" \n{\n"
        j = 0
        # 生成属性
        if (classinfo[i][3] != []):
            while j < len(temp[3]):
                # private datatype classinfo;
                codetemp += "\t" + str3 + " " + str5 + " " + str(temp[3][j]) + ";\n"
                j = j + 1

        # 生成函数
        codetemp += str2 + ":\n"
        # 生成友元 friend A;
        if temp[6]!=[]:
            j = 0
            while j < len(temp[6]):
                codetemp += "\t"+str6+" "+temp[6][j]+";\n"
                j = j + 1
        else:
            pass
        j = 0
        if (classinfo[i][4] != []):
            while j < len(temp[3]):
                # setelement(datatype element){}
                #
                codetemp += "\t" + str7 + " set" + str(temp[3][j]) + "( datatype temp" \
                            + " ){this." + str(temp[3][j]) + " = temp; }\n"
                codetemp += "\t" + "datatype get" + str(temp[3][j]) + "( ){ return this." + str(temp[3][j]) + "; }\n"
                j = j + 1
        k = 0
        if (classinfo[i][4] != []):
            while k < len(temp[4]):
                # void function(){}
                codetemp += "\t" + str7 + " " + str(temp[4][k]) + "( ){\n\t //Write your code here\n\t }\n"
                k = k + 1
        codetemp += "};\n"
        code.split('[')
        code.split(']')
        i = i + 1
        code += codetemp
    with open("code.txt", "w") as f:
        f.write(code)  # 自带文件关闭功能，不需要再写f.close()
    # pass

# main
Flie = getFile("./")
k = 0
f = open(Flie, 'r', encoding='utf-8')
line = f.read()
f.close()
dom = parseString(line)
# XMLFile 表示整个顶层文件
XMLFile = dom.documentElement
# elements 返回的是该文件标签为Elment的list 有几个element list里面就有几个元素
# element[i] 代表第 i 个element 即代表一个class
#print(XMLFile)
elementsList = XMLFile.getElementsByTagName("elements")
fr = elementsList[0].getElementsByTagName("dependencies")
classinfo = []
i = 0
# 第i个 classinfo：[i][0] = 类名  [i][1] = 类编号 [i][2] = 父类编号 没有就是-1 [i][3][0:n] 类的属性 [i][4][0:n] 类的方法 [i][5][0:n] 可以调用这些类的方法和属性 [i][6][0:n] 友元类名
# 这里获得所有类的信息
while i < len(elementsList):
    classinfo.append(getClassInfo(elementsList[i] , int(i)))
    classinfo[i].append([])
    i = i + 1
# 获取 友元类列表
i = 0
while i < len(classinfo):
    # class[i] 发送端
    if classinfo[i][5]!=[]:
        j = 0
        # class [j] 接收端
        while j < len(classinfo[i][5]):
            classinfo[classinfo[i][5][j]][6].append(classinfo[i][0])
            j = j + 1
    else:
        pass
    i = i + 1
# sorted
i = 0
j = 0
n = len(classinfo)
for i in range(0,n):
    for j in range(0,n-1-i):
        if int(classinfo[j][2])>int(classinfo[j+1][2]):
            classinfo[j],classinfo[j+1] = classinfo[j+1],classinfo[j]
# 生成 C++ code

createCode(classinfo)
