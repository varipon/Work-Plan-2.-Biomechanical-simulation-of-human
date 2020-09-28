# ================
# SOFTWARE LICENSE
# ================

# The MIT License (MIT)

# Copyright (c) 2020 Yutaka Sawai (Varipon)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ==============================================================
# LICENSE FOR CONTENT PROCEDURALLY GENERATED USING THIS SOFTWARE
# ==============================================================

# All content procedurally generated by this software and its permutations
# are licensed under Creative Commons Attribution By 3.0:

# https://creativecommons.org/licenses/by/3.0/


#!/usr/bin/python

import bpy
from bpy import *

import mathutils
import math
from mathutils import *
from math import *


class Formula:

    def __init__(self, P, A, J, move, part, helicity, start, end):

        global interval
        global frame_start
        global frame_end

        self.interval = interval
        self.frame_start = frame_start
        self.frame_end = frame_end

        # pivot factor
        self.P = P

        # scale factor
        self.A = A 
        
        # joint number
        self.J = J

        # name
        self.move = move

        # element
        self.part = part

        # element helicity
        self.helicity = helicity

        self.start = start
        self.end = end

        # Create armature and object
        self.amt = bpy.data.armatures.new(move + '.' + part + '.' + helicity + '.data')
        self.rig = bpy.data.objects.new(move + '.' + part + '.' + helicity, self.amt)

        # Joints α(n) -> a[n], β(n) -> b[n], γ(n) -> y[n], δ(n) -> o[n]
        self.a = [0 for i in range(4)] # Joint α
        self.b = [0 for i in range(self.J)] # Joint β
        self.y = [0 for i in range(self.J)] # Joint γ
        self.o = [0 for i in range(self.J)] # Joint δ

        # Configuration Movement
        self.configMovement(self.P, self.A, self.J, self.a, self.b, self.y, self.o)

        # Construction Movement
        self.constructMovement(self.J, self.helicity, self.amt, self.rig, self.a, self.b, self.y, self.o)

        # Construction Rotation
        self.configRotation(self.rig, self.interval, self.frame_start, self.frame_end, self.start, self.end)

        # Configuration Linkage
        self.configLink(self.A, self.J, self.helicity, self.rig, self.move, self.part)

        # Construction Linkage
        self.constructLink(self.A, self.J, self.helicity, self.rig, self.move, self.part)


    def configMovement(self, P, A, J, a, b, y, o):

        mat_a = [0 for i in range(4)] # Joint α matrix
        mat_b = [0 for i in range(self.J)] # Joint β matrix
        mat_y = [0 for i in range(self.J)] # Joint γ matrix
        mat_o = [0 for i in range(self.J)] # Joint δ matrix

        a[1] = mathutils.Euler((P, A, 0.0), 'XYZ')
        print ("a1 =", a[1])

        a[2] = mathutils.Euler((A, -A, 0.0), 'XYZ')
        print ("a2 =", a[2])

        b[1] = mathutils.Euler((-A, A, 0.0), 'XYZ')
        print ("b1 =", b[1])

        o[1] = mathutils.Euler((A, A, 0.0), 'XYZ')
        print ("o1 =", o[1])

        B = A * 2 * sqrt (2)
        C = B + (B * sqrt (2))
        D = C * sqrt (2)
        E = C + D

        a[0] = mathutils.Euler((-A - E + (D * 0.5), -A - (D * 0.5), 0.0), 'XYZ')
        print ("a0 =", a[0])
        mat_a[0] = Matrix.Translation(a[0])

        a[3] = mathutils.Euler((0-a[0].x, 0-a[0].y, 0-a[0].z), 'XYZ')
        print ("a3 =", a[3])
        mat_a[3] = Matrix.Translation(a[3]) 

        y[1] = mathutils.Euler((-A, -A, 0.0), 'XYZ')
        print ("y1 =", y[1])
        mat_y[1] = Matrix.Translation(y[1])

