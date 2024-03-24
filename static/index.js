import { createClient } from "@propelauth/javascript";

const authClient = createClient({
    authUrl: "https://819084454.propelauthtest.com", // Replace with your actual Auth URL
    enableBackgroundTokenRefresh: true,
});

// Hook up buttons to redirect to signup, login, etc
document.getElementById("signup").onclick = authClient.redirectToSignupPage;
document.getElementById("login").onclick = authClient.redirectToLoginPage;
document.getElementById("account").onclick = authClient.redirectToAccountPage;
document.getElementById("logout").onclick = authClient.logout;

// When the logged in status changes, display one of the divs
authClient.addLoggedInChangeObserver((isLoggedIn) => {
    if (isLoggedIn) {
        document.getElementById("display-when-logged-in").style.display = "revert";
        document.getElementById("display-when-logged-out").style.display = "none";

        // Get authentication info and set email to it
        authClient.getAuthenticationInfoOrNull()
            .then(authInfo => {
                document.getElementById("email").innerText = authInfo?.user?.email;
            });
    } else {
        document.getElementById("display-when-logged-in").style.display = "none";
        document.getElementById("display-when-logged-out").style.display = "revert";
    }
});
