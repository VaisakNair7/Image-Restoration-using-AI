from flask import Flask, flash, request, render_template, url_for, redirect
from werkzeug.utils import secure_filename
import os
import subprocess
import shutil
from glob import glob
from bs4 import BeautifulSoup
import cv2

#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

UPLOAD_ENHANCE_FOLDER = 'static/upload_enhance'
RESULT_ENHANCE_FOLDER = 'static/result_enhance'
UPLOAD_COLOR_FOLDER = 'static/upload_color'
RESULT_COLOR_FOLDER = 'static/result_color'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_ENHANCE_FOLDER'] = UPLOAD_ENHANCE_FOLDER
app.config['RESULT_ENHANCE_FOLDER'] = RESULT_ENHANCE_FOLDER
app.config['UPLOAD_COLOR_FOLDER'] = UPLOAD_COLOR_FOLDER
app.config['RESULT_COLOR_FOLDER'] = RESULT_COLOR_FOLDER
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Check the uploaded file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# To update the html tags everytime the page reloads
def update_options(options, enhance = True):
        
    # For enhance.html
    if enhance:
        if len(request.form.getlist('face')) > 0:
            options.find('input', {'id': 'face'}).attrs['checked'] = ''
        else:
            try:
                del options.find('input').attrs['checked']
            except:
                print('Could not delete checked attribur')

        options.find('input', {'id': 'scale'}).attrs['value'] = request.form.get('scale')
        options.find('output').string = request.form.get('scale')
        
    # For color.html
    else:
        if request.form.get('style') == 'artistic':
            if 'checked' not in options.find('input', {'id': 'artistic'}).attrs.keys():
                options.find('input', {'id': 'artistic'}).attrs['checked'] = ''
        else:
            if 'checked' not in options.find('input', {'id': 'stable'}).attrs.keys():
                options.find('input', {'id': 'stable'}).attrs['checked'] = ''
    
    return options


@app.route('/')
def home():   
    return render_template('index.html')


@app.route('/enhance', methods = ['GET', 'POST'])
def enhance():
    
    global options, upload_image, result_image, upload_text, result_text
    options = BeautifulSoup('<input type="checkbox" id="face" name="face" value="face" checked>'
                            '<label for="face">&nbsp;Enhance face(s)</label><br>'
                            '<p>Select Scaling Factor (1 - 4):</p>'
                            '<input type="range" min="1" max="4" step="0.1" value="2" id="scale" name="scale"'
                            'oninput="this.nextElementSibling.value = this.value">'
                            '<output>2.0</output>')
    
    upload_image, result_image = 'static/index/white.png', 'static/index/white.png'
    upload_text, result_text = '', ''
    
    # Upload Button in 'enhance.html'
    if request.form.get('upload_enhance') == 'upload_enhance':
        
        [os.remove(file) for file in glob('static/upload_enhance/*')]
        [os.remove(file) for file in glob('static/result_enhance/*')]
        [os.remove(file) for file in glob('src/Real-ESRGAN/uploads/*')]
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_ENHANCE_FOLDER'], filename))
            shutil.copy(f"static/upload_enhance/{os.listdir('static/upload_enhance')[0]}", 
                        f"src/Real-ESRGAN/uploads/{os.listdir('static/upload_enhance')[0]}")
        
        upload_image = glob('static/upload_enhance/*')[0]
        
        img = cv2.imread(upload_image)
        h, w = img.shape[0], img.shape[1]
        upload_text = f"Uploaded Image : {os.listdir('static/upload_enhance')[0]} ({h} x {w})"
        
        options = update_options(options, enhance = True)
        
        return render_template('enhance.html', upload_image = upload_image, result_image = result_image, options = options,
                              upload_text = upload_text, result_text = result_text)
    
    
    # Enhance button in 'enhance.html'
    if request.form.get('enhance_image') == 'enhance_image':
            
        scale_factor = request.form.get('scale')
        
        os.chdir('src/Real-ESRGAN')
        
        [os.remove(f'results/{file}') for file in os.listdir('results')]
        
        # Run the Real-ESRGAN inference python command
        # Change the --tile value below to fit your GPU memory / to avoid CUDA OOM error
        if len(request.form.getlist('face')) > 0:
            out = subprocess.run(['python', 'inference_realesrgan.py', '-n', 'RealESRGAN_x4plus', '-i', 'uploads', 
                                  '--outscale', scale_factor, '--half', '--face_enhance', '--tile', '300'],
                                  capture_output = True)
            print(out.stderr)
            print(out.stdout)
        else:
            out = subprocess.run(['python', 'inference_realesrgan.py', '-n', 'RealESRGAN_x4plus', '-i', 'uploads', 
                                  '--outscale', scale_factor, '--half', '--tile', '300'], 
                                 capture_output = True)   
            print(out.stderr)
            print(out.stdout)
        
        # Copy the results into 'static/result_enhance' folder
        shutil.copy(f"results/{os.listdir('results')[0]}", f"../../static/result_enhance/{os.listdir('results')[0]}")
        
        os.chdir('../..')
        
        upload_image = glob('static/upload_enhance/*')[0]
        result_image = glob('static/result_enhance/*')[0]
        
        img = cv2.imread(upload_image)
        h, w = img.shape[0], img.shape[1]
        upload_text = f"Uploaded Image : {os.listdir('static/upload_enhance')[0]} ({h} x {w})"
        result_text = 'Enhanced Image'
        
        options = update_options(options, enhance = True)
        
        return render_template('enhance.html', upload_image = upload_image, result_image = result_image, options = options,
                              upload_text = upload_text, result_text = result_text)
    
    return render_template('enhance.html', upload_image = upload_image, result_image = result_image, options = options,
                          upload_text = upload_text, result_text = result_text)

