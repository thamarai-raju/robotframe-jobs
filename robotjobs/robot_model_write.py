import sys
path = '/home/ubuntu/roboframe/tests_naresh'
sys.path.append(path)
from django.shortcuts import render
from models import Testdata, Tag
from django.http import HttpResponse
from lib.django.robot_testdata import RobotTestData


def home(request):
    load_testdata_to_db()
    testdatalist = Testdata.objects.all()
    return render(request, 'home.html', {'test_data': testdatalist})
def load_testdata_to_db():
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
                                if Tag.objects.get(name=tag_name):
                                    continue
                            except:
                                t = Tag(name=tag_name)
                                t.save()
                            print feature, test_suite, testcases, tag_name
                            tag_o = Tag.objects.get(name=tag_name)
                            testdata.tag.add(tag_o)
                        testdata.save()