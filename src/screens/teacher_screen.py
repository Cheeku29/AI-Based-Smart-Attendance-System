import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, check_pass, create_teacher, teacher_login

def teacher_screen():
    style_base_layout()
    style_background_dashboard() 

    if 'teacher_data' in st.session_state:
        teacher_dashboard()
        return
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    st.header(f"""
            Welcome, {teacher_data['name']}
                """)


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if(teacher):
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False



def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using password', text_alignment='center')

    st.space()
    st.space()

    teacher_username = st.text_input("Enter username", placeholder='Ananyaroy123', key='login_username')
    teacher_password = st.text_input("Enter password", type='password', placeholder='Enter your password', key='login_password')

    st.divider()

    btnc1, btnc2 = st.columns(2);

    with btnc1:
        if st.button('Login', icon=':material/passkey:', shortcut='control+enter', width='stretch', key="teacher_login_btn"):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Welcome back!")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password")

    with btnc2:
        if st.button('Register Instead', icon=':material/passkey:', type='primary', width='stretch', key="teacher_register_btn"):
            st.session_state.teacher_login_type = 'register'
            st.rerun()

    footer_dashboard()

def register_teacher(teacher_username, teacher_name, teacher_password, teacher_password_confirm):
    if not teacher_username or not teacher_name or not teacher_password or not teacher_password_confirm:
        return False, "All fields are required!"

    if teacher_password != teacher_password_confirm:
        return False, "Password doesn't match!"
    
    if check_teacher_exists(teacher_username):
        return False, 'Username already exists!'


    try:
        create_teacher(teacher_username, teacher_password, teacher_name)
        return True, "User registered successfully!, Login now"
    except:
        return False, "Unexpected Error"        
    


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='registerbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Register', text_alignment='center')
    
    st.space()
    st.space()
    
    teacher_username = st.text_input("Enter username", placeholder='AnanyaRoy123', key="register_username")
    teacher_name = st.text_input("Enter name", placeholder='Ananya Roy', key="register_name")
    teacher_password = st.text_input("Enter password", type='password', placeholder='Enter your password', key="register_password")
    teacher_password_confirm = st.text_input("Confirm password", type='password', placeholder='Confirm your password', key="register_password_confirm")
    
    st.divider()
    
    btnc1, btnc2 = st.columns(2);
    
    with btnc1:
        if st.button('Register now', icon=':material/passkey:', shortcut='control+enter', width='stretch', key="teacher_register_now_btn"):
            success, message = register_teacher(teacher_username, teacher_name, teacher_password, teacher_password_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = 'login'
                st.rerun()
            else:
                st.error(message)


    with btnc2:
        if st.button('Login Instead', icon=':material/passkey:', type='primary', width='stretch', key="teacher_login_instead_btn"):
            st.session_state.teacher_login_type = 'login'
            st.rerun()

    footer_dashboard()

# def teacher_screen_register():

#     c1, c2 = st.columns(
#         2,
#         vertical_alignment="center",
#         gap="xxlarge"
#     )

#     with c1:
#         header_dashboard()

#     with c2:
#         if st.button(
#             "Go back to Home",
#             type="secondary",
#             key="registerbackbtn",
#             shortcut="control+backspace"
#         ):
#             st.session_state["login_type"] = None
#             st.rerun()

#     st.header("Register", text_alignment="center")

#     st.space()
#     st.space()

#     teacher_username = st.text_input(
#         "Enter username",
#         placeholder="AnanyaRoy123",
#         key="register_username"
#     )

#     teacher_name = st.text_input(
#         "Enter name",
#         placeholder="Ananya Roy",
#         key="register_name"
#     )

#     teacher_password = st.text_input(
#         "Enter password",
#         type="password",
#         placeholder="Enter your password",
#         key="register_password"
#     )

#     teacher_password_confirm = st.text_input(
#         "Confirm password",
#         type="password",
#         placeholder="Confirm your password",
#         key="register_password_confirm"
#     )

#     st.divider()

#     btnc1, btnc2 = st.columns(2)

#     with btnc1:

#         if st.button(
#             "Register now",
#             icon=":material/passkey:",
#             shortcut="control+enter",
#             width="stretch",
#             key="teacher_register_now_btn"
#         ):

#             # TEMPORARY DEBUG
#             st.write("Username:", repr(teacher_username))
#             st.write("Name:", repr(teacher_name))
#             st.write("Password:", repr(teacher_password))
#             st.write(
#                 "Confirm Password:",
#                 repr(teacher_password_confirm)
#             )

#             success, message = register_teacher(
#                 teacher_username,
#                 teacher_name,
#                 teacher_password,
#                 teacher_password_confirm
#             )

#             st.write("Success:", success)
#             st.write("Message:", message)

#             if success:

#                 st.success(message)

#             else:

#                 st.error(message)

#     with btnc2:

#         if st.button(
#             "Login Instead",
#             icon=":material/passkey:",
#             type="primary",
#             width="stretch",
#             key="teacher_login_instead_btn"
#         ):

#             st.session_state.teacher_login_type = "login"
#             st.rerun()

#     footer_dashboard()



