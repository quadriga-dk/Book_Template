from IPython.display import HTML
import json
import uuid


def create_answer_box(question_id, rows=4):
    """Create an answer box with a submit button."""
    return HTML(f"""
    <div style="padding: 5px; border-radius: 5px; margin: 10px 0;">
        <textarea id="answer-{question_id}" rows="{rows}" style="width: 100%; margin-top: 10px; padding: 10px; border: 1px solid #ced4da; border-radius: 4px;" placeholder="Ihre Antwort"></textarea>
        <button id="btn-answer-{question_id}" onclick="lockAnswer('answer-{question_id}')" style="margin-top: 5px; padding: 5px 12px; background-color: #00305e; color: white; border: none; border-radius: 4px; cursor: pointer;">Bestätigen</button>
    </div>
    """)


class DragDropQuiz:
    """
    A simple drag-and-drop quiz generator for Jupyter Books.
    
    Usage:
    quiz = DragDropQuiz()
    quiz.create_matching_quiz(
        title="Your Quiz Title",
        descriptions=["Description 1", "Description 2", "Description 3"],
        options=["Option A", "Option B", "Option C"],
        correct_mapping={"Description 1": "Option A", "Description 2": "Option B", "Description 3": "Option C"}
    )
    """
    
    def __init__(self):
        self.quiz_counter = 0
    
    def create_matching_quiz(self, title, descriptions, options, correct_mapping, show_feedback=True, feedback_messages=None):
        """
        Create a drag-and-drop matching quiz.
        
        Parameters:
        - title (str): The quiz title/question
        - descriptions (list): List of items to be matched (static labels)
        - options (list): List of draggable options (draggable items)
        - correct_mapping (dict): Dictionary mapping descriptions to correct options
        - show_feedback (bool): Whether to show feedback after submission
        - feedback_messages (dict): Custom feedback messages with keys 'correct', 'incorrect', 'partial'
        """
        self.quiz_counter += 1
        quiz_id = f"drag_drop_quiz_{self.quiz_counter}_{uuid.uuid4().hex[:8]}"
        
        # Set default feedback messages if none provided
        if feedback_messages is None:
            feedback_messages = {
                "correct": "Perfekt! Alle {total} Zuordnungen sind korrekt!",
                "incorrect": "Leider sind keine Zuordnungen korrekt. Versuchen Sie es noch einmal!",
                "partial": "Teilweise richtig: {correct} von {total} Zuordnungen sind korrekt."
            }
        
        # Convert correct mapping to use indices for easier JavaScript handling
        desc_to_idx = {desc: i for i, desc in enumerate(descriptions)}
        opt_to_idx = {opt: i for i, opt in enumerate(options)}
        
        correct_pairs = []
        for desc, opt in correct_mapping.items():
            if desc in desc_to_idx and opt in opt_to_idx:
                correct_pairs.append([desc_to_idx[desc], opt_to_idx[opt]])
        
        html_content = self._generate_html(
            quiz_id, title, descriptions, options, correct_pairs, show_feedback, feedback_messages
        )
        
        return HTML(html_content)
    
    def _generate_html(self, quiz_id, title, descriptions, options, correct_pairs, show_feedback, feedback_messages):
        """Generate the complete HTML for the drag-and-drop quiz."""
        
        # Generate static description labels with drop zones
        description_zones = ""
        for i, desc in enumerate(descriptions):
            description_zones += f'''
                <div class="description-zone">
                    <div class="description-label">{desc}</div>
                    <div class="drop-area" data-zone-id="{i}" id="{quiz_id}_drop_{i}">
                        <span class="drop-placeholder">Hier ablegen</span>
                    </div>
                </div>
            '''
        
        # Generate draggable options
        draggable_options = ""
        for i, option in enumerate(options):
            draggable_options += f'''
                <div class="draggable-option" draggable="true" data-item-id="{i}" id="{quiz_id}_option_{i}">
                    {option}
                </div>
            '''
        
        return f'''
        <div class="drag-drop-quiz" id="{quiz_id}">
            <div class="quiz-title">{title}</div>
            
            <div class="quiz-main">
                <div class="descriptions-container">
                    {description_zones}
                </div>
            </div>
            
            <div class="options-container">
                <div class="options-title">Ziehen Sie diese zu den passenden Beschreibungen</div>
                <div class="options-list" id="{quiz_id}_options">
                    {draggable_options}
                </div>
            </div>
            
            <div class="quiz-controls">
                <button class="quiz-button" onclick="checkAnswer_{quiz_id}()">Antwort prüfen</button>
                <button class="quiz-button reset-button" onclick="resetQuiz_{quiz_id}()">Zurücksetzen</button>
            </div>
            
            <div id="{quiz_id}_feedback"></div>
        </div>
        <script>
            // Initialize this specific quiz
            document.addEventListener('DOMContentLoaded', function() {{
                if (window.dragDropQuizManager) {{
                    window.dragDropQuizManager.initializeQuiz(
                        '{quiz_id}',
                        {json.dumps(correct_pairs)},
                        {str(show_feedback).lower()},
                        {json.dumps(options)},
                        {json.dumps(feedback_messages)}
                    );
                }}
            }});
        </script>
        '''
    
    