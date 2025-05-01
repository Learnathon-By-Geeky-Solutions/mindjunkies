```
.
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── collectstatic.sh
├── config
│   ├── jass_jwt.py
│   └── models.py
├── conftest.py
├── coverage.xml
├── db.sqlite3
├── deployment-guide.md
├── dev.ps1
├── docker-compose.elasticsearch_redis.yml
├── docker-compose.yml
├── docs
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   ├── README.md
│   ├── SECURITY.md
│   ├── SRS.md
│   ├── apps
│   │   └── overview.md
│   ├── guides
│   │   ├── advanced-usage.md
│   │   └── getting-started.md
│   └── resources
│       ├── logo.png
│       └── tech-stack.png
├── entrypoint.sh
├── k8s
│   ├── apps
│   │   └── django-mindjunkies-web.yml
│   └── nginx
│       ├── deployment.yml
│       └── service.yml
├── manage.py
├── migrate.sh
├── mindjunkies
│   ├── __init__.py
│   ├── accounts
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── management
│   │   │   └── commands
│   │   │       └── create_superuser.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_user_is_teacher.py
│   │   │   ├── 0003_alter_profile_bio.py
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── signals.py
│   │   ├── templates
│   │   │   └── accounts
│   │   │       ├── account
│   │   │       │   ├── email_change.html
│   │   │       │   ├── email_confirm.html
│   │   │       │   ├── login.html
│   │   │       │   ├── logout.html
│   │   │       │   ├── password_change.html
│   │   │       │   ├── password_reset.html
│   │   │       │   ├── password_reset_done.html
│   │   │       │   ├── password_reset_from_key.html
│   │   │       │   ├── password_reset_from_key_done.html
│   │   │       │   ├── signup.html
│   │   │       │   └── verification_sent.html
│   │   │       ├── allauth
│   │   │       │   └── layouts
│   │   │       │       └── base.html
│   │   │       ├── edit_profile.html
│   │   │       ├── profile.html
│   │   │       └── socialaccount
│   │   │           ├── login.html
│   │   │           └── snippets
│   │   │               ├── login.html
│   │   │               └── provider_list.html
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── fixtures
│   │   │   │   ├── __init__.py
│   │   │   │   └── accounts.py
│   │   │   ├── test_models.py
│   │   │   └── test_view.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── courses
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_lastvisitedcourse.py
│   │   │   ├── 0003_rename_user_coursetoken_teacher_and_more.py
│   │   │   ├── 0004_coursetoken_intro_video_alter_coursetoken_motivation.py
│   │   │   ├── 0005_course_tags.py
│   │   │   ├── 0006_course_progression_module_progression.py
│   │   │   ├── 0007_remove_course_progression_remove_module_progression_and_more.py
│   │   │   ├── 0008_module_unique_order_per_course.py
│   │   │   ├── 0009_remove_coursetoken_intro_video_and_more.py
│   │   │   ├── 0010_remove_course_published_course_status_and_more.py
│   │   │   ├── 0011_alter_course_status.py
│   │   │   ├── 0012_alter_course_status.py
│   │   │   ├── 0013_alter_course_status.py
│   │   │   ├── 0014_remove_course_preview_video_remove_module_details.py
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   ├── course_token_form.html
│   │   │   └── courses
│   │   │       ├── category_courses.html
│   │   │       ├── course_details.html
│   │   │       ├── course_list.html
│   │   │       ├── create_course.html
│   │   │       ├── my_course.html
│   │   │       ├── new_course.html
│   │   │       ├── popular_course.html
│   │   │       └── rate_course.html
│   │   ├── templatetags
│   │   │   ├── __init__.py
│   │   │   └── courses_tags.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_templatetags.py
│   │   │   └── test_views.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── dashboard
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_certificate_teacherverification_and_more.py
│   │   │   ├── __init__.py
│   │   ├── mixins.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   ├── apply_teacher.html
│   │   │   ├── components
│   │   │   │   ├── archive.html
│   │   │   │   ├── balance.html
│   │   │   │   ├── content.html
│   │   │   │   └── draft.html
│   │   │   ├── dashboard
│   │   │   │   └── course_row.html
│   │   │   ├── dashboard.html
│   │   │   ├── enrollmentList.html
│   │   │   ├── teacher_verification.html
│   │   │   └── verification_wait.html
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_admin.py
│   │   │   ├── test_mixins.py
│   │   │   ├── test_models.py
│   │   │   └── test_views.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── forums
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── documents.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_remove_forumtopic_reactions_forumcomment_likes_and_more.py
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   └── forums
│   │   │       ├── comment.html
│   │   │       ├── forum_home.html
│   │   │       ├── forum_thread_details.html
│   │   │       ├── forum_threads.html
│   │   │       ├── partials
│   │   │       │   ├── empty.html
│   │   │       │   ├── like_button.html
│   │   │       │   ├── like_comment.html
│   │   │       │   ├── like_reply.html
│   │   │       │   └── like_topic.html
│   │   │       ├── reply.html
│   │   │       └── reply_form.html
│   │   ├── tests
│   │   │   ├── test_models.py
│   │   │   └── test_views.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── home
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── templates
│   │   │   └── home
│   │   │       ├── card.html
│   │   │       ├── continue_learning.html
│   │   │       ├── goal.html
│   │   │       ├── index.html
│   │   │       ├── review.html
│   │   │       ├── search_results.html
│   │   │       └── subcategory.html
│   │   ├── templatetags
│   │   │   ├── __init__.py
│   │   │   └── enrollment_tags.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_enrollment_tags.py
│   │   │   └── test_views.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── lecture
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── management
│   │   │   ├── __init__.py
│   │   │   └── commands
│   │   │       ├── __init__.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_lecturecompletion.py
│   │   │   ├── 0003_alter_lecturevideo_video_file.py
│   │   │   ├── 0004_lastvisitedmodule.py
│   │   │   ├── 0005_lecture_unique_order_per_module.py
│   │   │   ├── 0006_lastvisitedmodule_video.py
│   │   │   ├── 0007_remove_lastvisitedmodule_video.py
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── signals.py
│   │   ├── templates
│   │   │   └── lecture
│   │   │       ├── base.html
│   │   │       ├── create_content.html
│   │   │       ├── create_lecture.html
│   │   │       ├── create_module.html
│   │   │       ├── lecture_content.html
│   │   │       ├── lecture_home.html
│   │   │       ├── lecture_pdf.html
│   │   │       └── lecture_video.html
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_forms.py
│   │   │   ├── test_models.py
│   │   │   ├── test_signals.py
│   │   │   └── test_views.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── live_classes
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── private.pem
│   │   ├── templates
│   │   │   └── live_classes
│   │   │       ├── create_live_class.html
│   │   │       ├── join_live_class.html
│   │   │       └── list_live_classes.html
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   └── test_views.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── payments
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_balance_balancehistory.py
│   │   │   ├── 0003_alter_transaction_tran_id.py
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   └── payments
│   │   │       ├── checkout_success.html
│   │   │       └── failed.html
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   └── test_views.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── static
│   │   ├── css
│   │   │   ├── daisyui.js
│   │   │   ├── forum.css
│   │   │   ├── index.css
│   │   │   ├── source.css
│   │   │   └── tailwind.css
│   │   ├── images
│   │   │   ├── default-avatar.png
│   │   │   ├── logo.ico
│   │   │   └── logo.png
│   │   └── js
│   │       ├── external_api.js
│   │       └── index.js
│   └── templates
│       ├── 404.html
│       ├── base.html
│       └── includes
│           ├── footer.html
│           ├── header.html
│           └── message.html
├── project
│   ├── __init__.py
│   ├── asgi.py
│   ├── logging.py
│   ├── settings
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── test.py
│   ├── urls.py
│   └── wsgi.py
├── pyproject.toml
├── pytest-log.txt
├── redis.conf
├── scripts
│   ├── __init__.py
│   └── populate_course_categories.py
├── sonar-project.properties
├── tests
│   ├── __init__.py
│   ├── do_storage_bucket_test.py
│   └── media
│       └── test_video.mp4
└── uv.lock

113 directories, 439 files
```