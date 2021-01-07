from dearpygui.core import *
from dearpygui.simple import *
import webbrowser

from bar_element_1D_solver import *



def solve_button():
    clear_table("Displacements table")
    clear_table("Element stress table")
    clear_table("Element strain table")

    if get_value("Element type") == 0:
        Q, F, Stress, Strain = solve(get_value("Element type"), get_value("Number of elements"), get_value("A0"), get_value("E0"), get_value("L0"), get_value("Type0_Q"), get_value("Type0_F"))

    else:
        Q, F, Stress, Strain = solve(get_value("Element type"), get_value("Number of elements"), get_value("A1"), get_value("E1"), get_value("L1"), get_value("Type1_Q"), get_value("Type1_F"))

    Q = np.round(Q, 4)
    F = np.round(F, 4)
    Stress = np.round(Stress, 4)
    Strain = np.round(Strain, 4)

    nodes = list(range(1, get_value("Number of elements")+2))
    elements = nodes[0:-1]

    for i in nodes:
        add_row("Displacements table", [str(i), str(Q[i-1])])

    for i in nodes[0:-1]:
        add_row("Element stress table", [str(i), str(Stress[i - 1])])
        add_row("Element strain table", [str(i), str(Strain[i - 1])])


def run_data_checks(sender, data):
    close_popup("Confirmation Popup")

    clear_log(logger="log_window")

    log_info("<---Solver initiated--->", logger="log_window")
    log_info("Running data checks...", logger="log_window")

    if get_value("Number of elements") < 1:
        log_error("Number of elements cannot be less than 1.", logger="log_window")

        return 0

    else:
        log_info("Number of elements: OK", logger="log_window")

        if get_value("Element type") == 0:

            if get_value("A0") <= 0 or get_value("E0") <=0 or get_value("L0") <= 0:
                log_error("The area, young's modulus, length, or force", logger="log_window")
                log_error("cannot be less than or equal to 0.", logger="log_window")
                log_error("Please try again.", logger="log_window")

                return 0

            else:
                log_info("Area, young's modulus, length, and force: OK", logger="log_window")

                if get_value("Type0_Q") < 0.0:
                    log_error("The displacement cannot be less than 0.", logger="log_window")
                    log_error("Please try again.", logger="log_window")

                    return 0

                else:
                    log_info("Displacement: OK", logger="log_window")
                    log_info("Solving...", logger="log_window")
                    solve_button()
                    log_info("Solution has been calculated!", logger="log_window")
                    log_info("<---Solver terminated--->", logger="log_window")


        else:
            A = np.array(get_value("A1").split(","))
            E = np.array(get_value("E1").split(","))
            L = np.array(get_value("L1").split(","))
            Q = np.array(get_value("Type1_Q").split(","))
            F = np.array(get_value("Type1_F").split(","))

            try:
                A = A.astype(float)
                E = E.astype(float)
                L = L.astype(float)

                if (A > 0).all() and (E > 0).all() and (L > 0).all():
                    log_info("Area, modulus, and length: OK", logger="log_window")

                    if 'x' in Q:
                        solve_button()
                        log_info("Displacement and force: OK", logger="log_window")
                        log_info("Solution has been calculated!", logger="log_window")
                        log_info("<---Solver terminated--->", logger="log_window")


                else:
                    log_error("Please enter valid values", logger="log_window")
                    log_error("for area, modulus, and length", logger="log_window")
                    log_error("and try again.", logger="log_window")
                    return 0

            except:
                log_error("Please enter valid values and try again.", logger="log_window")
                return 0



def close_error_popup(sender, data):
    close_popup("Error popup")
    close_popup("Confirmation Popup")


def close_confirmation(sender, data):
    close_popup("Confirmation Popup")


def open_github(sender, data):
    webbrowser.open("https://github.com/RahulShagri/1D-bar-element-FEM-Solver")


