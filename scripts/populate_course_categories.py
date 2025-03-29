from mindjunkies.courses.models import CourseCategory


def run():
    categories = {
        "Computer Science": {
            "description": "Programming, AI, and Data Science",
            "subcategories": [
                {"name": "Programming", "description": "Learn various programming languages"},
                {"name": "Artificial Intelligence", "description": "Machine Learning, Deep Learning, and AI"},
                {"name": "Data Science", "description": "Big Data, Analytics, and Statistics"},
            ],
        },
        "Mathematics": {
            "description": "Algebra, Calculus, and Discrete Math",
            "subcategories": [
                {"name": "Algebra", "description": "Linear Algebra, Abstract Algebra"},
                {"name": "Calculus", "description": "Differential and Integral Calculus"},
                {"name": "Discrete Math", "description": "Logic, Graph Theory, and Combinatorics"},
            ],
        },
        "Engineering": {
            "description": "Electrical, Mechanical, and Civil Engineering",
            "subcategories": [
                {"name": "Electrical Engineering", "description": "Circuits, Electronics, and Power Systems"},
                {"name": "Mechanical Engineering", "description": "Thermodynamics, Mechanics, and Manufacturing"},
                {"name": "Civil Engineering",
                 "description": "Structural, Geotechnical, and Transportation Engineering"},
            ],
        },
        "Business": {
            "description": "Finance, Marketing, and Management",
            "subcategories": [
                {"name": "Finance", "description": "Investing, Accounting, and Risk Management"},
                {"name": "Marketing", "description": "Branding, Digital Marketing, and Sales"},
                {"name": "Management", "description": "Leadership, Strategy, and Operations"},
            ],
        },
        "Art & Design": {
            "description": "Graphic Design, Music, and Photography",
            "subcategories": [
                {"name": "Graphic Design", "description": "UI/UX, Branding, and Motion Graphics"},
                {"name": "Music", "description": "Composition, Instruments, and Production"},
                {"name": "Photography", "description": "Editing, Portraits, and Landscapes"},
            ],
        },
    }

    for category_name, category_data in categories.items():
        category, created = CourseCategory.objects.get_or_create(
            name=category_name, defaults={"description": category_data["description"]}
        )
        if created:
            print(f"✅ Added category: {category.name}")
        else:
            print(f"⚠️ Category already exists: {category.name}")

        # Add subcategories
        for subcategory_data in category_data["subcategories"]:
            subcategory, sub_created = CourseCategory.objects.get_or_create(
                name=subcategory_data["name"],
                defaults={"description": subcategory_data["description"], "parent": category},
            )
            if sub_created:
                print(f"  ✅ Added subcategory: {subcategory.name} under {category.name}")
            else:
                print(f"  ⚠️ Subcategory already exists: {subcategory.name}")
