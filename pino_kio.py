import bpy

context = bpy.context
scene = context.scene
#get a list of armatures in the scene
pk = [i for i in bpy.data.objects if i.type == 'ARMATURE']
#get the armature object
arm_ob = bpy.data.objects[pk[0].name]
#get the armature name
pk_ob = bpy.data.objects[pk[0].name].children[0].name


#Lists
#bones to target
tr_to_list = ["head", "neck", "spine03", "spine02", "spine01", "lowerarm_L", "lowerarm_R", ]
#bones to add IK
ik_list = ["upperarm_L", "upperarm_R"]
#bone target connections
ik_tar = {"upperarm_L": "lowerarm_L", "upperarm_R": "lowerarm_R"}
#track_to target names
tr_to_tar_list = ('headTarget', 'leftTarget', 'rightTarget')


#Track to Targets
tar_get = tr_to_tar_list[0]
tar_get2 = tr_to_tar_list[1]
tar_get3 = tr_to_tar_list[2]


#pino_kio_dictionary
#{bone name:[influence, up axis, track axis, target name]}
pk_dict = {'head': [1.0, 'UP_Y', 'TRACK_Z', tar_get],
        'neck': [0.5, 'UP_Y', 'TRACK_Z', tar_get],
        'spine03': [0.25, 'UP_Y', 'TRACK_Z', tar_get],
        'spine02': [0.1, 'UP_Y', 'TRACK_Z', tar_get],
        'spine01': [0.1, 'UP_Y', 'TRACK_Z', tar_get],
        'lowerarm_L': [1.0, 'UP_Z', 'TRACK_Y', tar_get2],
        'lowerarm_R': [1.0, 'UP_Z', 'TRACK_Y', tar_get3]}

############################################################################################################################### 

#set armature to object mode if not
if bpy.ops.object.mode_set(mode='OBJECT') == False:
    bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

#Create Custom Property
bpy.data.armatures[0]["Arm_IK"] = True
bpy.data.armatures[0]["Arm_IK"] = 0.75


#Add Track to Targets
for i in range(3):
    bpy.ops.object.empty_add(type='SPHERE', radius=0.1, view_align=False, location=(0, -1, 1.5))
bpy.data.objects["Empty"].name = tar_get
bpy.data.objects["Empty.001"].location.x = 0.5
bpy.data.objects["Empty.001"].name = tar_get2
bpy.data.objects["Empty.002"].location.x = -0.5
bpy.data.objects["Empty.002"].name = tar_get3


#Select Armature
bpy.data.objects[arm_ob.name].select = True
bpy.context.scene.objects.active = arm_ob
#Set pose mode 
bpy.ops.object.mode_set(mode='POSE')

############################################################################################################################### 

#ADD BONE IK DRIVERS
def add_IK_drive(pbs):
    tdr = arm_ob.driver_add("pose.bones[\"" + pbs + "\"].constraints[\"IK\"].influence").driver
    tdr.type = 'AVERAGE'
    var = tdr.variables.new()
    var.targets[0].id_type = 'ARMATURE'
    var.targets[0].id = bpy.data.armatures[0]
    var.targets[0].data_path = "[\"Arm_IK\"]"
    var.name = "IK_influence"
    print(pbs + "<<<driver>>>")


############################################################################################################################### 

###__MAIN__###

def pino_kio():
    #TRACK_TO_CONSTRAINT
    for bo in bpy.context.object.pose.bones:
        if bo.name in tr_to_list:
            tt = pk_dict.get(bo.name)
            nc = bo.constraints.new(type='TRACK_TO')
            nc.target = bpy.data.objects[tt[3]]
            nc.influence = tt[0]
            nc.use_target_z = True
            nc.up_axis = tt[1]
            nc.track_axis = tt[2]

    #IK_CONSTRAINT
    for bo in bpy.context.object.pose.bones:
        if bo.name in ik_list:
            nc = bo.constraints.new(type='IK')
            nc.target = bpy.data.objects[arm_ob.name]
            nc.subtarget = ik_tar.get(bo.name)
            nc.influence = 0.5
            nc.use_rotation = True
            nc.use_location = True
            nc.chain_count = 1
    
    #Add Drivers
    for d in ik_list:
        add_IK_drive(d)
    
    #Set object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    #Deselect everything
    bpy.ops.object.select_all(action='DESELECT')

############################################################################################################################### 

#run script
pino_kio()