### pattern A

        b[2] = mathutils.Euler((a[0].x + E + (A * 2), a[0].y + (A * 2), 0.0), 'XYZ')
        print ("b2 =", b[2])
        mat_b[2] = Matrix.Translation(b[2])

        b[3] = mathutils.Euler((a[0].x + E - (D * 0.5), a[0].y - (A * 2), 0.0), 'XYZ')
        print ("b3 =", b[3])
        mat_b[3] = Matrix.Translation(b[3])
        
        y[2] = mathutils.Euler((a[0].x + E, a[0].y, 0.0), 'XYZ')
        print ("y2 =", y[2])
        mat_y[2] = Matrix.Translation(y[2])

        y[3] = mathutils.Euler((a[0].x + E - (D * 0.5), a[0].y - (D * 0.5), 0.0), 'XYZ')
        print ("y3 =", y[3])
        mat_y[3] = Matrix.Translation(y[3])

        o[2] = mathutils.Euler((a[0].x + E + (A * 2), a[0].y - (A * 2), 0.0), 'XYZ')
        print ("o2 =", o[2])
        mat_o[2] = Matrix.Translation(o[2])
        
        o[3] = mathutils.Euler((a[0].x + E - (D * 0.5) - (A * 2), a[0].y - (D * 0.5) - (A * 2), 0.0), 'XYZ')
        print ("o3 =", o[3])
        mat_o[3] = Matrix.Translation(o[3])

### pattern A end

        org_rot_mat = Matrix.Rotation(math.radians(0), 4, 'Z')

        # define the rotation
        rot_mat = Matrix.Rotation(math.radians(-45), 4, 'Z')   

        for j in range(2, J - 2):

            mat_y[j + 2] = mat_a[0] @ org_rot_mat @ rot_mat @ mat_a[3] @ mat_y[j]

#            obj.matrix_world = mat_y[j + 2]
            # extract components back out of the matrix
            loc, rot, sca = mat_y[j + 2].decompose()
            y[j + 2] = mathutils.Euler(loc, 'XYZ')
            print("y"+str(j + 2)+" = ", y[j + 2], rot, sca)

            mat_b[j + 2] = mat_a[0] @ org_rot_mat @ rot_mat @ mat_a[3] @ mat_b[j]
            
#            obj.matrix_world = mat_b[j + 2]
            # extract components back out of the matrix
            loc, rot, sca = mat_b[j + 2].decompose()
            b[j + 2] = mathutils.Euler(loc, 'XYZ')
            print("b"+str(j + 2)+" = ", b[j + 2], rot, sca)

            mat_o[j + 2] = mat_a[0] @ org_rot_mat @ rot_mat @ mat_a[3] @ mat_o[j]
            
#            obj.matrix_world = mat_o[j + 2]
            # extract components back out of the matrix
            loc, rot, sca = mat_o[j + 2].decompose()
            o[j + 2] = mathutils.Euler(loc, 'XYZ')
            print("o"+str(j + 2)+" = ", o[j + 2], rot, sca)


    def constructMovement(self, J, helicity, amt, rig, a, b, y, o):

        # Linkages
        aa = [[0 for i in range(4)] for j in range(4)] # Link α(i) - α(j)
        ab = [[0 for i in range(4)] for j in range(4)] # Link α(i) - β(j)
        ya = [[0 for i in range(4)] for j in range(4)] # Link γ(i) - α(j)
        ao = [[0 for i in range(4)] for j in range(4)] # Link α(i) - δ(j)
        ob = [[0 for i in range(self.J)] for j in range(self.J)] # Link δ(i) - β(j)
        yy = [[0 for i in range(self.J)] for j in range(self.J)] # Link γ(i) - γ(j)
        by = [[0 for i in range(self.J)] for j in range(self.J)] # Link β(i) - γ(j)
        yo = [[0 for i in range(self.J)] for j in range(self.J)] # Link γ(i) - δ(j)

        rig.location = mathutils.Euler((0.0, 0.0, 0.0), 'XYZ')
        rig.show_in_front = True
        amt.show_names = True
        amt.display_type = 'STICK'
