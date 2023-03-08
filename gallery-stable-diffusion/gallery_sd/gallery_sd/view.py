from django.shortcuts import render
from django.db import connections
from gallery import models
import random
import requests
import re
import time, string, os
import shutil
import browser_cookie3


def gallery_home(request):
    folder_n = {}
    dir_path = 'E:\\gallery-stable-diffusion\\gallery_sd\\gallery_sd\\static\\data\\Checkpoint'
    folder_names = []
    for entry in os.listdir(dir_path):
        folder_names.append(entry)

    # print('Folder names:', folder_names)
    folder_n['folder_names'] = folder_names
    return render(request, 'gallery.html', folder_n)


def parsing(request):
    if request.method == 'POST':
        parsing_result = {}
        # if nothing inputted
        try:
            url = request.POST.getlist('url')[0]
        except IndexError as Exception:
            parsing_result['link_error'] = True
            return render(request, 'parsing.html', {"parsing_result": parsing_result})
        
        # if 'civitai' not in url
        if 'civitai' not in url:
            parsing_result['link_error'] = True
            return render(request, 'parsing.html', {"parsing_result": parsing_result})

        # print(url)
        try:
            ci = browser_cookie3.load(domain_name='civitai.com')
        except:
            ci = ''
            print('Not logged in error')
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 '
                          'Safari/537.36 ',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }

        try:
            page_content = requests.get(url=url, headers=headers, cookies=ci).text
        except:
            parsing_result['timeout'] = True
            return render(request, 'parsing.html', {"parsing_result": parsing_result})

        # print('$' * 100)
        # print('page_content')
        # print(page_content)

        ex = '<img class=".*?" src="(.*?)/width=.*?'
        img_src_l = re.findall(ex, page_content, re.S)
        # print('match img_src_l', img_src_l)
        img_src_l = [img_src_l[0] + '/width=300']
        parsing_result['url'] = img_src_l[0]

        ex1 = '<pre class="mantine-Code-root mantine-Code-block .*?" dir="ltr">(.*?)</pre></div>'
        img_pro = re.findall(ex1, page_content, re.S)

        ex_sampler = '<div class=".*?">Sampler</div><code class=".*?" dir="ltr">(.*?)</code></div>'
        ex_scale = '<div class=".*?">CFG scale</div><code class=".*?" dir="ltr">(.*?)</code></div>'
        ex_steps = '<div class=".*?">Steps</div><code class=".*?" dir="ltr">(.*?)</code></div>'
        ex_seed = '<div class=".*?">Seed</div><code class=".*?" dir="ltr">(.*?)</code></div>'
        sampler = re.findall(ex_sampler, page_content, re.S)
        scale = re.findall(ex_scale, page_content, re.S)
        steps = re.findall(ex_steps, page_content, re.S)
        seed = re.findall(ex_seed, page_content, re.S)

        try:
            parsing_result['scale'] = scale[0]
            parsing_result['Steps'] = steps[0]
            parsing_result['Sampler'] = sampler[0]
            parsing_result['Seed'] = seed[0]
        
            if len(img_pro) == 1:
                ex_n_prompt = '<div class=".*?">Negative prompt.*?" dir="ltr">(.*?)</code></div>'
                n_prompt = re.findall(ex_n_prompt, page_content, re.S)

                parsing_result['propmt'] = img_pro[0]
                parsing_result['negetive'] = n_prompt[0]
            else:
                parsing_result['propmt'] = img_pro[0]
                parsing_result['negetive'] = img_pro[1]
        except IndexError as Exception:
            pass

        for i in img_src_l:
            try:
                os.remove('E:\\gallery-stable-diffusion\\gallery_sd\\gallery_sd\\static\\data\\temp\\default.jpg')
            except FileNotFoundError:
                print("File not found")
            try:
                jpg_content = requests.get(url=i, headers=headers).content
            except:
                parsing_result['timeout'] = True
                return render(request, 'parsing.html', {"parsing_result": parsing_result})
            if '%252F' in url:
                sav_fold = url.split('52F')[-1]
            else:
                sav_fold = url.split('%2F')[-1]  # realistic-vision-v13
            parsing_result['cp_name'] = sav_fold
            jpg_name = 'default.jpg'
            folder = 'E:\\gallery-stable-diffusion\\gallery_sd\\gallery_sd\\static\\data\\temp\\'
            jpg_path = folder + jpg_name
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(jpg_path, 'wb') as fp:
                fp.write(jpg_content)
            # print('Download {} done'.format(jpg_name))
        parsing_result['parsing_done'] = True
        print('requests done')
    return render(request, 'parsing.html', locals())


