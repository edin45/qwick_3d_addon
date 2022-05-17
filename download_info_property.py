import bpy

class DonwloadInfoPropertyGroup(bpy.types.PropertyGroup):
    res : bpy.props.EnumProperty(
        name = "res",
        description = "abc",
        items=[
            ('1k','1K','1k'),
            ('2k','2K','2k'),
            ('4k','4K','4k'),
        ],
        default='4k'
    )