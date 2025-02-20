import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY", "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"))

@csrf_exempt  # Disable CSRF for testing (use proper security in production)
def exam_home(request):
    generated_mcqs = []  # Default MCQs variable
    correct_answers = []  # For storing the correct answers
    user_answers = []  # For storing user's selected answers
    score = 0  # Initialize score

    if request.method == "POST":
        input_text = request.POST.get("text", "").strip()

        # Handle MCQ Generation
        if input_text:
            prompt = f"""
            Generate 5 multiple-choice questions from the following text. 
            Each question should have 4 options and 1 correct answer.

            Text: {input_text}

            Format:
            Question: <MCQ Question>
            a) <Option 1>
            b) <Option 2>
            c) <Option 3>
            d) <Option 4>
            Answer: <Correct Option>
            """
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are an AI that generates MCQ questions."},
                          {"role": "user", "content": prompt}],
                model="llama3-8b-8192",  # You can change the model to a more appropriate one if needed
            )

            if chat_completion.choices and chat_completion.choices[0].message.content:
                mcq_text = chat_completion.choices[0].message.content
                mcq_list = mcq_text.split("\n\n")

                for mcq in mcq_list:
                    parts = mcq.split("\n")
                    question = parts[0].split(":")[-1].strip()

                    options = {}
                    for i in range(1, 5):
                        if len(parts) > i:
                            option_label = chr(97 + i - 1)  # a, b, c, d
                            options[option_label] = parts[i][3:].strip()

                    correct_answer = parts[-1].split(":")[-1].strip() if len(parts) > 4 else None

                    generated_mcqs.append({
                        'question': question,
                        'options': options,
                        'correct_answer': correct_answer,
                    })

        # Handle user answers submission
        if 'submit_answers' in request.POST:
            for i, mcq in enumerate(generated_mcqs):
                user_answer = request.POST.get(f"answer_{i+1}", "")
                if user_answer == mcq['correct_answer']:
                    score += 1  # Increase score if the answer is correct

            # Return results with score
            return render(request, "exam/index.html", {
                "mcqs": generated_mcqs,
                "score": score,
                "user_answers": user_answers,
                "input_text": input_text,
            })

    # Return the page with generated MCQs or prompt for text input
    return render(request, "exam/index.html", {"mcqs": generated_mcqs, "input_text": ""})

