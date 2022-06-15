
import bpy
import os


def convertToObj(file, saveFile):
    '''
    other file (dae, gltf, glb,fbx) convert to obj
    :param file: before file (ex:*.dae, *.fbx)
    :param saveFile: save file name(new file name)
    :return:
    '''
    bpy.ops.object.delete()
    type = file.split('.')[len(file.split('.'))-1]
    file_loc = file
    if type == 'fbx':
        object =bpy.ops.import_scene.fbx(filepath=file_loc)
    elif type == 'gltf' or type == 'glb':
        object =bpy.ops.import_scene.gltf(filepath=file_loc)
    elif type == 'dae':
        object =bpy.ops.wm.collada_import(filepath=file_loc)
    bpy.ops.export_scene.obj(filepath=saveFile)
    obj=bpy.ops.import_scene.obj(filepath=saveFile)
    bpyObj = bpy.context.selected_objects[0]
    bpyObjName = bpy.data.objects[1].name

def getVertex(readFile):
    '''
    Get vertex list from obj file
    :param readFile: obj file full path
    :return: vertex list
    '''
    rf = open(readFile, "r")
    vertexLst=[]
    while True:
        line = rf.readline()
        split = line.split()
        if len(split) > 2:
            if split[0] == 'v':
                vtLst = (float(split[1]), float(split[2]),float(split[3]))
                vertexLst.append(vtLst)
        if not line:
            break
    rf.close()
    return vertexLst

def getVertexTexture(readFile):
    '''
    Get vertex list from obj file
    :param readFile: obj file full path
    :return: vertex list
    '''
    rf = open(readFile, "r")
    vertexLstVT=[]
    while True:
        line = rf.readline()
        split = line.split()
        if len(split) > 2:
            if split[0] == 'vt':
                vtLst = (float(split[1]), float(split[2]))
                vertexLstVT.append(vtLst)
        if not line:
            break
    rf.close()
    return vertexLstVT

#get face vertext from objfile
def getFace(readFile):
    '''
    Get face list from obj file
    :param readFile: obj file full path
    :return: face list
    '''
    rf = open(readFile, "r")
    faceLst=[]
    vtFaceLst=[]
    while True:
        line = rf.readline()
        split = line.split()
        if len(split) > 2:
            if split[0] == 'f':
                lst=[]
                vtlst=[]
                for f in range(1,len(split)):
                    lst.append(split[f].split('/')[0])
                    vtlst.append(split[f].split('/')[1])
                faceLst.append(lst)
                vtFaceLst.append(vtlst)
        if not line:
            break
    rf.close()
    return faceLst,vtFaceLst
def getGroupName(objfileName):
    '''
    Get Group name in obj file for create header
    :param objfileName: obj file full path
    :return: group name (string)
    '''
    if os.path.exists(objfileName):
        rf=open(objfileName,"r")
        while True:
            line=rf.readline()
            split=line.split()
            if len(split)>1:
                if split[0]=="o":
                    rf.close()
                    return split[1]
    else:
        return  "objFile0.1"


def getMtlList(objfileName):
    '''
    Get Mtl file name in obj file for create header
    :param objfileName: obj file name full path
    :return: mtl file name (string)
    '''
    mtlFile = objfileName.split('.obj')[0] + '.mtl'
    mtllst=[]
    dic = {}
    if os.path.exists(mtlFile):
        rf = open(mtlFile, "r")
        while True:
            line = rf.readline()
            split = line.split()
            if len(split) > 1:
                if split[0] == "newmtl":
                    if len(dic)>1:
                        mtllst.append(dic)
                    dic.clear()
                    dic.setdefault("newmtl",split[1])
                elif split[0] == "Kd":
                    if len(split)>2:
                        dic.setdefault("Kd",[float(split[1]),float(split[2]),float(split[3])])
                elif split[0] == "Ka":
                    if len(split) > 2:
                        dic.setdefault("Ka", [float(split[1]), float(split[2]), float(split[3])])
                elif split[0] == "Ks":
                    if len(split) > 2:
                        dic.setdefault("Ks", [float(split[1]), float(split[2]), float(split[3])])
                elif split[0] == "Ke":
                    if len(split) > 2:
                        dic.setdefault("Ke", [float(split[1]), float(split[2]), float(split[3])])
                elif split[0]=="map_Kd":
                    if len(split)>2:
                        dic.setdefault("map_Kd",split[1])
            if not line:
                mtllst.append(dic)
                break
        rf.close()
    return mtllst