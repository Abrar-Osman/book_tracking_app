
// 



async function loginUser(event) {
    event.preventDefault(); 

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/', {
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
        const tokenPayload = JSON.parse(atob(data.token.split('.')[1]));
        const userId = tokenPayload.sub;

        
        localStorage.setItem('token', token);
        localStorage.setItem('userId', userId);

        
        window.location.href = '/home'; 
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during login. Please try again.');
    }
}

function decodeToken(token) {
    const payload = token.split('.')[1];
    return JSON.parse(atob(payload));
}


function logoutUser(){

    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    window.location.href = '/';

}

