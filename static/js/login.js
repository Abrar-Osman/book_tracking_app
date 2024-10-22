
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


function logoutUser(){

    localStorage.removeItem('token');
    window.location.href = '/';

}


function searchBook(e){
    e.preventDefault()

    const search = document.getElementById('search').value;
    const token = localStorage.getItem('token');  

        if (!token) {
            alert('You need to log in first.');
            window.location.href = '/login';
            return;
        }
    
        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`  
            },
            body: JSON.stringify({
                'search' : search
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to add the book.');
        });
    }
    



// const accessProtected = async (e) => {
//     e.preventDefault();  
    
//     const options = {
//         method: 'POST',
//         headers: {
//             Authorization: `Bearer ${localStorage.getItem('jwt')}`,
//         }
//     };

//     try {
//         const response = await fetch('/protected', options);
//         if (!response.ok) {
//             window.location.href = '/login';
//             return;
//         }

//         const data = await response.json();
//         console.log(data);  
//     } catch (error) {
//         console.error('Error accessing protected route:', error);
        
//     }
// };

// protectedLinks = document.getElementsByClassName('.protected')

// protectedLinks.forEach(link => {
//     link.addEventListener('click', accessProtected);  
// });







