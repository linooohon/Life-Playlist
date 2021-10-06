function onSignIn(googleUser) {
    var id_token = googleUser.getAuthResponse().id_token;
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
    
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.disconnect();
    // fetch('/google_sign_in', {
    //     method: "POST",
    //     body: JSON.stringify({ "id_token": id_token }),
    // }).then((_res) => {
    //     console.log('js login success');
    // });
    $.ajax({
        type: "POST",
        url: '/google_sign_in',
        data: JSON.stringify({ 'id_token': id_token }),
        success: function () {
            console.log('login success')
            window.location.href = "/app";
        },
        dataType: 'json',
        contentType: "application/json",
    });
}



function onLoadCallback() {
    $('span[id^="not_signed_"]').html('Login with Google');
    $('span[id^="not_signed_"]').css("letter-spacing", "1px");
    $('span[id^="not_signed_"]').css("margin-right", "20px");
    $('span[id^="not_signed_"]').css("font-weight", "600");
    $('span[id^="not_signed_"]').css("color", "#000");
    $('span[id^="not_signed_"]').css("font-family", "'Ubuntu Mono', monospace");
    $('div[class^="abcRioButton"]').css("border-radius", "5px");
    // $('div[class^="abcRioButton"]').css("width", "300px");
    // $('div[class^="abcRioButtonIcon"]').css("width", "50px");
}


function onLoadSignUpCallback() {
    $('span[id^="not_signed_"]').html('Sign in with Google');
    $('span[id^="not_signed_"]').css("letter-spacing", "1px");
    $('span[id^="not_signed_"]').css("margin-right", "20px");
    $('span[id^="not_signed_"]').css("font-weight", "600");
    $('span[id^="not_signed_"]').css("color", "#000");
    $('span[id^="not_signed_"]').css("font-family", "'Ubuntu Mono', monospace");
    $('div[class^="abcRioButton"]').css("border-radius", "5px");
    // $('div[class^="abcRioButton"]').css("width", "300px");
    // $('div[class^="abcRioButtonIcon"]').css("width", "50px");
}