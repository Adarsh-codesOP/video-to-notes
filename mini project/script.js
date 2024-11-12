function auth() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  // Predefined list of valid students
  var validUsers = [
      { email: "student1@lecturecapture.com", password: "student123" },
      { email: "student2@lecturecapture.com", password: "learn2024" },
      { email: "student3@lecturecapture.com", password: "notesforlife" },
      { email: "student4@lecturecapture.com", password: "smartlearn456" },
      { email: "student5@lecturecapture.com", password: "education789" }
  ];

  // Predefined list of valid teachers
  var validTeachers = [
      { email: "teacher1@lecturecapture.com", password: "teacherpass123" },
      { email: "teacher2@lecturecapture.com", password: "secureteacher2024" },
      { email: "teacher3@lecturecapture.com", password: "educateteach456" },
      { email: "teacher4@lecturecapture.com", password: "teachermaster789" },
      { email: "teacher5@lecturecapture.com", password: "classroom2024" }
  ];

  // Retrieve stored user data from localStorage (students)
  var users = JSON.parse(localStorage.getItem("users")) || [];

  // Check if the username exists in the valid students or teachers
  var userFound = false;

  // Check for students first
  for (var i = 0; i < validUsers.length; i++) {
      if (validUsers[i].email === username) {
          userFound = true;

          // Check if the email is already registered with a different password
          for (var j = 0; j < users.length; j++) {
              if (users[j].email === username && users[j].password !== password) {
                  alert("Error: This email is already registered with a different password.");
                  return;
              }
          }

          // If the password is correct, log in the student
          if (validUsers[i].password === password) {
              // Store user in localStorage
              users.push({ email: username, password: password });
              localStorage.setItem("users", JSON.stringify(users));

              alert("Login Successfully as Student");
              window.location.assign("https://lecturecapture.com/Home/StudentDashboard"); // Redirect to Student Dashboard
              return;
          } else {
              alert("Error: The password is incorrect for this email.");
              return;
          }
      }
  }

  // Check for teachers if student login fails
  for (var i = 0; i < validTeachers.length; i++) {
      if (validTeachers[i].email === username) {
          userFound = true;

          // Check if the teacher's password is correct
          if (validTeachers[i].password === password) {
              alert("Login Successfully as Teacher");
              window.location.assign("https://lecturecapture.com/Home/TeacherDashboard"); // Redirect to Teacher Dashboard
              return;
          } else {
              alert("Error: The password is incorrect for this email.");
              return;
          }
      }
  }

  // If the user is not found in either students or teachers
  if (!userFound) {
      alert("Invalid email or password.");
  }
}