def save_done(request):
    parsing_result = {}
    if request.method == 'POST':
        prompt = request.POST.getlist('prompt')[0]
        negetive = request.POST.getlist('negative prompt')[0]
        scale = request.POST.getlist('CFG Scale')[0]
        Steps = request.POST.getlist('steps')[0]
        Sampler = request.POST.getlist('sampler')[0]
        Seed = request.POST.getlist('seed')[0]
        cp_name = request.POST.getlist('checkpoint')[0]
        sel_cover = request.POST.getlist('cover')
        random_char = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        timenow = time.strftime('%Y%m%d', time.localtime(time.time()))
        pic_name = cp_name + '_' + str(timenow) + '_' + random_char + '.jpg'
        # save to database
        save_db = models.pics(cp=cp_name, pic_name=pic_name, prompt=prompt, n_prompt=negetive, cfg_scale=scale, steps=Steps, sampler=Sampler, seed=Seed)
        save_db.save()
        source_folder = "E:\\gallery-stable-diffusion\\gallery_sd\\gallery_sd\\static\\data\\temp\\default.jpg"
        target_folder = "E:\\gallery-stable-diffusion\\gallery_sd\\gallery_sd\\static\\data\\Checkpoint" + '\\' + cp_name
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            shutil.copy(source_folder, target_folder + '\\default.jpg')
        shutil.move(source_folder, target_folder + "\\" + pic_name)
        if os.path.exists(target_folder) and sel_cover:
            os.remove(target_folder + '\\default.jpg')
            shutil.copy(target_folder + "\\" + pic_name, target_folder + '\\default.jpg')
        print('Saved to DB and folder.')
        parsing_result['save_done'] = True
    return render(request, 'parsing.html', {"parsing_result": parsing_result})


def checkpoint(request):
    if request.method == 'GET':
        cp_name = request.GET.getlist('cp')[0]

        pic_n = {}
        dir_path = 'E:\\gallery-stable-diffusion\\gallery_sd\\gallery_sd\\static\\data\\Checkpoint\\' + cp_name
        pic_names = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                pic_names.append(file)
        pic_names.remove('default.jpg')

        pic_n['pic_names'] = pic_names
        pic_n['cp'] = cp_name
        return render(request, 'checkpoint.html', {"pic_n": pic_n})


def get_pic(request):
    if request.method == 'GET':
        pic = request.GET.getlist('pic')[0]
        pic_info_db = models.pics.objects.get(pic_name=pic)
        pic_info = {}
        pic_info['pic_info'] = pic_info_db
        return render(request, 'picture.html', pic_info)

    elif request.method == 'POST':
        pic_info = {}
        prompt = request.POST.getlist('prompt')[0]
        negetive = request.POST.getlist('negative prompt')[0]
        scale = request.POST.getlist('CFG Scale')[0]
        Steps = request.POST.getlist('steps')[0]
        Sampler = request.POST.getlist('sampler')[0]
        Seed = request.POST.getlist('seed')[0]
        pic_name = request.GET.getlist('pic')[0]
        sel_cover = request.POST.getlist('cover')

        # save to database
        save_db = models.pics.objects.get(pic_name=pic_name)
        db_cp = save_db.cp
        save_db.prompt = prompt
        save_db.n_prompt = negetive
        save_db.cfg_scale = scale
        save_db.steps = Steps
        save_db.sampler = Sampler
        save_db.seed = Seed
        save_db.save()
        print('Saved to DB and folder.')
        pic_info_db = models.pics.objects.get(pic_name=pic_name)
        pic_info['pic_info'] = pic_info_db
        pic_info['cp'] = db_cp
        pic_info['pic_name'] = pic_name
        pic_info['save_done'] = True
        if sel_cover:
            os.remove('E:\\gallery-stable-diffusion\\gallery_sd\\gallery_sd\\static\\data\\Checkpoint\\' + db_cp + '\\default.jpg')
            shutil.copy('E:\\gallery-stable-diffusion\\gallery_sd\\gallery_sd\\static\\data\\Checkpoint\\' + db_cp + '\\' + pic_name, 'E:\\gallery-stable-diffusion\\gallery_sd\\gallery_sd\\static\\data\\Checkpoint\\' + db_cp + '\\default.jpg')
        return render(request, 'picture.html', pic_info)

