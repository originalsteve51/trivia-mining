const rowContainer = document.getElementById('row-container');

async function fetchInfo() {
    try {
    	console.log('fetchInfo called')
        const response = await fetch('/song_info?song_number='+song_number); // Here we get the data from setlist_web.py
        const data = await response.json();
        console.log(data['info'])
        rowContainer.innerHTML = data['info'];
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

document.addEventListener("DOMContentLoaded", 
    function()
    {
        console.log("The page was either loaded or refreshed");

        // Need to clear rows before getting them again, otherwise
        // the list keeps repeating itself
        rowContainer.innerHTML = ''; // Clear existing rows
        fetchInfo();
    });
