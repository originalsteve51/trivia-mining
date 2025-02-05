
const rowContainer = document.getElementById('row-container');

_last_question_id = 0;

function lengthOfLongestWord(s) 
{
    // Split the string into words using space as a delimiter
    const words = s.split(' ');

    // Use reduce to find the length of the longest word
    const longestLength = words.reduce((maxLength, word) => 
    {
        return Math.max(maxLength, word.length);
    }, 0);  // Initialize with 0
    
    return longestLength;
}

function createRow(textArray) 
{
    difficulty = ''
    date_string = ''
    textArray.forEach((text, index) => 
    {
        if (index < 3)
        {
            const columnDiv = document.createElement('div');
            if (index==0)
            {
                if (lengthOfLongestWord(text) > 10)
                {
                    columnDiv.className = 'column content-category-8';
                }
                else
                {
                    columnDiv.className = 'column content-category-12';
                }
            }
            else if (index==1)
                columnDiv.className = 'column content-question';
            else if (index==2)
            {
                columnDiv.className = 'column content-answer';
                columnDiv.id = 'theAnswer'
            }
            /*
            else 
                columnDiv.className = 'column content-date';
            */
            columnDiv.innerHTML = '<b>'+text+'<b>';
            rowContainer.appendChild(columnDiv);
        }
        else if (index == 3)
        {
            // Place the date at the bottom of the category column
            // instead of putting it into its own column.
            date_string = text;
        }
        else if (index == 4)
        {
            // Add the difficulty to the category, which happens to
            // be the firstChild of the rowContainer
            rowContainer.firstChild.innerHTML += ('<br><b>'+text+'</b>');
            rowContainer.firstChild.innerHTML += ('<br><br><b>'+date_string+'</b>');
            console.log(rowContainer.firstChild.innerHTML);
        }
        else if (index == 5)
        {
            _last_question_id = text;
            console.log('last_question_id: ', _last_question_id)
        }
    });
}



function populateRow(data) 
{
    rowContainer.innerHTML = ''; 
    const aRow = createRow(data);
}


async function fetchQ_A() 
{
    try 
    {
        const response = await fetch('/api/next_q_a'); 
        const data = await response.json();
        populateRow(data);
    } 
    catch (error) 
    {
        console.error('Error fetching data:', error);
    }
}

async function rejectLastQuestion() 
{
    try 
    {
        const response = await fetch('/api/reject_question', 
        {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ 'question_id': _last_question_id })
        });

        if (!response.ok) 
        {
            throw new Error('Network response was not ok: ' + response.statusText);
        }


        const result = await response.json();
        console.log('Server response:', result);
    } catch (error) 
    {
        console.error('Error notifying server:', error);
    }
}


document.getElementById('nextButton').addEventListener('click', function() {
    console.log('Next button clicked');
    fetchQ_A();
    
});

document.getElementById('answerButton').addEventListener('click', function() {
    console.log('Answer button clicked');
    document.getElementById('theAnswer').className='column content-visible-answer';
});

document.getElementById('rejectButton').addEventListener('click', function() {
    console.log('Reject button clicked for question_id: ', _last_question_id);
    rejectLastQuestion();
    fetchQ_A();
});


document.addEventListener("DOMContentLoaded", 
    function()
    {
        console.log("The page was either loaded or refreshed");

        fetchQ_A();
    });
