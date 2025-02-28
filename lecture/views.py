from django.shortcuts import render
from datetime import datetime, timedelta

def lecture_home(request,course_id):
    # Dummy course data
    course = {
        'id': course_id,
        'title': 'Supervised Machine Learning: Regression and Classification',
        'start_date': datetime.now().date(),
        'end_date': datetime.now().date() + timedelta(days=60),
        'weeks': [
            {'number': 1, 'is_current': True},
            {'number': 2, 'is_current': False},
            {'number': 3, 'is_current': False},
        ]
    }

    # Dummy current week data
    current_week = {
        'number': 1,
        'title': 'Introduction to Machine Learning',
        'description': 'Welcome to the Machine Learning Specialization! You\'re joining millions of others who have taken either this or the original course, which led to the founding of Coursera, and has helped millions of other learners, like you, take a look at the exciting world of machine learning!',
        'video_duration': '1h 55m',
        'reading_duration': '2 min',
        'assessments_count': 2,
        'section_title': 'Overview of Machine Learning',
        'items': [
            {
                'type': 'video',
                'title': 'Welcome to machine learning!',
                'duration': '2 min'
            },
            {
                'type': 'video',
                'title': 'Applications of machine learning',
                'duration': '4 min'
            },
            {
                'type': 'quiz',
                'title': 'Intake Survey',
                'duration': '1 min'
            },
            {
                'type': 'reading',
                'title': '[IMPORTANT] Have questions, issues or ideas? Join our Forum!',
                'duration': '2 min'
            }
        ]
    }

    # Dummy upcoming deadlines
    upcoming_deadlines = [
        {
            'title': 'Practice quiz: Regression',
            'url': '#',
            'is_overdue': True,
            'days_left': 0,
            'type': 'Graded Assignment'
        },
        {
            'title': 'Practice quiz: Multiple linear regression',
            'url': '#',
            'is_overdue': False,
            'days_left': 3,
            'type': 'Graded Assignment'
        }
    ]

    context = {
        'course': course,
        'current_week': current_week,
        'upcoming_deadlines': upcoming_deadlines,
    }
    return render(request, 'lecture/lecture_home.html', context)