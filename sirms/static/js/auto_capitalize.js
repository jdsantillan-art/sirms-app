/**
 * Auto-capitalize names in input fields
 * Capitalizes the first letter of each word
 */

document.addEventListener('DOMContentLoaded', function() {
    // Find all input fields that should be capitalized
    const nameFields = document.querySelectorAll(
        'input[name*="name"]:not([name*="username"]):not([name*="section_name"]), ' +
        'input[name="first_name"], ' +
        'input[name="last_name"], ' +
        'input[name="middle_name"], ' +
        'input[name="reporter_first_name"], ' +
        'input[name="reporter_last_name"], ' +
        'input[name="reporter_middle_name"], ' +
        'input[name="teacher_name"], ' +
        'input[name="involved_students"]'
    );
    
    nameFields.forEach(function(field) {
        field.addEventListener('input', function(e) {
            const cursorPosition = this.selectionStart;
            const oldValue = this.value;
            
            // Capitalize first letter of each word
            this.value = this.value.replace(/\b\w/g, function(char) {
                return char.toUpperCase();
            });
            
            // Restore cursor position
            if (oldValue.length === this.value.length) {
                this.setSelectionRange(cursorPosition, cursorPosition);
            }
        });
        
        // Also capitalize on blur (when user leaves the field)
        field.addEventListener('blur', function(e) {
            this.value = this.value.replace(/\b\w/g, function(char) {
                return char.toUpperCase();
            });
        });
    });
});

/**
 * Function to manually capitalize a specific field
 * Usage: capitalizeField(document.getElementById('myField'))
 */
function capitalizeField(field) {
    if (field && field.value) {
        field.value = field.value.replace(/\b\w/g, function(char) {
            return char.toUpperCase();
        });
    }
}

/**
 * Function to capitalize all name fields in a form
 * Usage: capitalizeAllNames(document.getElementById('myForm'))
 */
function capitalizeAllNames(form) {
    const nameFields = form.querySelectorAll(
        'input[name*="name"]:not([name*="username"]), ' +
        'input[name="first_name"], ' +
        'input[name="last_name"], ' +
        'input[name="middle_name"]'
    );
    
    nameFields.forEach(function(field) {
        capitalizeField(field);
    });
}
