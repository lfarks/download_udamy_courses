import sys
import os
import requests
import json

if len(sys.argv) == 2:
    bearer = sys.argv[1]
else:
    bearer = raw_input("Enter the authentication token: ")


headers = {'Authorization': 'Bearer ' + bearer}
course = requests.get("https://www.udemy.com/api-2.0/users/me/subscribed-courses/", headers=headers)


courses = json.loads(course.content)
courses_ids = {}

first_page = True
while courses.get("next") != None or first_page:
    first_page = False
    for c in courses.get("results"):
        courses_ids[c.get("id")] = c.get("title")
    if courses.get("next") != None:
        course = requests.get(courses.get("next"), headers=headers)
        courses = json.loads(course.content)

first_page = True
for ci in courses_ids.keys():
    course = requests.get("https://www.udemy.com/api-2.0/users/me/subscribed-courses/%s/lectures?fields[asset]=title,asset_type,length,stream_urls,download_url"%ci, headers=headers)
    dict_res = json.loads(course.content)
    dir = courses_ids[ci]
    os.mkdir(dir)
    while dict_res.get("next") != None or first_page:
        first_page = False
        for r in dict_res["results"]:
            if r["asset"]["asset_type"] == "Video":
                file_name = dir + "/" + r["asset"]["title"]
                video_link = r["asset"]["stream_urls"]["Video"][0]["file"]

                print "Downloading file:%s"%file_name

                r = requests.get(video_link, stream=True)

                if r.status_code == 200:
                    with open(file_name, 'wb') as f:
                        for chunk in r.iter_content(chunk_size = 1024*1024):
                            if chunk:
                                f.write(chunk)

                    print "%s downloaded!\n"%file_name
                else:
                    print "Error while downloading %s!\n"%file_name
        if dict_res.get("next") != None:
            course = requests.get(dict_res.get("next"), headers=headers)
            dict_res = json.loads(course.content)
