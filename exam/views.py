import os
import fitz  # PyMuPDF for PDF text extraction
from django.shortcuts import render
from django.core.files.storage import default_storage
from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY", "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"))

  # Disable CSRF for testing (use proper security in production)
def exam_home(request):
    if request.method == "POST":
        # Handle MCQ Generation from PDF
        if "generate_questions" in request.POST:
            input_text = ""

            # Check if a PDF file is uploaded
            if "pdf_file" in request.FILES:
                pdf_file = request.FILES["pdf_file"]
                file_path = default_storage.save(f"temp/{pdf_file.name}", pdf_file)
                
                print(f"PDF file saved at: {file_path}")  # Debug print statement

                try:
                    # Open the PDF using the 'with' statement to ensure it closes after reading
                    with fitz.open(default_storage.path(file_path)) as doc:
                        for page_num, page in enumerate(doc, start=1):
                            page_text = page.get_text("text")
                            input_text += page_text + "\n"
                            print(f"Page {page_num} Text: {page_text[:500]}...")  # Print the first 500 characters of each page

                    # Delete the file after processing
                    default_storage.delete(file_path)

                    print("Extracted text from PDF:")
                    print(input_text)  # Print extracted text to check

                except Exception as e:
                    return render(request, "exam/index.html", {
                        "error": f"Error processing PDF: {str(e)}"
                    })
                
            # Check if any text was extracted
            if input_text.strip():  # Ensure text is extracted
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
                
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are an AI that generates MCQ questions."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama3-8b-8192",
                    )

                    generated_mcqs = []
                    if chat_completion.choices and chat_completion.choices[0].message.content:
                        mcq_text = chat_completion.choices[0].message.content
                        mcq_list = mcq_text.split("\n\n")

                        for mcq in mcq_list:
                            parts = mcq.split("\n")
                            if len(parts) < 5:
                                continue  # Skip invalid responses

                            question = parts[0].split(":")[-1].strip()
                            options = {chr(97 + i - 1): parts[i][3:].strip() for i in range(1, 5)}
                            correct_answer = parts[-1].split(":")[-1].strip()

                            generated_mcqs.append({
                                'question': question,
                                'options': options,
                                'correct_answer': correct_answer,
                            })

                    # Store MCQs in session to persist for answer submission
                    request.session['mcqs'] = generated_mcqs
                    request.session.modified = True

                    return render(request, "exam/index.html", {"mcqs": generated_mcqs, "input_text": input_text})

                except Exception as e:
                    return render(request, "exam/index.html", {
                        "error": f"Error generating MCQs: {str(e)}"
                    })

            else:
                return render(request, "exam/index.html", {
                    "error": "No text extracted from the PDF. Please check the file format."
                })

        # Handle Answer Submission
        elif "submit_answers" in request.POST:
            generated_mcqs = request.session.get('mcqs', [])  # Retrieve MCQs from session
            user_answers = {}
            score = 0

            for i, mcq in enumerate(generated_mcqs):
                user_answer = request.POST.get(f"answer_{i+1}", "")
                user_answers[mcq['question']] = {
                    "selected": user_answer,
                    "correct": mcq["correct_answer"],
                    "is_correct": user_answer == mcq["correct_answer"]
                }
                print(user_answer)
                if user_answer == mcq["correct_answer"]:
                    score += 1  # Increase score for correct answers

            return render(request, "exam/index.html", {
                "mcqs": generated_mcqs,
                "score": score,
                "user_answers": user_answers,
                "show_results": True  # Flag to show results in template
            })

    return render(request, "exam/index.html", {"mcqs": [], "input_text": ""})
