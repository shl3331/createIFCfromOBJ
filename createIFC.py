import tempfile
import ifcopenshell
import time
import uuid


O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.

global creator
global organization
newFile="20220608.ifc"
def create_ifcaxis2placement(ifcfile, point=O, dir1=Z, dir2=X):
    '''
    Creates an IfcAxis2Placement3D from Location, Axis and RefDirection specified as Python tuples
    :param ifcfile: ifcFile
    :param point: object vertex point
    :param dir1: Direction Z Z = 0., 0., 1.
    :param dir2: Direction X X = 1., 0., 0.
    :return: new axise2D Placement
    '''
    point = ifcfile.createIfcCartesianPoint(point)
    dir1 = ifcfile.createIfcDirection(dir1)
    dir2 = ifcfile.createIfcDirection(dir2)
    axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
    return axis2placement

# Creates an IfcLocalPlacement from Location, Axis and RefDirection, specified as Python tuples, and relative placement
def create_ifclocalplacement(ifcfile, point=O, dir1=Z, dir2=X, relative_to=None):
    '''
    Creates an IfcLocalPlacement from Location, Axis and RefDirection, specified as Python tuples, and relative placement
    :param ifcfile: ifcFile
    :param point: object vertex point
    :param dir1: Direction Z Z = 0., 0., 1.
    :param dir2: Direction X X = 1., 0., 0.
    :param relative_to: None
    :return: local placement
    '''
    axis2placement = create_ifcaxis2placement(ifcfile, point, dir1, dir2)
    ifclocalplacement2 = ifcfile.createIfcLocalPlacement(relative_to, axis2placement)
    return ifclocalplacement2


# Creates an IfcPolyLine from a list of points, specified as Python tuples
def create_ifcpolyline(ifcfile, point_list):
    '''
    Creates an IfcPolyLine from a list of points, specified as Python tubles
    :param ifcfile: ifcfile
    :param point_list: obj file object vertex list
    :return: ifcpolyline
    '''
    ifcpts = []
    for point in point_list:
        point = ifcfile.createIfcCartesianPoint(point)
        ifcpts.append(point)
    polyline = ifcfile.createIfcPolyLine(ifcpts)
    return polyline
def create_ifcCartesianPoint(ifcfile,point_list):
    '''
    obj object vertex list to ifc point
    :param ifcfile:ifcFile
    :param point_list:obj file object vertex list
    :return:
    '''
    for point in point_list:
        point=ifcfile.createIfcCartesianPoint(point)

def create_ifcTextureVertex(ifcfile,vt_list):
    '''
    obj object vertex list to ifc point
    :param ifcfile:ifcFile
    :param point_list:obj file object vertex list
    :return:
    '''
    pointLst=[]
    for point in vt_list:
        point=ifcfile.createIfcTextureVertex(point)
        pointLst.append(point)

# Creates an IfcExtrudedAreaSolid from a list of points, specified as Python tuples
def create_ifcextrudedareasolid(ifcfile, point_list, ifcaxis2placement, extrude_dir, extrusion):
    polyline = create_ifcpolyline(ifcfile, point_list)
    ifcclosedprofile = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
    ifcdir = ifcfile.createIfcDirection(extrude_dir)
    ifcextrudedareasolid = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile, ifcaxis2placement, ifcdir, extrusion)
    return ifcextrudedareasolid

def create_ifcFacetedBrep(ifcfile, point_list,face_list,vtList,vtMapList):
    '''
    create ifcfile face from objfile object vertex list
    :param ifcfile: ifcfile
    :param point_list: obj file object vertex list
    :param face_list: obj file object face list
    :return: ifcfile shape
    '''
    facelist=[]
    ifcptslst = []
    ifcpointlst=[]
    ifctexturevertexlst=[]
    for point in point_list:
        point=ifcfile.createIfcCartesianPoint(point)
        ifcpointlst.append(point)
    for vt in vtList:
        ifctexturevertexlst.append(ifcfile.createIfcTextureVertex(vt))
    for vtMap in vtMapList:
        ifcfile.createIfctexturemap([ifctexturevertexlst[int(vtMap[0])-1],ifctexturevertexlst[int(vtMap[1])-1],ifctexturevertexlst[int(vtMap[2])-1]])
    for facelst in face_list:
        ifcpts = []
        for face in facelst:
            ifcpts.append(ifcpointlst[int(face)-1])
        ifcptslst.append(ifcpts)
    for pts in ifcptslst:
        polyloop=ifcfile.createIfcPolyLoop(pts)
        faceouterbound=ifcfile.createIfcFaceOuterBound(polyloop,True)
        face=ifcfile.createIfcFace([faceouterbound])
        facelist.append(face)
    closedshell=ifcfile.createIfcClosedShell(facelist)
    shape = ifcfile.createIfcFacetedBrep(closedshell)
    return shape

def moveElementProxy(ifcBuildingElementProxy,locationList):
    '''
    create moveElementProxy in ifcfile
    :param ifcBuildingElementProxy: get ifcBuildingElementProxy in ifcFile
    :param locationList: locationList x,y,z
    :return: ifcBuildingElementProxy in ifcFile
    '''
    ifcBuildingElementProxy.ObjectPlacement.RelativePlacement.Location.Coordinates = (locationList[0], locationList[1], locationList[2])
    return ifcBuildingElementProxy