@app.route('/color', methods = ['GET', 'POST'])
def color():
    
    global options, upload_image, result_image, upload_text, result_text
    options = BeautifulSoup('<input type="radio" id="artistic" name="style" value="artistic" checked>'
                            '<label for="artistic"> Artistic (Highest quality results in image coloration,'
                            ' details and vibrance)</label><br><br>'
                            '<input type="radio" id="stable" name="style" value="stable">'
                            '<label for="stable"> Stable (Achieves the best results with landscapes and portraits)</label>')
    
    upload_image, result_image = 'static/index/white.png', 'static/index/white.png'
    upload_text, result_text = '', ''
    
    # Upload button in 'color.html'
    if request.form.get('upload_color') == 'upload_color':
        
        [os.remove(file) for file in glob('static/upload_color/*')]
        [os.remove(file) for file in glob('static/result_color/*')]
        [os.remove(file) for file in glob('src/DeOldify/test_images/*')]
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_COLOR_FOLDER'], filename))
            shutil.copy(f"static/upload_color/{os.listdir('static/upload_color')[0]}", 
                        f"src/DeOldify/test_images/{os.listdir('static/upload_color')[0]}")
        
        upload_image = glob('static/upload_color/*')[0]
        
        img = cv2.imread(upload_image)
        h, w = img.shape[0], img.shape[1]
        upload_text = f"Uploaded Image : {os.listdir('static/upload_color')[0]} ({h} x {w})"
        
        options = update_options(options, enhance = False)
        
        return render_template('color.html', upload_image = upload_image, result_image = result_image, options = options,
                              upload_text = upload_text, result_text = result_text)
    
    
    # Colorize button in 'color.html'
    if request.form.get('color_image') == 'color_image':
        
        os.chdir('src/DeOldify')

        # Use DeOldify's code to color the image
        from ImageColorizer import colorize
        
        [os.remove(file) for file in glob('result_images/*')]
        
        
        # Change the render_factor in 'ImageColorizer.py' to fit your GPU memory / to avoid CUDA OOM error
        if request.form.get('style') == 'artistic':
            colorize(artistic = True)
        else:
            colorize(artistic = False)
        
        # Copy the results into 'static/result_color' folder
        shutil.copy(glob('result_images/*')[0], f"../../static/result_color/{os.listdir('result_images')[0]}")
        
        os.chdir('../..')
        
        upload_image = glob('static/upload_color/*')[0]
        result_image = glob('static/result_color/*')[0]
        
        img = cv2.imread(upload_image)
        h, w = img.shape[0], img.shape[1]
        upload_text = f"Uploaded Image : {os.listdir('static/upload_color')[0]} ({h} x {w})"
        result_text = 'Colorized Image'
        
        options = update_options(options, enhance = False)
        
        return render_template('color.html', upload_image = upload_image, result_image = result_image, options = options,
                              upload_text = upload_text, result_text = result_text)
    
    return render_template('color.html', upload_image = upload_image, result_image = result_image, options = options,
                          upload_text = upload_text, result_text = result_text)


if __name__ == '__main__':
    app.run(debug = True, use_reloader = False)