#        amt.display_type = 'BBONE'

        # Link object to scene

        bpy.data.collections['movement'].objects.link(rig)
        bpy.context.view_layer.objects.active = rig
        bpy.context.view_layer.update()

        # Edit
        bpy.ops.object.editmode_toggle()

        # Construction Linkage
        aa[2][1] = amt.edit_bones.new('a2a1')
        aa[2][1].head = a[2]
        aa[2][1].tail = a[1]
        
        ab[1][1] = amt.edit_bones.new('a1b1')
        ab[1][1].head = a[1]
        ab[1][1].tail = b[1]
        ab[1][1].parent = aa[2][1]
 
        by[1][1] = amt.edit_bones.new('b1y1')
        by[1][1].head = b[1]
        by[1][1].tail = y[1]
        by[1][1].parent = ab[1][1]
        by[1][1].use_inherit_rotation = False

        ya[1][2] = amt.edit_bones.new('y1a2')
        ya[1][2].head = y[1]
        ya[1][2].tail = a[2]
        ya[1][2].parent = by[1][1]

        ao[2][1] = amt.edit_bones.new('a2o1')
        ao[2][1].head = a[2]
        ao[2][1].tail = o[1]
        ao[2][1].parent = ya[1][2]

        ob[1][2] = amt.edit_bones.new('o1b2')
        ob[1][2].head = o[1]
        ob[1][2].tail = b[2]
        ob[1][2].parent = ao[2][1]
        
        yy[1][2] = amt.edit_bones.new('y1y2')
        yy[1][2].head = y[1]
        yy[1][2].tail = y[2]
        yy[1][2].parent = by[1][1]

        for j in range(2, J - 1):

            by[j][j] = amt.edit_bones.new('b'+ str(j) + 'y'+ str(j))
            by[j][j].head = b[j]
            by[j][j].tail = y[j]
            by[j][j].parent = ob[j-1][j]

            yo[j][j] = amt.edit_bones.new('y'+ str(j) + 'o'+ str(j))
            yo[j][j].head = y[j]
            yo[j][j].tail = o[j]
            yo[j][j].parent = yy[j-1][j]

            yy[j][j+1] = amt.edit_bones.new('y'+ str(j) + 'y'+ str(j+1))
            yy[j][j+1].head = y[j]
            yy[j][j+1].tail = y[j+1]
            yy[j][j+1].parent = by[j][j]

            if j < (J-2):
                ob[j][j+1] = amt.edit_bones.new('o'+ str(j) + 'b'+ str(j+1))
                ob[j][j+1].head = o[j]
                ob[j][j+1].tail = b[j+1]
                ob[j][j+1].parent = yo[j][j]

        # all bones select

        # Bone constraints. Armature must be in pose mode.
        bpy.ops.object.mode_set(mode='POSE')

        bpy.ops.pose.select_all(action="SELECT")

        # Edit
        bpy.ops.object.editmode_toggle()

        if helicity == 'right':
            bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')
        else:
            bpy.ops.armature.calculate_roll(type='GLOBAL_NEG_Z')
 
        # IK constraint
        cns = rig.pose.bones['y1a2'].constraints.new('IK')
        cns.name = 'Ik'
        cns.target = rig
        cns.subtarget = 'a2a1'
        cns.chain_count = 2
        cns.use_stretch = False

        for j in range(2, J - 1):
            cns = rig.pose.bones['b'+str(j) +'y'+str(j)].constraints.new('IK')
            cns.name = 'Ik'
            cns.target = rig
            cns.subtarget = 'y'+str(j)+'o'+str(j)
            cns.iterations = 500
            cns.chain_count = 2
            cns.use_stretch = False

        bpy.ops.object.mode_set(mode='OBJECT')
        

    def configRotation(self, rig, interval, frame_start, frame_end, start, end):

        # Bone constraints. Armature must be in pose mode.
        bpy.ops.object.mode_set(mode='POSE')

        # key insert 
        keyframe_insert_interval = interval

        rig.pose.bones["a1b1"].rotation_mode = 'XYZ'
        rig.pose.bones["a1b1"].rotation_euler.z = math.radians(start) 
        rig.pose.bones["a1b1"].keyframe_insert(data_path="rotation_euler",frame=frame_start)

        rig.pose.bones["a1b1"].rotation_mode = 'XYZ'
        rig.pose.bones["a1b1"].rotation_euler.z = math.radians(end)
        rig.pose.bones["a1b1"].keyframe_insert(data_path="rotation_euler",frame=frame_end)

        for curve in bpy.context.active_object.animation_data.action.fcurves:
            cycles = curve.modifiers.new(type='CYCLES')
            cycles.mode_before = 'REPEAT_OFFSET'
            cycles.mode_after = 'REPEAT_OFFSET'

            for keyframe in curve.keyframe_points:
                keyframe.interpolation = 'LINEAR'

        bpy.ops.object.mode_set(mode='OBJECT')


    def configLink(self, A, J, helicity, rig, move, part):

        bpy.ops.object.mode_set(mode='OBJECT')
    
        Q = (0.18648+0.146446)*A
    #   Z = -Q*2
        Z = 0.0

        obj_joint = bpy.data.objects["joint.gold.000"].copy()
        obj_joint.location = (0.0, 0.0, -Q*3+Z)
        obj_joint.scale = (A, A, A)
        obj_joint.name = "a2a1.mesh." + move + '.' + part +'.' + helicity
        bpy.data.collections['link'].objects.link(obj_joint)

        obj_joint = bpy.data.objects["joint.silver.001"].copy()
        obj_joint.location = (0.0, 0.0, +Q+Z)
        obj_joint.scale = (A, A, A)
        obj_joint.name = "y1a2.mesh." + move + '.' + part +'.' + helicity
        bpy.data.collections['link'].objects.link(obj_joint)

        obj_joint = bpy.data.objects["joint.copper.001"].copy()
        obj_joint.location = (0.0, 0.0, +Q*3+Z)
        obj_joint.scale = (A, A, A)
        obj_joint.name = "a2o1.mesh." + move + '.' + part +'.' + helicity
        bpy.data.collections['link'].objects.link(obj_joint)

        obj_joint = bpy.data.objects["joint.blue.001"].copy()
        obj_joint.location = (0.0, 0.0, -Q*2+Z)
        obj_joint.scale = (A, A, A)
        obj_joint.name = "a1b1.mesh." + move + '.' + part +'.' + helicity
        bpy.data.collections['link'].objects.link(obj_joint)


        for n in range(1, J - 1):

            if n <= (J-2):

                # Pattern 2 of by
                obj_joint = bpy.data.objects["joint.green.001"].copy()
                obj_joint.location = (0.0, 0.0, -Q + Q*((n+1) % 2)*4 +Z)
                obj_joint.scale = (A, A, A)
                obj_joint.name = "b"+str(n)+"y"+str(n)+".mesh." + move + '.' + part +'.' + helicity
                bpy.data.collections['link'].objects.link(obj_joint)

                # Pattern 2 of yy
                obj_joint = bpy.data.objects["joint.gold.00"+str(1 + (n+1) % 2)].copy()
                obj_joint.location = (0.0, 0.0, +Q*(1 - (n % 2))*2+Z)
                obj_joint.scale = (A, A, A)
                obj_joint.name = "y"+str(n)+"y"+str(n+1)+".mesh." + move + '.' + part +'.' + helicity
                bpy.data.collections['link'].objects.link(obj_joint)


            if n <= (J-3):

                # Pattern 1 of ob
                obj_joint = bpy.data.objects["joint.blue.001"].copy()
                obj_joint.location = (0.0, 0.0, -Q*2 + Q*(n % 2)*6 +Z)
                obj_joint.scale = (A, A, A)
                obj_joint.name = "o"+str(n)+"b"+str(n+1)+".mesh." + move + '.' + part +'.' + helicity
                bpy.data.collections['link'].objects.link(obj_joint)

                # Pattern 2 of yo
                obj_joint = bpy.data.objects["joint.copper.001"].copy()
                obj_joint.location = (0.0, 0.0, -Q + Q*((n+1) % 2)*4 +Z)
                obj_joint.scale = (A, A, A)
                obj_joint.name = "y"+str(n+1)+"o"+str(n+1)+".mesh." + move + '.' + part +'.' + helicity
                bpy.data.collections['link'].objects.link(obj_joint)


        for ob in data.collections['link'].objects:
            if "mesh" in ob.name:
                ob.select_set(state = True, view_layer = None)

        bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True, material=True, animation=True)
        bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')


    def constructLink(self, A, J, helicity, rig, move, part):

        # Move and rotate the tip bone in pose mode
        bpy.context.view_layer.objects.active = rig 

        Y = 1.1838*A

        for n in rig.pose.bones:
            if n.name != "o" + str(J-2) + "b" + str(J-1):
                # we can get the object from the pose bone
                obj = n.id_data
                matrix_final = obj.matrix_world @ n.matrix

                # Create armature and object
                lnk = bpy.data.armatures.new(n.name[:len(n.name)]+'.data.' + helicity)
                lnk_rig = bpy.data.objects.new(n.name[:len(n.name)]+'.link.' + helicity, lnk)
                lnk_rig.location = mathutils.Euler((0.0, 0.0, 0.0), 'XYZ')

                # rig.show_in_front = True
                lnk.show_names = True
                lnk.display_type = 'STICK'

                bpy.data.collections['link'].objects.link(lnk_rig)
                bpy.context.view_layer.objects.active = lnk_rig
                bpy.context.view_layer.update()

                # Create bones

                # mode='EDIT'
                bpy.ops.object.editmode_toggle()
    
                link = lnk.edit_bones.new(n.name[:len(n.name)])
                link.head = (0.0, 0.0, 0.0)
                link.tail = (0.0, Y, 0.0)

                link_head = lnk.edit_bones.new('head')
                link_head.head = (0.0, 0.0, 0.1)
                link_head.tail = (0.0, 0.0, 0.0)
                link_head.parent = link
                link_head.use_inherit_scale = False

                link_tail = lnk.edit_bones.new('tail')
                link_tail.head = (0.0, Y, 0.0)
                link_tail.tail = (0.0, Y, -0.1)
                link_tail.parent = link
                link_tail.use_inherit_scale = False

                bpy.ops.object.mode_set(mode='OBJECT')

                ob = bpy.data.objects[n.name[:len(n.name)]+'.mesh.' + move + '.' + part +'.' + helicity]
                ob.location = mathutils.Euler((0.0, 0.0, 0.0), 'XYZ')
    
                # Give mesh object an armature modifier, using vertex groups but
                # not envelopes
                mod = ob.modifiers.new('MyRigModif', 'ARMATURE')
                mod.object = lnk_rig
                mod.use_bone_envelopes = False
                mod.use_vertex_groups = True

                # Bone constraints. Armature must be in pose mode.
                bpy.ops.object.mode_set(mode='POSE')
 
                # Copy rotation constraints Base -> Tip
                pBase = lnk_rig.pose.bones[n.name[:len(n.name)]]
                cns = pBase.constraints.new('COPY_LOCATION')
                cns.name = 'Copy_Location'
                cns.target = rig
                cns.subtarget = n.name[:len(n.name)]
                cns.owner_space = 'WORLD'
                cns.target_space = 'WORLD'

                # Copy rotation constraints Base -> Tip
                pBase = lnk_rig.pose.bones[n.name[:len(n.name)]]
                cns = pBase.constraints.new('COPY_ROTATION')
                cns.name = 'Copy_Rotation'
                cns.target = rig
                cns.subtarget = n.name[:len(n.name)]
                cns.owner_space = 'WORLD'
                cns.target_space = 'WORLD'

                # StretchTo constraint Mid -> Tip with influence 0.5
                cns1 = pBase.constraints.new('STRETCH_TO')
                cns1.name = 'Stretch'
                cns1.target = rig
                cns1.subtarget = n.name[:len(n.name)]
                cns1.head_tail = 1
                cns1.rest_length = Y
                cns1.influence = 1
                cns1.keep_axis = 'PLANE_Z'
                cns1.volume = 'NO_VOLUME'

                bpy.ops.object.mode_set(mode='OBJECT')


