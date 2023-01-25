cmake_minimum_required(VERSION 3.5)
# cmake_policy(VERSION 3.5)

project(Shiboken-QtAds)

# find_package(Qt6 REQUIRED Core)
# find_package(Qt6 REQUIRED Gui)
# find_package(Qt6 REQUIRED Widgets)
find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)
if (UNIX AND NOT APPLE)
    include_directories(${Qt${QT_VERSION_MAJOR}Gui_PRIVATE_INCLUDE_DIRS})
endif()

set(CMAKE_CXX_STANDARD 14)
set(qtads_library "libqtadsbinding")
set(shiboken_library "ShibokenQtAds")
set(wrapped_header ${CMAKE_SOURCE_DIR}/bindings.h)
set(typesystem_file ${CMAKE_SOURCE_DIR}/bindings.xml)
set(generated_sources
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CAutoHideDockContainer_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CAutoHideSideBar_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CAutoHideTab_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CDockAreaTabBar_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CDockAreaTitleBar_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CTitleBarButton_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CSpacerWidget_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CDockAreaWidget_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CDockComponentsFactory_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CDockContainerWidget_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CDockFocusController_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CDockManager_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CDockOverlay_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CDockOverlayCross_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CDockSplitter_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CDockWidget_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CDockWidgetTab_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CElidingLabel_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CFloatingDockContainer_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_IFloatingWidget_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CFloatingDragPreview_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CIconProvider_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CPushButton_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/ads_CResizeHandle_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/shibokenqtads_module_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${qtads_library}_autogen/mocs_compilation_${CMAKE_BUILD_TYPE}.cpp)

if (UNIX AND NOT APPLE)
    set(generated_sources
        %{generated_sources}
        ${CMAKE_CURRENT_BINARY_DIR}/${shiboken_library}/linux/ads_CFloatingWidgetTitleBar_wrapper.cpp)
endif()


find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

if(NOT python_interpreter)
    find_program(python_interpreter "python")
endif()

macro(pyside_config option output_var)
    if(${ARGC} GREATER 2)
        set(is_list ${ARGV2})
    else()
        set(is_list "")
    endif()

    execute_process(
      COMMAND ${python_interpreter} "${CMAKE_SOURCE_DIR}/../pyside_config.py"
		${option}
      OUTPUT_VARIABLE ${output_var}
      OUTPUT_STRIP_TRAILING_WHITESPACE)

    if ("${${output_var}}" STREQUAL "")
        message(FATAL_ERROR "Error: Calling pyside_config.py ${option} returned no output.")
    endif()
    if(is_list)
        string (REPLACE " " ";" ${output_var} "${${output_var}}")
    endif()
endmacro()

pyside_config(--shiboken-module-path shiboken_module_path)
pyside_config(--shiboken-generator-path shiboken_generator_path)
pyside_config(--pyside-path pyside_path)
pyside_config(--python-include-path python_include_dir)
pyside_config(--shiboken-generator-include-path shiboken_include_dir 1)
pyside_config(--shiboken-module-shared-libraries-cmake shiboken_shared_libraries 0)
pyside_config(--pyside-shared-libraries-cmake pyside6_link 0)

set(shiboken_path "${shiboken_generator_path}/shiboken6${CMAKE_EXECUTABLE_SUFFIX}")
if(NOT EXISTS ${shiboken_path})
    message(FATAL_ERROR "Shiboken executable not found at path: ${shiboken_path}")
endif()

set(CMAKE_SKIP_BUILD_RPATH FALSE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH ${shiboken_module_path} ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)


