
async function loginUser(event) {
    event.preventDefault(); 

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'email': email,
                'password': password
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(errorData.message); 
            return;
        }

        const data = await response.json();
        const token = data.token;

        
        localStorage.setItem('token', token);

        
        window.location.href = '/home'; 
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during login. Please try again.');
    }
}



function accessProtectedPage() {
    const token = localStorage.getItem('access_token');
    if (!token) {    
        window.location.href = '/login';
    } else {
        
        fetch('/search', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ${token}'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);  
        });
    }
}




