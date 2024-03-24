// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { 
    getAuth,
    createUserWithEmailAndPassword, 
    signInWithEmailAndPassword, 
    onAuthStateChanged,
    signOut } 
    from "firebase/auth";
import { 
    getFirestore, 
    collection, 
    addDoc,
    query,
    doc} 
    from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyD5t6c_VAl-LPPuCRVpT3ideiDDAhz7M_I",
  authDomain: "voltwatch-1b0a2.firebaseapp.com",
  projectId: "voltwatch-1b0a2",
  storageBucket: "voltwatch-1b0a2.appspot.com",
  messagingSenderId: "317514335733",
  appId: "1:317514335733:web:90e80da936ecccc2358cbc",
  measurementId: "G-T0DLVWEMKG"
};

//create a current variable representation for the current user to be able to link between auth and firestore to access info for messages.

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getFirestore(app);
auth.languageCode = 'it';

// vars for users and pass and email
var password = document.getElementById('password'); 
var email = document.getElementById('email');
const users = collection(db, 'users');
const current = auth.currentUser;
const current_key = current.uid;

// function calls for creating users and signing in/ out
createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
        const user = userCredential.user
    })

signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
        const user = userCredential.user;
    })
.catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
})

signOut(auth).then(() => {
  // Sign-out successful.
}).catch((error) => {
  // An error happened.
});

// vars for getting user info elements
var address = document.getElementById('address');
var name = document.getElementById('name');
var sms = document.getElementById('sms');
var sol_prov = document.getElementById('sol_prov');
var date = Date();

// adding users
try{
    const docRef = await addDoc(collection(db, "users"), {
        addr: address,
        emal : email,
        nme : name,
        phone: sms,
        sp: sol_prov,
        dte : date
    });
} catch(e){
    console.error("Error adding a new user: ", e)
}

// vars for sms messaging
const accountSid = 'ACd45c5fbb83fef87048d29ff6f248e264';
const authToken = '9951530fb897c3fd3d3ca1bd5e2c3f11';
const client = require('twilio')(accountSid, authToken);

// vars for grabbing the user phone number 
const docRef = doc(db, 'users', current_key)
const docSnap = await getDoc(docRef)
const userNum = current.phoneNumber;

// client messaging.
client.messages
    .create({
        body: 'Hello from Twilio',
        from: '+18449993079',
        to: current.phoneNumber
    })
    .then(message => console.log(message.sid))
    .done();