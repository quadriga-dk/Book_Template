// Function to lock an answer after submission
function lockAnswer(id) {
    const textarea = document.getElementById(id);
    const button = document.getElementById('btn-' + id);
    
    if (textarea.value.trim() === '') {
      alert('Please enter your answer before submitting.');
      return;
    }
    
    textarea.readOnly = true;
    textarea.style.fontWeight = 'bold';
    textarea.style.color = '#666';
    textarea.style.backgroundColor = '#f8f9fa';
    button.style.display = 'none';
  }


class DragDropQuizManager {
    constructor() {
        this.quizzes = new Map();
    }
    
    initializeQuiz(quizId, correctPairs, showFeedback, originalOptions, customFeedback) {
        const quizData = {
            quizId,
            correctPairs,
            showFeedback,
            originalOptions,
            customFeedback,
            draggedElement: null
        };
        
        this.quizzes.set(quizId, quizData);
        this.initializeOptions(quizId);
        this.setupEventListeners(quizId);
        this.createGlobalFunctions(quizId);
    }
    
    // Shuffle array function
    shuffleArray(array) {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }
    
    // Initialize options with shuffling
    initializeOptions(quizId) {
        const quiz = this.quizzes.get(quizId);
        const optionsList = document.getElementById(`${quizId}_options`);
        const shuffledOptions = this.shuffleArray(quiz.originalOptions.map((option, index) => ({ option, index })));
        
        optionsList.innerHTML = '';
        shuffledOptions.forEach(item => {
            const draggableOption = document.createElement('div');
            draggableOption.className = 'draggable-option';
            draggableOption.draggable = true;
            draggableOption.dataset.itemId = item.index;
            draggableOption.id = `${quizId}_option_${item.index}`;
            draggableOption.textContent = item.option;
            optionsList.appendChild(draggableOption);
        });
        
        this.initializeDragEvents(quizId);
    }
    
    // Add event listeners to draggable options
    initializeDragEvents(quizId) {
        const quiz = this.quizzes.get(quizId);
        const draggableOptions = document.querySelectorAll(`#${quizId} .draggable-option`);
        
        draggableOptions.forEach(option => {
            option.addEventListener('dragstart', (e) => {
                quiz.draggedElement = option;
                option.classList.add('dragging');
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/html', option.outerHTML);
            });
            
            option.addEventListener('dragend', (e) => {
                option.classList.remove('dragging');
            });
        });
    }
    
    setupEventListeners(quizId) {
        const quiz = this.quizzes.get(quizId);
        const dropAreas = document.querySelectorAll(`#${quizId} .drop-area`);
        
        dropAreas.forEach(area => {
            area.addEventListener('dragover', (e) => {
                e.preventDefault();
                area.classList.add('drag-over');
            });
            
            area.addEventListener('dragleave', (e) => {
                area.classList.remove('drag-over');
            });
            
            area.addEventListener('drop', (e) => {
                e.preventDefault();
                area.classList.remove('drag-over');
                
                if (quiz.draggedElement) {
                    // Clear the drop area
                    area.innerHTML = '';
                    
                    // Create a new element for the dropped item
                    const droppedItem = document.createElement('div');
                    droppedItem.className = 'dropped-item';
                    droppedItem.textContent = quiz.draggedElement.textContent;
                    droppedItem.dataset.itemId = quiz.draggedElement.dataset.itemId;
                    
                    // Add click listener to return item to original position
                    droppedItem.addEventListener('click', () => {
                        this.returnItemToOriginal(quizId, droppedItem);
                    });
                    
                    area.appendChild(droppedItem);
                    
                    // Remove the original draggable option
                    quiz.draggedElement.remove();
                    quiz.draggedElement = null;
                }
            });
        });
    }
    
    // Function to return item to original position
    returnItemToOriginal(quizId, droppedItem) {
        const optionsList = document.getElementById(`${quizId}_options`);
        
        // Create new draggable option
        const newDraggableOption = document.createElement('div');
        newDraggableOption.className = 'draggable-option';
        newDraggableOption.draggable = true;
        newDraggableOption.dataset.itemId = droppedItem.dataset.itemId;
        newDraggableOption.id = `${quizId}_option_${droppedItem.dataset.itemId}`;
        newDraggableOption.textContent = droppedItem.textContent;
        
        optionsList.appendChild(newDraggableOption);
        
        // Remove from drop zone and restore placeholder
        const dropArea = droppedItem.parentElement;
        dropArea.innerHTML = '<span class="drop-placeholder">Hier ablegen</span>';
        
        // Re-initialize drag events for the new option
        this.initializeDragEvents(quizId);
    }
    
    // Check answer function
    checkAnswer(quizId) {
        const quiz = this.quizzes.get(quizId);
        if (!quiz.showFeedback) return;
        
        const feedback = document.getElementById(`${quizId}_feedback`);
        let correctCount = 0;
        let totalPairs = quiz.correctPairs.length;
        
        // Check each correct pair and apply visual feedback
        quiz.correctPairs.forEach(([descId, optionId]) => {
            const dropArea = document.getElementById(`${quizId}_drop_${descId}`);
            const droppedItem = dropArea.querySelector('.dropped-item');
            
            // Remove previous feedback classes
            dropArea.classList.remove('correct-answer', 'incorrect-answer');
            
            if (droppedItem) {
                if (parseInt(droppedItem.dataset.itemId) === optionId) {
                    correctCount++;
                    dropArea.classList.add('correct-answer');
                } else {
                    dropArea.classList.add('incorrect-answer');
                }
            } else {
                // Empty drop area is also incorrect
                dropArea.classList.add('incorrect-answer');
            }
        });
        
        let message, className;
        if (correctCount === totalPairs) {
            message = quiz.customFeedback.correct.replace('{total}', totalPairs);
            className = 'correct';
        } else if (correctCount === 0) {
            message = quiz.customFeedback.incorrect;
            className = 'incorrect';
        } else {
            message = quiz.customFeedback.partial
                .replace('{correct}', correctCount)
                .replace('{total}', totalPairs);
            className = 'partial';
        }
        
        feedback.innerHTML = `<div class="feedback ${className}">${message}</div>`;
    }
    
    // Reset quiz function
    resetQuiz(quizId) {
        const dropAreas = document.querySelectorAll(`#${quizId} .drop-area`);
        const feedback = document.getElementById(`${quizId}_feedback`);
        
        // Clear all drop areas and remove feedback classes
        dropAreas.forEach(area => {
            area.innerHTML = '<span class="drop-placeholder">Hier ablegen</span>';
            area.classList.remove('correct-answer', 'incorrect-answer');
        });
        
        // Clear feedback
        feedback.innerHTML = '';
        
        // Re-initialize options with new shuffle
        this.initializeOptions(quizId);
    }
    
    // Create global functions for each quiz
    createGlobalFunctions(quizId) {
        window[`checkAnswer_${quizId}`] = () => this.checkAnswer(quizId);
        window[`resetQuiz_${quizId}`] = () => this.resetQuiz(quizId);
    }
}

// Global instance
window.dragDropQuizManager = new DragDropQuizManager();