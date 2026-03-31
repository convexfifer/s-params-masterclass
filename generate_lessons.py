#!/usr/bin/env python3
import os
import re

# Module structure
modules = {
    "1": {
        "title": "What Are S-Parameters?",
        "lessons": {
            "1-1": "Introduction and Overview",
            "1-2": "Understanding S-Parameters",
            "1-3": "S-Parameter Fundamentals",
            "1-4": "Practical Applications"
        }
    },
    "2": {
        "title": "Patterns and Meaning",
        "lessons": {
            "2-1": "Return Loss Patterns",
            "2-2": "Insertion Loss Analysis",
            "2-3": "Frequency Domain Interpretation"
        }
    },
    "3": {
        "title": "4-Port S-Parameters",
        "lessons": {
            "3-1": "Introduction to 4-Port Systems",
            "3-2": "Crosstalk Analysis",
            "3-3": "Time Domain Reflectometry"
        }
    },
    "4": {
        "title": "Mixed-Mode S-Parameters",
        "lessons": {
            "4-1": "Differential vs Single-Ended",
            "4-2": "Common Mode Analysis",
            "4-3": "Mixed-Mode Applications"
        }
    }
}

# Navigation helper
def get_prev_next(lesson_id):
    all_lessons = []
    for mod in ["1", "2", "3", "4"]:
        for les_id in modules[mod]["lessons"].keys():
            all_lessons.append(les_id)
    
    idx = all_lessons.index(lesson_id) if lesson_id in all_lessons else -1
    prev_lesson = all_lessons[idx - 1] if idx > 0 else None
    next_lesson = all_lessons[idx + 1] if idx < len(all_lessons) - 1 else None
    
    return prev_lesson, next_lesson

def format_transcript(text):
    """Convert transcript text to HTML paragraphs"""
    # Split into paragraphs
    paragraphs = text.strip().split('\n')
    html_parts = []
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        # Escape HTML special chars
        para = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Wrap inline math with $ ... $ for MathJax
        # Common patterns: S11, S21, etc.
        para = re.sub(r'\bS(\d{2})\b', r'\\(S_{\1}\\)', para)
        
        html_parts.append(f'            <p>{para}</p>')
    
    return '\n'.join(html_parts)

def create_lesson_page(lesson_id, lesson_title, module_num, module_title, transcript_text):
    prev_lesson, next_lesson = get_prev_next(lesson_id)
    
    # Format content
    content = format_transcript(transcript_text)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lesson {lesson_id}: {lesson_title} - S-Parameters Masterclass</title>
    <link rel="stylesheet" href="style.css">
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
    <header>
        <h1>S-Parameters Masterclass</h1>
        <p>Module {module_num}: {module_title}</p>
    </header>

    <nav>
        <a href="index.html">Home</a>
        <div class="module-nav">
            <select onchange="if(this.value) window.location.href=this.value">
                <option value="">Go to Module...</option>
                <option value="lesson1-1.html">Module 1: What Are S-Parameters?</option>
                <option value="lesson2-1.html">Module 2: Patterns and Meaning</option>
                <option value="lesson3-1.html">Module 3: 4-Port S-Parameters</option>
                <option value="lesson4-1.html">Module 4: Mixed-Mode S-Parameters</option>
            </select>
            <select onchange="if(this.value) window.location.href=this.value">
                <option value="">Go to Lesson...</option>
"""
    
    # Add all lessons to dropdown
    for mod in ["1", "2", "3", "4"]:
        for les_id, les_title in modules[mod]["lessons"].items():
            selected = ' selected' if les_id == lesson_id else ''
            html += f'                <option value="lesson{les_id}.html"{selected}>Lesson {les_id}: {les_title}</option>\n'
    
    html += """            </select>
        </div>
    </nav>

    <main>
        <article>
            <h2>Lesson {}: {}</h2>
            
            <div class="content">
{}
            </div>
        </article>

        <nav class="lesson-nav">
""".format(lesson_id, lesson_title, content)
    
    # Previous button
    if prev_lesson:
        prev_title = None
        for mod in modules.values():
            if prev_lesson in mod["lessons"]:
                prev_title = mod["lessons"][prev_lesson]
                break
        html += f'            <a href="lesson{prev_lesson}.html">← Previous: {prev_title}</a>\n'
    else:
        html += '            <span class="disabled">← Previous</span>\n'
    
    # Home button
    html += '            <a href="index.html">📚 All Modules</a>\n'
    
    # Next button
    if next_lesson:
        next_title = None
        for mod in modules.values():
            if next_lesson in mod["lessons"]:
                next_title = mod["lessons"][next_lesson]
                break
        html += f'            <a href="lesson{next_lesson}.html">Next: {next_title} →</a>\n'
    else:
        html += '            <span class="disabled">Next →</span>\n'
    
    html += """        </nav>
    </main>

    <footer>
        <p>&copy; 2024 S-Parameters Masterclass. Educational resource based on lectures by Dr. Eric Bogatin.</p>
    </footer>
</body>
</html>
"""
    
    return html

# Main generation
base_path = "/Users/khan/clawd/s-params-videos"
blog_path = os.path.join(base_path, "blog")

for module_num, module_data in modules.items():
    for lesson_id, lesson_title in module_data["lessons"].items():
        # Read transcript
        transcript_file = os.path.join(base_path, f"lesson{lesson_id}.txt")
        
        try:
            with open(transcript_file, 'r') as f:
                transcript_text = f.read()
            
            # Generate HTML
            html_content = create_lesson_page(
                lesson_id,
                lesson_title,
                module_num,
                module_data["title"],
                transcript_text
            )
            
            # Write lesson page
            output_file = os.path.join(blog_path, f"lesson{lesson_id}.html")
            with open(output_file, 'w') as f:
                f.write(html_content)
            
            print(f"✓ Created lesson{lesson_id}.html")
            
        except FileNotFoundError:
            print(f"✗ Transcript not found: {transcript_file}")

print("\n✅ All lesson pages generated!")
