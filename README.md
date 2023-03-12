# gallery-stable-diffusion
Collect picture from civitai.com and copy prompt... quickly

Before using, please install browser_cookie3 with command 'pip3 install browser_cookie3'.

**How to install:**
1. Download zip file to your computer disk E:, this was hardcode in some files. If you want to install on other disks please search and change it in the code.
2. Enter CMD.
3. cd to E:\gallery-stable-diffusion\gallery_sd folder.
4. Input python manage.py runserver 8080
5. Open browser and go to http://127.0.0.1:8080/

**How to use:**
1. Login civitai.com if you want to collect some 18+ pictures.
2. Copy the picture information page from civitai.com and paste the url to input box on the page, then click 'Parsing now' button.
3. After several seconds, picture's information will be displayed on the page, update if needed, then click 'Save' button.
4. Go to 'Gallery' page from the left navi bar, all pictures sorted by checkpoint name are displayed there.
5. Go to detail picture, you can copy the prompt, negative prompt, sampler, CFG scale, Steps, Seed by click 'Copy' button behind, then paste the information to stable-diffusion-webui. You can also set one picture as 'default cover', so this picture will be displayed on the 'Gallery' page as cover.

**Limitation:**
Only tested on Windows.

**To do:**
1. Record picture url in database also, in case parsing the same page twice.
2. Collect tag information.

**Note:**
This tool is created for stable-diffusion webui learning, do NOT use illegal.