def switch_solver(sender, data):
    if (get_value("Element type") == 1):
        if (does_item_exist("Type1_matprop")):
            return 0

        else:
            delete_item("Type0_matprop")
            delete_item("Type0_disp")
            delete_item("Type0_force")

            with window( "Type1_matprop", label="3. Material Properties of each element", x_pos=10, y_pos=170, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=450, height=105):
                add_input_text("A1", label="Cross-sectional area", tip="Enter the area of cross section of each element without spaces.\nEx: 100,150,450")
                add_input_text("E1", label="Young's modulus", tip="Enter the young's modulus of each element without spaces.\nEx: 100,150,450")
                add_input_text("L1", label="Length", tip="Enter length of each element without spaces.\nEx: 100,150,450")

            with window("Type1_disp", label="4. Known and unknown nodal displacements", x_pos=10, y_pos=285, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=450, height=60):
                add_input_text("Type1_Q", label="Displacements", tip="Enter all known nodal displacements at each node and\nenter x for unknown displacements. Ex: 0,x,x,0.03\nNote: first nodal dispalcement will always be 0.")

            with window("Type1_force", label="5. Known and unknown nodal forces", x_pos=10, y_pos=355, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=450, height=60):
                add_input_text("Type1_F", label="Forces", tip="Enter all known forces at each node and\nenter 0 for unknown forces. Ex: 0,-300,0,5000")

    else:
        if (does_item_exist("Type0_matprop")):
            return 0

        else:
            delete_item("Type1_matprop")
            delete_item("Type1_disp")
            delete_item("Type1_force")

            with window("Type0_matprop", label="3. Material Properties of the bar", x_pos=10, y_pos=170, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=450, height=105):
                add_input_float("A0", label="Cross-sectional area")
                add_input_float("E0", label="Young's modulus")
                add_input_float("L0", label="Length")

            with window( "Type0_disp", label="4. Free end displacement (if known)", x_pos=10, y_pos=285, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=450, height=60):
                add_input_float("Type0_Q", label="Displacement", tip="Enter 0 if free end displacement is unknown.")

            with window("Type0_force", label="5. Free end force", x_pos=10, y_pos=355, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=450, height=60):
                add_input_float("Type0_F", label="Force", tip="Enter the tension or compression force acting on the free\nend of the bar (+ve for tension and -ve for compression).")

with window("Main"):
    set_theme_item(mvGuiCol_Text, 0, 0, 0, 255)
    set_theme_item(mvGuiCol_TextDisabled, 128, 128, 128, 255)
    set_theme_item(mvGuiCol_WindowBg, 255, 255, 255, 240)
    set_theme_item(mvGuiCol_ChildBg, 255, 255, 255, 0)
    set_theme_item(mvGuiCol_PopupBg, 196, 196, 196, 240)
    set_theme_item(mvGuiCol_Border, 0, 0, 0, 128)
    set_theme_item(mvGuiCol_BorderShadow, 0, 0, 0, 0)
    set_theme_item(mvGuiCol_FrameBg, 0, 0, 0, 76)
    set_theme_item(mvGuiCol_FrameBgHovered, 102, 102, 102, 102)
    set_theme_item(mvGuiCol_FrameBgActive, 46, 46, 46, 171)
    set_theme_item(mvGuiCol_TitleBg, 220, 220, 220, 255)
    set_theme_item(mvGuiCol_TitleBgActive, 215, 215, 215, 255)
    set_theme_item(mvGuiCol_TitleBgCollapsed, 222, 222, 222, 130)
    set_theme_item(mvGuiCol_MenuBarBg, 184, 184, 184, 255)
    set_theme_item(mvGuiCol_ScrollbarBg, 207, 207, 207, 154)
    set_theme_item(mvGuiCol_ScrollbarGrab, 109, 109, 109, 255)
    set_theme_item(mvGuiCol_ScrollbarGrabHovered, 76, 76, 76, 255)
    set_theme_item(mvGuiCol_ScrollbarGrabActive, 86, 86, 86, 255)
    set_theme_item(mvGuiCol_CheckMark, 89, 89, 89, 255)
    set_theme_item(mvGuiCol_SliderGrab, 68, 68, 68, 255)
    set_theme_item(mvGuiCol_SliderGrabActive, 74, 74, 74, 255)
    set_theme_item(mvGuiCol_Button, 0, 0, 0, 68)
    set_theme_item(mvGuiCol_ButtonHovered, 117, 120, 122, 255)
    set_theme_item(mvGuiCol_ButtonActive, 107, 107, 107, 255)
    set_theme_item(mvGuiCol_Header, 49, 49, 49, 79)
    set_theme_item(mvGuiCol_HeaderHovered, 179, 179, 179, 204)
    set_theme_item(mvGuiCol_HeaderActive, 122, 128, 133, 255)
    set_theme_item(mvGuiCol_Separator, 110, 110, 128, 128)
    set_theme_item(mvGuiCol_SeparatorHovered, 184, 184, 184, 199)
    set_theme_item(mvGuiCol_SeparatorActive, 130, 130, 130, 255)
    set_theme_item(mvGuiCol_ResizeGrip, 232, 232, 232, 64)
    set_theme_item(mvGuiCol_ResizeGripHovered, 207, 207, 207, 171)
    set_theme_item(mvGuiCol_ResizeGripActive, 117, 117, 117, 242)
    set_theme_item(mvGuiCol_Tab, 214, 214, 214, 255)
    set_theme_item(mvGuiCol_TabHovered, 177, 177, 177, 255)
    set_theme_item(mvGuiCol_TabActive, 92, 92, 92, 255)
    set_theme_item(mvGuiCol_TabUnfocused, 18, 26, 38, 247)
    set_theme_item(mvGuiCol_TabUnfocusedActive, 36, 66, 107, 255)
    set_theme_item(mvGuiCol_DockingPreview, 66, 150, 250, 179)
    set_theme_item(mvGuiCol_DockingEmptyBg, 51, 51, 51, 255)
    set_theme_item(mvGuiCol_PlotLines, 156, 156, 156, 255)
    set_theme_item(mvGuiCol_PlotLinesHovered, 255, 110, 89, 255)
    set_theme_item(mvGuiCol_PlotHistogram, 186, 153, 38, 255)
    set_theme_item(mvGuiCol_PlotHistogramHovered, 255, 153, 0, 255)
    set_theme_item(mvGuiCol_TextSelectedBg, 222, 222, 222, 89)
    set_theme_item(mvGuiCol_DragDropTarget, 255, 255, 0, 230)
    set_theme_item(mvGuiCol_NavHighlight, 153, 153, 153, 255)
    set_theme_item(mvGuiCol_NavWindowingHighlight, 255, 255, 255, 179)
    set_theme_item(mvGuiCol_NavWindowingDimBg, 204, 204, 204, 51)
    set_theme_item(mvGuiCol_ModalWindowDimBg, 204, 204, 204, 89)

    set_main_window_size(width=840, height=740)
    set_main_window_resizable(False)
    set_main_window_pos(x=0, y=0)
    set_style_window_padding(5.00, 5.00)
    set_style_frame_padding(4.00, 2.00)
    set_style_item_spacing(10.00, 3.00)
    set_style_item_inner_spacing(4.00, 4.00)
    set_style_touch_extra_padding(0.00, 0.00)
    set_style_indent_spacing(12.00)
    set_style_scrollbar_size(10.00)
    set_style_grab_min_size(10.00)
    set_style_window_border_size(1.00)
    set_style_child_border_size(1.00)
    set_style_popup_border_size(0.00)
    set_style_frame_border_size(0.00)
    set_style_tab_border_size(0.00)
    set_style_window_rounding(12.00)
    set_style_child_rounding(12.00)
    set_style_frame_rounding(4.00)
    set_style_popup_rounding(12.00)
    set_style_scrollbar_rounding(12.00)
    set_style_grab_rounding(12.00)
    set_style_tab_rounding(4.00)
    set_style_window_title_align(0.51, 0.50)
    set_style_window_menu_button_position(mvDir_Right)
    set_style_color_button_position(mvDir_Right)
    set_style_button_text_align(0.50, 0.50)
    set_style_selectable_text_align(0.00, 0.00)
    set_style_display_safe_area_padding(4.00, 4.00)
    set_style_global_alpha(1.00)
    set_style_antialiased_lines(True)
    set_style_antialiased_fill(True)
    set_style_curve_tessellation_tolerance(1.25)
    set_style_circle_segment_max_error(1.60)
    set_main_window_title("1D Bar Element FEM Sovler")

