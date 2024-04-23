from django.urls import path
from university import views

app_name ='university'
urlpatterns = [
    # Degree
    path('degree/', views.degree, name='degree'),
    
     # DegreeCourse
    path('degreecourse/', views.degreecourse, name='degreecourse'),
    
    # Course
    path('course/', views.course, name='course'),
    path('course/add_course/', views.add_course, name='add_course'),
    path('course/delete_course/', views.delete_course, name='delete_course'),
    path('course/<str:Course_Id>/edit_course/', views.edit_course, name='edit_course'),
    
    # Instructor
    path('instructor/', views.instructor, name='instructor'),
    
    # Section
    path('section/', views.section, name='section'),
    
    # Objective
    path('objective/', views.objective, name='objective'),
    
    # Evaluation
    path('evaluation/', views.evaluation, name='evaluation'),
    # Queries involving evaluations
    path('evaluationquery/', views.evaluationquery, name='evaluationquery'),
    path('passratequery/', views.passratequery, name='passratequery'),
]