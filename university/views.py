from django.http import HttpResponse, Http404
from django.shortcuts import render,redirect
from university import models


# Course
def course(request):
    queryset = models.Course.objects.all().order_by('course_id')
    return render(request, 'university/course/course.html',{'queryset':queryset})

def add_course(request):
    if request.method == "GET":
        return render(request,'university/course/add_course.html')
    Course_Id = request.POST.get("course_id")
    Name = request.POST.get("name")
    models.Course.objects.create(course_id=Course_Id, name=Name)
    return redirect("/course/")

def delete_course(request):
    Course_Id = request.GET.get("course_id")
    models.Course.objects.filter(course_id=Course_Id).delete()
    return redirect("/course/")
    
def edit_course(request, Course_Id):
    if request.method =='GET':
        row_object = models.Course.objects.filter(course_id=Course_Id).first()
        return render(request,'university/course/edit_course.html', {"row_object":row_object})
    
    Name = request.POST.get("name")
    models.Course.objects.filter(course_id=Course_Id).update(name=Name)
    return redirect("/course/")

# Degree
def degree(request):
    queryset = models.Degree.objects.all()
    return render(request, 'university/degree/degree.html',{'queryset':queryset})

# DegreeCourse
def degreecourse(request):
    queryset = models.DegreeCourse.objects.all()
    return render(request, 'university/degreecourse/degreecourse.html',{'queryset':queryset})

# Instructor
def instructor(request):
    queryset = models.Instructor.objects.all()
    return render(request, 'university/instructor/instructor.html',{'queryset':queryset})

# Section
def section(request):
    queryset = models.Section.objects.all()
    return render(request, 'university/section/section.html',{'queryset':queryset})

# Objective
def objective(request):
    queryset = models.Objective.objects.all()
    return render(request, 'university/objective/objective.html',{'queryset':queryset})

# Evaluation
def evaluation(request):
    queryset = models.Evaluation.objects.all()
    return render(request, 'university/evaluation/evaluation.html',{'queryset':queryset})
 # Queries involving evaluations
# def evaluationquery(request):
#     queryset = models.Evaluation.objects.all()
#     return render(request, 'university/evaluation/evaluationquery.html',{'queryset':queryset})

# def evaluationquery(request):
#     semester_param = request.GET.get('semester', None)
#     percentage_param = request.GET.get('percentage', None)

#     if semester_param is None and percentage_param is None:
#         # 第一次加载页面时不显示警告
#         return render(request, 'university/evaluation/evaluationquery.html', {'initial_load': True})
    
#     if semester_param == '':
#         # 如果semester参数为空，显示警告
#         return render(request, 'university/evaluation/evaluationquery.html', {'error': 'Semester is required.'})

#     # 处理及格率查询
#     if percentage_param:
#         if percentage_param == '':
#             return render(request, 'university/evaluation/evaluationquery.html', {'error': 'Percentage is required.'})
#         return handle_pass_rate_query(request, semester_param, percentage_param)
    
#     # 处理总体评估信息查询
#     return handle_total_evaluation_query(request, semester_param)

# def handle_total_evaluation_query(request, semester_param):
#     if len(semester_param) >= 6:
#         year = semester_param[:4]
#         semester = semester_param[4:]
#         queryset = models.Evaluation.objects.filter(
#             section__semester=semester, 
#             section__year=int(year)
#         )
#         if queryset.exists():
#             return render(request, 'university/evaluation/evaluationquery.html', {'queryset': queryset})
#         else:
#             return render(request, 'university/evaluation/evaluationquery.html', {'message': 'No data available for the provided semester.'})
#     else:
#         return render(request, 'university/evaluation/evaluationquery.html', {'error': 'Invalid semester format.'})
# def handle_pass_rate_query(request, semester_param, percentage_param):
#     if len(semester_param) >= 6:
#         year = semester_param[:4]
#         semester = semester_param[4:]
#         queryset = models.Evaluation.objects.filter(
#             section__semester=semester, 
#             section__year=int(year)
#         )
#         if not queryset.exists():
#             return render(request, 'university/evaluation/evaluationquery.html', {'percentage_message': 'No data available for the provided semester.'})

