import platform
__sys__ = platform.system()

from PySide6.QtGui import QColor
from editor.common import native
from editor.common.util import getIde
from editor.widgets.misc.menu_style import MenuStyleMacOS, MenuStyleWindows

native.setDarkAppearance()
# native.setLightAppearance()


menuConfLight = {
	# 'border'              :    QColor('#aaa'),
	'borderWidth'           :    0,
	'borderRadius'          :    7,

	'background'            :    QColor('#e8e8e8'),
	'backgroundHovered'     :    QColor('#498afd'),
	
	'text'                  :    QColor('#222'),
	'textHovered'           :    QColor('#fff'),
	'shortcut'              :    QColor('#aaa'),
	'separator'             :    QColor('#bbb'),

	'fontSize'              :    13,
	'contentPadding'        :    15,
	'checkedPadding'        :    10,
	'subMenuOverlap'        :    5,

	'separatorHeight'       :    1,
	'separatorVSpacing'     :    4,

	'itemHeight'            :    22,
	'itemBackgroundPadding' :    5,
	'itemBackgroundRadius'  :    4,

	'submenuIcon'           :    'submenu.png',
	'submenuIconHovered'    :    'submenu2.png',
	'submenuIconSize'       :    12,
	'submenuIconOffsetX'    :    1,
	'submenuIconOffsetY'    :    1,

	'checkedIcon'           :    'check.png',
	'checkedIconHovered'    :    'check2.png',
	'checkedIconSize'       :    12,
	'checkedIconOffsetX'    :    -1,
	'checkedIconOffsetY'    :    1,
	
	'menuScrollerIcon'      :    'submenu2.png',
}

menuConfDark = {
	'border'                :    QColor('#6b6b6b'),
	'borderWidth'           :    1,
	'borderRadius'          :    7,

	'background'            :    QColor('#383736'),
	'backgroundHovered'     :    QColor('#47f'),
	
	'text'                  :    QColor('#eee'),
	'textHovered'           :    QColor('#eee'),
	'shortcut'              :    QColor('#aaa'),
	'separator'             :    QColor('#6b6b6b'),

	'fontSize'              :    13,
	'contentPadding'        :    15,
	'checkedPadding'        :    10,
	'subMenuOverlap'        :    5,

	'separatorHeight'       :    1,
	'separatorVSpacing'     :    4,

	'itemHeight'            :    22,
	'itemBackgroundPadding' :    5,
	'itemBackgroundRadius'  :    4,

	'submenuIcon'           :    'submenu2.png',
	'submenuIconHovered'    :    'submenu2.png',
	'submenuIconSize'       :    12,
	'submenuIconOffsetX'    :    1,
	'submenuIconOffsetY'    :    1,

	'checkedIcon'           :    'check2.png',
	'checkedIconHovered'    :    'check2.png',
	'checkedIconSize'       :    12,
	'checkedIconOffsetX'    :    -1,
	'checkedIconOffsetY'    :    1,

	'menuScrollerIcon'      :    'submenu2.png',
}

if __sys__ == 'Darwin':
	menuStyle = MenuStyleMacOS(menuConfDark)
	# menuStyle = MenuStyle(menuConfLight)
	getIde().setStyle(menuStyle)

elif __sys__ == 'Windows':
	menuStyle = MenuStyleWindows()
	getIde().setStyle(menuStyle)

