
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


// async function searchBook(e){
//     e.preventDefault()

//     const search = document.getElementById('search').value;
//     const token = localStorage.getItem('token');  

//         if (!token) {
//             alert('You need to log in first.');
//             window.location.href = '/login';
//             return;
//         }
//     try {
//         const reponse = await fetch('/search', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Authorization': `Bearer ${token}`  
//             },
//             body: JSON.stringify({
//                 'search' : search
//             })
//         })
        
//         if (!response.ok) {
//             const errorData = await response.json();
//             alert(errorData.message); 
//             return;
//         }
         
//         window.location.href = '/home'; 
//     }

//         catch(error) {
//             console.error('Error:', error);
//             alert('Failed to get the book.');
//         };
//     }
    



// const accessProtected = async (e) => {
//     e.preventDefault();  
    
//     const options = {
//         method: 'GET',
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


// function addBook(event, bookId) {
//     event.preventDefault(); 
    
//     const token = localStorage.getItem('token'); 
    
    
//     const form = document.getElementById(`add-book-form-${bookId}`);
    
    
//     const formData = new FormData(form);
    
    
//     const data = {
//       book_id: formData.get('book_id'),
//       book_title: formData.get('title'),
//       book_authors: formData.get('authors'),
//       book_genre: formData.get('genre'),
//       book_page_count: formData.get('page_numbers')
//     };
    
    
//     fetch('/add_book', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//         'Authorization': `Bearer ${token}` 
//       },
//       body: JSON.stringify(data) 
//     })
//     .then(response => response.json())
//     .then(result => {
//       if (result.message) {
//         alert(result.message); 
//       } else {
//         alert('Error: ' + result.error); 
//       }
//     })
//     .catch(error => console.error('Error:', error));
//   }
  




