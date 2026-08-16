/*!
* Start Bootstrap - Blog Home v5.0.8 (https://startbootstrap.com/template/blog-home)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-blog-home/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

$(document).ready(function () {
  $('input[type="radio"]').click(function () {
    var questionNo = parseInt($(this).attr('name').substring(1));
    var choice = $(this).attr('value')
    console.log(questionNo);
    set_answers(questionNo, choice);
  });

});
function set_answers(no, value) {
  var answersArr = $('#id_stud_answers_hidden').val().split("");
  answersArr[no - 1] = value;
  $('#id_stud_answers_hidden').val(answersArr.join(""));
  console.log(answersArr.join(""))

}

function get_answers(answers, no) {
  return answers[no - 1];
}
function showSolution(element) {
    // Get the parent card element and its data attributes
    var card = element.closest('.card');
    var level = card.getAttribute('data-level');
    var folder = card.getAttribute('data-folder');
    var questionId = card.getAttribute('data-question-id');

    // Get the image URL from the card
    var imageUrl = card.querySelector('img').src;

    // Show loading state in modal
    document.getElementById('solutionModalBody').innerHTML = `
        <div class="d-flex justify-content-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;

    // Fetch solution via AJAX
    $.ajax({
        url: `/quiz/solution/${level}/${folder}/${questionId}/`,
        method: 'GET',
        success: function(response) {
            document.getElementById('solutionModalBody').innerHTML = `
                <div class="solution-content">
                    <img src="${imageUrl}" class="img-fluid mb-3" alt="Question Image">
                    <div class="solution-container">
                        <p class="correct-answer">✅ Correct Answer: ${response.correct_option}</p>
                        <p class="explanation-title">Explanation</p>
                        <div class="explanation">
                            ${response.solution}
                        </div>
                    </div>
                </div>
            `;
        },
        error: function(xhr, status, error) {
            document.getElementById('solutionModalBody').innerHTML = `
                <div class="alert alert-danger">
                    <h5>Error Loading Solution</h5>
                    <p>Failed to load solution for:</p>
                    <ul>
                        <li>Level: ${level}</li>
                        <li>Folder: ${folder}</li>
                        <li>Question: ${questionId}</li>
                    </ul>
                    <p>Error: ${error}</p>
                </div>
            `;
        }
    });
}
