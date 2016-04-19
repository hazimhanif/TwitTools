'''
Created on Apr 14, 2016

@author: Hazim
'''

import os
import shutil

depth=0
counter=0
user=0

def clean(doc,dir_id):
    list_file = os.listdir(dir_id)
    if not("followers.txt" in list_file and "friends.txt" in list_file and "tweets.dump" in list_file and "user_data.dump" in list_file):
        dir_temp = "%s/drop" % dir_id   
        f = open(dir_temp,"wb")
        f.close()
        dst_dir = "D:/Classify/Drop/%s" % doc
        try:
            os.makedirs(dst_dir)
        except FileExistsError:
            shutil.rmtree(dir_id)
            return
        
        list_file = os.listdir(dir_id)
        for file in list_file:
            src_f = "%s/%s" %(dir_id,file)
            dst_f = "%s/%s" %(dst_dir,file)
            shutil.move(src_f, dst_f)
        os.rmdir(dir_id)
        return True   
    else:
        return False

while depth<3:
    dir_depth = 'D:/Twitter/Depth-%d' % depth
    list_dir = os.listdir(dir_depth)
    for doc in list_dir:
        user+=1
        dir_id = '%s/%s' % (dir_depth,str(doc))
        clean_status=clean(doc,dir_id)
        print("Total Number user: ",user)
        if clean_status==True:
            counter +=1
            print("Clean user count: ", counter)
    
    depth +=1
