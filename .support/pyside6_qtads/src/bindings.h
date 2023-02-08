#define QT_ANNOTATE_ACCESS_SPECIFIER(a) __attribute__((annotate(#a)))

#include "ads_globals.h"
#include "AutoHideDockContainer.h"
#include "AutoHideSideBar.h"
#include "AutoHideTab.h"
#include "DockAreaTabBar.h"
#include "DockAreaTitleBar.h"
#include "DockAreaTitleBar_p.h"
#include "DockAreaWidget.h"
#include "DockComponentsFactory.h"
#include "DockContainerWidget.h"
#include "DockFocusController.h"
#include "DockManager.h"
#include "DockOverlay.h"
#include "DockSplitter.h"
#include "DockWidget.h"
#include "DockWidgetTab.h"
#include "ElidingLabel.h"
#include "FloatingDockContainer.h"
#include "FloatingDragPreview.h"
#include "IconProvider.h"
#include "PushButton.h"
#include "ResizeHandle.h"

#ifdef Q_OS_LINUX
#include "linux/FloatingWidgetTitleBar.h"
#endif