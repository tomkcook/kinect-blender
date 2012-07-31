import bpy


class KinectCapturePanel(bpy.types.Panel):
    bl_label = "Kinect Capture"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Kinect Capture", icon='WORLD_DATA')

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.prop(obj, "name")


class KinectCaptureOperator(bpy.types.Operator):
    '''Capture skeleton animation from Kinect sensor.'''
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Kinect Capture"

    _timer = None
    
    tracking = False

    def modal(self, context, event):
        if event.type == 'ESC':
            return self.cancel(context)

        if event.type == 'TIMER':
            if self.Tracking:
                # change theme color, silly!
                right_humerus_ori = self.skel_cap.get_joint_orientation(self.track_id, SKEL_RIGHT_SHOULDER).matrix
                right_humerus_bone = bpy.context.object.pose.bones["Humerus.R"]

        return {'PASS_THROUGH'}

    def execute(self, context):
        # Set up OpenNI
        self.ctx = openni.Context()
        self.ctx.init()
        self.user = openni.UserGenerator()
        self.user.create(self.ctx)
        self.skel_cap = self.user.skeleton_cap
        
        self.user.register_user_cb(self.new_user, self.lost_user)
#        self.skel_cap.register_pose_detected_cb(self.pose_detected)
        self.skel_cap.register_c_start_cb(self.calibration_start)
        self.skel_cap.register_c_complete_cb(self.calibration_complete)

        self.skel_cap.set_profile(openni.SKEL_PROFILE_ALL)
        self.ctx.start_generating_all()
        bpy.ops.object.mode_set(mode='POSE')
        
        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(0.1, context.window)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        self.tracking = False
        context.window_manager.event_timer_remove(self._timer)
        return {'CANCELLED'}
    
    def new_user(self, src, id):
        self.skel_cap.request_calibration(id, True)
        
    def calibration_start(self, src, id):
        print('Calibrating user')
        
    def calibration_complete(self,src,id,status):
        if status == CALIBRATION_STATUS_OK:
            self.skel_cap.start_tracking(id)
            self.track_id = id
            self.tracking = True
            
    def lost_user(self,src,id):
        self.cancel(bpy.context)
    
def register():
    bpy.utils.register_class(KinectCapturePanel)
    bpy.utils.register_class(KinectCaptureOperator)


def unregister():
    bpy.utils.unregister_class(KinectCapturePanel)
    bpy.utils.unregister_class(KinectCaptureOperator)


if __name__ == "__main__":
    register()
