/*
Javascript that obtains row data in JSON format by getting /get_rows.
The JSON is parsed row by row. Data is added to the rowContainer div 
of index.html as div elements that are children of the rowContainer
div. Each row can be toggled by clicking. 
*/
song_number = 0

const rowContainer = document.getElementById('row-container');
function createRow(textArray) {
    const rowDiv = document.createElement('div');
    if (song_number == 0)
        rowDiv.className = 'row-first';
    else
        rowDiv.className = 'row';
    // Create four columns
    textArray.forEach((text, index) => {
        if (index<4)
        {
            const columnDiv = document.createElement('div');
            columnDiv.className = 'column';
            columnDiv.innerText = text;
            // Update whole row on column click
            //columnDiv.onclick = (event) => {
            //    event.stopPropagation(); // Prevent triggering parent row click
            //    rowDiv.classList.toggle('active-row');
            //};
            rowDiv.appendChild(columnDiv);
        }
    });
    
    const colDiv = document.createElement('div');
    colDiv.innerHTML='<a class="fa fa-info-circle" style="font-size:18px" href="/get_song_info?song_number='+textArray[4]+'"></a>';
    colDiv.className = 'column.right';
    song_number = song_number+1;
    rowDiv.appendChild(colDiv);
    return rowDiv;
}
async function fetchRows() {
    song_number = 0;
    try {
        const response = await fetch('/get_rows'); // Here we get the data from setlist_web.py
        const data = await response.json();
        populateRows(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
function populateRows(data) {
    rowContainer.innerHTML = ''; // Clear existing rows
    data.forEach((textArray) => {
        console.log(textArray)
        const row = createRow(textArray);
        rowContainer.appendChild(row);
    });
}

document.addEventListener("DOMContentLoaded", 
    function()
    {
        console.log("The page was either loaded or refreshed");

        // Need to clear rows before getting them again, otherwise
        // the list keeps repeating itself
        rowContainer.innerHTML = ''; // Clear existing rows
        fetchRows();
        setInterval(fetchRows, 1000)
    });

