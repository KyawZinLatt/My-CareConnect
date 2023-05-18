console.log(`Hello from main.js`);
function getCookie(name) {
    const value = '; ' + document.cookie;
    const parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
}

document.addEventListener('DOMContentLoaded', () => {
    // Select the form and the submit button
    let phoneNumberForm = document.getElementById('phoneNumberForm');
    let clientId = phoneNumberForm.dataset.clientId;
    console.log('this is clientId: ', clientId);
    let submitPhoneNumberButton = document.getElementById('submitPhoneNumber');

    // Attach an event listener to the submit button
    submitPhoneNumberButton.addEventListener('click', function (event) {
        event.preventDefault();
        console.log("Submit button clicked");
        let formData = new FormData(phoneNumberForm);
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
        }
        console.log(clientId);
        // Get the error message element
        let errorMessageElement = document.getElementById('formErrorMessage');
        fetch(`/clients/${clientId}/additional-ph`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    console.log("Form submitted successfully.");
                    // If the form was submitted successfully, hide the error message
                    errorMessageElement.classList.add('d-none');

                    // Hide the modal
                    const modalElement = document.getElementById('phoneNumberModal');
                    const bootstrapModal = bootstrap.Modal.getInstance(modalElement);
                    bootstrapModal.hide();

                    // Clear form fields
                    phoneNumberForm.reset();

                    // Select the additionalPhoneNumbers element
                    let additionalPhoneNumbers = document.getElementById('additionalPhoneNumbers');

                    // Create new div elements
                    let newPhoneNumberRow = document.createElement('div');
                    let newPhoneNumberLabelCol = document.createElement('div');
                    let newPhoneNumberValueCol = document.createElement('div');
                    let newPhoneNumberLabel = document.createElement('p');
                    let newPhoneNumberValue = document.createElement('p');

                    // Add classes to new elements
                    newPhoneNumberRow.classList.add('row');
                    newPhoneNumberLabelCol.classList.add('col-6', 'text-end');
                    newPhoneNumberValueCol.classList.add('col-6', 'text-start');
                    newPhoneNumberValue.classList.add('text-muted', 'mb-1');

                    // Set inner text of new elements
                    newPhoneNumberLabel.innerHTML = `<strong>Additional Phone ${additionalPhoneNumbers.children.length + 1} :</strong>`;
                    newPhoneNumberValue.textContent = data.new_phone;

                    // Append new elements
                    newPhoneNumberLabelCol.append(newPhoneNumberLabel);
                    newPhoneNumberValueCol.append(newPhoneNumberValue);
                    newPhoneNumberRow.append(newPhoneNumberLabelCol);
                    newPhoneNumberRow.append(newPhoneNumberValueCol);
                    additionalPhoneNumbers.append(newPhoneNumberRow);

                } else {
                    console.log("Form submission failed.");
                    // If the form submission failed, show the error message
                    errorMessageElement.textContent = data.error_message;
                    errorMessageElement.classList.remove('d-none');
                }
            })
            .catch(error => {
                console.log("An error occurred:", error);
                // If an error occurred while making the fetch request, show an error message
                errorMessageElement.textContent = 'An error occurred while submitting the form. Please try again.';
                errorMessageElement.classList.remove('d-none');
            });
    });


    // Select the form and the submit button
    let submitUserInfoButton = document.getElementById('submitUserInfo');

    // Attach an event listener to the submit button
    submitUserInfoButton.addEventListener('click', function (event) {
        event.preventDefault();

        let userInfoForm = document.getElementById('userInfoForm');
        let userInfoClientId = userInfoForm.dataset.clientId;
        let canContactSelect = document.getElementById('id_can_contact');
        let ageRangeSelect = document.getElementById('id_age_range');

        // Get the error message element
        let errorMessageElement = document.getElementById('userInfoFormErrorMessage');

        // Check if a valid option is selected
        if (canContactSelect.value === "" || ageRangeSelect.value === "") {
            errorMessageElement.textContent = 'Please fill out all fields.';
            errorMessageElement.classList.remove('d-none');
            return;
        }

        console.log("Submit button clicked");
        let formData = new FormData(userInfoForm);
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
        }


        fetch(`/clients/${userInfoClientId}/info/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(data)
                if (data.success) {
                    console.log("Form submitted successfully.");

                    // If the form was submitted successfully, hide the error message
                    errorMessageElement.classList.add('d-none');

                    // Hide the modal and reset the form
                    let userInfoModal = bootstrap.Modal.getInstance(document.getElementById('userInfoModal'));
                    userInfoModal.hide();
                    userInfoForm.reset();

                    // // Update the page with the new user info
                    // document.getElementById('canBeContacted').textContent = data.user_info.can_be_contacted;
                    // document.getElementById('ageRange').textContent = data.user_info.age_range;

                    // Get the card body element
                    let cardBody = document.querySelector('#userInfoCard .card-body');

                    // Create new data row for 'Can be contacted?'
                    let newRow1 = document.createElement('div');
                    newRow1.classList.add('row');

                    let newCol1a = document.createElement('div');
                    newCol1a.classList.add('col-sm-7');
                    let newP1a = document.createElement('p');
                    newP1a.classList.add('mb-0');
                    newP1a.textContent = 'Can be contacted?';
                    newCol1a.appendChild(newP1a);

                    let newCol1b = document.createElement('div');
                    newCol1b.classList.add('col-sm-5');
                    let newP1b = document.createElement('p');
                    newP1b.classList.add('text-muted', 'mb-0');
                    newP1b.textContent = data.user_info.can_be_contacted === "True" ? "Yes" : "No";
                    newCol1b.appendChild(newP1b);

                    newRow1.appendChild(newCol1a);
                    newRow1.appendChild(newCol1b);

                    // Create new data row for 'Age Range'
                    let newRow2 = document.createElement('div');
                    newRow2.classList.add('row');

                    let newCol2a = document.createElement('div');
                    newCol2a.classList.add('col-sm-7');
                    let newP2a = document.createElement('p');
                    newP2a.classList.add('mb-0');
                    newP2a.textContent = 'Age Range';
                    newCol2a.appendChild(newP2a);

                    let newCol2b = document.createElement('div');
                    newCol2b.classList.add('col-sm-5');
                    let newP2b = document.createElement('p');
                    newP2b.classList.add('text-muted', 'mb-0');
                    newP2b.textContent = data.user_info.age_range;
                    newCol2b.appendChild(newP2b);

                    newRow2.appendChild(newCol2a);
                    newRow2.appendChild(newCol2b);

                    // Get the reference node (the node before which the new rows should be inserted)
                    let refNode = document.querySelector('#userInfoCard .card-body .last-row');
                    console.log(`refNode ${refNode}`);

                    // Insert the new rows before the reference node
                    cardBody.insertBefore(newRow1, refNode);
                    cardBody.insertBefore(document.createElement('hr'), refNode);
                    cardBody.insertBefore(newRow2, refNode);
                    cardBody.insertBefore(document.createElement('hr'), refNode);

                    let userInfoModalButton = document.getElementById('userInfoModalButton');
                    // Disable the modal trigger button
                    userInfoModalButton.disabled = true;

                } else {
                    console.log("Form submission failed.");

                    // If the form submission failed, show the error message
                    errorMessageElement.textContent = data.error_message;
                    errorMessageElement.classList.remove('d-none');
                }
            })
            .catch(error => {
                console.log("An error occurred:", error);

                // If an error occurred while making the fetch request, show an error message
                errorMessageElement.textContent = 'An error occurred while submitting the form. Please try again.';
                errorMessageElement.classList.remove('d-none');
            });
    });


    document.getElementById('symptomsModalButton').addEventListener('click', function () {
        const ageRange = document.getElementById('ageRange').textContent;
        let formHTML = '';

        if (ageRange === 'FifteenAndAbove') {
            // Define the form for "FifteenAndAbove"
            formHTML = `
                    <div class="mb-3">
                        <label for="question1" class="form-label">&gt;2 weeks cough</label>
                        <select name="question1" class="form-control" required id="id_question1">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question2" class="form-label">haemoptysis</label>
                        <select name="question2" class="form-control" required id="id_question2">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question3" class="form-label">&gt;2 weeks low grade fever</label>
                        <select name="question3" class="form-control" required id="id_question3">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question4" class="form-label">Loss of Appetite</label>
                        <select name="question4" class="form-control" required id="id_question4">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question5" class="form-label">unexplained weight loss</label>
                        <select name="question5" class="form-control" required id="id_question5">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question6" class="form-label">Chest Pain</label>
                        <select name="question6" class="form-control" required id="id_question6">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question7" class="form-label">Neck gland</label>
                        <select name="question7" class="form-control" required id="id_question7">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question8" class="form-label">contact with TB patient</label>
                        <select name="question8" class="form-control" required id="id_question8">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
        `;
        } else if (ageRange === 'BelowFifteen') {
            // Define the form for "BelowFifteen"
            formHTML = `
                    <div class="mb-3">
                        <label for="question1" class="form-label">&gt;2 weeks cough or &gt;2 weeks low grade fever</label>
                        <select name="question1" class="form-control" required id="id_question1">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question2" class="form-label">failure to thrive</label>
                        <select name="question2" class="form-control" required id="id_question2">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question3" class="form-label">contact with TB patient</label>
                        <select name="question3" class="form-control" required id="id_question3">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
        `;
        }

        // Insert the form into the modal
        document.getElementById('symptomsByCallForm').innerHTML = formHTML;
    });
    
    let submitSymptomsByCallButton = document.getElementById('submitSymptomsByCall');
    submitSymptomsByCallButton.addEventListener('click', function (event) {
        event.preventDefault();
        
        const ageRange = document.getElementById('ageRange').textContent;
        console.log('Submit button clicked');
        
        let symptomsByCallForm = document.getElementById('symptomsByCallForm');
        let clientId = symptomsByCallForm.dataset.clientId;
        
        let formData = new FormData(symptomsByCallForm);
        for (var pair of formData.entries()) {
            console.log('this is under formData' + pair[0] + ', ' + pair[1]);
        }
        
        let errorMessageElement = document.getElementById('symptomsByCallFormErrorMessage');
        
        let isFormValid = true;
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
            // Check if a valid option is selected
            if(pair[1] === "") {
                isFormValid = false;
                break;
            }
        }

        if(!isFormValid){
            let errorMessageElement = document.getElementById('symptomsByCallFormErrorMessage');
            errorMessageElement.textContent = 'Please fill out all fields.';
            errorMessageElement.classList.remove('d-none');
            return;
        }
        
        fetch(`/clients/${clientId}/symptoms/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(data)
                if (data.success) {
                    console.log("Form submitted successfully.");
                    
                    // If the form was submitted successfully, hide the error message
                    errorMessageElement.classList.add('d-none');
                    
                    // Hide the modal and reset the form
                    let symptomsModal = bootstrap.Modal.getInstance(document.getElementById('symptomsModal'));
                    symptomsModal.hide();
                    symptomsByCallForm.reset();
                    
                    // Get the card body element
                    let cardBody = document.querySelector('#symptomsCard .card-body');
                    
                    // // Remove existing symptoms elements, if any
                    // while (cardBody.firstChild) {
                    //     cardBody.removeChild(cardBody.firstChild);
                    // }
                    
                    // Update the submitted values on the page
                    let questionLabels;
                    if (ageRange === 'FifteenAndAbove') {
                        questionLabels = ['>2 weeks cough', 'haemoptysis', '>2 weeks low grade fever', 'Loss of Appetite', 'unexplained weight loss', 'Chest Pain', 'Neck gland', 'contact with TB patient'];
                    } else if (ageRange === 'BelowFifteen') {
                        questionLabels = ['>2 weeks cough or >2 weeks low grade fever', 'failure to thrive', 'contact with TB patient'];
                    }

                    // Get the last row element
                    let lastRow = document.querySelector('#symptomsCard .card-body .last-row');

                    
                    // Generate HTML elements for each question and its response
                    for (let i = 0; i < questionLabels.length; i++) {
                        let questionRow = document.createElement('div');
                        questionRow.classList.add('row');
                        
                        let questionCol = document.createElement('div');
                        questionCol.classList.add('col-sm-7');

                        let questionText = document.createElement('p');
                        questionText.classList.add('mb-0');
                        questionText.textContent = questionLabels[i];
                        questionCol.appendChild(questionText);
                        questionRow.appendChild(questionCol);

                        let answerCol = document.createElement('div');
                        answerCol.classList.add('col-sm-5');

                        let answerText = document.createElement('p');
                        answerText.classList.add('text-muted', 'mb-0');
                        answerText.textContent = formData.get(`question${i+1}`);
                        answerCol.appendChild(answerText);
                        questionRow.appendChild(answerCol);
            
                        let hr = document.createElement('hr');
                        
                        // Insert questionRow and hr before the lastRow
                        cardBody.insertBefore(questionRow, lastRow);
                        cardBody.insertBefore(hr, lastRow);
                        
                        let symptomsModalButton = document.getElementById('symptomsModalButton');
                        // Disable the modal trigger button
                        symptomsModalButton.disabled = true;
                    }
                }
            }).catch(error => {
                console.error('Error:', error);
                // Show the error message
                errorMessageElement.textContent = 'There was an error submitting the form. Please try again.';
                errorMessageElement.classList.remove('d-none');
            });
    });
});