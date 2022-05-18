import bpy

class DonwloadInfoPropertyGroup(bpy.types.PropertyGroup):
    res : bpy.props.EnumProperty(
        name = "Resolution",
        description = "",
        items=[
            ('1k','1K','1k'),
            ('2k','2K','2k'),
            ('4k','4K','4k'),
        ],
        default='4k'
    )

    model_search : bpy.props.StringProperty(name = "Search (Press enter to search)",default="",options={'TEXTEDIT_UPDATE'})

    update_ui : bpy.props.BoolProperty(name='update_ui',description='',default=True)

    start: bpy.props.IntProperty(name="start_pagination",description='',default=0)
    
    end: bpy.props.IntProperty(name="end_pagination",description='',default=10)

    page_step_size: bpy.props.IntProperty(name="page_step_size",description='',default=10)