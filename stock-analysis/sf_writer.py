
def html_writer(html_path, content_list):
    f = open(html_path,"w")
    for i in content_list:
        f.write(i)
        f.write('\n')
    f.close

def file_writer(filename, content_list):
    f = open(filename,"w")
    for i in content_list:
        f.write(i + " ")
    f.close