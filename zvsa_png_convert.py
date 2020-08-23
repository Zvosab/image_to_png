# https://pysimplegui.readthedocs.io/en/latest/
import ntpath
import time
import PySimpleGUI as sG
from PIL import Image, ImageOps, UnidentifiedImageError


str_list = []


def remove_every_nth(li, n):
    del li[n - 1::n]
    return li


sG.theme('DarkBlue2')

layout = [
    [sG.Text('Choose images you want to convert and where to save them: ')],
    [sG.Text('Select images:', size=(15, 1)), sG.Input(), sG.FilesBrowse()],
    [sG.Text('Store location:', size=(15, 1)), sG.Input(), sG.FolderBrowse()],
    [sG.Submit('Convert'), sG.Cancel('Close'), sG.Submit('INFO')]
]

window = sG.Window('ZVSA PNG converter v1.02', layout, location=(500, 500), icon='png-image-file-type-interface'
                                                                                 '-symbol-of-rounded-rectangular'
                                                                                 '-stroke_icon-icons.com_57521.ico')
while True:
    counter = 0
    event, values = window.read()
    print(event, values)
    t1 = time.time()
    if event == sG.WIN_CLOSED or event == 'Close':
        break
    if event == 'Convert':
        chosen_images = values[0]
        str_list = chosen_images.split(';')
        try:
            for images in str_list:
                paths = []
                sG.one_line_progress_meter('Progress', counter + 1, len(str_list))
                image = Image.open(images, 'r')
                paths.append(images)
                if image.size[0] != image.size[1]:
                    img = ImageOps.pad(image, (400, 400), Image.ANTIALIAS, color=(255, 255, 255))
                else:
                    img = ImageOps.pad(image, (400, 400), Image.ANTIALIAS)
                converted = img.convert('P', palette=Image.ADAPTIVE)
                newpath = ntpath.basename(paths[0])
                newlist = newpath.split('.')
                remove_every_nth(newlist, 2)
                new_str = newlist[0].lower()
                converted.save(f'{values[1]}/{new_str[:]}.png', 'png')
                paths.clear()
                counter += 1
        except AttributeError:
            popup1 = sG.popup_ok_cancel('No images selected.', keep_on_top=True, icon='png-image-file-type-interface'
                                                                                      '-symbol-of-rounded-rectangular'
                                                                                      '-stroke_icon-icons.com_57521'
                                                                                      '.ico',
                                        image='icons8-no-image-64.png')
            if popup1 == 'OK':
                continue
            else:
                break
        except UnidentifiedImageError:
            popup3 = sG.popup_ok_cancel('Please select an image format only.', keep_on_top=True,
                                        icon='png-image-file-type-interface-symbol-of-rounded-rectangular-stroke_icon'
                                             '-icons.com_57521.ico', image='icons8-no-image-64.png')
            if popup3 == 'OK':
                continue
            else:
                break
    if event == 'INFO':
        popup4 = sG.popup('ZVSA PNG converter\n\nv1.02\n\ncopyright©2020\n\nINSTRUCTIONS\n'
                          '1. Browse for images you want to convert\n2. Choose where to save converted files\n3. Click '
                          'Convert\n\nABOUT\nProgram converts images to 400x400x8bit format needed for catalog '
                          'preview\n\nCONTACT\nzvosab@gmail.com', title='INFO & INSTRUCTIONS', line_width=100,
                          keep_on_top=True, icon='png-image-file-type-interface-symbol-of-rounded-rectangular'
                                                 '-stroke_icon-icons.com_57521.ico')
        if popup4 == 'OK':
            continue
        else:
            continue
    sG.os.startfile(f'{values[1]}')
    t2 = time.time()
    t3 = t2 - t1
    popup2 = sG.Popup(f'{len(str_list)} images converted, took {t3} seconds', keep_on_top=True, location=(200, 200),
                      icon='png-image-file-type-interface-symbol-of-rounded-rectangular-stroke_icon-icons.com_57521.ico'
                      )
    if popup2 == 'OK':
        continue
    else:
        break

window.close()