create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)
timestamp = time.time()
timestring = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp))
application, application_version = "IfcOpenShell", "0.6"
project_globalid, project_name = create_guid(), "Hello Wall"

# A template IFC file to quickly populate entity instances for an IfcProject with its dependencies
template = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
FILE_NAME('""" + newFile + """','2020-11-20T12:19:44+09:00',(),(),'IfcOpenShell 0.6.0b0','BlenderBIM 0.0.200621','Moult');
FILE_SCHEMA(('IFC4'));
ENDSEC;
DATA;
#1=IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.);
#2=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);
#3=IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.);
#4=IFCUNITASSIGNMENT((#1,#2,#3));
#5=IFCACTORROLE(.ARCHITECT.,$,'Draws the pretty pictures');
#6=IFCPOSTALADDRESS(.OFFICE.,'Headquarters',$,'Cupboard under the stairs',('221B Baker Street'),$,'MyTown','Middle-Earth','42','Narnia');
#7=IFCTELECOMADDRESS(.OFFICE.,'Headquarters',$,('0123456789'),$,$,('dion@thinkmoult.com'),'https://thinkmoult.com',('irc://irc.freenode.net##architect'));
#8=IFCPERSON('Moult','Moult','Dion',('Sebastian','Isan','Tan'),('Mr'),('UE'),(#5),(#6,#7));
#9=IFCACTORROLE(.USERDEFINED.,'CONTRIBUTOR',$);
#10=IFCTELECOMADDRESS(.USERDEFINED.,'The main webpage of the software collection.','WEBPAGE',$,$,$,$,'https://ifcopenshell.org',$);
#11=IFCTELECOMADDRESS(.USERDEFINED.,'The BlenderBIM webpage of the software collection.','WEBPAGE',$,$,$,$,'https://blenderbim.org',$);
#12=IFCTELECOMADDRESS(.USERDEFINED.,'The source code repository of the software collection.','REPOSITORY',$,$,$,$,'https://github.com/IfcOpenShell/IfcOpenShell.git',$);
#13=IFCORGANIZATION($,'IfcOpenShell','IfcOpenShell is an open source (LGPL) software library that helps users and software developers to work with the IFC file format.',(#9),(#10,#11,#12));
#14=IFCCARTESIANPOINT((0.,0.,0.));
#15=IFCDIRECTION((0.,0.,1.));
#16=IFCDIRECTION((1.,0.,0.));
#17=IFCAXIS2PLACEMENT3D(#14,#15,#16);
#18=IFCPERSONANDORGANIZATION(#8,#13,$);
#19=IFCAPPLICATION(#13,'0.0.200621','BlenderBIM','BlenderBIM');
#20=IFCOWNERHISTORY(#18,#19,.READWRITE.,.NOCHANGE.,1605842384,#18,#19,1605842384);
#21=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-05,#17,$);
#22=IFCGEOMETRICREPRESENTATIONSUBCONTEXT('Body','Model',*,*,*,*,#21,$,.MODEL_VIEW.,$);
#23=IFCPROJECT('1nr0ixnS13wfYAfjpLBIT8',$,'My Project',$,$,$,$,(#21),#4);
#24=IFCOBJECTIVE('Beauty','The built form should be beautiful',.HARD.,$,$,$,$,$,$,.DESIGNINTENT.,$);
#25=IFCOBJECTIVE('Safety','No facilities exist to generate killer artificial intelligence',.HARD.,$,$,$,$,$,$,.HEALTHANDSAFETY.,$);
#26=IFCSHAPEREPRESENTATION(#22,'Body','Brep',());
#27=IFCREPRESENTATIONMAP(#17,#26);
ENDSEC;
END-ISO-10303-21;
""" % locals()

# Write the template to a temporary file
temp_handle, temp_filename = tempfile.mkstemp(suffix=".ifc")
with open(temp_filename, "wb") as f:
    f.write(template.encode())

# Obtain references to instances defined in template
ifcfile = ifcopenshell.open(temp_filename)

def addObjecttoIfcFile(newFile,infoDic,vertextlst,face_list,mtlList,groupName,vtList,vtMapList):
    owner_history = ifcfile.by_type("IfcOwnerHistory")[0]
    project = ifcfile.by_type("IfcProject")[0]
    context = ifcfile.by_type("IfcGeometricRepresentationContext")[0]
    subcontext = ifcfile.by_type("IfcGeometricRepresentationSubContext")[0]
    axis2placement = ifcfile.by_type("IfcAxis2Placement3D")[0]
    representationMap = ifcfile.by_type("IfcRepresentationMap")[0]
    shape = create_ifcFacetedBrep(ifcfile, vertextlst, face_list,vtList,vtMapList)
    shapeRepresentation = ifcfile.createIfcShapeRepresentation(context, "Body", "Brep", [shape])
    createdMap = ifcfile.createIfcRepresentationMap(axis2placement, shapeRepresentation)
    materialLst = []
    for dic in mtlList:
        rgb1 = ifcfile.createIfcColourRgb(None, dic.get("Kd")[0], dic.get("Kd")[1], dic.get("Kd")[2])
        rgb2 = ifcfile.createIfcColourRgb(None, dic.get("Ka")[0], dic.get("Ka")[1], dic.get("Ka")[2])
        ssr = ifcfile.createIfcSurfaceStyleRendering(rgb1, -0, rgb2, None, None, None, None, None, "NOTDEFINED")
        iss = ifcfile.createIfcSurfaceStyle(dic.get("newmtl"), "BOTH", [ssr])
        styledItem = ifcfile.createIfcStyledItem(None, [iss], dic.get("newmtl"))
        styleDrepresentation = ifcfile.createIfcStyledRepresentation(context, None, None, [styledItem])
        material = ifcfile.createIfcMaterial(dic.get("newmtl"))
        materialDefinitionRepresentation = ifcfile.createIfcMaterialDefinitionRepresentation(dic.get("newmtl"),
                                                                                             None,
                                                                                             [styleDrepresentation],
                                                                                             material)

        materialLst.append(material)
    site_placement = create_ifclocalplacement(ifcfile)
    site = ifcfile.createIfcSite(create_guid(), owner_history, "Site", None, None, site_placement, None, None,
                                 "ELEMENT",
                                 None, None, None, None, None)
    building_placement = create_ifclocalplacement(ifcfile, relative_to=site_placement)
    building = ifcfile.createIfcBuilding(create_guid(), owner_history, 'Building', None, None, building_placement, None,
                                         None, "ELEMENT", None, None, None)
    storey_placement = create_ifclocalplacement(ifcfile, relative_to=building_placement)
    elevation = 0.0
    building_storey = ifcfile.createIfcBuildingStorey(create_guid(), owner_history, 'Storey', None, None,
                                                      storey_placement,
                                                      None, None, "ELEMENT", elevation)
    container_storey = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Building Container", None,
                                                      building,
                                                      [building_storey])
    container_site = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Site Container", None, site,
                                                    [building])
    container_project = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Project Container", None, project,
                                                       [site])

    pt = ifcfile.createIfcCartesianPoint((0., 0., 0.))
    dir1 = ifcfile.createIfcDirection((0., 0., 1.0))
    dir2 = ifcfile.createIfcDirection((1., 0., 0.))
    axis = ifcfile.createIfcAxis2Placement3D(pt, dir1, dir2)
    local = ifcfile.createIfcLocalPlaceMent(storey_placement, axis)

    dir3 = ifcfile.createIfcDirection(X)
    dir4 = ifcfile.createIfcDirection(Y)
    pt2 = ifcfile.createIfcCartesianPoint((0., 0., 0.))
    dir5 = ifcfile.createIfcDirection(Z)
    cartesiantranspormationperator3D = ifcfile.createIfcCartesianTransformationOperator3D(dir3, dir4, pt2, 1., dir5)
    mappedItem = ifcfile.createIfcMappedItem(createdMap, cartesiantranspormationperator3D)
    shaperepresantation2 = ifcfile.createIfcShapeRepresentation(subcontext, 'Body', 'MappedRepresentation',
                                                                [mappedItem])
    ProductDefinitionShape = ifcfile.createIfcProductDefinitionShape(None, None, [shaperepresantation2])
    buildingElementProxy = ifcfile.createIfcBuildingElementProxy(ifcopenshell.guid.compress(uuid.uuid1().hex),
                                                                 owner_history, groupName, None, None,
                                                                 local, ProductDefinitionShape, None, None)
    # buildingElementProxy = moveElementProxy(buildingElementProxy, resultDic.get("XyzList")[i])
    ifcfile.createIfcRelContainedInspatialStructure(ifcopenshell.guid.compress(uuid.uuid1().hex), owner_history, None,
                                                    None, [buildingElementProxy], building_storey)
    for m in materialLst:
        ifcfile.createIfcRelassociatesMaterial(ifcopenshell.guid.compress(uuid.uuid1().hex), owner_history, None, None,
                                               [buildingElementProxy], m)
    property_values = []
    for key, value in infoDic.items():
        property_values.append(
            ifcfile.createIfcPropertySingleValue(key, newFile, ifcfile.create_entity("IfcText", str(value)), None))
    property_set = ifcfile.createIfcPropertySet(create_guid(), owner_history, "Json Data", None, property_values)
    ifcfile.createIfcRelDefinesByProperties(create_guid(), owner_history, None, None, [buildingElementProxy],
                                            property_set)
    ifcfile.add(project)
    ifcfile.add(buildingElementProxy)
    return ifcfile




def excute(creator,organization,objectType,newIFCFile,infoDic, vertexList, faceList, MaterialList, groupName,vtList,vtMapList):
    global newFile
    newFile=newIFCFile


    resultIFC=addObjecttoIfcFile(newIFCFile, infoDic, vertexList, faceList, MaterialList, groupName,vtList,vtMapList)
    resultIFC.write(newIFCFile)


