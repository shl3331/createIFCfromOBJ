import exportObj
import createIFC

glb = ".\model\curve_45.glb"
dae = ".\model\curve_45.dae"
fbx = ".\model\joint-700mm_normal.fbx"
gltf = ".\model\curve_45.gltf"
saveFile = ".\model\curve_45d.obj"
fbx_hole = ".\model\hole.fbx"
sampleobjfile=".\model\curve_45d.obj"
saveFile= ".\model\joint.obj"
M2= ".\model\cube.obj"

def print_hi(name):
    # 스크립트를 디버그하려면 하단 코드 줄의 중단점을 사용합니다.
    print(f'Hi, {name}')  # 중단점을 전환하려면 Ctrl+F8을(를) 누릅니다.


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    exportObj.convertToObj(fbx,saveFile)
    vertexList=exportObj.getVertex(M2)
    vtList,vnList=exportObj.getVertexTexture(M2)
    faceList,vtMapList,vnMapList=exportObj.getFace(M2)
    groupName=exportObj.getGroupName(M2)
    MaterialList=exportObj.getMtlList(M2)
    newIFCFile=".\model\cube_0705.ifc"
    infoDic={"fid":1,"lat":283718.4593,"lon":373939.1107,"alt":-1.28,"geo":-1.28,"distance":1.85,"line_num":3000,"type":0,"pipe_type":2,"depth":2.54,"instrument_height":180,"diameter":600,"create_date":"2020-02-20 16:35","img":"gnseA/200220-01-1.JPG,gnseA/200220-01-2.jpg,gnseA/200220-01-3.jpg","azimuth":354.0624431,"heading":-0.99,"pitch":-2.17,"roll":0,"curve_deg":"","curve_lat":"","curve_lon":"","curve_pitch":"","curve_depth":"","company_name":"chmetal","model_name":"ks_d_3590","material":"PE","qid":""}
    createIFC.excute("Movements","Movements","Curve",newIFCFile,infoDic, vertexList, faceList, MaterialList, groupName,vtList,vtMapList,vnList,vnMapList)
    print(MaterialList)

# https://www.jetbrains.com/help/pycharm/에서 PyCharm 도움말 참조
