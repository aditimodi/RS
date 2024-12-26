import matplotlib

import matplotlib.font_manager as fm
print(matplotlib.matplotlib_fname())

# for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
#     print(font)
    
for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
    if 'Arial Narrow' in font:
        print(font)
    else:
        print("font not found")
        
print(sorted(fm.get_font_names()))