console.log(`Hello from main.js`);
let clientStatus = document.getElementById('clientStatus');
console.log(clientStatus.textContent);
function getCookie(name) {
    const value = '; ' + document.cookie;
    const parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function getXPath(element) {
    var xpath = '';
    for (; element && element.nodeType == 1; element = element.parentNode) {
        var id = Array.from(element.parentNode.children).indexOf(element) + 1;
        id = id > 1 ? '[' + id + ']' : '';
        xpath = '/' + element.nodeName.toLowerCase() + id + xpath;
    }
    return xpath;
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
                    newP2b.setAttribute("id", "ageRange");
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
                        <select name="question1" class="form-select" required id="id_question1">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question2" class="form-label">haemoptysis</label>
                        <select name="question2" class="form-select" required id="id_question2">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question3" class="form-label">&gt;2 weeks low grade fever</label>
                        <select name="question3" class="form-select" required id="id_question3">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question4" class="form-label">Loss of Appetite</label>
                        <select name="question4" class="form-select" required id="id_question4">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question5" class="form-label">unexplained weight loss</label>
                        <select name="question5" class="form-select" required id="id_question5">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question6" class="form-label">Chest Pain</label>
                        <select name="question6" class="form-select" required id="id_question6">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question7" class="form-label">Neck gland</label>
                        <select name="question7" class="form-select" required id="id_question7">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question8" class="form-label">contact with TB patient</label>
                        <select name="question8" class="form-select" required id="id_question8">
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
                        <select name="question1" class="form-select" required id="id_question1">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question2" class="form-label">failure to thrive</label>
                        <select name="question2" class="form-select" required id="id_question2">
                            <option value="" selected>Select Answer</option>
                            <option value="True">Yes</option>
                            <option value="False">No</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="question3" class="form-label">contact with TB patient</label>
                        <select name="question3" class="form-select" required id="id_question3">
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
            if (pair[1] === "") {
                isFormValid = false;
                break;
            }
        }

        if (!isFormValid) {
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
                        answerText.textContent = formData.get(`question${i + 1}`);
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


    // Get the form and button elements
    let tbReferralForm = document.getElementById('tbReferralForm');
    let submitTbReferralButton = document.getElementById('submitTbReferral');

    // Add event listener to the button
    submitTbReferralButton.addEventListener('click', function (event) {
        event.preventDefault();  // Prevent the form from submitting normally

        let errorMessageElement = document.getElementById('tbReferralFormErrorMessage');

        // Create a FormData object from the form
        let formData = new FormData(tbReferralForm);

        let isFormValid = true;
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
            // Check if a valid option is selected
            if (pair[1] === "") {
                isFormValid = false;
                break;
            }
        }

        if (!isFormValid) {
            errorMessageElement.textContent = 'Please fill out all fields.';
            errorMessageElement.classList.remove('d-none');
            return;
        }

        // Make the fetch call
        fetch(`/clients/${tbReferralForm.dataset.clientId}/refer/`, {
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
                    // Hide the modal
                    let tbReferralModal = bootstrap.Modal.getInstance(document.getElementById('tbReferralModal'));
                    tbReferralModal.hide();


                    // Reset the form
                    tbReferralForm.reset();


                    // Get the parent element
                    let parentElement = document.querySelector('#tbReferralCard .card-body');

                    // Create and append new elements for 'Willing to be referred?'
                    let row1 = document.createElement('div');
                    row1.classList.add('row');

                    let col1a = document.createElement('div');
                    col1a.classList.add('col-sm-7');
                    col1a.innerHTML = '<p class="mb-0">Willing to be referred?</p>';
                    row1.appendChild(col1a);

                    let col1b = document.createElement('div');
                    col1b.classList.add('col-sm-5');
                    col1b.innerHTML = `<p class="text-muted mb-0">${data.is_willing_to_be_referred}</p>`;
                    row1.appendChild(col1b);


                    // Create and append new elements for 'Confirmed Name'
                    let row2 = document.createElement('div');
                    row2.classList.add('row');

                    let col2a = document.createElement('div');
                    col2a.classList.add('col-sm-7');
                    col2a.innerHTML = '<p class="mb-0">Confirmed Name</p>';
                    row2.appendChild(col2a);

                    let col2b = document.createElement('div');
                    col2b.classList.add('col-sm-5');
                    col2b.innerHTML = `<p class="text-muted mb-0">${data.name}</p>`;
                    row2.appendChild(col2b);


                    // Get the reference node (the node before which the new rows should be inserted)
                    let refNode = document.querySelector('#tbReferralCard .card-body .last-row');

                    // Insert the new rows before the reference node
                    parentElement.insertBefore(row1, refNode);
                    parentElement.insertBefore(document.createElement('hr'), refNode);
                    parentElement.insertBefore(row2, refNode);
                    parentElement.insertBefore(document.createElement('hr'), refNode);

                    let tbReferralModalButton = document.getElementById('tbReferralModalButton');
                    // Disable the modal trigger button
                    tbReferralModalButton.disabled = true;

                } else {
                    console.log("Form submission failed.");

                    // Show error messages
                    errorMessageElement.textContent = '';
                    for (let [field, errors] of Object.entries(data.errors)) {
                        for (let error of errors) {
                            errorMessageElement.textContent += `${field}: ${error} `;
                        }
                    }
                    document.getElementById('tbReferralFormErrorMessage').classList.remove('d-none');

                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Show the error message
                document.getElementById('tbReferralFormErrorMessage').textContent = 'There was an error submitting the form. Please try again.';
                document.getElementById('tbReferralFormErrorMessage').classList.remove('d-none');
            });
    });


    let submitSocialPlatform = document.getElementById('submitSocialPlatform')
    submitSocialPlatform.addEventListener('click', function (event) {
        event.preventDefault();  // Prevent the default form submission

        // Create a FormData instance
        let formData = new FormData(document.getElementById('socialPlatformForm'));

        // Get client ID
        let clientId = document.getElementById('socialPlatformForm').dataset.clientId;

        let isFormValid = true;
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
            // Check if a valid option is selected
            if (pair[1] === "") {
                isFormValid = false;
                break;
            }
        }

        let errorMessageElement = document.getElementById('socialPlatformFormErrorMessage');
        if (!isFormValid) {
            errorMessageElement.textContent = 'Please fill out all fields.';
            errorMessageElement.classList.remove('d-none');
            return;
        }

        // Fetch options
        let options = {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        };

        // Make the fetch request
        fetch(`/clients/${clientId}/social-platforms/`, options)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Hide the modal
                    let socialPlatformModal = bootstrap.Modal.getInstance(document.getElementById('socialPlatformModal'));
                    socialPlatformModal.hide();

                    // Reset the form
                    document.getElementById('socialPlatformForm').reset();

                    // Update the page, etc...
                    // Get the parent element
                    let parentElement = document.querySelector('#socialPlatformCard .card-body');

                    // Create and append new elements for 'Viber'
                    let row1 = document.createElement('div');
                    row1.classList.add('row');

                    let col1a = document.createElement('div');
                    col1a.classList.add('col-sm-7');
                    col1a.innerHTML = '<p class="mb-0">Viber</p>';
                    row1.appendChild(col1a);

                    let col1b = document.createElement('div');
                    col1b.classList.add('col-sm-5');
                    col1b.innerHTML = `<p class="text-muted mb-0">${data.platform1}</p>`;
                    row1.appendChild(col1b);


                    // Create and append new elements for 'Telegram'
                    let row2 = document.createElement('div');
                    row2.classList.add('row');

                    let col2a = document.createElement('div');
                    col2a.classList.add('col-sm-7');
                    col2a.innerHTML = '<p class="mb-0">Telegram</p>';
                    row2.appendChild(col2a);

                    let col2b = document.createElement('div');
                    col2b.classList.add('col-sm-5');
                    col2b.innerHTML = `<p class="text-muted mb-0">${data.platform2}</p>`;
                    row2.appendChild(col2b);


                    // Create and append new elements for 'Telegram'
                    let row3 = document.createElement('div');
                    row3.classList.add('row');

                    let col3a = document.createElement('div');
                    col3a.classList.add('col-sm-7');
                    col3a.innerHTML = '<p class="mb-0">Whatsapp</p>';
                    row3.appendChild(col3a);

                    let col3b = document.createElement('div');
                    col3b.classList.add('col-sm-5');
                    col3b.innerHTML = `<p class="text-muted mb-0">${data.platform3}</p>`;
                    row3.appendChild(col3b);

                    // Get the reference node (the node before which the new rows should be inserted)
                    let refNode = document.querySelector('#socialPlatformCard .card-body .last-row');

                    // Insert the new rows before the reference node
                    parentElement.insertBefore(row1, refNode);
                    parentElement.insertBefore(document.createElement('hr'), refNode);
                    parentElement.insertBefore(row2, refNode);
                    parentElement.insertBefore(document.createElement('hr'), refNode);
                    parentElement.insertBefore(row3, refNode);
                    parentElement.insertBefore(document.createElement('hr'), refNode);


                    let socialPlatformModalButton = document.getElementById('socialPlatformModalButton');
                    // Disable the modal trigger button
                    socialPlatformModalButton.disabled = true;

                } else {
                    console.log("Form submission failed.");

                    // Show the error message
                    errorMessageElement.textContent = '';

                    // Show error messages
                    for (let [field, errors] of Object.entries(data.errors)) {
                        for (let error of errors) {
                            errorMessageElement.textContent += `${field}: ${error} `;
                        }
                    }
                    errorMessageElement.classList.remove('d-none');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                // Show the error message
                document.getElementById('socialPlatformFormErrorMessage').textContent = 'There was an error submitting the form. Please try again.';
                document.getElementById('socialPlatformFormErrorMessage').classList.remove('d-none');
            });
    });

    document.getElementById('tbReferLocationModalButton').addEventListener('click', function () {

        document.getElementById('tbReferLocationForm').reset();

        fetch('/state_regions/')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {

                const townshipDropdown = document.getElementById('township');
                // Remove existing options
                while (townshipDropdown.firstChild) {
                    townshipDropdown.removeChild(townshipDropdown.firstChild);
                }

                const channelDropdown = document.getElementById('channel');
                // Remove existing options
                while (channelDropdown.firstChild) {
                    channelDropdown.removeChild(channelDropdown.firstChild);
                }

                const siteAddressDropdown = document.getElementById('siteAddress');
                // Remove existing options
                while (siteAddressDropdown.firstChild) {
                    siteAddressDropdown.removeChild(siteAddressDropdown.firstChild);
                }

                let stateRegionSelect = document.getElementById('stateRegion');
                stateRegionSelect.innerHTML = '<option value="" selected>Select State Region</option>';
                stateRegionSelect.innerHTML += data.map(option => `<option value="${option.id}">${option.name}</option>`).join('');
            })
            .catch(e => {
                console.error('Error: ' + e.message);
            });
    });



    document.getElementById('stateRegion').addEventListener('change', function () {
        // Get the selected state region id
        let stateRegionId = this.value;

        // Clear the township dropdown
        let townshipDropdown = document.getElementById('township');


        // If a state region is selected, fetch the corresponding townships
        if (stateRegionId) {
            fetch(`/townships/${stateRegionId}/`)
                .then(response => response.json())
                .then(data => {

                    const townshipDropdown = document.getElementById('township');
                    // Remove existing options
                    while (townshipDropdown.firstChild) {
                        townshipDropdown.removeChild(townshipDropdown.firstChild);
                    }

                    const channelDropdown = document.getElementById('channel');
                    // Remove existing options
                    while (channelDropdown.firstChild) {
                        channelDropdown.removeChild(channelDropdown.firstChild);
                    }

                    const siteAddressDropdown = document.getElementById('siteAddress');
                    // Remove existing options
                    while (siteAddressDropdown.firstChild) {
                        siteAddressDropdown.removeChild(siteAddressDropdown.firstChild);
                    }

                    townshipDropdown.innerHTML = '<option value="" selected>Select Township</option>';
                    // Append the townships to the township dropdown
                    data.forEach(township => {
                        let option = new Option(township.name, township.id);
                        townshipDropdown.add(option);
                    });
                })
                .catch(error => console.log(error));
        }
    });





    document.getElementById('township').addEventListener('change', function () {
        // Get the selected township id
        let townshipId = this.value;

        // Clear the channel dropdown
        let channelDropdown = document.getElementById('channel');


        // If a township is selected, fetch the corresponding channels
        if (townshipId) {
            fetch(`/channels/${townshipId}/`)
                .then(response => response.json())
                .then(data => {

                    const channelDropdown = document.getElementById('channel');
                    // Remove existing options
                    while (channelDropdown.firstChild) {
                        channelDropdown.removeChild(channelDropdown.firstChild);
                    }

                    const siteAddressDropdown = document.getElementById('siteAddress');
                    // Remove existing options
                    while (siteAddressDropdown.firstChild) {
                        siteAddressDropdown.removeChild(siteAddressDropdown.firstChild);
                    }

                    channelDropdown.innerHTML = '<option value="" selected>Select Channel</option>';
                    // Append the channels to the channel dropdown
                    data.forEach(channel => {
                        let option = new Option(channel.name, channel.id);
                        channelDropdown.add(option);
                    });
                })
                .catch(error => console.log(error));
        }
    });



    document.querySelector("#channel").addEventListener("change", function () {
        let channelID = this.value;
        let townshipID = document.querySelector("#township").value;
        let stateRegionID = document.querySelector("#stateRegion").value;
        if (channelID && townshipID && stateRegionID) {
            fetch(`/site_addresses/${stateRegionID}/${townshipID}/${channelID}/`)
                .then(response => response.json())
                .then(data => {

                    const siteAddressDropdown = document.getElementById('siteAddress');
                    // Remove existing options
                    while (siteAddressDropdown.firstChild) {
                        siteAddressDropdown.removeChild(siteAddressDropdown.firstChild);
                    }
                    siteAddressDropdown.innerHTML = '<option value="" selected>Select Site</option>';
                    let optionHTML = "";
                    for (let siteLocation of data) {
                        optionHTML += `<option value="${siteLocation.id}">${siteLocation.site_address}, ${siteLocation.site_address_mm}, ${siteLocation.clinic_name}, ${siteLocation.clinic_name_mm}, ${siteLocation.organization_name}</option>`;
                    }
                    siteAddressDropdown.innerHTML += optionHTML;
                });
        }
    });

    let submitTbReferLocation = document.getElementById('submitTbReferLocation')
    submitTbReferLocation.addEventListener('click', function (event) {
        event.preventDefault();  // Prevent the default form submission

        // Create a FormData instance
        let formData = new FormData(document.getElementById('tbReferLocationForm'));

        // Get client ID
        let clientId = document.getElementById('tbReferLocationForm').dataset.clientId;

        let isFormValid = true;
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
            // Check if a valid option is selected
            if (pair[1] === "") {
                isFormValid = false;
                break;
            }
        }
        
        let errorMessageElement = document.getElementById('tbReferLocationFormErrorMessage');
        if (!isFormValid) {
            errorMessageElement.textContent = 'Please fill out all fields.';
            errorMessageElement.classList.remove('d-none');
            return;
        }

        // Fetch options
        let options = {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        };

        // Make the fetch request
        fetch(`/clients/${clientId}/refer-locations/`, options)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Hide the modal
                    let tbReferLocationModal = bootstrap.Modal.getInstance(document.getElementById('tbReferLocationModal'));
                    tbReferLocationModal.hide();

                    // Reset the form
                    document.getElementById('tbReferLocationForm').reset();

                    // Update the page, etc...

                    let newCard = `
                                <div class="card mb-4">
                                    <div class="card-header">Referred Location</div>
                                    <div class="card-body">
                                        <div class="row">
                                            <div class="col-sm-7">
                                                <p class="mb-0">State/Region</p>
                                            </div>
                                            <div class="col-sm-5">
                                                <p class="text-muted mb-0">${data.state_region}</p>
                                            </div>
                                        </div>
                                        <hr>
                                        <div class="row">
                                            <div class="col-sm-7">
                                                <p class="mb-0">Township</p>
                                            </div>
                                            <div class="col-sm-5">
                                                <p class="text-muted mb-0">${data.township}</p>
                                            </div>
                                        </div>
                                        <hr>
                                        <div class="row">
                                            <div class="col-sm-7">
                                                <p class="mb-0">Channel Name</p>
                                            </div>
                                            <div class="col-sm-5">
                                                <p class="text-muted mb-0">${data.channel}</p>
                                            </div>
                                        </div>
                                        <hr>
                                        <div class="row">
                                            <div class="col-sm-7">
                                                <p class="mb-0">Org Name</p>
                                            </div>
                                            <div class="col-sm-5">
                                                <p class="text-muted mb-0">${data.org}</p>
                                            </div>
                                        </div>
                                        <hr>
                                        <div class="row">
                                            <div class="col-sm-7">
                                                <p class="mb-0">Site Address</p>
                                            </div>
                                            <div class="col-sm-5">
                                                <p class="text-muted mb-0">
                                                    ${data.site_address} ${data.site_address_mm}
                                                </p>
                                            </div>
                                        </div>
                                        <hr>
                    `;
                    if (data.clinic_name) {

                        newCard += `
                                            <div class="row">
                                                <div class="col-sm-7">
                                                    <p class="mb-0">Clinic Name</p>
                                                </div>
                                                <div class="col-sm-5">
                                                    <p class="text-muted mb-0">
                                                        ${data.clinic_name} ${data.clinic_name_mm}
                                                    </p>
                                                </div>
                                            </div>
                                            <hr>
                        `;
                    }


                    newCard += `
                                        <div class="row">
                                            <div class="col-sm-7">
                                                <p class="mb-0">Referred Date</p>
                                            </div>
                                            <div class="col-sm-5">
                                                <p class="text-muted mb-0">${data.referred_date}</p>
                                            </div>
                                        </div>
                                        <hr>
                                        
                                    </div>
                                </div>
                                <div class="card mb-4">
                                <div class="card-header">Referred Location</div>
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-sm-7">
                                            // <a class="btn btn-info"
                                            //   href="{% url 'client_ref_locations' id=client.id %}">Add</a>
                                            <!-- Button trigger modal -->
                                            <button type="button" 
                                                class="btn btn-info tbReferLocationModalButton" 
                                                data-bs-toggle="modal" 
                                                data-bs-target="#tbReferLocationModal" 
                                                id="tbReferLocationModalButton">Add</button>
                                        </div>
                                        <div class="col-sm-5"></div>
                                    </div>
                                </div>
                            </div>
                                
                    `;



                    // Get the button by its ID
                    let tbReferLocationModalButton = document.getElementById('tbReferLocationModalButton');

                    // Walk up the DOM to find the enclosing card
                    let originalCard = tbReferLocationModalButton;
                    while (originalCard && !originalCard.classList.contains('card')) {
                        originalCard = originalCard.parentElement;
                    }

                    if (originalCard) {
                        // originalCard.outerHTML += newCard;
                        originalCard.outerHTML = newCard;
                        // let originalCardButton = originalCard.querySelector('#tbReferLocationModalButton');
                        // console.log(originalCardButton);
                        // if (originalCardButton) {
                        //     originalCardButton.style.display = 'none';
                        // }
                        // let previousCard = originalCard.previousElementSibling;
                        // console.log(previousCard);
                        // if (previousCard) {
                        //     let previousCardButton = previousCard.querySelector('#tbReferLocationModalButton');
                        //     console.log(previousCardButton);
                        //     if (previousCardButton) {
                        //         previousCardButton.style.display = 'none';
                        //     }  
                        // }
                        
                    } else {
                        console.error("Couldn't find a card containing the button!");
                    }
                    


                } else {
                    console.log("Form submission failed.");

                    // Show the error message
                    errorMessageElement.textContent = '';

                    // Show error messages
                    if (data.errors) {
                        // Show error messages
                        for (let [field, errors] of Object.entries(data.errors)) {
                            for (let error of errors) {
                                errorMessageElement.textContent += `${field}: ${error} `;
                            }
                        }
                    }
                    errorMessageElement.classList.remove('d-none');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                // Show the error message
                document.getElementById('tbReferLocationFormErrorMessage').textContent = 'There was an error submitting the form. Please try again.';
                document.getElementById('tbReferLocationFormErrorMessage').classList.remove('d-none');
            });
    });
    
    
    let submitReachInfoButton = document.getElementById('submitReachInfo');

    // Add event listener to the button
    submitReachInfoButton.addEventListener('click', function (event) {
        event.preventDefault();  // Prevent the form from submitting normally

        let errorMessageElement = document.getElementById('reachInfoFormErrorMessage');
        
        // Get the form and button elements
        let reachInfoForm = document.getElementById('reachInfoForm');
        
        // Create a FormData object from the form
        let formData = new FormData(reachInfoForm);

        let isFormValid = true;
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
            // Check if a valid option is selected
            if (pair[1] === "") {
                isFormValid = false;
                break;
            }
        }

        if (!isFormValid) {
            errorMessageElement.textContent = 'Please fill out all fields.';
            errorMessageElement.classList.remove('d-none');
            return;
        }

        // Make the fetch call
        fetch(`/clients/${reachInfoForm.dataset.clientId}/reach-info/`, {
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
                    // Hide the modal
                    let reachInfoModal = bootstrap.Modal.getInstance(document.getElementById('reachInfoModal'));
                    //let reachInfoModal = document.getElementById('reachInfoModal');
                    reachInfoModal.hide();


                    // Reset the form
                    reachInfoForm.reset();


                    // Get the parent element
                    let parentElement = document.querySelector('#reachInfoCard .card-body');

                    // Create and append new elements for 'Is reached to referral site?'
                    let row1 = document.createElement('div');
                    row1.classList.add('row');

                    let col1a = document.createElement('div');
                    col1a.classList.add('col-sm-7');
                    col1a.innerHTML = '<p class="mb-0">Is reached to referral site?</p>';
                    row1.appendChild(col1a);

                    let col1b = document.createElement('div');
                    col1b.classList.add('col-sm-5');
                    col1b.innerHTML = `<p class="text-muted mb-0">${data.is_reached}</p>`;
                    row1.appendChild(col1b);


                    // Create and append new elements for 'Reach date'
                    let row2 = document.createElement('div');
                    row2.classList.add('row');

                    let col2a = document.createElement('div');
                    col2a.classList.add('col-sm-7');
                    col2a.innerHTML = '<p class="mb-0">Reach date</p>';
                    row2.appendChild(col2a);

                    let col2b = document.createElement('div');
                    col2b.classList.add('col-sm-5');
                    col2b.innerHTML = `<p class="text-muted mb-0">${data.reach_date}</p>`;
                    row2.appendChild(col2b);


                    // Get the reference node (the node before which the new rows should be inserted)
                    let refNode = document.querySelector('#reachInfoCard .card-body .last-row');

                    // Insert the new rows before the reference node
                    parentElement.insertBefore(row1, refNode);
                    parentElement.insertBefore(document.createElement('hr'), refNode);
                    parentElement.insertBefore(row2, refNode);
                    parentElement.insertBefore(document.createElement('hr'), refNode);

                    let reachInfoModalButton = document.getElementById('reachInfoModalButton');
                    // Disable the modal trigger button
                    reachInfoModalButton.disabled = true;

                } else {
                    console.log("Form submission failed.");

                    // Show error messages
                    errorMessageElement.textContent = '';
                    for (let [field, errors] of Object.entries(data.errors)) {
                        for (let error of errors) {
                            errorMessageElement.textContent += `${field}: ${error} `;
                        }
                    }
                    document.getElementById('reachInfoFormErrorMessage').classList.remove('d-none');

                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Show the error message
                document.getElementById('reachInfoFormErrorMessage').textContent = 'There was an error submitting the form. Please try again.';
                document.getElementById('reachInfoFormErrorMessage').classList.remove('d-none');
            });
    });
    
    document.getElementById('takenInvestigationModalButton').addEventListener('click', function () {

        
        
        const investigationTypeDropdown = document.getElementById('investigation-type-select');
        // Remove existing options
        while (investigationTypeDropdown.firstChild) {
            investigationTypeDropdown.removeChild(investigationTypeDropdown.firstChild);
        }

        const investigationResultDropdown = document.getElementById('investigation-result-select');
        // Remove existing options
        while (investigationResultDropdown.firstChild) {
            investigationResultDropdown.removeChild(investigationResultDropdown.firstChild);
        }
        
        document.getElementById('takenInvestigationForm').reset();
        
        fetch('/investigation_types/')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {

                

                let investigationTypeSelect = document.getElementById('investigation-type-select');
                investigationTypeSelect.innerHTML = '<option value="" selected>Select Investigation Type</option>';
                investigationTypeSelect.innerHTML += data.map(option => `<option value="${option.id}">${option.type_description}</option>`).join('');
            })
            .catch(e => {
                console.error('Error: ' + e.message);
            });
    });

    document.getElementById('investigation-type-select').addEventListener('change', function () {
        // Get the selected investigation type id
        let investigationTypeId = this.value;
        
        const investigationResultDropdown = document.getElementById('investigation-result-select');
        // Remove existing options
        while (investigationResultDropdown.firstChild) {
            investigationResultDropdown.removeChild(investigationResultDropdown.firstChild);
        }
        
        document.getElementById('id_investigation_date').value='';

        // If a investigation type is selected, fetch the corresponding investigation result
        if (investigationTypeId) {
            fetch(`/investigation_results/${investigationTypeId}/`)
                .then(response => response.json())
                .then(data => {

                    

                    investigationResultDropdown.innerHTML = '<option value="" selected>Select Investigation Result</option>';
                    // Append the townships to the township dropdown
                    data.forEach(investigation_result => {
                        let option = new Option(investigation_result.result_description, investigation_result.id);
                        investigationResultDropdown.add(option);
                    });
                })
                .catch(error => console.log(error));
        }
    });
    
    document.getElementById('investigation-result-select').addEventListener('change', function () {
        // Get the selected investigation result id
        let investigationResultId = this.value;

        // Clear the date
        document.getElementById('id_investigation_date').value='';

        
    });
    
    let submitTakenInvestigation = document.getElementById('submitTakenInvestigation')
    submitTakenInvestigation.addEventListener('click', function (event) {
        event.preventDefault();  // Prevent the default form submission

        // Create a FormData instance
        let formData = new FormData(document.getElementById('takenInvestigationForm'));

        // Get client ID
        let clientId = document.getElementById('takenInvestigationForm').dataset.clientId;

        let isFormValid = true;
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
            // Check if a valid option is selected
            if (pair[1] === "") {
                isFormValid = false;
                break;
            }
        }
        
        let errorMessageElement = document.getElementById('takenInvestigationFormErrorMessage');
        if (!isFormValid) {
            errorMessageElement.textContent = 'Please fill out all fields.';
            errorMessageElement.classList.remove('d-none');
            return;
        }

        // Fetch options
        let options = {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        };

        // Make the fetch request
        fetch(`/clients/${clientId}/taken-investigations/`, options)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Hide the modal
                    let takenInvestigationModal = bootstrap.Modal.getInstance(document.getElementById('takenInvestigationModal'));
                    takenInvestigationModal.hide();

                    // Reset the form
                    document.getElementById('takenInvestigationForm').reset();

                    // Update the page, etc...

                    let newCard = `
                                <div class="card mb-4">
                                    <div class="card-header">Taken Investigation</div>
                                    <div class="card-body">
                                        <div class="row">
                                            <div class="col-sm-7">
                                                <p class="mb-0">${data.investigation_type}</p>
                                            </div>
                                            <div class="col-sm-5">
                                                <p class="text-muted mb-0">${data.investigation_result}</p>
                                            </div>
                                        </div>
                                        <hr>
                                        
                                        <div class="row">
                                            <div class="col-sm-7">
                                                <p class="mb-0">Investigation Date</p>
                                            </div>
                                            <div class="col-sm-5">
                                                <p class="text-muted mb-0">${data.investigation_date}</p>
                                            </div>
                                        </div>
                                        <hr>
                    `;
                    


                    newCard += `        
                                    </div>
                                </div>
                                <div class="card mb-4">
                                <div class="card-header">Taken Investigation</div>
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-sm-7">
                                            
                                            <!-- Button trigger modal -->
                                            <button type="button" 
                                                class="btn btn-info takenInvestigationModalButton" 
                                                data-bs-toggle="modal" 
                                                data-bs-target="#takenInvestigationModal" 
                                                id="takenInvestigationModalButton">Add</button>
                                        </div>
                                        <div class="col-sm-5"></div>
                                    </div>
                                </div>
                            </div>
                                
                    `;



                    // Get the button by its ID
                    let takenInvestigationModalButton = document.getElementById('takenInvestigationModalButton');

                    // Walk up the DOM to find the enclosing card
                    let originalCard = takenInvestigationModalButton;
                    while (originalCard && !originalCard.classList.contains('card')) {
                        originalCard = originalCard.parentElement;
                    }

                    if (originalCard) {
                        // originalCard.outerHTML += newCard;
                        originalCard.outerHTML = newCard;
                        // let originalCardButton = originalCard.querySelector('#tbReferLocationModalButton');
                        // console.log(originalCardButton);
                        // if (originalCardButton) {
                        //     originalCardButton.style.display = 'none';
                        // }
                        // let previousCard = originalCard.previousElementSibling;
                        // console.log(previousCard);
                        // if (previousCard) {
                        //     let previousCardButton = previousCard.querySelector('#tbReferLocationModalButton');
                        //     console.log(previousCardButton);
                        //     if (previousCardButton) {
                        //         previousCardButton.style.display = 'none';
                        //     }  
                        // }
                        
                    } else {
                        console.error("Couldn't find a card containing the button!");
                    }
                    


                } else {
                    console.log("Form submission failed.");

                    // Show the error message
                    errorMessageElement.textContent = '';

                    // Show error messages
                    if (data.errors) {
                        // Show error messages
                        for (let [field, errors] of Object.entries(data.errors)) {
                            for (let error of errors) {
                                errorMessageElement.textContent += `${field}: ${error} `;
                            }
                        }
                    }
                    errorMessageElement.classList.remove('d-none');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                // Show the error message
                document.getElementById('takenInvestigationFormErrorMessage').textContent = 'There was an error submitting the form. Please try again.';
                document.getElementById('takenInvestigationFormErrorMessage').classList.remove('d-none');
            });
    });
    
        
        
    let submitTbConfirmationButton = document.getElementById('submitTbConfirmation');

    // Add event listener to the button
    submitTbConfirmationButton.addEventListener('click', function (event) {
        event.preventDefault();  // Prevent the form from submitting normally

        let errorMessageElement = document.getElementById('tbConfirmationFormErrorMessage');
        
        // Get the form and button elements
        let tbConfirmationForm = document.getElementById('tbConfirmationForm');
        
        // Create a FormData object from the form
        let formData = new FormData(tbConfirmationForm);
        
        // Get client ID
        let clientId = document.getElementById('tbConfirmationForm').dataset.clientId;


        let isFormValid = true;
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
            // Check if a valid option is selected
            if (pair[1] === "") {
                isFormValid = false;
                break;
            }
        }

        if (!isFormValid) {
            errorMessageElement.textContent = 'Please fill out all fields.';
            errorMessageElement.classList.remove('d-none');
            return;
        }

        // Make the fetch call
        fetch(`/clients/${clientId}/tb-confirmation/`, {
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
                    // Hide the modal
                    let tbConfirmationModal = bootstrap.Modal.getInstance(document.getElementById('tbConfirmationModal'));
                    //let reachInfoModal = document.getElementById('reachInfoModal');
                    tbConfirmationModal.hide();


                    // Reset the form
                    tbConfirmationForm.reset();


                    // Get the parent element
                    let parentElement = document.querySelector('#tbConfirmationCard .card-body');

                    // Create and append new elements for 'Is bat confirmed?'
                    let row1 = document.createElement('div');
                    row1.classList.add('row');

                    let col1a = document.createElement('div');
                    col1a.classList.add('col-sm-7');
                    col1a.innerHTML = '<p class="mb-0">Is bat confirmed?</p>';
                    row1.appendChild(col1a);

                    let col1b = document.createElement('div');
                    col1b.classList.add('col-sm-5');
                    col1b.innerHTML = `<p class="text-muted mb-0">${data.is_bat_confirmed}</p>`;
                    row1.appendChild(col1b);


                    // Create and append new elements for 'TB Diagnosis'
                    let row2 = document.createElement('div');
                    row2.classList.add('row');

                    let col2a = document.createElement('div');
                    col2a.classList.add('col-sm-7');
                    col2a.innerHTML = '<p class="mb-0">TB Diagnosis</p>';
                    row2.appendChild(col2a);

                    let col2b = document.createElement('div');
                    col2b.classList.add('col-sm-5');
                    col2b.innerHTML = `<p class="text-muted mb-0">${data.tb_diagnosis}</p>`;
                    row2.appendChild(col2b);
                    
                    
                    // Create and append new elements for 'Diagnosis Date'
                    let row3 = document.createElement('div');
                    row3.classList.add('row');

                    let col3a = document.createElement('div');
                    col3a.classList.add('col-sm-7');
                    col3a.innerHTML = '<p class="mb-0">Diagnosis Date</p>';
                    row3.appendChild(col3a);

                    let col3b = document.createElement('div');
                    col3b.classList.add('col-sm-5');
                    col3b.innerHTML = `<p class="text-muted mb-0">${data.diagnosis_date}</p>`;
                    row3.appendChild(col3b);



                    // Get the reference node (the node before which the new rows should be inserted)
                    let refNode = document.querySelector('#tbConfirmationCard .card-body .last-row');

                    // Insert the new rows before the reference node
                    parentElement.insertBefore(row1, refNode);
                    parentElement.insertBefore(document.createElement('hr'), refNode);
                    parentElement.insertBefore(row2, refNode);
                    parentElement.insertBefore(document.createElement('hr'), refNode);
                    parentElement.insertBefore(row3, refNode);
                    parentElement.insertBefore(document.createElement('hr'), refNode);

                    let tbConfirmationModalButton = document.getElementById('tbConfirmationModalButton');
                    // Disable the modal trigger button
                    tbConfirmationModalButton.disabled = true;

                } else {
                    console.log("Form submission failed.");

                    // Show error messages
                    errorMessageElement.textContent = '';
                    for (let [field, errors] of Object.entries(data.errors)) {
                        for (let error of errors) {
                            errorMessageElement.textContent += `${field}: ${error} `;
                        }
                    }
                    document.getElementById('tbConfirmationFormErrorMessage').classList.remove('d-none');

                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Show the error message
                document.getElementById('tbConfirmationFormErrorMessage').textContent = 'There was an error submitting the form. Please try again.';
                document.getElementById('tbConfirmationFormErrorMessage').classList.remove('d-none');
            });
    });
    
    document.getElementById('tbTxModalButton').addEventListener('click', function () {

        document.getElementById('tbTxForm').reset();

        fetch('/tb_regimes/')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {

                
                let txRegimeSelect = document.getElementById('id_tx_regime');
                txRegimeSelect.innerHTML = '<option value="" selected>Select Regime</option>';
                txRegimeSelect.innerHTML += data.map(option => `<option value="${option.id}">${option.type}</option>`).join('');
            })
            .catch(e => {
                console.error('Error: ' + e.message);
            });
    });
    
    let submitTbTxButton = document.getElementById('submitTbTx');

    // Add event listener to the button
    submitTbTxButton.addEventListener('click', function (event) {
        event.preventDefault();  // Prevent the form from submitting normally

        let errorMessageElement = document.getElementById('tbTxFormErrorMessage');
        
        // Get the form and button elements
        let tbTxForm = document.getElementById('tbTxForm');
        
        // Create a FormData object from the form
        let formData = new FormData(tbTxForm);
        
        // Get client ID
        let clientId = document.getElementById('tbTxForm').dataset.clientId;


        let isFormValid = true;
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
            // Check if a valid option is selected
            if (pair[1] === "") {
                isFormValid = false;
                break;
            }
        }

        if (!isFormValid) {
            errorMessageElement.textContent = 'Please fill out all fields.';
            errorMessageElement.classList.remove('d-none');
            return;
        }

        // Make the fetch call
        fetch(`/clients/${clientId}/tb-treatment/`, {
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
                    // Hide the modal
                    let tbTxModal = bootstrap.Modal.getInstance(document.getElementById('tbTxModal'));
                    //let reachInfoModal = document.getElementById('reachInfoModal');
                    tbTxModal.hide();


                    // Reset the form
                    tbTxForm.reset();


                    // Get the parent element
                    let parentElement = document.querySelector('#tbTxCard .card-body');

                    // Create and append new elements for 'Is registered for Tx?'
                    let row1 = document.createElement('div');
                    row1.classList.add('row');

                    let col1a = document.createElement('div');
                    col1a.classList.add('col-sm-7');
                    col1a.innerHTML = '<p class="mb-0">Is registered for Tx?</p>';
                    row1.appendChild(col1a);

                    let col1b = document.createElement('div');
                    col1b.classList.add('col-sm-5');
                    col1b.innerHTML = `<p class="text-muted mb-0">${data.is_registered_for_tx}</p>`;
                    row1.appendChild(col1b);


                    // Create and append new elements for 'TB Regime'
                    let row2 = document.createElement('div');
                    row2.classList.add('row');

                    let col2a = document.createElement('div');
                    col2a.classList.add('col-sm-7');
                    col2a.innerHTML = '<p class="mb-0">TB Regime</p>';
                    row2.appendChild(col2a);

                    let col2b = document.createElement('div');
                    col2b.classList.add('col-sm-5');
                    col2b.innerHTML = `<p class="text-muted mb-0">${data.tx_regime}</p>`;
                    row2.appendChild(col2b);
                    
                    
                    // Create and append new elements for 'TB Register Date'
                    let row3 = document.createElement('div');
                    row3.classList.add('row');

                    let col3a = document.createElement('div');
                    col3a.classList.add('col-sm-7');
                    col3a.innerHTML = '<p class="mb-0">TB Register Date</p>';
                    row3.appendChild(col3a);

                    let col3b = document.createElement('div');
                    col3b.classList.add('col-sm-5');
                    col3b.innerHTML = `<p class="text-muted mb-0">${data.registered_date}</p>`;
                    row3.appendChild(col3b);



                    // Get the reference node (the node before which the new rows should be inserted)
                    let refNode = document.querySelector('#tbTxCard .card-body .last-row');

                    // Insert the new rows before the reference node
                    parentElement.insertBefore(row1, refNode);
                    parentElement.insertBefore(document.createElement('hr'), refNode);
                    parentElement.insertBefore(row2, refNode);
                    parentElement.insertBefore(document.createElement('hr'), refNode);
                    parentElement.insertBefore(row3, refNode);
                    parentElement.insertBefore(document.createElement('hr'), refNode);

                    let tbTxModalButton = document.getElementById('tbTxModalButton');
                    // Disable the modal trigger button
                    tbTxModalButton.disabled = true;

                } else {
                    console.log("Form submission failed.");

                    // Show error messages
                    errorMessageElement.textContent = '';
                    for (let [field, errors] of Object.entries(data.errors)) {
                        for (let error of errors) {
                            errorMessageElement.textContent += `${field}: ${error} `;
                        }
                    }
                    document.getElementById('tbTxFormErrorMessage').classList.remove('d-none');

                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Show the error message
                document.getElementById('tbTxFormErrorMessage').textContent = 'There was an error submitting the form. Please try again.';
                document.getElementById('tbTxFormErrorMessage').classList.remove('d-none');
            });
    });

    






});

