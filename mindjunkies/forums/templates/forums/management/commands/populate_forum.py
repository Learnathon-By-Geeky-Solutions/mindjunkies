from django.contrib.auth import get_user_model
from mindjunkies.courses.models import Course, Module
from mindjunkies.forum.models import ForumTopic, ForumComment, Reply, LikedPost, LikedComment, LikedReply
from django.utils.text import slugify
import random
from datetime import datetime, timedelta

def populate_forum_data():
    User = get_user_model()
    
    # Get existing users (at least 5 for variety)
    users = list(User.objects.all())
    if len(users) < 5:
        raise Exception(f"Need at least 5 users in the database. Found only {len(users)}.")
    
    # Get existing course and module
    try:
        course = Course.objects.order_by('?').first()  # Random course
        if not course:
            raise Course.DoesNotExist
        module = Module.objects.filter(course=course).order_by('?').first()  # Random module for the course
        if not module:
            raise Module.DoesNotExist
    except Course.DoesNotExist:
        raise Exception("No Course found in the database. Please create at least one Course.")
    except Module.DoesNotExist:
        raise Exception("No Module found for the selected Course. Please create at least one Module.")
    
    # Sample data for topics
    topics_data = [
        {
            'title': 'Best practices for course completion',
            'content': 'What are your tips for staying motivated throughout the course?'
        },
        {
            'title': 'Module 1 discussion: Key concepts',
            'content': 'Let’s discuss the main concepts from Module 1.'
        },
        {
            'title': 'Study group formation',
            'content': 'Anyone interested in forming a study group for this course?'
        },
        {
            'title': 'Resources for extra practice',
            'content': 'Can anyone share good resources for additional practice?'
        },
        {
            'title': 'Troubleshooting assignment issues',
            'content': 'Having trouble with the latest assignment. Any advice?'
        }
    ]
    
    # Create topics
    for topic_data in topics_data:
        topic = ForumTopic.objects.create(
            title=topic_data['title'],
            slug=slugify(topic_data['title']),
            content=topic_data['content'],
            author=random.choice(users),
            course=course,
            module=module,
            created_at=datetime.now() - timedelta(days=random.randint(1, 30)),
            updated_at=datetime.now() - timedelta(days=random.randint(1, 30))
        )
        
        # Create likes for the topic (1-3 random users)
        for user in random.sample(users, random.randint(1, min(3, len(users)))):
            LikedPost.objects.create(topic=topic, user=user)
        
        # Create 2-4 comments per topic
        for i in range(random.randint(2, 4)):
            comment = ForumComment.objects.create(
                topic=topic,
                content=f"Comment {i+1}: This is a sample response to the topic.",
                author=random.choice(users),
                created_at=datetime.now() - timedelta(days=random.randint(1, 20)),
                updated_at=datetime.now() - timedelta(days=random.randint(1, 20))
            )
            
            # Create likes for the comment (0-2 random users)
            for user in random.sample(users, random.randint(0, min(2, len(users)))):
                LikedComment.objects.create(comment=comment, user=user)
            
            # Create 1-2 replies per comment
            for j in range(random.randint(1, 2)):
                reply = Reply.objects.create(
                    author=random.choice(users),
                    parent_comment=comment,
                    body=f"Reply {j+1}: This is a sample reply to the comment.",
                    created=datetime.now() - timedelta(days=random.randint(1, 15))
                )
                
                # Create likes for the reply (0-2 random users)
                for user in random.sample(users, random.randint(0, min(2, len(users)))):
                    LikedReply.objects.create(reply=reply, user=user)

if __name__ == '__main__':
    populate_forum_data()
    print("Successfully populated forum data with 5 topics, comments, and replies.")