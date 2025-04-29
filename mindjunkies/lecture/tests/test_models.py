import pytest
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from model_bakery import baker
from django.db.utils import IntegrityError
import cloudinary
from cloudinary.models import CloudinaryField


from mindjunkies.lecture.models import Lecture, LecturePDF, LectureVideo, LectureCompletion, LastVisitedModule


# The correct way to add a generator for CloudinaryField
def cloudinary_field_generator():
    return "video/upload/v1234567890/sample_video"  # This returns just the public ID part

# Register the generator
baker.generators.add(CloudinaryField, cloudinary_field_generator)


@pytest.mark.django_db
class TestLectureModel:
    def test_create_lecture(self):
        """Test that a lecture can be created with required fields"""
        lecture = baker.make('lecture.lecture')
        assert lecture.id is not None
        assert lecture.title is not None
        assert lecture.course is not None
        assert lecture.module is not None
        
    def test_lecture_str_method(self):
        """Test the string representation of a lecture"""
        course = baker.make('courses.course', title="Python Programming")
        lecture = baker.make('lecture.lecture', title="Introduction", course=course)
        assert str(lecture) == "Python Programming - Introduction"
        
    def test_auto_slug_creation(self):
        """Test that a slug is automatically created from the title"""
        lecture = baker.make('lecture.lecture', title="Advanced Django")
        assert lecture.slug.startswith('advanced-django')
        
    def test_custom_slug(self):
        """Test that a custom slug can be set"""
        custom_slug = "custom-lecture-slug"
        lecture = baker.make('lecture.lecture', slug=custom_slug)
        assert lecture.slug == custom_slug
        
    def test_unique_order_constraint(self):
        """Test that lectures in the same module must have unique order"""
        module = baker.make('courses.module')
        baker.make('lecture.lecture', module=module, order=1)
        
        # Creating a second lecture with the same order in the same module should fail
        with pytest.raises(ValidationError):
            lecture = baker.prepare('lecture.lecture', module=module, order=1)
            lecture.save()
            
    def test_different_modules_same_order(self):
        """Test that lectures in different modules can have the same order"""
        module1 = baker.make('courses.module')
        module2 = baker.make('courses.module')
        
        lecture1 = baker.make('lecture.lecture', module=module1, order=1)
        lecture2 = baker.make('lecture.lecture', module=module2, order=1)
        
        assert lecture1.order == lecture2.order
        assert lecture1.module != lecture2.module
        
    def test_ordering(self):
        """Test lectures are ordered by their order field"""
        module = baker.make('courses.module')
        lecture1 = baker.make('lecture.lecture', module=module, order=2)
        lecture2 = baker.make('lecture.lecture', module=module, order=1)
        lecture3 = baker.make('lecture.lecture', module=module, order=3)
        
        lectures = Lecture.objects.filter(module=module)
        assert list(lectures) == [lecture2, lecture1, lecture3]


@pytest.mark.django_db
class TestLecturePDFModel:
    def test_create_lecture_pdf(self):
        """Test creating a PDF file for a lecture"""
        lecture = baker.make('lecture.lecture')
        pdf = baker.make('lecture.lecturepdf', lecture=lecture, pdf_title="Course Notes")
        
        assert pdf.id is not None
        assert pdf.lecture == lecture
        assert pdf.pdf_title == "Course Notes"
        assert pdf.pdf_file is not None
        
    def test_lecture_pdf_str_method(self):
        """Test the string representation of a lecture PDF"""
        lecture = baker.make('lecture.lecture', title="Database Design")
        pdf = baker.make('lecture.lecturepdf', lecture=lecture)
        
        assert str(pdf) == "PDF for Database Design"


