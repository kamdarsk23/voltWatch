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
    addDoc } 
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

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getFirestore(app);
auth.languageCode = 'it';


var password; 
var email;

createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
        const user = userCredential.user
    })

var address;
var name;
var sms;
var sol_prov;

try{
    const docRef = await addDoc(collection(db, "users"), {
        addr: address,
        emal : email,
        nme : name,
        phone: sms,
        sp: sol_prov
    });
} catch(e){
    console.error("Error adding a new user: ", e)
}

