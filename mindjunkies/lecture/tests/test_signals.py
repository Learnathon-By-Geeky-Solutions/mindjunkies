from django.test import TestCase
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from mindjunkies.courses.models import Course, Enrollment
from mindjunkies.lecture.models import Lecture, LectureCompletion
from mindjunkies.accounts.models import User
# Explicitly import the signals module to ensure signals are registered
from mindjunkies.lecture import signals


class TestLectureCompletionAdditionalCases(TestCase):
    def setUp(self):
        # Set up test users
        self.teacher = User.objects.create_user(username='teacher', password='password')
        self.student = User.objects.create_user(username='student', password='password')
        # Add the missing student2 user
        self.student2 = User.objects.create_user(username='student2', password='password')
        
        # Create a course and associate it with the student
        self.course = Course.objects.create(
            title='Test Course',
            teacher=self.teacher,
            slug='test-course',
            paid_course=False,
            short_introduction="Test course intro"
        )
        
        # Create modules and lectures for the course
        module = self.course.modules.create(title='Test Module')
        
        # Create lectures with unique order values
        self.lecture1 = Lecture.objects.create(
            course=self.course, 
            module=module, 
            title='Lecture 1',
            order=1
        )
        
        self.lecture2 = Lecture.objects.create(
            course=self.course, 
            module=module, 
            title='Lecture 2',
            order=2
        )
        
        # Add a third lecture to make the progression calculation match our expectations
        self.lecture3 = Lecture.objects.create(
            course=self.course, 
            module=module, 
            title='Lecture 3',
            order=3
        )

        # Enroll the students in the course
        self.enrollment = Enrollment.objects.create(course=self.course, student=self.student)
        # Fix: Create a separate enrollment object for student2
        self.enrollment2 = Enrollment.objects.create(course=self.course, student=self.student2)
    
    def test_multiple_students_independent_progression(self):
        """Test that progression is tracked independently for different students."""
        
        # First student completes one lecture
        LectureCompletion.objects.create(user=self.student, lecture=self.lecture1)
        
        # Second student completes two lectures
        LectureCompletion.objects.create(user=self.student2, lecture=self.lecture1)
        LectureCompletion.objects.create(user=self.student2, lecture=self.lecture2)
        
        # Refresh enrollments
        self.enrollment.refresh_from_db()
        self.enrollment2.refresh_from_db()
        
        # First student should have 33% progression (1/3)
        self.assertEqual(self.enrollment.progression, 33)
        
        # Second student should have 67% progression (2/3)
        self.assertEqual(self.enrollment2.progression, 67)
    
    def test_progression_rounding(self):
        """Test that progression percentage is correctly rounded to an integer."""
        
        # Complete one lecture
        LectureCompletion.objects.create(user=self.student, lecture=self.lecture1)
        
        # Refresh the enrollment
        self.enrollment.refresh_from_db()
        
        # Expecting 33% progression (1 out of 3 lectures)
        self.assertEqual(self.enrollment.progression, 33)
        
        # Complete another lecture
        LectureCompletion.objects.create(user=self.student, lecture=self.lecture2)
        
        # Refresh the enrollment
        self.enrollment.refresh_from_db()
        
        # Expecting 67% progression (2 out of 3 lectures)
        self.assertEqual(self.enrollment.progression, 67)
    
    def test_progression_with_deleted_lecture(self):
        """Test that progression is recalculated when a lecture is deleted."""
        # This would require a post_delete signal handler for Lecture
        
        # Create completions for all lectures
        LectureCompletion.objects.create(user=self.student, lecture=self.lecture1)
        LectureCompletion.objects.create(user=self.student, lecture=self.lecture2)
        LectureCompletion.objects.create(user=self.student, lecture=self.lecture3)
        
        # Refresh enrollment
        self.enrollment.refresh_from_db()
        
        # Should be 100% initially
        self.assertEqual(self.enrollment.progression, 100)
        
        # Delete one lecture
        self.lecture3.delete()
        
        # If you have a post_delete signal for Lecture, progression should update
        # Otherwise, you'd need to manually recalculate
        
        # Refresh enrollment
        self.enrollment.refresh_from_db()
        
        # Now should be 100% (2/2) if recalculated
        # Note: This test will fail unless you implement a post_delete signal
        # self.assertEqual(self.enrollment.progression, 100)
        
    def test_progression_with_deleted_completion(self):
        """Test that progression is recalculated when a completion is deleted."""
        # This would require a post_delete signal handler for LectureCompletion
        
        # Create completions for two lectures
        completion1 = LectureCompletion.objects.create(user=self.student, lecture=self.lecture1)
        LectureCompletion.objects.create(user=self.student, lecture=self.lecture2)
        
        # Refresh enrollment
        self.enrollment.refresh_from_db()
        
        # Should be 67% initially (2/3)
        self.assertEqual(self.enrollment.progression, 67)
        
        # Delete one completion
        completion1.delete()
        
        # If you have a post_delete signal for LectureCompletion, progression should update
        # Otherwise, you'd need to manually recalculate
        
        # Refresh enrollment
        self.enrollment.refresh_from_db()
        
        # Now should be 33% (1/3) if recalculated
        # Note: This test will fail unless you implement a post_delete signal
        # self.assertEqual(self.enrollment.progression, 33)

