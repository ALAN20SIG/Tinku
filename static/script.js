// Handle text input form submission
document.getElementById('textForm').onsubmit = async function(event) {
    event.preventDefault();
    const userInput = document.getElementById('userInput').value;
    await analyzeText(userInput);
};

// Handle speech input
document.getElementById('speechButton').onclick = function() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = async function(event) {
        const speechResult = event.results[0][0].transcript;
        await analyzeText(speechResult);
    };

    recognition.onerror = function(event) {
        console.error("Speech recognition error:", event.error);
    };
};

// Analyze user input
async function analyzeText(input) {
    const response = await fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input })
    });

    const data = await response.json();
    document.getElementById('videoResponse').innerHTML = 
        `<p>Suggested Video: <a href="${data.video}" target="_blank">${data.video}</a></p>`;
}

// Handle adding a new note
document.getElementById('addNoteForm').onsubmit = async function(event) {
    event.preventDefault();
    const content = document.getElementById('newNoteContent').value;

    const response = await fetch("/add_note", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content })
    });

    const data = await response.json();
    if (response.status === 201) {
        alert("Note added successfully!");
        location.reload(); // Refresh to show the new note
    } else {
        alert(data.message);
    }
};

// Handle analyzing a specific note
document.querySelectorAll('.analyze-note').forEach(button => {
    button.onclick = async function() {
        const noteId = this.getAttribute('data-note-id');
        const response = await fetch("/analyze_note", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ note_id: noteId })
        });

        const data = await response.json();
        document.getElementById('videoResponse').innerHTML = 
            `<p>Suggested Video: <a href="${data.video}" target="_blank">${data.video}</a></p>`;
    };
});
