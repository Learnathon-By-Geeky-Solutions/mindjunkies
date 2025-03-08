from django.test import TestCase
from django.utils.text import slugify
from accounts.models import User
from courses.models import Course, CourseRequirement, CourseObjective, CourseTeacher, Enrollment, Module

# Constant values to avoid repeated string literals
COURSE_TITLE = "Advanced Python Course"
COURSE_DESCRIPTION = "An in-depth Python course covering advanced topics."
COURSE_LEVEL = "beginner"
REQUIREMENT_TEXT = "Basic Python knowledge"
OBJECTIVE_TEXT = "Master Django ORM"
TEACHER_ROLE = "teacher"
ENROLLMENT_STATUS = "pending"
MODULE_TITLE = "Django Basics"

class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title=COURSE_TITLE,
            course_description=COURSE_DESCRIPTION,
            level=COURSE_LEVEL
        )
    
    def test_course_creation(self):
        self.assertEqual(self.course.title, COURSE_TITLE)
        self.assertEqual(self.course.course_description, COURSE_DESCRIPTION)
        self.assertEqual(self.course.level, COURSE_LEVEL)
    
    def test_slug_generation_on_save(self):
        self.assertEqual(self.course.slug, slugify(COURSE_TITLE))

    def test_average_rating_with_no_ratings(self):
        self.assertEqual(self.course.average_rating(), 0.0)

class CourseRequirementTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title=COURSE_TITLE)
        self.requirement = CourseRequirement.objects.create(course=self.course, requirement=REQUIREMENT_TEXT)
    
    def test_requirement_creation(self):
        self.assertEqual(self.requirement.requirement, REQUIREMENT_TEXT)
        self.assertEqual(self.requirement.course, self.course)

class CourseObjectiveTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title=COURSE_TITLE)
        self.objective = CourseObjective.objects.create(course=self.course, objective=OBJECTIVE_TEXT)
    
    def test_objective_creation(self):
        self.assertEqual(self.objective.objective, OBJECTIVE_TEXT)
        self.assertEqual(self.objective.course, self.course)

class CourseTeacherTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title=COURSE_TITLE)
        self.teacher = User.objects.create(username="teacher_user")
        self.course_teacher = CourseTeacher.objects.create(course=self.course, teacher=self.teacher, role=TEACHER_ROLE)
    
    def test_teacher_assignment(self):
        self.assertEqual(self.course_teacher.course, self.course)
        self.assertEqual(self.course_teacher.teacher, self.teacher)
        self.assertEqual(self.course_teacher.role, TEACHER_ROLE)

class EnrollmentTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title=COURSE_TITLE)
        self.student = User.objects.create(username="student_user")
        self.enrollment = Enrollment.objects.create(course=self.course, student=self.student, status=ENROLLMENT_STATUS)
    
    def test_enrollment_creation(self):
        self.assertEqual(self.enrollment.course, self.course)
        self.assertEqual(self.enrollment.student, self.student)
        self.assertEqual(self.enrollment.status, ENROLLMENT_STATUS)
    
    def test_enrollment_increments_course_enrollment_count(self):
        self.assertEqual(self.course.number_of_enrollments, 1)

class ModuleTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title=COURSE_TITLE)
        self.module = Module.objects.create(title=MODULE_TITLE, course=self.course, order=1)
    
    def test_module_creation(self):
        self.assertEqual(self.module.title, MODULE_TITLE)
        self.assertEqual(self.module.course, self.course)
        self.assertEqual(self.module.order, 1)
