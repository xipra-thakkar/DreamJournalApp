let notes = []; // Placeholder, your notes data will be populated dynamically
let noteIdBeingEdited = null; // Track which note is being edited

// Function to add rich text formatting
function formatText(command) {
    document.execCommand(command, false, null);
}

// Adding a new note
document.getElementById('note-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').innerHTML;
    const tags = document.getElementById('note-tags').value.split(',').map(tag => tag.trim());

    if (title && content) {
        const newNote = {
            id: Date.now(), // Unique ID
            title,
            content,
            tags
        };
        notes.push(newNote);
        displayNotes();
        clearForm();
    } else {
        alert('Please fill in both title and content.');
    }
});

// Clear the form after submission
function clearForm() {
    document.getElementById('note-title').value = '';
    document.getElementById('note-content').innerHTML = '';
    document.getElementById('note-tags').value = '';
}

// Display all notes or filtered notes
function displayNotes(filteredNotes = notes) {
    const noteList = document.getElementById('notes');
    noteList.innerHTML = '';
    filteredNotes.forEach(note => {
        const noteItem = createNoteElement(note);
        noteList.appendChild(noteItem);
    });
}

// Create a note element
function createNoteElement(note) {
    const noteItem = document.createElement('li');
    noteItem.classList.add('list-group-item');
    noteItem.id = `note-${note.id}`;
    noteItem.innerHTML = `
        <strong>${note.title}</strong><br>
        <span>${note.content}</span><br>
        <small class="text-muted">Tags: ${note.tags.join(', ')}</small><br>
        <button class="btn btn-danger btn-sm" onclick="deleteNote(${note.id})">Delete</button>
        <button class="btn btn-primary btn-sm" onclick="editNoteForm(${note.id})">Edit</button>
    `;
    return noteItem;
}

// Search functionality
document.getElementById('search').addEventListener('input', searchNotes);

function searchNotes() {
    const query = document.getElementById('search').value.toLowerCase();
    const filteredNotes = notes.filter(note => {
        return note.title.toLowerCase().includes(query) || 
               note.content.toLowerCase().includes(query) ||
               note.tags.some(tag => tag.toLowerCase().includes(query));
    });
    
    displayNotes(filteredNotes);
}

// Edit and save functionality
function editNoteForm(noteId) {
    const note = notes.find(note => note.id === noteId);
    document.getElementById('edit-note-title').value = note.title;
    document.getElementById('edit-note-text').value = note.content;
    document.getElementById('edit-note-tags').value = note.tags.join(', ');
    noteIdBeingEdited = noteId;
    document.getElementById('edit-form').style.display = 'block';
}

function saveEdit() {
    const updatedTitle = document.getElementById('edit-note-title').value;
    const updatedContent = document.getElementById('edit-note-text').value;
    const updatedTags = document.getElementById('edit-note-tags').value.split(',').map(tag => tag.trim());

    notes = notes.map(note => {
        if (note.id === noteIdBeingEdited) {
            return {
                ...note,
                title: updatedTitle,
                content: updatedContent,
                tags: updatedTags
            };
        }
        return note;
    });

    displayNotes();
    document.getElementById('edit-form').style.display = 'none';
}

// Cancel edit
function cancelEdit() {
    document.getElementById('edit-form').style.display = 'none';
    noteIdBeingEdited = null;
}

// Delete a note
function deleteNote(noteId) {
    // Delete from the notes array
    notes = notes.filter(note => note.id !== noteId);
    
    // Display updated notes
    displayNotes();
}