#         total_passed = total_students = 0
#         for eval in queryset:
#             total_passed += eval.levelA_stu_num + eval.levelB_stu_num + eval.levelC_stu_num
#             total_students += eval.levelA_stu_num + eval.levelB_stu_num + eval.levelC_stu_num + eval.levelF_stu_num

#         if total_students > 0:
#             pass_rate = (total_passed / total_students) * 100
#             if pass_rate >= float(percentage_param):
#                 return render(request, 'university/evaluation/evaluationquery.html', {'percentage_result': f'Pass rate is {pass_rate:.2f}%, which is above or equal to the threshold of {percentage_param}%.'})
#             else:
#                 return render(request, 'university/evaluation/evaluationquery.html', {'percentage_result': f'Pass rate is {pass_rate:.2f}%, which is below the threshold of {percentage_param}%.'})
#         else:
#             return render(request, 'university/evaluation/evaluationquery.html', {'percentage_message': 'No students data available to calculate pass rate.'})
#     else:
#         return render(request, 'university/evaluation/evaluationquery.html', {'error': 'Invalid semester format.'})

def evaluationquery(request):
    semester_param = request.GET.get('semester', None)  # None表示未指定时默认值
    if semester_param is None:
        # 第一次加载页面时不显示警告
        return render(request, 'university/evaluation/evaluationquery.html', {'initial_load': True})
    elif semester_param == '':
        # 如果参数为空字符串，显示警告
        return render(request, 'university/evaluation/evaluationquery.html', {'error': 'Semester is required.'})

    # 处理正常情况，即用户已输入semester
    if len(semester_param) >= 6:
        year = semester_param[:4]
        semester = semester_param[4:]
        queryset = models.Evaluation.objects.filter(
            section__semester=semester, 
            section__year=int(year)
        )
        if queryset.exists():
            return render(request, 'university/evaluation/evaluationquery.html', {'queryset': queryset})
        else:
            return render(request, 'university/evaluation/evaluationquery.html', {'message': 'No data available for the provided semester.'})
    else:
        # 格式错误的处理
        return render(request, 'university/evaluation/evaluationquery.html', {'error': 'Invalid semester format.'})
    
def handle_pass_rate_query(request, semester_param, percentage_param):
    try:
        year = semester_param[:4]
        semester = semester_param[4:]
        queryset = models.Evaluation.objects.filter(
            section__semester=semester,
            section__year=int(year)
        )
        if not queryset:
            return render(request, 'university/evaluation/passratequery.html', {'message': 'No evaluations found for the provided semester.'})
        
        total_passed = total_students = 0
        for eval in queryset:
            # Assuming all these fields are integers and include the count of students at each grade level
            passed = eval.levelA_stu_num + eval.levelB_stu_num + eval.levelC_stu_num
            total = passed + eval.levelF_stu_num

            if total > 0:
                total_passed += passed
                total_students += total

        if total_students > 0:
            pass_rate = (total_passed / total_students) * 100
            # Check if pass rate meets the specified percentage threshold
            if pass_rate >= float(percentage_param):
                return render(request, 'university/evaluation/passratequery.html', {
                    'pass_rate': f'Pass rate is {pass_rate:.2f}% and meets or exceeds the threshold of {percentage_param}%.'})
            else:
                return render(request, 'university/evaluation/passratequery.html', {
                    'pass_rate': f'Pass rate is {pass_rate:.2f}% and does not meet the threshold of {percentage_param}%.'})
        else:
            return render(request, 'university/evaluation/passratequery.html', {'message': 'No student data available to calculate pass rate.'})
        
    except ValueError:
        return render(request, 'university/evaluation/passratequery.html', {'error': 'Invalid semester format or percentage value.'})

# 及格率查询
def passratequery(request):
    semester_param = request.GET.get('semester', None)
    percentage_param = request.GET.get('percentage', None)
    if semester_param is None or percentage_param is None:
        return render(request, 'university/evaluation/passratequery.html', {'initial_load': True})
    if semester_param == '' or percentage_param == '':
        return render(request, 'university/evaluation/passratequery.html', {'error': 'Both semester and percentage are required.'})
    
    return handle_pass_rate_query(request, semester_param, percentage_param)