class Leg(Formula):

    J = 7 #joint number

    # Overriding
    def __init__(self, P, A, move, part, helicity, start, end):

        global interval
        global frame_start
        global frame_end

        self.interval = interval
        self.frame_start = frame_start
        self.frame_end = frame_end

        # pivot factor
        self.P = P

        # scale factor
        self.A = A 

        # name
        self.move = move

        # element
        self.part = part

        # element helicity
        self.helicity = helicity

        self.start = start
        self.end = end

        # Create armature and object
        self.amt = bpy.data.armatures.new(move + '.' + part + '.' + helicity + '.data')
        self.rig = bpy.data.objects.new(move + '.' + part + '.' + helicity, self.amt)

        # Joints
        self.a = [0 for i in range(4)] # Joint α
        self.b = [0 for i in range(self.J)] # Joint β
        self.y = [0 for i in range(self.J)] # Joint γ
        self.o = [0 for i in range(self.J)] # Joint δ

        # Configuration Movement
        self.configMovement(self.P, self.A, self.J, self.a, self.b, self.y, self.o)

        # Construction Movement
        self.constructMovement(self.J, self.helicity, self.amt, self.rig, self.a, self.b, self.y, self.o)

        # Construction Rotation
        self.configRotation(self.rig, self.interval, self.frame_start, self.frame_end, self.start, self.end)

        # Configuration Linkage
        self.configLink(1.25*self.A*0.8, self.J, self.helicity, self.rig, self.move, self.part)

        # Construction Linkage
        self.constructLink(1.25*self.A*0.8, self.J, self.helicity, self.rig, self.move, self.part)

    # Overriding Configuration Movement
    def configMovement(self, P, A, J, a, b, y, o):

        a[1] = mathutils.Euler((P, A, 0.0), 'XYZ')
        print ("a1 =", a[1])

        a[2] = mathutils.Euler((A, -A, 0.0), 'XYZ')
        print ("a2 =", a[2])

        b[1] = mathutils.Euler((-A, A, 0.0), 'XYZ')
        print ("b1 =", b[1])

        o[1] = mathutils.Euler((A, A, 0.0), 'XYZ')
        print ("o1 =", o[1])

        B = A * 2 * sqrt (2)
        C = B + (B * sqrt (2))
        D = C * sqrt (2)
        E = C + D

        y[1] = mathutils.Euler((-A, -A, 0.0), 'XYZ')
        print ("y1 =", y[1])
        
        b[2] = mathutils.Euler(((8.90101/0.45)*A, (-7.03036/0.45)*A, 0.0), 'XYZ')
        print ("b2 =", b[2])

        b[3] = mathutils.Euler(((7.78023/0.45)*A, (-8.39959/0.45)*A, 0.0), 'XYZ')
        print ("b3 =", b[3])

        b[4] = mathutils.Euler(((2.27024/0.45)*A, (-9.93452/0.45)*A, 0.0), 'XYZ')
        print ("b4 =", b[4])
        
        b[5] = mathutils.Euler(((0.300777/0.45)*A, (-14.8735/0.45)*A, 0.0), 'XYZ')
        print ("b5 =", b[5])

        y[2] = mathutils.Euler(((8.00326/0.45)*A, (-7.93191/0.45)*A, 0.0), 'XYZ')
        print ("y2 =", y[2])

        y[3] = mathutils.Euler(((8.04806/0.45)*A, (-8.608/0.45)*A, 0.0), 'XYZ')
        print ("y3 =", y[3])

        y[4] = mathutils.Euler(((0.581859/0.45)*A, (-12.6181/0.45)*A, 0.0), 'XYZ')
        print ("y4 =", y[4])

        y[5] = mathutils.Euler(((-0.827196/0.45)*A, (-14.6613/0.45)*A, 0.0), 'XYZ')
        print ("y5 =", y[5])

        y[6] = mathutils.Euler(((-1.57677/0.45)*A, (-15.7459/0.45)*A, 0.0), 'XYZ')
        print ("y6 =", y[6])

        o[2] = mathutils.Euler(((8.20915/0.45)*A, (-7.92449/0.45)*A, 0.0), 'XYZ')
        print ("o2 =", o[2])

        o[3] = mathutils.Euler(((8.65552/0.45)*A, (-9.66126/0.45)*A, 0.0), 'XYZ')
        print ("o3 =", o[3])
        
        o[4] = mathutils.Euler(((-0.768116/0.45)*A, (-13.3545/0.45)*A, 0.0), 'XYZ')
        print ("o4 =", o[4])
        
        o[5] = mathutils.Euler(((-0.831786/0.45)*A, (-15.0341/0.45)*A, 0.0), 'XYZ')
        print ("o5 =", o[5])
        
    def configLink(self, A, J, helicity, rig, move, part):

        bpy.ops.object.mode_set(mode='OBJECT')
    
        Q = (0.18648+0.146446)*A
    #   Z = -Q*2
        Z = 0.0

        if part == 'leg-right':
            obj_joint = bpy.data.objects["joint.gold.a2a1.leg-right"].copy()
        else:
            obj_joint = bpy.data.objects["joint.gold.a2a1.leg-left"].copy()
        
        obj_joint.location = (0.0, 0.0, -Q*3+Z)
        obj_joint.scale = (A, A, A)
        obj_joint.name = "a2a1.mesh." + move + '.' + part +'.' + helicity
        bpy.data.collections['link'].objects.link(obj_joint)

        obj_joint = bpy.data.objects["joint.silver.001"].copy()
        obj_joint.location = (0.0, 0.0, +Q+Z)
        obj_joint.scale = (A, A, A)
        obj_joint.name = "y1a2.mesh." + move + '.' + part +'.' + helicity
        bpy.data.collections['link'].objects.link(obj_joint)

        obj_joint = bpy.data.objects["joint.copper.001"].copy()
        obj_joint.location = (0.0, 0.0, +Q*3+Z)
        obj_joint.scale = (A, A, A)
        obj_joint.name = "a2o1.mesh." + move + '.' + part +'.' + helicity
        bpy.data.collections['link'].objects.link(obj_joint)

        obj_joint = bpy.data.objects["joint.blue.001"].copy()
        obj_joint.location = (0.0, 0.0, -Q*2+Z)
        obj_joint.scale = (A, A, A)
        obj_joint.name = "a1b1.mesh." + move + '.' + part +'.' + helicity
        bpy.data.collections['link'].objects.link(obj_joint)


        for n in range(1, J - 1):

            if n <= (J-2):

                # Pattern 2 of by
                obj_joint = bpy.data.objects["joint.green.001"].copy()
                obj_joint.location = (0.0, 0.0, -Q + Q*((n+1) % 2)*4 +Z)
                obj_joint.scale = (A, A, A)
                obj_joint.name = "b"+str(n)+"y"+str(n)+".mesh." + move + '.' + part +'.' + helicity
                bpy.data.collections['link'].objects.link(obj_joint)

                # Pattern 2 of yy
                obj_joint = bpy.data.objects["joint.gold.00"+str(1 + (n+1) % 2)].copy()
                obj_joint.location = (0.0, 0.0, +Q*(1 - (n % 2))*2+Z)
                obj_joint.scale = (A, A, A)
                obj_joint.name = "y"+str(n)+"y"+str(n+1)+".mesh." + move + '.' + part +'.' + helicity
                bpy.data.collections['link'].objects.link(obj_joint)


            if n <= (J-3):

                # Pattern 1 of ob
                obj_joint = bpy.data.objects["joint.blue.001"].copy()
                obj_joint.location = (0.0, 0.0, -Q*2 + Q*(n % 2)*6 +Z)
                obj_joint.scale = (A, A, A)
                obj_joint.name = "o"+str(n)+"b"+str(n+1)+".mesh." + move + '.' + part +'.' + helicity
                bpy.data.collections['link'].objects.link(obj_joint)

                # Pattern 2 of yo
                obj_joint = bpy.data.objects["joint.copper.001"].copy()
                obj_joint.location = (0.0, 0.0, -Q + Q*((n+1) % 2)*4 +Z)
                obj_joint.scale = (A, A, A)
                obj_joint.name = "y"+str(n+1)+"o"+str(n+1)+".mesh." + move + '.' + part +'.' + helicity
                bpy.data.collections['link'].objects.link(obj_joint)


        for ob in data.collections['link'].objects:
            if "mesh" in ob.name:
                ob.select_set(state = True, view_layer = None)

        bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True, material=True, animation=True)
        bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')


