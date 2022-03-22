import requests
import re

def generate_dict(url, image_count=1):
    '''
        returns a dictionary dictionary containing the preview elements:
            dict_keys :
                'title' : '',
                'description': '',
                'images': '',
                'website': ''
    '''
    return_dict = {}
    try:
        html = requests.get(url).text
        meta_elems = re.findall('<[\s]*meta[^<>]+og:(?:title|image|description)(?!:)[^<>]+>', html)
        og_map = map(return_og, meta_elems)
        og_dict = dict(list(og_map))
    
    # title
        try:
            return_dict['title'] = og_dict['og.title']
        except KeyError:
            return_dict['title'] = find_title(html)
    
    # description
        try:
            return_dict['description'] = og_dict['og.description']
        except KeyError:
            return_dict['description'] = find_meta_desc(html)
    
    # website
        return_dict['website'] = find_host_website(url)
    
    # Image
        return_dict['images'] = []
        image_path = og_dict.get('og.image')
        if image_path:
            return_dict['images'].append(image_path)

        image_path = find_image(html)
        if 'http' not in image_path and len(image_path) > 0:
            image_path = 'http://' + return_dict['website'] + image_path
        if len(image_path) > 0:
            return_dict['images'].append(image_path)

        image_paths = find_images(html, image_count)
        for image_path in image_paths:
            if 'http' not in image_path:
                image_path = 'http://' + return_dict['website'] + image_path
            return_dict['images'].append(image_path)
        return_dict['images'] = list(dict.fromkeys(return_dict['images']))
        if len(return_dict['images']) > image_count:
            return_dict['images'] = return_dict['images'][0:image_count]

        return return_dict
    
    except Exception as e:
        'Raises Occurred Exception'
        raise e

def return_og(elem):
    '''
        returns content of og_elements
    '''
    content = re.findall('content[\s]*=[\s]*"[^<>"]+"', elem)[0]
    p = re.findall('"[^<>]+"', content)[0][1:-1]
    if 'og:title' in elem:
        return ("og.title", p)
    elif 'og:image' in elem and 'og:image:' not in elem:
        return ("og.image", p)
    elif 'og:description' in elem:
        return ("og.description", p)
    
def find_title(html):
    '''
        returns the <title> of html
    '''
    try:
        title_elem = re.findall('<[\s]*title[\s]*>[^<>]+<[\s]*/[\s]*title[\s]*>', html)[0]
        title = re.findall('>[^<>]+<', title_elem)[0][1:-1]
    except:
        title = ''
    return title

def find_meta_desc(html):
    '''
        returns the description (<meta name="description") of html
    '''
    try:
        meta_elem = re.findall('<[\s]*meta[^<>]+name[\s]*=[\s]*"[\s]*description[\s]*"[^<>]*>', html)[0]
        content = re.findall('content[\s]*=[\s]*"[^<>"]+"', meta_elem)[0]
        description = re.findall('"[^<>]+"', content)[0][1:-1]
    except:
        description = ''
    return description

def find_image(html):
    '''
        returns the favicon of html
    '''
    try:
        favicon_elem = re.findall('<[\s]*link[^<>]+rel[\s]*=[\s]*"[\s]*shortcut icon[\s]*"[^<>]*>', html)[0]
        href = re.findall('href[\s]*=[\s]*"[^<>"]+"', favicon_elem)[0]
        image = re.findall('"[^<>]+"', href)[0][1:-1]
    except:
        image = ''
    return image

def find_images(html, count=1):
    '''
        returns an array of image urls
    '''
    try:
        images = []
        image_elems = re.findall('<[\s]*img[^<>]*>', html)
        for elem in image_elems:
            src_elem = re.findall('src[\s]*=[\s]*"[^<>"]+"', elem)[0]
            images.append(re.findall('"[^<>]+"', src_elem)[0][1:-1])
    except:
        pass
    return images

def find_host_website(url):
    '''
        returns host website from the url
    '''
    return list(filter(lambda x: '.' in x, url.split('/')))[0]