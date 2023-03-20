from PySide6.QtGui import QColor
from editor.common import native
from editor.common.util import getIde
from editor.widgets.misc.menu_style import MenuStyle

native.setDarkAppearance()
# native.setLightAppearance()


menuConfLight = {
	# 'border'              :    QColor('#aaa'),
	'borderWidth'           :    0,
	'borderRadius'          :    6,

	'background'            :    QColor('#e8e8e8'),
	'backgroundHovered'     :    QColor('#498afd'),
	
	'text'                  :    QColor('#222'),
	'textHovered'           :    QColor('#fff'),
	'shortcut'              :    QColor('#aaa'),
	'separator'             :    QColor('#bbb'),

	'contentPadding'        :    15,
	'checkedPadding'        :    10,
	'subMenuOverlap'        :    5,

	'separatorHeight'       :    1,
	'separatorVSpacing'     :    4,

	'itemHeight'            :    22,
	'itemBackgroundPadding' :    5,
	'itemBackgroundRadius'  :    4,

	'fontSize'              :    12,
	'shortcutLetterSpacing' :    2,

	'submenuIcon'           :    'submenu.png',
	'submenuIconHovered'    :    'submenu2.png',
	'submenuIconSize'       :    12,
	'submenuIconOffsetX'    :    2,
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
	'borderRadius'          :    6,

	'background'            :    QColor('#383736'),
	'backgroundHovered'     :    QColor('#47f'),
	
	'text'                  :    QColor('#fff'),
	'textHovered'           :    QColor('#fff'),
	'shortcut'              :    QColor('#aaa'),
	'separator'             :    QColor('#6b6b6b'),

	'contentPadding'        :    15,
	'checkedPadding'        :    10,
	'subMenuOverlap'        :    5,

	'separatorHeight'       :    1,
	'separatorVSpacing'     :    4,

	'itemHeight'            :    22,
	'itemBackgroundPadding' :    5,
	'itemBackgroundRadius'  :    4,

	'fontSize'              :    12,
	'shortcutLetterSpacing' :    2,

	'submenuIcon'           :    'submenu2.png',
	'submenuIconHovered'    :    'submenu2.png',
	'submenuIconSize'       :    12,
	'submenuIconOffsetX'    :    2,
	'submenuIconOffsetY'    :    1,

	'checkedIcon'           :    'check2.png',
	'checkedIconHovered'    :    'check2.png',
	'checkedIconSize'       :    12,
	'checkedIconOffsetX'    :    -1,
	'checkedIconOffsetY'    :    1,

	'menuScrollerIcon'      :    'submenu2.png',
}

menuStyle = MenuStyle(menuConfDark)
# menuStyle = MenuStyle(menuConfLight)
getIde().setStyle(menuStyle)