def formula():

# pivot factor
    P = 0

# scale factor
    A = 1
    
# joint number
    J = 6
    
# name
    move = 'formula'

# element
    part = 'universe'

# left or right
    helicity = 'left'

    start = 0
    end = start+360

    formula = Formula(P, A, J, move, part, helicity, start, end)


def legs():

# scale factor
    A = 0.45

# pivot factor
    P = (0.26/0.45)*A
    
# name
    move = 'running'

# element
    part = 'leg-left'

# left or right
    helicity = 'right'

    start = 90
    end = start+720

    global leg_right
    leg_right = Leg(P, A, move, part, helicity, start, end)

    leg_loc = ((-1.22621/0.45)*A, (11.0924/0.45)*A, (-1.05034/0.45)*A)
    leg_rot = mathutils.Euler((math.radians(0.0), math.radians(-180), math.radians(-8.0)), 'XYZ')

    # position
    leg_right.rig.location.x += leg_loc[0]
    leg_right.rig.location.y += leg_loc[1]
    leg_right.rig.location.z += leg_loc[2]

    leg_right.rig.rotation_euler = leg_rot

# element
    part = 'leg-right'

# left or right
    helicity = 'left'
    
    start = 90
    end = start-720

    global leg_left
    leg_left = Leg(P, A, move, part, helicity, start, end)

    leg_loc = ((-1.22621/0.45)*A, (11.0976/0.45)*A, (3.51433/0.45)*A)
    leg_rot = mathutils.Euler((math.radians(0.0), math.radians(-180), math.radians(-8.0)), 'XYZ')

    # position 
    leg_left.rig.location.x += leg_loc[0]
    leg_left.rig.location.y += leg_loc[1]
    leg_left.rig.location.z += leg_loc[2]

    leg_left.rig.rotation_euler = leg_rot
    

def main(origin):
    
    # create new collection
    newCol = bpy.data.collections.new('movement')
    # link the newCol to the scene
    bpy.context.scene.collection.children.link(newCol)

    newCol = bpy.data.collections.new('link')
    bpy.context.scene.collection.children.link(newCol)

    global interval
    global frame_start
    global frame_end

    frame_start = 0
    frame_end = 240

    interval = frame_end - frame_start

#    formula()
    legs()

if __name__ == "__main__":
    # renaming of corrada objects
#    for ob in context.collection.objects:
#        if "joint_" in ob.name:
#            ob.name = ob.name.replace("_", ".")
            
    main((0.0, 0.0, 0.0)) 
