import datetime
import os,sys
import time

def html_kmaker(element_list):
    content_list = ['<!DOCTYPE html>',
                    '<html>',
                    '<head>',
                    '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />',
                    '<title>stock filter %s </title>' % (datetime.date.today()),
                    '<link rel="linkaction" type="text/css" href="links.css">',
                    '<link rel="font-family" type="text/css" href="fonts.css">',
                    '</head>',
                    '<body>',]
    for i in element_list:
        link = '<a href="https://xueqiu.com/S/%s">%s</a> </br>' % (i,i)
        image = '<img src="kline/%s.jpg" alt="%s"> </br>' % (i,i)
        content_list.append(link)
        content_list.append(image)
    
    content_list.append("</body>")
    content_list.append("</html>")
    return content_list

def html_pmaker(element_list):
    content_list = ['<!DOCTYPE html>',
                    '<html>',
                    '<head>',
                    '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />',
                    '<title>stock filter %s </title>' % (datetime.date.today()),
                    '<link rel="linkaction" type="text/css" href="links.css">',
                    '<link rel="font-family" type="text/css" href="fonts.css">',
                    '</head>',
                    '<body>',]
    for i in element_list:
        link = '<a href="https://xueqiu.com/S/%s">%s</a> </br>' % (i,i)
        image = '<img src="pondraw/%s.jpg" alt="%s"> </br>' % (i,i)
        content_list.append(link)
        content_list.append(image)
    
    content_list.append("</body>")
    content_list.append("</html>")
    return content_list


def file_maker():

    now = time.strftime("%Y-%m-%d-%H_%M",time.localtime(time.time()))
    
    # Python program to explain os.mkdir() method 

    directory = "stock_" + now + ".html"

    parent_dir = "/usr/share/nginx/html"

    path = os.path.join(parent_dir, directory) 

    os.mkdir(path)
    print("Directory '%s' created" %directory)
    return path


