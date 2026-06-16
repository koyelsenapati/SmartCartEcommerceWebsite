function validateForm() {

    let password =
        document.getElementById("password").value;


    if(password.length < 8) {

        alert("Password must contain at least 8 characters");

        return false;
    }


    return true;

}