@pytest.mark.django_db
class TestLectureVideoModel:
    def test_create_lecture_video(self):
        """Test creating a video for a lecture"""
        lecture = baker.make('lecture.lecture')
        # Provide an explicit value for video_file to avoid generator issues
        video = baker.make(
            'lecture.lecturevideo', 
            lecture=lecture, 
            video_title="Introduction Video",
            status=LectureVideo.PENDING,
            video_file="video/upload/v1234567890/test_video"
        )
        
        assert video.id is not None
        assert video.lecture == lecture
        assert video.video_title == "Introduction Video"
        assert video.status == LectureVideo.PENDING
        assert video.is_running is False
        
    def test_lecture_video_str_method(self):
        """Test the string representation of a lecture video"""
        # Provide an explicit value for video_file to avoid generator issues
        video = baker.make(
            'lecture.lecturevideo', 
            video_title="Advanced Concepts",
            video_file="video/upload/v1234567890/test_video"
        )
        
        assert str(video) == "Advanced Concepts"


@pytest.mark.django_db
class TestLectureCompletionModel:
    def test_create_lecture_completion(self):
        """Test marking a lecture as completed by a user"""
        user = baker.make('accounts.user')
        lecture = baker.make('lecture.lecture')
        completion = baker.make('lecture.lecturecompletion', user=user, lecture=lecture)
        
        assert completion.id is not None
        assert completion.user == user
        assert completion.lecture == lecture
        assert completion.completed_at is not None
        
    def test_unique_together_constraint(self):
        """Test that a user can only mark a lecture as completed once"""
        user = baker.make('accounts.user')
        lecture = baker.make('lecture.lecture')
        baker.make('lecture.lecturecompletion', user=user, lecture=lecture)
        
        # Trying to create another completion record for the same user and lecture should fail
        with pytest.raises(IntegrityError):
            baker.make('lecture.lecturecompletion', user=user, lecture=lecture)


@pytest.mark.django_db
class TestLastVisitedModuleModel:
    def test_create_last_visited_module(self):
        """Test tracking a user's last visited module and lecture"""
        user = baker.make('accounts.user')
        module = baker.make('courses.module')
        lecture = baker.make('lecture.lecture', module=module)
        
        last_visited = baker.make(
            'lecture.lastvisitedmodule', 
            user=user, 
            module=module,
            lecture=lecture
        )
        
        assert last_visited.id is not None
        assert last_visited.user == user
        assert last_visited.module == module
        assert last_visited.lecture == lecture
        assert last_visited.last_visited is not None
        
    def test_unique_together_constraint(self):
        """Test unique_together constraint for module, user, and lecture"""
        user = baker.make('accounts.user')
        module = baker.make('courses.module')
        lecture = baker.make('lecture.lecture', module=module)
        
        baker.make('lecture.lastvisitedmodule', user=user, module=module, lecture=lecture)
        
        # Trying to create another record for the same user, module and lecture should fail
        with pytest.raises(IntegrityError):
            baker.make('lecture.lastvisitedmodule', user=user, module=module, lecture=lecture)
            
    def test_str_method(self):
        """Test the string representation of LastVisitedModule"""
        user = baker.make('accounts.user', username="student1")
        lecture = baker.make('lecture.lecture', title="APIs")
        module = baker.make('courses.module')
        
        last_visited = baker.make(
            'lecture.lastvisitedmodule', 
            user=user, 
            module=module,
            lecture=lecture
        )
        
        assert str(last_visited) == f"student1 - APIs - {last_visited.last_visited}"
        
    def test_ordering(self):
        """Test that LastVisitedModule records are ordered by last_visited in descending order"""
        user = baker.make('accounts.user')
        module = baker.make('courses.module')
        lecture1 = baker.make('lecture.lecture', module=module, order=1)
        lecture2 = baker.make('lecture.lecture', module=module, order=2)
        
        # Create visit records in a specific order
        visit1 = baker.make('lecture.lastvisitedmodule', user=user, module=module, lecture=lecture1)
        visit2 = baker.make('lecture.lastvisitedmodule', user=user, module=module, lecture=lecture2)
        
        # Force visit1 to be more recent than visit2
        visit1.save()  # This updates last_visited to now
        
        visits = LastVisitedModule.objects.filter(user=user)
        assert list(visits) == [visit1, visit2]