set(ads_src_dir ${CMAKE_SOURCE_DIR}/src)
set(ads_SRCS
    ${ads_src_dir}/ads_globals.cpp
    ${ads_src_dir}/DockAreaTabBar.cpp
    ${ads_src_dir}/DockAreaTitleBar.cpp
    ${ads_src_dir}/DockAreaWidget.cpp
    ${ads_src_dir}/DockContainerWidget.cpp
    ${ads_src_dir}/DockManager.cpp
    ${ads_src_dir}/DockOverlay.cpp
    ${ads_src_dir}/DockSplitter.cpp
    ${ads_src_dir}/DockWidget.cpp
    ${ads_src_dir}/DockWidgetTab.cpp
    ${ads_src_dir}/DockingStateReader.cpp
    ${ads_src_dir}/DockFocusController.cpp
    ${ads_src_dir}/ElidingLabel.cpp
    ${ads_src_dir}/FloatingDockContainer.cpp
    ${ads_src_dir}/FloatingDragPreview.cpp
    ${ads_src_dir}/IconProvider.cpp
    ${ads_src_dir}/DockComponentsFactory.cpp
    ${ads_src_dir}/AutoHideSideBar.cpp
    ${ads_src_dir}/AutoHideTab.cpp
    ${ads_src_dir}/AutoHideDockContainer.cpp
    ${ads_src_dir}/PushButton.cpp
    ${ads_src_dir}/ResizeHandle.cpp
    ${ads_src_dir}/ads.qrc
)
set(ads_HEADERS
    ${ads_src_dir}/ads_globals.h
    ${ads_src_dir}/DockAreaTabBar.h
    ${ads_src_dir}/DockAreaTitleBar.h
    ${ads_src_dir}/DockAreaTitleBar_p.h
    ${ads_src_dir}/DockAreaWidget.h
    ${ads_src_dir}/DockContainerWidget.h
    ${ads_src_dir}/DockManager.h
    ${ads_src_dir}/DockOverlay.h
    ${ads_src_dir}/DockSplitter.h
    ${ads_src_dir}/DockWidget.h
    ${ads_src_dir}/DockWidgetTab.h
    ${ads_src_dir}/DockingStateReader.h
    ${ads_src_dir}/DockFocusController.h
    ${ads_src_dir}/ElidingLabel.h
    ${ads_src_dir}/FloatingDockContainer.h
    ${ads_src_dir}/FloatingDragPreview.h
    ${ads_src_dir}/IconProvider.h
    ${ads_src_dir}/DockComponentsFactory.h
    ${ads_src_dir}/AutoHideSideBar.h
    ${ads_src_dir}/AutoHideTab.h
    ${ads_src_dir}/AutoHideDockContainer.h
    ${ads_src_dir}/PushButton.h
    ${ads_src_dir}/ResizeHandle.h
)
if (UNIX AND NOT APPLE)
    set(ads_SRCS ${ads_src_dir}/linux/FloatingWidgetTitleBar.cpp ${ads_SRCS})
    set(ads_HEADERS ${ads_src_dir}/linux/FloatingWidgetTitleBar.h ${ads_HEADERS})
endif()

if(BUILD_STATIC)
    set(CMAKE_STATIC_LIBRARY_SUFFIX "_static${CMAKE_STATIC_LIBRARY_SUFFIX}")
endif()

if(BUILD_STATIC)
    add_library(${qtads_library} STATIC ${ads_SRCS} ${ads_HEADERS})
    target_compile_definitions(${qtads_library} PUBLIC ADS_STATIC)
else()
    add_library(${qtads_library} SHARED ${ads_SRCS} ${ads_HEADERS})
    target_compile_definitions(${qtads_library} PUBLIC ADS_SHARED_EXPORT)
endif()

set_target_properties(${qtads_library} PROPERTIES
    AUTOMOC ON
    AUTORCC ON
)
target_include_directories(${qtads_library} PRIVATE ${ads_src_dir})
# set(${qtads_library}_sources qobjectwithenum.cpp demo.cpp)
# add_library(${qtads_library} SHARED ${${qtads_library}_sources})
target_link_libraries(${qtads_library} Qt6::Core Qt6::Gui Qt6::Widgets)
set_property(TARGET ${qtads_library} PROPERTY PREFIX "")

