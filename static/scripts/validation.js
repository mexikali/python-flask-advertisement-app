function checkPassword() {
    var password = document.getElementById("password").value;
    
    var upperCaseLettersString = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    var lowerCaseLettersString = 'abcdefghijklmnopqrstuvwxyz';
    var specialCharactersString = '+!*-';
    var numbers = '0123456789';

    if (password.length < 10) {
        alert("Password length should be at least ten!!!");
        return false;
    }
    
    if (!checkChars(password, upperCaseLettersString)) {
        alert("Password should have at least one upper-case letter!!!");
        return false;
    }

    if (!checkChars(password, lowerCaseLettersString)) {
        alert("Password should have at least one lower-case letter!!!");
        return false;
    }

    if (!checkChars(password, specialCharactersString)) {
        alert("Password should have at least one special characters('+', '!', '*', '-')!!!");
        return false;
    }

    if (!checkChars(password, numbers)) {
        alert("Password should have at least one digit!!!");
        return false;
    }

    return true;
}


function checkChars(str1, str2) {
    for (var i = 0; i < str1.length; i++) {
        if (str2.includes(str1[i])) {
            return true;
        }
    }
    return false;
}