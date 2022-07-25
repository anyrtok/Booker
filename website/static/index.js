function deleteBook(bookId) {
  fetch("/delete-book", {
    method: "POST",
    body: JSON.stringify({ bookId: bookId }),
  }).then((_res) => {
    //reload window
    window.location.href = "/";
  });
}

function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    //reload window
    window.location.href = "/draft";
  });
}

// for the typewriting effect
function typeWrite() {
  const texts = [
    "Welcome to CS50 final project!",
    "This is the site where you can search, add to the bookshelf, delete and make notes about your favourite books!",
    "Created by Kotryna Ratkevičiūtė, Vilnius LITHUANIA",
  ];
  let count = 0;
  let index = 0;
  let currentText = "";
  let letter = "";

  (function type() {
    currentText = texts[count];
    letter = currentText.slice(0, ++index);

    document.querySelector(".typing").textContent = letter;
    if (letter.length === currentText.length) {
      count++;
      index = 0;
    }
    setTimeout(type, 100);
  })();
}
