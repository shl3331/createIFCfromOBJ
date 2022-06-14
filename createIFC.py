import tempfile
import ifcopenshell
import time
import uuid


O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.

def getTempIfcfile():
    # Write the template to a temporary file
    temp_handle, temp_filename = tempfile.mkstemp(suffix=".ifc")
    with open(temp_filename, "wb") as f:
        f.write(template.encode())
    return ifcopenshell.open(temp_filename)

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


def create_ifcFacetedBrep(ifcfile, point_list,face_list):
    '''
    create ifcfile face from objfile object vertex list
    :param ifcfile: ifcfile
    :param point_list: obj file object vertex list
    :param face_list: obj file object face list
    :return: ifcfile shape
    '''
    facelist=[]
    ifcptslst = []
    ifcpointlist=[]
    for point in point_list:
        point=ifcfile.createIfcCartesianPoint(point)
        ifcpointlist.append(point)
    for facelst in face_list:
        ifcpts = []
        for face in facelst:
            ifcpts.append(ifcpointlist[int(face)-1])
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

def addObjecttoIfcFile(ifcfile,newFile,infoDic,vertextlst,face_list,mtlList,groupName):
    owner_history = ifcfile.by_type("IfcOwnerHistory")[0]
    project = ifcfile.by_type("IfcProject")[0]
    context = ifcfile.by_type("IfcGeometricRepresentationContext")[0]
    # subcontext = ifcfile.by_type("IfcGeometricRepresentationSubContext")[0]
    axis2placement = ifcfile.by_type("IfcAxis2Placement3D")[0]
    shape = create_ifcFacetedBrep(ifcfile, vertextlst, face_list)
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
    building = ifcfile.createIfcBuilding(create_guid(), owner_history, 'Building', None, None, building_placement,
                                         None,
                                         None, "ELEMENT", None, None, None)
    storey_placement = create_ifclocalplacement(ifcfile, relative_to=building_placement)
    elevation = 0.0
    building_storey = ifcfile.createIfcBuildingStorey(create_guid(), owner_history, 'Storey', None, None,
                                                      storey_placement,
                                                      None, None, "ELEMENT", elevation)
    # container_storey = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Building Container", None,
    #                                                   building,
    #                                                   [building_storey])
    # container_site = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Site Container", None, site,
    #                                                 [building])
    # container_project = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Project Container", None,
    #                                                    project,
    #                                                    [site])

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
    shaperepresantation = ifcfile.createIfcShapeRepresentation(context, 'Body', 'MappedRepresentation',
                                                                [mappedItem])
    ProductDefinitionShape = ifcfile.createIfcProductDefinitionShape(None, None, [shaperepresantation])
    buildingElementProxy = ifcfile.createIfcBuildingElementProxy(ifcopenshell.guid.compress(uuid.uuid1().hex),
                                                                 owner_history, groupName, None, None,
                                                                 local, ProductDefinitionShape, None, None)
    buildingElementProxy = moveElementProxy(buildingElementProxy, [0.0,0.0,0.0])
    ifcfile.createIfcRelContainedInspatialStructure(ifcopenshell.guid.compress(uuid.uuid1().hex), owner_history,
                                                    None,
                                                    None, [buildingElementProxy], building_storey)
    for m in materialLst:
        ifcfile.createIfcRelassociatesMaterial(ifcopenshell.guid.compress(uuid.uuid1().hex), owner_history, None,
                                               None,
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


create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)

filename = ""
timestamp = time.time()
timestring = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp))
creator = "Movements"
organization = "Movements"
objectTpye="Wall"
application, application_version = "IfcOpenShell", "0.5"
project_globalid, project_name = create_guid(), objectTpye

template = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
FILE_NAME('%(filename)s','%(timestring)s',('%(creator)s'),('%(organization)s'),'%(application)s','%(application)s','');
FILE_SCHEMA(('IFC2X3'));
ENDSEC;
DATA;
#1=IFCPERSON($,$,'%(creator)s',$,$,$,$,$);
#2=IFCORGANIZATION($,'%(organization)s',$,$,$);
#3=IFCPERSONANDORGANIZATION(#1,#2,$);
#4=IFCAPPLICATION(#2,'%(application_version)s','%(application)s','');
#5=IFCOWNERHISTORY(#3,#4,$,.ADDED.,$,#3,#4,%(timestamp)s);
#6=IFCDIRECTION((1.,0.,0.));
#7=IFCDIRECTION((0.,0.,1.));
#8=IFCCARTESIANPOINT((0.,0.,0.));
#9=IFCAXIS2PLACEMENT3D(#8,#7,#6);
#10=IFCDIRECTION((0.,1.,0.));
#11=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-05,#9,#10);
#12=IFCDIMENSIONALEXPONENTS(0,0,0,0,0,0,0);
#13=IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.);
#14=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);
#15=IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.);
#16=IFCSIUNIT(*,.PLANEANGLEUNIT.,$,.RADIAN.);
#17=IFCMEASUREWITHUNIT(IFCPLANEANGLEMEASURE(0.017453292519943295),#16);
#18=IFCCONVERSIONBASEDUNIT(#12,.PLANEANGLEUNIT.,'DEGREE',#17);
#19=IFCUNITASSIGNMENT((#13,#14,#15,#18));
#20=IFCPROJECT('%(project_globalid)s',#5,'%(project_name)s',$,$,$,$,(#11),#19);
ENDSEC;
END-ISO-10303-21;
""" % locals()


def excute(creator,organization,objectType,newIFCFile,infoDic, vertexList, faceList, MaterialList, groupName):
    filename=newIFCFile
    creator=creator
    organization=organization
    objectTpye=objectType
    ifcfile=getTempIfcfile()
    resultIFC=addObjecttoIfcFile(ifcfile, newIFCFile, infoDic, vertexList, faceList, MaterialList, groupName)
    resultIFC.write(newIFCFile)


