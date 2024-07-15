document.getElementById('uploadButton').addEventListener('click', () => {
    const imageInput = document.getElementById('imageInput').files[0];
    if (imageInput) {
        const formData = new FormData();
        formData.append('file', imageInput);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            document.getElementById('result').innerText = `Skin Color: ${data.skin_color}`;
            // Store the skin color for later use
            localStorage.setItem('skinColor', JSON.stringify(data.skin_color));
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').innerText = 'An error occurred. Please try again.';
        });
    } else {
        alert('Please select an image file first.');
    }
});

document.getElementById('jewelleryButton').addEventListener('click', () => {
    getRecommendations('jewellery');
});

document.getElementById('outfitButton').addEventListener('click', () => {
    getRecommendations('outfit');
});

document.getElementById('makeupButton').addEventListener('click', () => {
    getRecommendations('makeup');
});

function getRecommendations(type) {
    const skinColor = JSON.parse(localStorage.getItem('skinColor'));
    if (!skinColor) {
        alert('Please upload an image first to get your skin color.');
        return;
    }

    fetch('/get_recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ type: type })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const recommendations = data.recommendations;
        
        document.getElementById('result').innerHTML = `
            <p>Recommendations: ${recommendations}</p>
        `;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'An error occurred. Please try again.';
    });
}
