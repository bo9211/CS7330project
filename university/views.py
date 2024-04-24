from django.shortcuts import render, redirect
from university import models, forms


# Course
def course(request):
    queryset = models.Course.objects.all().order_by('course_id')
    return render(request, 'university/course/course.html', {'queryset': queryset})


def add_course(request):
    if request.method == "GET":
        return render(request, 'university/course/add_course.html')
    Course_Id = request.POST.get("course_id")
    Name = request.POST.get("name")
    models.Course.objects.create(course_id=Course_Id, name=Name)
    return redirect("/course/")


def delete_course(request):
    Course_Id = request.GET.get("course_id")
    models.Course.objects.filter(course_id=Course_Id).delete()
    return redirect("/course/")


def edit_course(request, Course_Id):
    if request.method == 'GET':
        row_object = models.Course.objects.filter(course_id=Course_Id).first()
        return render(request, 'university/course/edit_course.html', {"row_object": row_object})

    Name = request.POST.get("name")
    models.Course.objects.filter(course_id=Course_Id).update(name=Name)
    return redirect("/course/")


# Degree
def degree(request):
    queryset = models.Degree.objects.all()
    return render(request, 'university/degree/degree.html', {'queryset': queryset})


# DegreeCourse
def degreecourse(request):
    queryset = models.DegreeCourse.objects.all()
    return render(request, 'university/degreecourse/degreecourse.html', {'queryset': queryset})


# Instructor
def instructor(request):
    queryset = models.Instructor.objects.all()
    return render(request, 'university/instructor/instructor.html', {'queryset': queryset})


# Section
def section(request):
    queryset = models.Section.objects.all()
    return render(request, 'university/section/section.html', {'queryset': queryset})


# Objective
def objective(request):
    queryset = models.Objective.objects.all()
    return render(request, 'university/objective/objective.html', {'queryset': queryset})


# Evaluation
def evaluation(request):
    queryset = models.Evaluation.objects.all()
    return render(request, 'university/evaluation/evaluation.html', {'queryset': queryset})


# Queries involving evaluations
def evaluationquery(request):
    queryset = models.Evaluation.objects.all()
    return render(request, 'university/evaluation/evaluationquery.html', {'queryset': queryset})


def query_course(request):
    form = forms.QueryCourseForm(request.POST or None)
    sections = None

    if request.method == 'POST' and form.is_valid():
        course = form.cleaned_data['course']
        year = form.cleaned_data['year']
        semester = form.cleaned_data['semester']
        sections = models.Section.objects.filter(
            course=course,
            year=year,
            semester=semester
        )
    return render(
        request,
        'university/course/course_result.html',
        {'form': form, 'sections': sections}
    )


def instructor_sections(request):
    form = forms.QueryInstructorForm(request.POST or None)
    sections = None
    if request.method == 'POST' and form.is_valid():
        instructor = form.cleaned_data['instructor']
        year = form.cleaned_data['year']
        semester = form.cleaned_data['semester']
        sections = models.Section.objects.filter(
            instructor=instructor,
            year=year,
            semester=semester
        )

    return render(request, 'university/instructor/instructor_result.html', {
        'form': form,
        'sections': sections
    })


def degree_details(request):
    # Initialize the form with POST data or None
    form = forms.DegreeQueryForm(request.POST or None)

    # Prepare the initial context
    context = {'form': form}

    if request.method == 'POST' and form.is_valid():
        degree = form.cleaned_data['degree']

        if degree:
            courses = models.Course.objects.filter(degreecourse__degree=degree)
            sections = models.Section.objects.filter().order_by('-year', 'semester')

            objectives = models.Objective.objects.all()

            objectives_courses = {
                objective: models.Course.objects.filter(objective=objective)
                for objective in objectives
            }

            context.update({
                'degree': degree,
                'courses': courses,
                'sections': sections,
                'objectives': objectives,
                'objectives_courses': objectives_courses,
            })

    return render(request, 'university/degree/degree_result.html', context)
