import sys
import os
import shutil
from robotjobs.models import Testdata, Tag
from lib.django.robot_testdata import RobotTestData
from git import Repo

def clone_repo(path):
    sys.path.append(path) 
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        return False

    try:
        output = Repo.clone_from("ssh://git@stash.internal.cloudgenix.com:7999/maserati/robot_web.git", path)
    except:
        return False
    return True

def load_testdata_to_db(git_clone=True):
    if len(Testdata.objects.all()) == 0 and git_clone:
        path='/tmp/roboframe'
        if clone_repo(path):
            test_data_obj = RobotTestData(path)
            mydict = test_data_obj.get_data()
            q = [(mydict, [])]
            while q:
                n, p = q.pop(0)
                if isinstance(n, dict):
                   for k, v in n.items():
                       q.append((v, p+[k]))
                elif isinstance(n, list):
                    for i, v in enumerate(n):
                        if isinstance(v, dict):
                            q.append((v, p))
                            if v.get("testcase",None) and v.get("testcase_tags",None):
                                feature = p[-2]
                                test_suite =  p[-1]
                                tags = v.get("testcase_tags",None)
                                testcases= v.get("testcase",None)
                                raw_tag_names = "|".join(tags)+'|'+'full'
                                print "raw tag", raw_tag_names
                                testdata = Testdata()
                                testdata.testsuite = feature
                                testdata.testfile = test_suite
                                testdata.testcase = testcases
                                testdata.save()
                                tag_names = [name for name in raw_tag_names.split('|') if name]
                                print "tag name list", tag_names
                                for tag_name in tag_names:
                                    try:
                                        Tag.objects.get(name=tag_name)
                                    except:
                                        t = Tag(name=tag_name)
                                        t.save()
                                    finally:
                                        print feature, test_suite, testcases, tag_name
                                        tag_o = Tag.objects.get(name=tag_name)
                                        testdata.tag.add(tag_o)
                                        testdata.save()