get_target_property(qtcore_lib_includes Qt6::Core INTERFACE_INCLUDE_DIRECTORIES)
get_target_property(qtgui_lib_includes Qt6::Gui INTERFACE_INCLUDE_DIRECTORIES)
get_target_property(qtwidget_lib_includes Qt6::Widgets INTERFACE_INCLUDE_DIRECTORIES)
list(JOIN qtcore_lib_includes ";-I" qtcore_lib_includes)
list(JOIN qtgui_lib_includes ";-I" qtgui_lib_includes)
list(JOIN qtwidget_lib_includes ";-I" qtwidget_lib_includes)

target_compile_definitions(${qtads_library} PRIVATE BINDINGS_BUILD)
target_compile_definitions(${qtads_library} PRIVATE CUSTOM_CAST)

set(shiboken_options --generator-set=shiboken --enable-parent-ctor-heuristic
    --enable-return-value-heuristic --use-isnull-as-nb_nonzero
    --avoid-protected-hack
    --enable-pyside-extensions
    -I${qtcore_lib_includes}
    -I${qtgui_lib_includes}
    -I${qtwidget_lib_includes}
    -I${ads_src_dir}
    -I${CMAKE_SOURCE_DIR}
    -T${CMAKE_SOURCE_DIR}
    -T${pyside_path}/typesystems/
    --output-directory=${CMAKE_CURRENT_BINARY_DIR}
    )

set(generated_sources_dependencies ${wrapped_header} ${typesystem_file})

add_custom_command(OUTPUT ${generated_sources}
                    COMMAND ${shiboken_path}
                    ${shiboken_options} ${wrapped_header} ${typesystem_file}
                    DEPENDS ${generated_sources_dependencies}
                    IMPLICIT_DEPENDS CXX ${wrapped_header}
                    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
                    COMMENT "Running generator for ${typesystem_file}.")


set(${shiboken_library}_sources ${generated_sources})
link_directories(${Python3_LIBRARY_DIRS})

add_library(${shiboken_library} MODULE ${${shiboken_library}_sources})

target_include_directories(${shiboken_library} PRIVATE ${python_include_dir})
target_include_directories(${shiboken_library} PRIVATE ${pyside_path}/include/)
target_include_directories(${shiboken_library} PRIVATE ${pyside_path}/include/QtCore)
target_include_directories(${shiboken_library} PRIVATE ${pyside_path}/include/QtGui)
target_include_directories(${shiboken_library} PRIVATE ${pyside_path}/include/QtWidgets)
target_include_directories(${shiboken_library} PRIVATE ${shiboken_include_dir})
target_include_directories(${shiboken_library} PRIVATE ${CMAKE_SOURCE_DIR})
target_include_directories(${shiboken_library} PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/${qtads_library}_autogen/include_${CMAKE_BUILD_TYPE})
target_include_directories(${shiboken_library} PRIVATE ${ads_src_dir})

target_link_libraries(${shiboken_library} PRIVATE ${shiboken_shared_libraries})
target_link_libraries(${shiboken_library} PRIVATE ${qtads_library})
target_link_libraries(${shiboken_library} PRIVATE ${pyside6_link})

set_property(TARGET ${shiboken_library} PROPERTY PREFIX "")
set_property(TARGET ${shiboken_library} PROPERTY OUTPUT_NAME
             "${shiboken_library}${PYTHON_EXTENSION_SUFFIX}")
if(WIN32)
    set_property(TARGET ${shiboken_library} PROPERTY SUFFIX ".pyd")
endif()

set(install_dest_dir ${CMAKE_CURRENT_SOURCE_DIR}/dist)
install(TARGETS ${shiboken_library} ${qtads_library}
        LIBRARY DESTINATION ${install_dest_dir}
        RUNTIME DESTINATION ${install_dest_dir}
        )
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/__init__.py
        DESTINATION ${install_dest_dir}
        )
