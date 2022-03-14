#NOTE:  This must be the first call in order to work properly!
import os
from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
device.set(device = DeviceId.GPU0)

from deoldify.visualize import *
plt.style.use('dark_background')
torch.backends.cudnn.benchmark = True
import warnings
warnings.filterwarnings("ignore", category = UserWarning, message=".*?Your .*? set is empty.*?")

def colorize(artistic = True):    
    
    if artistic:
        colorizer = get_image_colorizer(artistic = True)
        render_factor = 24
    else:
        colorizer = get_image_colorizer(artistic = False)
        render_factor = 16

    #Max is 45 with 11GB video cards. 35 is a good default

    source_path = f"test_images/{os.listdir('test_images')[0]}"
    result_path = None

    result_path = colorizer.plot_transformed_image(path = source_path, render_factor = render_factor)