with window("1. Initial Setup", x_pos=10, y_pos=10, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=450, height=80):
    add_spacing()
    add_radio_button("Element type", items= ["One uniform bar divided into multiple elements", "Each element has different material properties"])
    set_item_callback("Element type", callback=switch_solver)

with window("2. Discretization", x_pos=10, y_pos=100, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=450, height=60):
    add_spacing()
    add_input_int("Number of elements", default_value=1)

with window("Type0_matprop", label="3. Material properties of the bar", x_pos=10, y_pos=170, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=450, height=105):
    add_spacing()
    add_input_float("A0", label="Cross-sectional area")
    add_input_float("E0", label="Young's modulus")
    add_input_float("L0", label="Length")

with window("Type0_disp", label="4. Free end displacement (if known)", x_pos=10, y_pos=285, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=450, height=60):
    add_input_float("Type0_Q", label="Displacement", tip="Enter 0 if free end displacement is unknown.")

with window("Type0_force", label="5. Free end force", x_pos=10, y_pos=355, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=450, height=60):
    add_input_float("Type0_F", label="Force", tip="Enter the tension or compression force acting on the free\nend of the bar (+ve for tension and -ve for compression).")

with window("Solve", x_pos=10, y_pos=425, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=450, height=46, no_title_bar=True):
    add_button("Solve!", width=432, height=30)
    add_popup("Solve!", 'Confirmation Popup', modal=True, mousebutton=mvMouseButton_Left)
    add_text("Are you sure you want to solve?")
    add_button("Yes", width=150, callback=run_data_checks)
    add_same_line(spacing=10)
    add_button("No", width=150, callback=close_confirmation)

with window("Logger", x_pos=10, y_pos=481, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=450, height=210):
    add_logger("log_window", log_level=0)
    log("Welcome to the 1D bar element FEM Solver!", logger="log_window")

with window("Results", x_pos=470, y_pos=10, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=300, height=681):
    add_table("Displacements table", ["Node number", "Displacements"], width=285, height=212)
    add_table("Element stress table", ["Element number", "Stress"], width=285, height=212)
    add_table("Element strain table", ["Element number", "Strain"], width=285, height=212)

with window("Help", x_pos=775, y_pos=10, no_resize=True, no_move=True, no_collapse=True, no_close=True, width=40, height=40, no_title_bar=True):
    add_button("?", width=30, height=30, tip="Get more information on github.", callback=open_github)


start_dearpygui(primary_window="Main")