from ttkbootstrap import Style

def setup_dark_theme():
    style = Style(theme='cyborg')
    
    # Additional customizations
    style.configure('TButton', font=('Segoe UI', 10))
    style.configure('Treeview', rowheight=25)
    style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
    
    return style